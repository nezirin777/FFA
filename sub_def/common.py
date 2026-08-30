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
from sub_def import lock_state
import json
import time
import urllib.parse
import html
from typing import NoReturn
from http import cookies

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
        if content_length > Config["max_post_body_bytes"]:
            show_error("送信内容が大きすぎます。")
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
    stale_seconds = Config.get("lock_stale_seconds", 300)

    if lock_state.is_owned(lock_path):
        lock_state.enter(lock_path)
        return True
    
    start_time = time.time()
    while True:
        try:
            os.mkdir(lock_path)
            lock_state.enter(lock_path)
            return True
        except FileExistsError:
            if lock_state.remove_stale_lock_dir(lock_path, stale_seconds):
                continue
            if time.time() - start_time > timeout:
                raise TimeoutError(f"ロックタイムアウト: {lock_name}")
            time.sleep(0.2)

def release_lock(lock_name):
    """
    排他ロックを解除（ディレクトリ削除）します。
    """
    lock_path = os.path.join(Config['lock_dir'], f"{lock_name}.lock")
    if not lock_state.is_owned(lock_path):
        return
    try:
        if lock_state.leave(lock_path):
            os.rmdir(lock_path)
    except FileNotFoundError:
        pass

# === 4. セーブデータのロード・セーブ ===
# sub_def のアトミック I/O モジュールを読み込み、データの整合性を一元保証 (ガイドライン2.1に準拠)
from sub_def.file_ops import load_user_all, save_user_all as save_user_unified

# 現行の能力値キー。旧版の配列順を意味として固定し、表示名と内部キーを一致させる。
STAT_KEYS = ("str", "int", "mnd", "vit", "dex", "agi", "cha", "karma")
ACCESSORY_RATE_KEYS = ("hit_rate", "evasion_rate", "special_rate")

def decode_html_entities(value):
    """旧版データ内のHTMLエンティティを再帰的に文字へ戻します。"""
    if isinstance(value, str):
        return html.unescape(value)
    if isinstance(value, list):
        return [decode_html_entities(item) for item in value]
    if isinstance(value, dict):
        return {key: decode_html_entities(item) for key, item in value.items()}
    return value

def chara_load(user_id):
    """キャラクターの基本ステータスをロードします (統合JSONデータから読み出し)"""
    data = load_user_all(user_id)
    return data.get("chara") if data else None


def get_all_players():
    """保存済みの全キャラクターを読み込む共通の一覧取得処理。"""
    players = []
    save_dir = Config["save_dir"]
    if not os.path.exists(save_dir):
        return players
    for user_id in os.listdir(save_dir):
        if not os.path.isdir(os.path.join(save_dir, user_id)):
            continue
        chara = chara_load(user_id)
        if chara:
            players.append(chara)
    return players

def equipment_load(user_id):
    """所持アイテムデータをロードします (統合JSONデータから読み出し)"""
    data = load_user_all(user_id)
    return data.get("equipment") if data else None


def default_equipment():
    """装備データが未作成のキャラクターに使う初期装備を返します。"""
    return {
        "weapon": {"name": "素手", "atk": 0, "hit_rate": 0},
        "armor": {"name": "衣服", "defense": 0, "evasion_rate": 0},
        "accessory": {
            "name": "なし", "effect_id": 0,
            "bonus": {"str": 0, "int": 0, "mnd": 0, "vit": 0, "dex": 0, "agi": 0, "cha": 0, "karma": 0},
            "hit_rate": 0, "evasion_rate": 0, "special_rate": 0, "description": ""
        }
    }


def load_json_list(file_path):
    """データディレクトリ配下の JSON 配列を読み込み、読込失敗時は空配列を返します。"""
    full_path = file_path if os.path.isabs(file_path) else os.path.join(BASE_DIR, file_path)
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        sys.stderr.write(f"JSON配列の読込に失敗しました: {full_path}: {error}\n")
        return []
    return decode_html_entities(data) if isinstance(data, list) else []


