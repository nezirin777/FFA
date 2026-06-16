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
FFA Python/CGI - ログイン前トップ・その他メニュー表示スクリプト (others.py)
"""
import sys
import os
import time
import json

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
Config = config.Config

DEFAULT_WINNER = {
    "id": "sys",
    "site": "サイト",
    "url": "URL",
    "name": "無名の剣士",
    "sex": 1,
    "img": 0,
    "str": 10,
    "int": 10,
    "dex": 10,
    "vit": 10,
    "agi": 10,
    "mnd": 10,
    "lck": 10,
    "lp": 0,
    "job": 0,
    "hp": 1000,
    "max_hp": 1000,
    "level": 1,
    "unused21": 0,
    "unused22": 0,
    "comment": "無名",
    "equipped_item": {
        "weapon": { "name": "素手", "dmg": 0, "effect": 0 },
        "armor": { "name": "衣服", "def": 0, "effect": 0 },
        "accessory": {
            "name": "なし",
            "effect_id": 0,
            "bonus": {
                "str": 0, "int": 0, "dex": 0, "vit": 0, "agi": 0, "mnd": 0, "lck": 0, "lp": 0
            },
            "attrib": 0,
            "spare1": 0,
            "spare2": 0,
            "spare3": 0
        }
    },
    "unused30": 0,
    "host": "127.0.0.1",
    "job_level": 0,
    "last_challenger": {
        "id": "sys",
        "name": "無名の剣士",
        "site": "サイト",
        "url": "URL"
    },
    "win_count": 0,
    "max_win_count": 0,
    "max_win_id": "sys",
    "max_win_name": "無名の剣士",
    "max_win_site": "サイト",
    "max_win_url": "URL",
    "gold": 100
}

def get_winner():
    winner_path = os.path.join(common.BASE_DIR, Config['winner_file'])
    if not os.path.exists(winner_path):
        return DEFAULT_WINNER
    try:
        with open(winner_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_WINNER

def main():
    if Config['maintenance_mode']:
        from sub_def.utils import show_error
        show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    # === 暗号化クッキーセッション管理の導入 (改ざん・不正アクセス防御) ===
    from sub_def.crypto import get_session, token_generate, save_session
    from sub_def.file_ops import load_user_all
    from sub_def.utils import redirect, render_template
    from http import cookies
    
    # ユーザーID保存用クッキー (Remember Me) の読み込み
    cookie_str = os.environ.get("HTTP_COOKIE", "")
    cookie = cookies.SimpleCookie()
    cookie.load(cookie_str)
    c_id = ""
    if "FFAPY_SAVED_USER" in cookie:
        c_id = cookie["FFAPY_SAVED_USER"].value
        
    is_logged_in = False
    chara_name = ""
    session = get_session()
    if session.get("user_id"):
        user_id = session["user_id"]
        user_data = load_user_all(user_id)
        if user_data and user_data.get("chara"):
            chara = user_data["chara"]
            # セッションハッシュと一致するか検証 (None-Safety 確保)
            if chara.get("pass") == session.get("password_hash"):
                is_logged_in = True
                chara_name = chara.get("name", "冒険者")
                
    # CSRF トークンを生成してセッションに紐付ける (ガイドラインに準拠)
    csrf_token = token_generate(session)
    cookie_header = save_session(session)
    
    # チャンプデータの読み込み
    winner = get_winner()
    
    # クラス名算出
    class_flg = int(winner["job_level"] / 10)
    class_marks = [
        "■□□□□□ (Beginner)",
        "■■□□□□ (Challenger)",
        "■■■□□□ (Low Class)",
        "■■■■□□ (Normal Class)",
        "■■■■■□ (High Class)",
        "■■■■■■ (Top Class)",
        "★★★★★★ (Master)"
    ]
    if class_flg >= len(class_marks):
        class_flg = len(class_marks) - 1
    winner_class = class_marks[class_flg]
    
    # 勝率算出
    win_count = winner["win_count"]
    total_count = winner["level"]
    win_ratio = int((win_count / total_count) * 100) if total_count > 0 else 0
        
    # バーのピクセル幅計算
    divpm = int(Config['max_param'] / 100)
    if divpm <= 0:
        divpm = 1
        
    def get_bar_width(val):
        w = int(val / divpm)
        return min(max(w, 1), 100)
        
    bw = {
        "str": get_bar_width(winner["str"]),
        "int": get_bar_width(winner["int"]),
        "dex": get_bar_width(winner["dex"]),
        "vit": get_bar_width(winner["vit"]),
        "agi": get_bar_width(winner["agi"]),
        "mnd": get_bar_width(winner["mnd"]),
        "lck": get_bar_width(winner["lck"]),
        "lp": get_bar_width(winner["lp"])
    }
    
    # 命中率・回避率・必殺率の計算
    hit_base = int(winner["dex"] / 10) + 51
    hit_base = min(hit_base, 150)
    
    kaihi_base = int(winner["agi"] / 20)
    kaihi_base = min(kaihi_base, 50)
    
    waza_base = int(winner["lp"] / 15) + 10 + winner["job_level"]
    waza_base = min(waza_base, 75)
    
    weapon_effect = winner["equipped_item"]["weapon"]["effect"]
    armor_effect = winner["equipped_item"]["armor"]["effect"]
    acs_lp = winner["equipped_item"]["accessory"]["bonus"]["lp"]
    
    bw_hit = int(0.5 * (hit_base + weapon_effect))
    bw_kaihi = int(0.5 * (kaihi_base + armor_effect))
    bw_waza = int(waza_base + acs_lp)
    
    bw["hit"] = min(max(bw_hit, 1), 100)
    bw["kaihi"] = min(max(bw_kaihi, 1), 100)
    bw["waza"] = min(max(bw_waza, 1), 100)
    
    # テストプレイの可否判定 (10分のロック時間制御)
    test_playable = True
    test_data = load_user_all("test")
    if test_data and test_data.get("chara"):
        test_chara = test_data["chara"]
        last_time = test_chara.get("last_time", 0)
        if time.time() - last_time < 600:
            test_playable = False
            
    # 現在の冒険者一覧HTML取得
    guests_html = common.update_and_get_guests("", "")
    
    # テンプレートレンダリング (CSRFトークンを注入)
    context = {
        "csrf_token": csrf_token,
        "c_id": c_id,  # ログイン画面のユーザー名入力フィールド初期値
        "is_logged_in": is_logged_in,
        "chara_name": chara_name,
        "test_playable": test_playable,
        "winner": winner,
        "winner_class": winner_class,
        "win_ratio": win_ratio,
        "bw": bw,
        "hit_base": hit_base,
        "kaihi_base": kaihi_base,
        "waza_base": waza_base,
        "guests_html": guests_html
    }
    render_template("others.html", context, extra_headers=[cookie_header])

if __name__ == "__main__":
    main()
