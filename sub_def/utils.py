"""
FFA Python/CGI 共通ユーティリティ（レンダラー・NoReturnハンドラなど） (sub_def/utils.py)
"""
import os
import sys
import time
from typing import NoReturn, Any
from jinja2 import Environment, FileSystemLoader

try:
    import config
except ImportError:
    from .. import config

def render_template(template_name: str, context: dict[str, Any] | None = None, extra_headers: list[str] | None = None) -> None:
    """Jinja2テンプレートをレンダリングし、CGIヘッダー付きで出力します。"""
    if context is None:
        context = {}
    if extra_headers is None:
        extra_headers = []
        
    # POSTリクエスト（状態変化を伴う操作）時のみCSRFトークンを強制再生成（ワンタイムトークン化）
    # GETリクエスト（画像一覧の別窓表示や単なる画面遷移など）時は既存トークンを維持し、トークン破壊を防ぐ
    from sub_def.crypto import get_session, token_generate, token_regenerate, save_session, SESSION_COOKIE_NAME
    session = get_session()
    method = os.environ.get("REQUEST_METHOD", "GET").upper()
    if method == "POST":
        csrf_token = token_regenerate(session)
    else:
        csrf_token = token_generate(session)
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
    }
    merged_context = {**default_context, **context}
    # 呼び出し元での古いトークンの上書きを防止し、確実に最新トークンをフォーム等に反映
    merged_context["csrf_token"] = csrf_token
    
    template_dir = config.Config.get("template_dir", "./templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
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
    except Exception as e:
        sys.stdout.write(f"<html><body><h1>Jinja2 Rendering Error</h1><pre>{e}</pre></body></html>")

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
