#!D:\Python\Python314\python.exe
# -*- coding: utf-8 -*-
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

# 自モジュールから設定を読み込む
try:
    import config
except ImportError:
    from . import config

# パス定義
BASE_DIR = os.path.dirname(os.path.abspath(__file__))




# === 1. パラメータ解析・デコード ===
def decode_params():
    """
    CGIパラメータを解析し、辞書で返します（UTF-8デコード済み）。
    GETとPOST両方に対応しています。
    """
    method = os.environ.get("REQUEST_METHOD", "GET").upper()
    query_string = os.environ.get("QUERY_STRING", "")
    
    body = ""
    if method == "POST":
        try:
            content_length = int(os.environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            content_length = 0
        if content_length > 0:
            body = sys.stdin.read(content_length)

    full_query = query_string
    if body:
        full_query = (full_query + "&" + body) if full_query else body
        
    params = urllib.parse.parse_qs(full_query)
    
    in_dict = {}
    for k, v in params.items():
        if v:
            in_dict[k] = v[0]
        else:
            in_dict[k] = ""
    return in_dict

# === 2. クッキーの取得・設定 ===
def get_cookie(key=None):
    """
    クライアントから送られたCookieを取得します。
    """
    cookie_str = os.environ.get("HTTP_COOKIE", "")
    c = cookies.SimpleCookie()
    c.load(cookie_str)
    
    if key:
        return c.get(key).value if c.get(key) else None
    return {k: v.value for k, v in c.items()}

def set_cookie_header(key, value, max_age=30*24*60*60):
    """
    Cookieを設定するためのSet-Cookieヘッダー文字列を返します。
    """
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
    os.makedirs(config.Config['lock_dir'], exist_ok=True)
    lock_path = os.path.join(config.Config['lock_dir'], f"{lock_name}.lock")
    
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
    lock_path = os.path.join(config.Config['lock_dir'], f"{lock_name}.lock")
    try:
        os.rmdir(lock_path)
    except FileNotFoundError:
        pass

# === 4. セーブデータのロード・セーブ ===
def _user_path(user_id):
    return os.path.join(config.Config['save_dir'], user_id)

def chara_load(user_id):
    """キャラクターの基本ステータスをロードします"""
    path = os.path.join(_user_path(user_id), "chara.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def item_load(user_id):
    """所持アイテムデータをロードします"""
    path = os.path.join(_user_path(user_id), "item.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def syoku_load(user_id):
    """職業熟練度データをロードします"""
    path = os.path.join(_user_path(user_id), "syoku.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def login_log_load(user_id):
    """ログイン履歴をロードします"""
    path = os.path.join(_user_path(user_id), "login_log.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def message_load(user_id):
    """個人メッセージをロードします"""
    path = os.path.join(_user_path(user_id), "message.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def all_message_load():
    """全体メッセージをロードします"""
    path = os.path.join(config.Config['save_dir'], "all_message.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def chara_regist(user_id, chara_data):
    """キャラクターの基本ステータスを保存します"""
    user_dir = _user_path(user_id)
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, "chara.json")
    if "gold" in chara_data and chara_data["gold"] > config.Config['max_gold']:
        chara_data["gold"] = config.Config['max_gold']
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chara_data, f, ensure_ascii=False, indent=2)

def item_regist(user_id, item_data):
    """所持アイテムデータを保存します"""
    user_dir = _user_path(user_id)
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, "item.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item_data, f, ensure_ascii=False, indent=2)

def syoku_regist(user_id, syoku_data):
    """職業熟練度データを保存します"""
    user_dir = _user_path(user_id)
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, "syoku.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(syoku_data, f, ensure_ascii=False, indent=2)

def login_log_regist(user_id, log_data):
    """ログイン履歴を保存します"""
    user_dir = _user_path(user_id)
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, "login_log.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def message_regist(user_id, msg_data):
    """個人メッセージを保存します"""
    user_dir = _user_path(user_id)
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, "message.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(msg_data, f, ensure_ascii=False, indent=2)

def all_message_regist(msg_data):
    """全体メッセージを保存します"""
    os.makedirs(config.Config['save_dir'], exist_ok=True)
    path = os.path.join(config.Config['save_dir'], "all_message.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(msg_data, f, ensure_ascii=False, indent=2)

def save_user_all(user_id, chara, item, syoku):
    """ユーザー全データを一括保存します"""
    get_lock(user_id)
    try:
        chara_regist(user_id, chara)
        if item is not None:
            item_regist(user_id, item)
        if syoku is not None:
            syoku_regist(user_id, syoku)
    finally:
        release_lock(user_id)

def souko_load(user_id, item_type):
    """倉庫データ(item_type: 'item', 'def', 'acs')をロードします"""
    path = os.path.join(_user_path(user_id), f"souko_{item_type}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def souko_regist(user_id, item_type, data):
    """倉庫データ(item_type: 'item', 'def', 'acs')を保存します"""
    user_dir = _user_path(user_id)
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, f"souko_{item_type}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# === 5. オンラインゲスト更新・表示 ===
def update_and_get_guests(user_id, chara_name):
    """
    ゲストの生存時間を更新し、現在のアクティブな冒険者一覧HTMLを返します。
    """
    guest_path = os.path.join(config.Config['save_dir'], "guest.json")
    now = int(time.time())
    
    get_lock("guest")
    try:
        if os.path.exists(guest_path):
            with open(guest_path, "r", encoding="utf-8") as f:
                guests = json.load(f)
        else:
            guests = []
            
        # 120秒以内のアクティブユーザーを抽出（自分自身を除く）
        active_guests = [g for g in guests if g["time"] + config.Config['active_time'] > now and g["id"] != user_id]
        
        # 自分を追加
        active_guests.append({"time": now, "name": chara_name, "id": user_id})
        
        # 保存
        with open(guest_path, "w", encoding="utf-8") as f:
            json.dump(active_guests, f, ensure_ascii=False, indent=2)
    finally:
        release_lock("guest")
        
    # HTMLリンク構築
    links = []
    for g in active_guests:
        links.append(f'<a href="{config.Config['system_script']}?mode=chara_sts&id={g["id"]}">{g["name"]}</a><font size="1" color="#ffff00">★</font>')
        
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
    if context is None:
        context = {}
    if extra_headers is None:
        extra_headers = []
        
    default_context = {
        "config": config.Config,
        "ltime": int(time.time()),
    }
    
    merged_context = {**default_context, **context}
    
    env = Environment(loader=FileSystemLoader(config.Config['template_dir']))
    
    sys.stdout.write("Cache-Control: no-cache\n")
    sys.stdout.write("Pragma: no-cache\n")
    
    for header in extra_headers:
        sys.stdout.write(header + "\n")
        
    sys.stdout.write("Content-type: text/html; charset=utf-8\n\n")
    
    try:
        template = env.get_template(template_name)
        html = template.render(merged_context)
        sys.stdout.write(html)
    except Exception as e:
        sys.stdout.write(f"<html><body><h1>Jinja2 Rendering Error</h1><pre>{e}</pre></body></html>")

def show_error(msg: str, context: dict | None = None) -> NoReturn:
    """エラー画面を表示します。"""
    if context is None:
        context = {}
    err_context = {
        "error_message": msg,
        **context
    }
    render_template("error.html", err_context)
    sys.exit(0)

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
    path = os.path.join(_user_path(user_id), "chocolog.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def choco_regist(user_id, choco_data):
    """チョコボデータを保存します"""
    user_dir = _user_path(user_id)
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, "chocolog.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(choco_data, f, ensure_ascii=False, indent=2)

def farm_winner_load():
    """農場王者データをロードします"""
    path = os.path.join(config.Config['save_dir'], "farm_winner.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def farm_winner_regist(winner_data):
    """農場王者データを保存します"""
    os.makedirs(config.Config['save_dir'], exist_ok=True)
    path = os.path.join(config.Config['save_dir'], "farm_winner.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(winner_data, f, ensure_ascii=False, indent=2)

def choco_list_load(list_type):
    """お見合い用・野生チョコボリスト('chocoboms', 'chocoboos', 'chocobofile')をロードします"""
    path = os.path.join(config.Config['save_dir'], f"{list_type}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def choco_list_regist(list_type, data):
    """お見合い用・野生チョコボリスト('chocoboms', 'chocoboos', 'chocobofile')を保存します"""
    os.makedirs(config.Config['save_dir'], exist_ok=True)
    path = os.path.join(config.Config['save_dir'], f"{list_type}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def choco_g1_load(user_id):
    """チョコボ重賞(G1)履歴データをロードします"""
    path = os.path.join(_user_path(user_id), "chocog1.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def choco_g1_regist(user_id, g1_data):
    """チョコボ重賞(G1)履歴データを保存します"""
    user_dir = _user_path(user_id)
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, "chocog1.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(g1_data, f, ensure_ascii=False, indent=2)



