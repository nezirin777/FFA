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
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#
"""
FFA Python/CGI 共通モジュール (common.py)
データの読み書き、パラメータ解析、排他制御、Jinja2テンプレート制御を行います。
"""

import os
import sys
import json
import time
import urllib.parse
from typing import NoReturn
from http import cookies
from jinja2 import Environment, FileSystemLoader

# 自モジュールから設定を読み込む（sub_def配下に移動したため親ディレクトリを参照）
try:
    import config
except ImportError:
    from .. import config
Config = config.Config

# パス定義（sub_def配下に移動したため、親ディレクトリをベースディレクトリにする）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




# === 1. パラメータ解析・デコード ===
_decoded_params_cache = None

def decode_params():
    """
    CGIパラメータを解析し、辞書で返します（UTF-8デコード済み）。
    GETとPOST両方に対応しており、同じキーが重複した場合はPOSTボディの値を優先します。
    【CGIストリーム保護キャッシュ】
    標準入力(stdin)は一度しか読み取れないため、パース結果をプロセス内でキャッシュし、
    インポート先で複数回呼び出されても正しくデータを返せるようにします。
    """
    global _decoded_params_cache
    if _decoded_params_cache is not None:
        return _decoded_params_cache

    query_string = os.environ.get("QUERY_STRING", "")
    method = os.environ.get("REQUEST_METHOD", "GET").upper()
    
    body = ""
    if method == "POST":
        try:
            content_length = int(os.environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            content_length = 0
        if content_length > 0:
            body = sys.stdin.read(content_length)

    # クエリパラメータとPOSTボディをそれぞれ個別にパース (クエリよりPOSTを優先するため)
    query_params = urllib.parse.parse_qs(query_string)
    body_params = urllib.parse.parse_qs(body) if body else {}
    
    in_dict = {}
    # まずクエリパラメータを登録
    for k, v in query_params.items():
        if v:
            in_dict[k] = v[0]
        else:
            in_dict[k] = ""
            
    # 次にPOSTボディパラメータを登録（クエリパラメータを上書き）
    for k, v in body_params.items():
        if v:
            in_dict[k] = v[0]
        else:
            in_dict[k] = ""
            
    _decoded_params_cache = in_dict
    return in_dict

# === 2. クッキーの取得・設定 ===
def get_cookie(key=None):
    """
    クライアントから送られたCookieを取得します。
    【セキュリティ堅牢化】
    レガシーの cookie_name (FFAPYCOOKIE) が指定された場合、
    暗号化セッション (FFAPY_SESSION) をデコードして擬似的なクッキー文字列
    "id<>{user_id},pass<>{password_hash}" を返すことで、
    各アクションハンドラの互換性を完全に維持しつつ安全に移行します。
    """
    if key == Config.get('cookie_name'):
        from sub_def.crypto import get_session
        session = get_session()
        if session.get("user_id") and session.get("password_hash"):
            return f"id<>{session['user_id']},pass<>{session['password_hash']}"
        return None
        
    cookie_str = os.environ.get("HTTP_COOKIE", "")
    c = cookies.SimpleCookie()
    c.load(cookie_str)
    
    if key:
        return c.get(key).value if c.get(key) else None
    return {k: v.value for k, v in c.items()}

def set_cookie_header(key, value, max_age=30*24*60*60):
    """
    Cookieを設定するためのSet-Cookieヘッダー文字列を返します。
    【セキュリティ堅牢化】
    レガシーの cookie_name に対する設定が要求された場合、
    値から id と pass を抽出し、暗号化セッションクッキーに変換して保存・返却します。
    """
    if key == Config.get('cookie_name'):
        from sub_def.crypto import get_session, save_session
        user_id = None
        password_hash = None
        pairs = value.split(",")
        for pair in pairs:
            if "<>" in pair:
                k, v = pair.split("<>", 1)
                if k == "id":
                    user_id = v
                elif k == "pass":
                    password_hash = v
        if user_id and password_hash:
            session = get_session()
            session["user_id"] = user_id
            session["password_hash"] = password_hash
            return save_session(session)
            
    c = cookies.SimpleCookie()
    c[key] = value
    c[key]["path"] = "/"
    c[key]["max-age"] = max_age
    return c.output()

# === 3. 排他制御 (ファイル/ディレクトリロック) ===
def get_lock(lock_name, timeout=10):
    """
    os.mkdirを用いたOSアトミックな排他ロックを取得します。
    """
    os.makedirs(Config['lock_dir'], exist_ok=True)
    lock_path = os.path.join(Config['lock_dir'], f"{lock_name}.lock")
    
    start_time = time.time()
    while True:
        try:
            os.mkdir(lock_path)
            return True
        except FileExistsError:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"ロックタイムアウト: {lock_name}")
            time.sleep(0.2)