def find_master_record(file_path, record_id):
    """番号付きJSONマスターから1件を取り出し、倉庫用の ``id`` も付けて返す。"""
    try:
        record_id = int(record_id)
    except (TypeError, ValueError):
        return None
    for record in load_json_list(file_path):
        if isinstance(record, dict) and record.get("no") == record_id:
            result = dict(record)
            result["id"] = record_id
            return result
    return None


def master_records_for_job(file_path, job_id):
    """指定職業が装備できる番号付きマスターのレコードを返す。"""
    return [
        record for record in load_json_list(file_path)
        if isinstance(record, dict) and job_id in record.get("job_ids", [])
    ]


def format_accessory_bonus(bonus):
    """装飾品の能力ボーナスを旧版と同じ短い表記に整える。"""
    labels = (
        ("str", "力"), ("int", "知"), ("mnd", "信"), ("vit", "生"),
        ("dex", "器"), ("agi", "速"), ("cha", "魅"), ("karma", "カ"),
    )
    parts = []
    for key, label in labels:
        value = bonus.get(key, 0)
        if value:
            parts.append(f"{label}{'+' if value > 0 else ''}{value}")
    return " ".join(parts) if parts else "効果なし"

def syoku_load(user_id):
    """職業熟練度データをロードします (統合JSONデータから読み出し)"""
    data = load_user_all(user_id)
    return data.get("syoku") if data else None

def login_log_load(user_id):
    """ログイン履歴をロードします (統合JSONデータから読み出し)"""
    data = load_user_all(user_id)
    return data.get("login_log", []) if data else []

def all_message_load():
    """全体メッセージをロードします (共有ファイル排他ロード)"""
    from sub_def.file_ops import load_data_with_lock
    file_path = os.path.join(Config['save_dir'], "all_message.json")
    return load_data_with_lock(file_path, "all_message") or []

def chara_regist(user_id, chara_data):
    """キャラクターの基本ステータスを保存します"""
    if "gold" in chara_data and chara_data["gold"] > Config['max_gold']:
        chara_data["gold"] = Config['max_gold']
    save_user_sections(user_id, chara=chara_data)

def equipment_regist(user_id, item_data):
    """所持アイテムデータを保存します"""
    save_user_sections(user_id, equipment=item_data)

def syoku_regist(user_id, syoku_data):
    """職業熟練度データを保存します"""
    save_user_sections(user_id, syoku=syoku_data)

def login_log_regist(user_id, log_data):
    """ログイン履歴を保存します"""
    save_user_sections(user_id, login_log=log_data)

def all_message_regist(msg_data):
    """全体メッセージを保存します (共有ファイルアトミック保存)"""
    from sub_def.file_ops import save_data_atomically
    file_path = os.path.join(Config['save_dir'], "all_message.json")
    save_data_atomically(msg_data, file_path, "all_message")

def bbs_load():
    """掲示板の投稿一覧をロードします (共有ファイル排他ロード)"""
    from sub_def.file_ops import load_data_with_lock
    file_path = os.path.join(Config['save_dir'], "bbs.json")
    return load_data_with_lock(file_path, "bbs") or []

def bbs_regist(posts):
    """掲示板の投稿一覧を保存します (共有ファイルアトミック保存)"""
    from sub_def.file_ops import save_data_atomically
    file_path = os.path.join(Config['save_dir'], "bbs.json")
    save_data_atomically(posts, file_path, "bbs")

def save_user_all(user_id, chara, item, syoku):
    """ユーザー全データを一括保存します"""
    sections = {"chara": chara}
    if item is not None:
        sections["equipment"] = item
    if syoku is not None:
        sections["syoku"] = syoku
    save_user_sections(user_id, **sections)


