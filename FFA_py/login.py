#!D:\Python\Python314\python.exe
#------------------------------------------------------#
#  FFA改 Vips Ver 3.00
#  作成者: ねじりん
#------------------------------------------------------#
#------------------------------------------------------#
#　本スクリプトの著作権は下記の4人にあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
#　FF ADVENTURE 改i v2.1
#　programed by jun-k
#　http://www5b.biglobe.ne.jp/~jun-kei/
#　jun-kei@vanilla.freemail.ne.jp
#------------------------------------------------------#
#　FF ADVENTURE v0.21
#　programed by CUMRO
#　http://cgi.members.interq.or.jp/sun/cumro/mm/
#　cumro@sun.interq.or.jp
#------------------------------------------------------#
#  FF ADVENTURE(改) v1.021
#  remodeling by GUN
#  http://www2.to/meeting/
#  gun24@j-club.ne.jp
#------------------------------------------------------#
"""
FFA Python/CGI - アクションルーティング・エントリポイント (login.py)
"""
import sys
import os
import importlib

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

# モジュール検索パスにルートを追加し、cgi_py/ の中からインポート可能にする
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
from sub_def.crypto import get_session, save_session, destroy_session, token_check, token_generate, hash_password
from sub_def.file_ops import load_user_all
from sub_def.utils import redirect, show_error

# ルーティングマッピング定義 (遅延ロード用)
# ※サブモード(yado, geneiなど)からも直接各モジュールにルーティングできるようエイリアスを追加
FUNCTION_MAP = {
    "main": "cgi_py.ffadventure",
    "sts": "cgi_py.sts",
    "tac_change": "cgi_py.tac_change",
    "passchange": "cgi_py.passchange",
    "tensyoku": "cgi_py.tensyoku",
    "shop": "cgi_py.shop",
    "yado": "cgi_py.shop",             # (宿屋サブモード)
    "shop_item": "cgi_py.shop_item",
    "shop_def": "cgi_py.shop_def",
    "shop_acs": "cgi_py.shop_acs",
    "bank": "cgi_py.bank",
    "souko": "cgi_py.souko",
    "battle": "cgi_py.battle",
    "select_battle": "cgi_py.select_battle",
    "sentaku": "cgi_py.select_battle", # (対戦選択)
    "monster": "cgi_py.monster",
    "genei": "cgi_py.monster",         # (修行サブモード: 幻影の城)
    "isekiai": "cgi_py.monster",       # (修行サブモード: 異世界)
    "legend": "cgi_py.legend",
    "boss": "cgi_py.legend",           # (伝説サブモード: ボス挑戦)
    "post_message": "cgi_py.post_message",
    "chocofarm": "cgi_py.chocofarm",
    "morifarm": "cgi_py.morifarm",
    "choco": "cgi_py.morifarm",         # (チョコボの森サブモード)
    "crace": "cgi_py.crace",
    "ctrain": "cgi_py.ctrain",
    "dendo": "cgi_py.dendo",
    "farmrace": "cgi_py.farmrace",
    "system": "cgi_py.system",
    "chara_sts": "cgi_py.system",       # (他者ステータス閲覧)
    "img_list": "cgi_py.system",        # (画像一覧表示)
    "ranking": "cgi_py.system",         # (登録者一覧)
    "tenka": "cgi_py.tenka",
    "all_tenka": "cgi_py.all_tenka",
    "tenka_log": "cgi_py.tenka_log",
    "rank": "cgi_py.rank",
    "chocorank": "cgi_py.chocorank"
}