def release_lock(lock_name):
    """
    排他ロックを解除（ディレクトリ削除）します。
    """
    lock_path = os.path.join(Config['lock_dir'], f"{lock_name}.lock")
    try:
        os.rmdir(lock_path)
    except FileNotFoundError:
        pass

# === 4. セーブデータのロード・セーブ ===
# sub_def のアトミック I/O モジュールを読み込み、データの整合性を一元保証 (ガイドライン2.1に準拠)
from sub_def.file_ops import load_user_all, save_user_all as save_user_unified

def chara_load(user_id):
    """キャラクターの基本ステータスをロードします (統合JSONデータから読み出し)"""
    data = load_user_all(user_id)
    return data.get("chara") if data else None

def item_load(user_id):
    """所持アイテムデータをロードします (統合JSONデータから読み出し)"""
    data = load_user_all(user_id)
    return data.get("item") if data else None

def syoku_load(user_id):
    """職業熟練度データをロードします (統合JSONデータから読み出し)"""
    data = load_user_all(user_id)
    return data.get("syoku") if data else None

def login_log_load(user_id):
    """ログイン履歴をロードします (統合JSONデータから読み出し)"""
    data = load_user_all(user_id)
    return data.get("login_log", []) if data else []

def message_load(user_id):
    """個人メッセージをロードします (統合JSONデータから読み出し)"""
    data = load_user_all(user_id)
    return data.get("message", []) if data else []

def all_message_load():
    """全体メッセージをロードします (共有ファイル排他ロード)"""
    from sub_def.file_ops import load_data_with_lock
    file_path = os.path.join(Config['save_dir'], "all_message.json")
    return load_data_with_lock(file_path, "all_message") or []

def chara_regist(user_id, chara_data):
    """キャラクターの基本ステータスを保存します"""
    data = load_user_all(user_id) or {}
    if "gold" in chara_data and chara_data["gold"] > Config['max_gold']:
        chara_data["gold"] = Config['max_gold']
    data["chara"] = chara_data
    save_user_unified(user_id, data)

def item_regist(user_id, item_data):
    """所持アイテムデータを保存します"""
    data = load_user_all(user_id) or {}
    data["item"] = item_data
    save_user_unified(user_id, data)

def syoku_regist(user_id, syoku_data):
    """職業熟練度データを保存します"""
    data = load_user_all(user_id) or {}
    data["syoku"] = syoku_data
    save_user_unified(user_id, data)

def login_log_regist(user_id, log_data):
    """ログイン履歴を保存します"""
    data = load_user_all(user_id) or {}
    data["login_log"] = log_data
    save_user_unified(user_id, data)

def message_regist(user_id, msg_data):
    """個人メッセージを保存します"""
    data = load_user_all(user_id) or {}
    data["message"] = msg_data
    save_user_unified(user_id, data)

def all_message_regist(msg_data):
    """全体メッセージを保存します (共有ファイルアトミック保存)"""
    from sub_def.file_ops import save_data_atomically
    file_path = os.path.join(Config['save_dir'], "all_message.json")
    save_data_atomically(msg_data, file_path, "all_message")

def save_user_all(user_id, chara, item, syoku):
    """ユーザー全データを一括保存します"""
    data = load_user_all(user_id) or {}
    data["chara"] = chara
    if item is not None:
        data["item"] = item
    if syoku is not None:
        data["syoku"] = syoku
    save_user_unified(user_id, data)

def souko_load(user_id, item_type):
    """倉庫データ(item_type: 'item', 'def', 'acs')をロードします"""
    data = load_user_all(user_id)
    return data.get(f"souko_{item_type}", []) if data else []

def souko_regist(user_id, item_type, data):
    """倉庫データ(item_type: 'item', 'def', 'acs')を保存します"""
    u_data = load_user_all(user_id) or {}
    u_data[f"souko_{item_type}"] = data
    save_user_unified(user_id, u_data)