def save_user_sections(user_id, **sections):
    """同一ユーザーの複数セクションを1回のread-modify-writeで保存する。

    呼び出し側はユーザー単位のcommon.get_lock()を保持して、別リクエストとの
    競合を防ぐ。chara/equipment/syoku/chocoを個別保存して途中状態を作らない。
    """
    data = load_user_all(user_id) or {}
    data.update(sections)
    save_user_unified(user_id, data)

def souko_load(user_id, item_type):
    """倉庫データ(item_type: 'weapon', 'armor', 'accessory')をロードします"""
    data = load_user_all(user_id)
    return data.get(f"souko_{item_type}", []) if data else []

def souko_regist(user_id, item_type, data):
    """倉庫データ(item_type: 'weapon', 'armor', 'accessory')を保存します"""
    save_user_sections(user_id, **{f"souko_{item_type}": data})


# === 5. アクティブキャラクター更新・表示 ===
def escape_html_text(value) -> str:
    """HTML文字列を組み立てる必要がある互換表示向けの最小エスケープ。"""
    return html.escape(str(value), quote=True)


def update_and_get_active_characters(user_id, chara_name):
    """
    現在アクセス中の他キャラクターを更新し、一覧HTMLを返します。

    ここでいう「アクティブ」はテスト用ゲストアカウントの意味ではなく、
    一定時間以内に街や牧場へアクセスしたキャラクターを指します。
    """
    from sub_def.file_ops import update_data_atomically
    active_character_path = Config["active_characters_file"]
    now = int(time.time())

    def update(characters):
        active_characters = [
            character for character in (characters or [])
            if isinstance(character, dict)
            and character.get("time", 0) + Config["active_character_timeout_seconds"] > now
            and character.get("id") != user_id
        ]
        if user_id:
            active_characters.append({"time": now, "name": chara_name, "id": user_id})
        return active_characters

    active_characters = update_data_atomically(
        active_character_path, "active_characters", update, default=[]
    )

    # HTMLリンク構築
    links = []
    for character in active_characters:
        safe_id = urllib.parse.quote(str(character.get("id", "")), safe="")
        safe_name = escape_html_text(character.get("name", "名無し"))
        links.append(
            f'<a href="{Config["system_script"]}?mode=chara_sts&id={safe_id}">'
            f'{safe_name}</a><font size="1" color="#ffff00">★</font>'
        )

    num = len(active_characters)
    html = f'<font size=2 color=#aaaaff>現在冒険中の人(<B>{num}人</B>)：</font>\n'
    if links:
        html += "".join(links)
    else:
        html += "誰もいません"
        
    return html

# === 6. Jinja2 テンプレート制御とレスポンス出力 ===
def render_template(template_name, context=None, extra_headers=None, session_data=None):
    """
    Jinja2テンプレートをレンダリングし、CGIヘッダー付きで出力します。
    """
    from sub_def.utils import render_template as utils_render
    utils_render(template_name, context, extra_headers, session_data)

def show_error(msg: str, context: dict | None = None) -> NoReturn:
    """エラー画面を表示します。"""
    from sub_def.utils import show_error as utils_show_error
    utils_show_error(msg, context)

def redirect_with_flash(
    url: str,
    message: str,
    toast_type: str = "success",
    duration: int = 3500,
    extra_headers: list[str] | None = None,
) -> NoReturn:
    """トースト通知を積んでから指定URLへリダイレクトします。"""
    from sub_def.utils import redirect_with_flash as utils_redirect_with_flash
    utils_redirect_with_flash(url, message, toast_type, duration, extra_headers)

def to_int(value, default=0):
    """ユーザー入力を安全に整数化する。変換不能なら default を返す（非数値入力によるクラッシュ防止）。"""
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return default

_acs_master_cache = None

def acs_master_get(acs_id):
    """装飾品マスタから指定IDのデータを返します。"""
    global _acs_master_cache
    try:
        acs_id = int(acs_id)
    except (ValueError, TypeError):
        return None
    if acs_id <= 0:
        return None

    if _acs_master_cache is None:
        _acs_master_cache = load_json_list(Config["accessory_file"])

    for item in _acs_master_cache:
        if item.get("no") == acs_id:
            return item
    return None