def main():
    FORM = common.decode_params()
    
    # URLクエリパラメータから直接 'mode' を優先取得 (POST優先のFORMに上書きされない、本来のルーティング先)
    import urllib.parse
    query_string = os.environ.get("QUERY_STRING", "")
    query_params = urllib.parse.parse_qs(query_string)
    route_mode = query_params.get("mode", [""])[0]
    
    # クエリに無い場合は、FORMのmode（POSTボディなど）を使用
    if not route_mode:
        route_mode = FORM.get("mode", "main")
        
    mode = route_mode
    method = os.environ.get("REQUEST_METHOD", "GET").upper()
    
    # 1. ログイン処理 (mode=log_in)
    if mode == "log_in" and method == "POST":
        session = get_session()
        
        # CSRF トークン検証を実行
        token_check(FORM, session)
        
        user_id = FORM.get("id", "").strip()
        password = FORM.get("pass", "").strip()
        
        # 入力値バリデーション (セキュリティ防衛ライン)
        from sub_def.validation import validate_username, validate_password
        err = validate_username(user_id) or validate_password(password)
        if err:
            show_error(err)
            
        user_data = load_user_all(user_id)
        if not user_data or not user_data.get("chara"):
            show_error("登録されていないか、データが見つかりません。")
            
        chara = user_data["chara"]
        
        # パスワード検証 (平文およびストレッチングハッシュ双方に対応)
        hashed_pass = hash_password(password)
        if chara.get("pass") != password and chara.get("pass") != hashed_pass:
            show_error("パスワードが一致しません。")
            
        # ログイン成功、暗号化クッキーセッションデータ生成
        session_data = {
            "user_id": user_id,
            "password_hash": chara.get("pass"),
            "csrf_token": session.get("csrf_token")
        }
        cookie_header = save_session(session_data)
        
        # ユーザーID保存用のクッキーを設定 (Remember Me用、有効期限30日)
        from http import cookies
        import datetime
        saved_user_cookie = cookies.SimpleCookie()
        saved_user_cookie["FFAPY_SAVED_USER"] = user_id
        saved_user_cookie["FFAPY_SAVED_USER"]["path"] = "/"
        
        # 30日間の有効期限を設定 (ブラウザのロケールやタイムゾーンを考慮しGMTフォーマット)
        expires = datetime.datetime.now() + datetime.timedelta(days=30)
        saved_user_cookie["FFAPY_SAVED_USER"]["expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        # ログイン完了後、メイン画面へリダイレクト
        redirect(f"login.py?mode=main", extra_headers=[cookie_header, saved_user_cookie.output()])
        
    # 2. ログアウト処理 (mode=log_out)
    elif mode == "log_out":
        cookie_header = destroy_session()
        redirect("others.py", extra_headers=[cookie_header])
        
    # 3. ログイン中および公開アクションの集中ルーティング
    else:
        session = get_session()
        # ログインが不要な公開モード（ゲストでも閲覧可能）
        public_modes = {"rank", "system", "chara_sts", "img_list", "ranking"}
        
        is_logged_in = False
        user_id = session.get("user_id")
        
        if user_id:
            user_data = load_user_all(user_id)
            if user_data and user_data.get("chara"):
                chara = user_data["chara"]
                # セッション情報とセーブデータのパスワードハッシュを検証
                if chara.get("pass") == session.get("password_hash"):
                    is_logged_in = True
                    
        # 未ログインかつ公開モードでもない場合は、トップページへ強制リダイレクト
        if not is_logged_in and mode not in public_modes:
            redirect("others.py")
            
        # POST メソッド時のみ CSRF トークン検証を行い、不正アクセスを排除
        if method == "POST":
            token_check(FORM, session)
            
        # アクションの動的遅延インポートと実行 (CGI応答性能向上)
        if mode not in FUNCTION_MAP:
            show_error("無効なモード要求です。")
            
        module_path = FUNCTION_MAP[mode]
        try:
            module = importlib.import_module(module_path)
            # 各モジュールをインポートして main() を起動
            module.main()
        except Exception as e:
            # 開発デバッグ用に詳細を表示
            show_error(f"システム実行エラーが発生しました。<pre>{e}</pre>")

if __name__ == "__main__":
    main()