# === 5. オンラインゲスト更新・表示 ===
def update_and_get_guests(user_id, chara_name):
    """
    ゲストの生存時間を更新し、現在のアクティブな冒険者一覧HTMLを返します。
    """
    from sub_def.file_ops import load_data_with_lock, save_data_atomically
    guest_path = os.path.join(Config['save_dir'], "guest.json")
    now = int(time.time())
    
    guests = load_data_with_lock(guest_path, "guest") or []
    
    # 指定秒以内のアクティブユーザーを抽出（自分自身を除く）
    active_guests = [g for g in guests if g["time"] + Config['active_time'] > now and g["id"] != user_id]
    
    if user_id:
        # 自分を追加
        active_guests.append({"time": now, "name": chara_name, "id": user_id})
        
    save_data_atomically(active_guests, guest_path, "guest")
        
    # HTMLリンク構築
    links = []
    for g in active_guests:
        links.append(f'<a href="{Config["system_script"]}?mode=chara_sts&id={g["id"]}">{g["name"]}</a><font size="1" color="#ffff00">★</font>')
        
    num = len(active_guests)
    html = f'<font size=2 color=#aaaaff>現在冒険中の人(<B>{num}人</B>)：</font>\n'
    if links:
        html += "".join(links)
    else:
        html += "誰もいません"
        
    return html

# === 6. Jinja2 テンプレート制御とレスポンス出力 ===
def render_template(template_name, context=None, extra_headers=None):
    """
    Jinja2テンプレートをレンダリングし、CGIヘッダー付きで出力します。
    """
    from sub_def.utils import render_template as utils_render
    utils_render(template_name, context, extra_headers)

def show_error(msg: str, context: dict | None = None) -> NoReturn:
    """エラー画面を表示します。"""
    from sub_def.utils import show_error as utils_show_error
    utils_show_error(msg, context)

# === 7. 日時フォーマット ===
def get_time_str(t=None):
    """
    時刻を表示用フォーマット (YYYY/MM/DD(曜日) HH:MM:SS) に変換します。
    """
    if t is None:
        t = time.time()
    lt = time.localtime(t)
    wdays = ["日", "月", "火", "水", "木", "金", "土"]
    wday_str = wdays[lt.tm_wday]
    return time.strftime(f"%Y/%m/%d({wday_str}) %H:%M:%S", lt)

# === 8. チョコボおよび農場王者データのロード・セーブ ===
def choco_load(user_id):
    """チョコボデータをロードします"""
    data = load_user_all(user_id)
    return data.get("choco") if data else None

def choco_regist(user_id, choco_data):
    """チョコボデータを保存します"""
    data = load_user_all(user_id) or {}
    data["choco"] = choco_data
    save_user_unified(user_id, data)

def farm_winner_load():
    """農場王者データをロードします"""
    from sub_def.file_ops import load_data_with_lock
    file_path = os.path.join(Config['save_dir'], "farm_winner.json")
    return load_data_with_lock(file_path, "farm_winner")

def farm_winner_regist(winner_data):
    """農場王者データを保存します"""
    from sub_def.file_ops import save_data_atomically
    file_path = os.path.join(Config['save_dir'], "farm_winner.json")
    save_data_atomically(winner_data, file_path, "farm_winner")

def choco_list_load(list_type):
    """お見合い用・野生チョコボリスト('chocoboms', 'chocoboos', 'chocobofile')をロードします"""
    from sub_def.file_ops import load_data_with_lock
    file_path = os.path.join(Config['save_dir'], f"{list_type}.json")
    return load_data_with_lock(file_path, f"choco_list_{list_type}") or []

def choco_list_regist(list_type, data):
    """お見合い用・野生チョコボリスト('chocoboms', 'chocoboos', 'chocobofile')を保存します"""
    from sub_def.file_ops import save_data_atomically
    file_path = os.path.join(Config['save_dir'], f"{list_type}.json")
    save_data_atomically(data, file_path, f"choco_list_{list_type}")

def choco_g1_load(user_id):
    """チョコボ重賞(G1)履歴データをロードします"""
    data = load_user_all(user_id)
    return data.get("choco_g1") if data else None

def choco_g1_regist(user_id, g1_data):
    """チョコボ重賞(G1)履歴データを保存します"""
    data = load_user_all(user_id) or {}
    data["choco_g1"] = g1_data
    save_user_unified(user_id, data)