def accessory_description(accessory, acs_id=0):
    """保存データに説明がない旧データでも、マスタからアクセ説明文を補完します。"""
    if not accessory:
        return ""
    desc = str(accessory.get("description", "")).strip()
    if desc:
        return desc

    master = acs_master_get(acs_id or accessory.get("id") or accessory.get("no"))
    if master:
        return str(master.get("description", "")).strip()
    return ""

def parse_cookie_user(cookie_str):
    """クッキー文字列 "id<>user_id,pass<>password" から ID とパスワードを抽出します。"""
    if not cookie_str:
        return None, None
    id_val = None
    pass_val = None
    for pair in cookie_str.split(","):
        if "<>" in pair:
            k, v = pair.split("<>", 1)
            if k == "id":
                id_val = v
            elif k == "pass":
                pass_val = v
    return id_val, pass_val

def require_owner(user_id):
    """状態変更操作の認可チェック（ロック取得前に呼ぶこと）。
    ログイン中のクッキーが対象 user_id 本人（かつパスワード一致）であることを要求する。
    他人のIDを指定した操作（IDOR）を防ぐ。閲覧系では呼ばない。
    条件を満たさない場合はエラー画面を表示して終了する。
    認証用に chara を（ロック無しで）読み込むだけなので、この時点でロックは保持しないこと。
    """
    cookie_str = get_cookie(Config['cookie_name'])
    c_id, c_pass = parse_cookie_user(cookie_str)
    chara = chara_load(user_id)
    if not c_id or c_id != user_id or not chara or c_pass != chara.get("pass"):
        show_error("認証に失敗しました。ご自身のキャラクターのみ操作できます。再度ログインしてください。")

# === 7. 日時フォーマット ===
def get_time_str(t=None):
    """
    時刻を表示用フォーマット (YYYY/MM/DD(曜日) HH:MM:SS) に変換します。
    """
    if t is None:
        t = time.time()
    lt = time.localtime(t)
    # Python の tm_wday は月曜=0、旧版 Perl の localtime は日曜=0。
    wdays = ["月", "火", "水", "木", "金", "土", "日"]
    wday_str = wdays[lt.tm_wday]
    return time.strftime(f"%Y/%m/%d({wday_str}) %H:%M:%S", lt)

# === 8. チョコボおよび農場王者データのロード・セーブ ===
_CHOCO_REQUIRED_KEYS = {
    "no", "max", "life", "train", "run", "win",
    "c0", "c1", "c2", "c3", "c4", "c5", "c6",
}

def is_choco_owned(choco_data):
    """現在飼育中のチョコボとして扱える実体データかを判定します。"""
    return isinstance(choco_data, dict) and _CHOCO_REQUIRED_KEYS.issubset(choco_data.keys())

def choco_load(user_id):
    """チョコボデータをロードします。未所持・空データは None に正規化します。"""
    data = load_user_all(user_id)
    if not data:
        return None
    choco_data = data.get("choco")
    return choco_data if is_choco_owned(choco_data) else None

def choco_regist(user_id, choco_data):
    """チョコボデータを保存します"""
    data = load_user_all(user_id) or {}
    data["choco"] = choco_data
    save_user_unified(user_id, data)

def choco_delete(user_id, reset_g1=True):
    """飼育中チョコボを未所持状態へ戻します。"""
    data = load_user_all(user_id) or {}
    data["choco"] = {}
    if reset_g1:
        data["choco_g1"] = {}
    save_user_unified(user_id, data)

def chocobo_champion_load():
    """農場王者データをロードします"""
    from sub_def.file_ops import load_data_with_lock
    file_path = Config["chocobo_champion_file"]
    return load_data_with_lock(file_path, "chocobo_champion")

