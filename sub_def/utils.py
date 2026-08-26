"""
FFA Python/CGI 共通ユーティリティ（レンダラー・NoReturnハンドラなど） (sub_def/utils.py)
"""
import os
import sys
import time
from typing import NoReturn, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape

try:
    import config
except ImportError:
    from .. import config

_FLASH_KEY = "_flash_messages"
_FLASH_TYPES = {"success", "error", "warning", "info"}


def add_flash_message(
    session: dict[str, Any],
    message: str,
    toast_type: str = "info",
    duration: int = 3500,
) -> None:
    """次回画面描画時に一度だけ表示するトースト通知をセッションへ積みます。"""
    if not message:
        return

    if toast_type not in _FLASH_TYPES:
        toast_type = "info"

    try:
        duration = int(duration)
    except (TypeError, ValueError):
        duration = 3500

    messages = session.setdefault(_FLASH_KEY, [])
    messages.append({
        "message": str(message),
        "type": toast_type,
        "duration": max(1000, min(duration, 10000)),
    })


def render_template(
    template_name: str,
    context: dict[str, Any] | None = None,
    extra_headers: list[str] | None = None,
    session_data: dict[str, Any] | None = None,
) -> None:
    """Jinja2テンプレートをレンダリングし、CGIヘッダー付きで出力します。"""
    if context is None:
        context = {}
    if extra_headers is None:
        extra_headers = []
        
    # 画面描画時は既存トークンを維持する。POST結果画面で毎回再生成すると、
    # 戻る操作や別タブに残ったフォームが即座に失効しやすいため。
    from sub_def.crypto import get_session, token_generate, save_session, SESSION_COOKIE_NAME
    session = session_data if session_data is not None else get_session()
    csrf_token = token_generate(session)
    flash_messages = session.pop(_FLASH_KEY, [])
    cookie_header = save_session(session)
    
    # 呼び出し元から渡された重複するクッキーヘッダーを除外
    filtered_headers = []
    for h in extra_headers:
        if h.strip().startswith(f"Set-Cookie: {SESSION_COOKIE_NAME}="):
            continue
        filtered_headers.append(h)
    extra_headers = filtered_headers
    extra_headers.append(cookie_header)
        
    default_context = {
        "config": config.Config,
        "ltime": int(time.time()),
        "csrf_token": csrf_token,
        "flash_messages": flash_messages,
    }
    merged_context = {**default_context, **context}
    # 呼び出し元での古いトークンの上書きを防止し、確実に最新トークンをフォーム等に反映
    merged_context["csrf_token"] = csrf_token
    merged_context["flash_messages"] = flash_messages
    
    template_dir = config.Config.get("template_dir", "./templates")
    # XSS対策: 既定で全ての {{ }} 出力を HTML エスケープする。
    # サーバー側で組み立てた HTML(戦闘ログ等)は明示的に | safe を付けた箇所のみ素通しする。
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(default=True, default_for_string=True),
    )
    
    # 標準CGIヘッダー (ブラウザキャッシュ無効化)
    sys.stdout.write("Cache-Control: no-cache\n")
    sys.stdout.write("Pragma: no-cache\n")
    
    for header in extra_headers:
        sys.stdout.write(f"{header}\n")
        
    sys.stdout.write("Content-type: text/html; charset=utf-8\n\n")
    
    try:
        template = env.get_template(template_name)
        html = template.render(merged_context)
        sys.stdout.write(html)
    except Exception:
        # テンプレートエラーの詳細はHTTP応答に混ぜず、Webサーバーログだけで確認する。
        import traceback
        sys.stderr.write("FFA template rendering error:\n" + traceback.format_exc())
        sys.stdout.write("<html><body><h1>画面を表示できませんでした</h1><p>時間をおいて再度お試しください。</p></body></html>")

def show_error(msg: str, context: dict[str, Any] | None = None) -> NoReturn:
    """エラー画面をレンダリングしてプロセスを終了します (NoReturn 保証)"""
    if context is None:
        context = {}
    err_context = {
        "error_message": msg,
        **context
    }
    render_template("error.html", err_context)
    # NoReturn関数設計に基づき、プロセスを即座に終了 (デッドコードの防止)
    sys.exit(0)

def redirect(url: str, extra_headers: list[str] | None = None) -> NoReturn:
    """指定されたURLへリダイレクトしてプロセスを終了します (NoReturn 保証)"""
    sys.stdout.write("Status: 302 Found\n")
    sys.stdout.write(f"Location: {url}\n")
    if extra_headers:
        for header in extra_headers:
            sys.stdout.write(f"{header}\n")
    # dev_server.py (CGIHTTPRequestHandler) は Status ヘッダーをHTTPステータスに
    # 反映しないため、meta refresh によるフォールバックボディを併せて出力する
    sys.stdout.write("Content-type: text/html; charset=utf-8\n\n")
    sys.stdout.write(
        f'<html><head><meta http-equiv="refresh" content="0;url={url}"></head>'
        f'<body><a href="{url}">移動しない場合はこちらをクリックしてください</a></body></html>'
    )
    # NoReturn関数設計に基づき、プロセスを即座に終了
    sys.exit(0)


def redirect_with_flash(
    url: str,
    message: str,
    toast_type: str = "success",
    duration: int = 3500,
    extra_headers: list[str] | None = None,
) -> NoReturn:
    """トースト通知を積んでから指定URLへリダイレクトします。"""
    from sub_def.crypto import get_session, save_session

    session = get_session()
    add_flash_message(session, message, toast_type, duration)
    headers = list(extra_headers or [])
    headers.append(save_session(session))
    redirect(url, headers)