def chocobo_champion_view(winner_data=None):
    """チョコボチャンプを各画面で共通表示するためのデータを作成します。"""
    if winner_data is None:
        winner_data = chocobo_champion_load()
    winner = dict(winner_data) if isinstance(winner_data, dict) else {}
    if not winner:
        winner = {
            "id": "admin",
            "breader": "管理者",
            "name": "ゴールドボコ",
            "no": 1,
            "type": 0,
            "run": 0,
            "win": 0,
            "max": 10,
            "c0": 10,
            "c1": 10,
            "c2": 10,
            "c3": 10,
            "c4": 10,
            "c5": 10,
            "c6": 10,
            "ren": 0,
            "lname": "なし",
            "lbreader": "なし",
        }

    def as_int(value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    win_count = as_int(winner.get("win"))
    class_names = (
        "新馬", "５００万", "９００万", "１６００万", "オープン",
        "グレードⅣ", "グレードⅢ", "グレードⅡ", "グレードⅠ",
    )
    if win_count == 0:
        class_name = class_names[0]
    elif win_count < 5:
        class_name = class_names[1]
    elif win_count < 15:
        class_name = class_names[2]
    elif win_count < 30:
        class_name = class_names[3]
    elif win_count < 50:
        class_name = class_names[4]
    elif win_count < 75:
        class_name = class_names[5]
    elif win_count < 105:
        class_name = class_names[6]
    elif win_count < 140:
        class_name = class_names[7]
    else:
        class_name = class_names[8]

    rank_images = (
        "e.gif", "d.gif", "c.gif", "c.gif", "b.gif", "b.gif", "a.gif",
        "a.gif", "s.gif", "s.gif", "ss.gif", "ss.gif", "ss.gif", "ss.gif",
        "ss.gif",
    )
    ability_labels = ("スピード", "スタミナ", "粘り", "落ち着き", "闘争心", "賢さ", "反射神経")
    abilities = []
    for index, label in enumerate(ability_labels):
        value = as_int(winner.get(f"c{index}"), 10)
        rank_index = min(len(rank_images) - 1, max(0, value // 100))
        abilities.append({"label": label, "value": value, "image": rank_images[rank_index]})

    image_index = as_int(winner.get("no"))
    images = Config.get("choco_images", {})
    image = images.get(image_index, images.get(0, "")) if isinstance(images, dict) else ""
    winner["run"] = as_int(winner.get("run"))
    winner["win"] = win_count
    winner["ren"] = as_int(winner.get("ren"))
    winner["max"] = as_int(winner.get("max"))

    return {
        "raw": winner,
        "id": winner.get("id", ""),
        "owner": winner.get("breader") or winner.get("id", "不明"),
        "name": winner.get("name", "名無しのチョコボ"),
        "image": image,
        "class_name": class_name,
        "distance": winner["max"],
        "run": winner["run"],
        "win": winner["win"],
        "streak": winner["ren"],
        "last_name": winner.get("lname") or "なし",
        "last_owner": winner.get("lbreader") or "なし",
        "abilities": abilities,
    }

def chocobo_champion_register(winner_data):
    """農場王者データを保存します"""
    from sub_def.file_ops import save_data_atomically
    file_path = Config["chocobo_champion_file"]
    save_data_atomically(winner_data, file_path, "chocobo_champion")

def choco_master_load():
    """野生チョコボの購入用マスターデータをロードします。"""
    from sub_def.file_ops import load_data_with_lock
    file_path = os.path.join(BASE_DIR, Config["wild_chocobo_file"])
    return load_data_with_lock(file_path, "chocobo_master") or []

def choco_list_load(list_type):
    """引退チョコボのお見合いリストをロードします。"""
    from sub_def.file_ops import load_data_with_lock
    file_path = os.path.join(Config['save_dir'], f"{list_type}.json")
    return load_data_with_lock(file_path, f"choco_list_{list_type}") or []

def choco_list_regist(list_type, data):
    """引退チョコボのお見合いリストを保存します。"""
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
