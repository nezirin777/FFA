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

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
Config = config.Config

def parse_winner_data(winner_str):
    """王者ファイルデータを解析し、キャラクター辞書を返します"""
    parts = winner_str.strip().split("<>")
    if parts and parts[-1] == "":
        parts = parts[:-1]
        
    def get_val(lst, idx, default=""):
        return lst[idx] if idx < len(lst) else default
        
    def to_i(val):
        try: return int(val)
        except: return 0

    winner_char = {
        "id": get_val(parts, 0, "sys"),
        "site": get_val(parts, 1),
        "url": get_val(parts, 2),
        "name": get_val(parts, 3, "無名の剣士"),
        "sex": to_i(get_val(parts, 4)),
        "img": to_i(get_val(parts, 5)),
        "str": to_i(get_val(parts, 6)),
        "int": to_i(get_val(parts, 7)),
        "dex": to_i(get_val(parts, 8)),
        "vit": to_i(get_val(parts, 9)),
        "agi": to_i(get_val(parts, 10)),
        "mnd": to_i(get_val(parts, 11)),
        "lck": to_i(get_val(parts, 12)),
        "lp": to_i(get_val(parts, 13)),
        "job": to_i(get_val(parts, 14)),
        "hp": to_i(get_val(parts, 15)),
        "max_hp": to_i(get_val(parts, 16)),
        "level": to_i(get_val(parts, 17)),
        "comment": get_val(parts, 20),
        "host": get_val(parts, 37),
        "job_level": to_i(get_val(parts, 38)),
        "win_count": to_i(get_val(parts, 43)),
        "max_win_count": to_i(get_val(parts, 44)),
        "max_win_id": get_val(parts, 45),
        "max_win_name": get_val(parts, 46),
        "gold": to_i(get_val(parts, 49)),
    }
    
    winner_item = {
        "weapon": {
            "name": get_val(parts, 21, "素手"),
            "dmg": to_i(get_val(parts, 22)),
            "effect": to_i(get_val(parts, 23))
        },
        "armor": {
            "name": get_val(parts, 24, "衣服"),
            "def": to_i(get_val(parts, 25)),
            "effect": to_i(get_val(parts, 26))
        },
        "accessory": {
            "name": get_val(parts, 27, "なし"),
            "effect_id": to_i(get_val(parts, 50)),
            "bonus": {
                "str": to_i(get_val(parts, 28)),
                "int": to_i(get_val(parts, 29)),
                "dex": to_i(get_val(parts, 30)),
                "vit": to_i(get_val(parts, 31)),
                "agi": to_i(get_val(parts, 32)),
                "mnd": to_i(get_val(parts, 33)),
                "lck": to_i(get_val(parts, 34)),
                "lp": to_i(get_val(parts, 35)),
            },
            "attrib": to_i(get_val(parts, 51)),
            "spare1": to_i(get_val(parts, 52)),
            "spare2": to_i(get_val(parts, 53)),
            "spare3": 0
        }
    }
    winner_char["equipped_item"] = winner_item
    return winner_char

def get_winner():
    winner_path = os.path.join(common.BASE_DIR, Config['winner_file'])
    if not os.path.exists(winner_path):
        return parse_winner_data("sys<>サイト<>URL<>無名の剣士<>1<>0<>10<>10<>10<>10<>10<>10<>10<>0<>0<>1000<>1000<>1<>0<>0<>無名<>素手<>0<>0<>衣服<>0<>0<>なし<>0<>0<>0<>0<>0<>0<>0<>0<>0<>127.0.0.1<>0<>sys<>無名の剣士<>サイト<>URL<>0<>0<>sys<>無名の剣士<>サイト<>URL<>100<>0<>0<>0<>")
    try:
        with open(winner_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return parse_winner_data("sys<>サイト<>URL<>無名の剣士<>1<>0<>10<>10<>10<>10<>10<>10<>10<>0<>0<>1000<>1000<>1<>0<>0<>無名<>素手<>0<>0<>衣服<>0<>0<>なし<>0<>0<>0<>0<>0<>0<>0<>0<>0<>127.0.0.1<>0<>sys<>無名の剣士<>サイト<>URL<>100<>0<>0<>0<>")
    return parse_winner_data(content)

def main():
    if Config['maintenance_mode']:
        from sub_def.utils import show_error
        show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    # === 暗号化クッキーセッション管理の導入 (改ざん・不正アクセス防御) ===
    from sub_def.crypto import get_session, token_generate, save_session
    from sub_def.file_ops import load_user_all
    from sub_def.utils import redirect, render_template
    
    session = get_session()
    if session.get("user_id"):
        user_id = session["user_id"]
        user_data = load_user_all(user_id)
        if user_data and user_data.get("chara"):
            chara = user_data["chara"]
            # セッションハッシュと一致するか検証 (None-Safety 確保)
            if chara.get("pass") == session.get("password_hash"):
                # すでに有効なセッションがある場合はメイン画面(login.py?mode=main)へ自動リダイレクト (NoReturn制御)
                redirect(f"{Config['login_script']}?mode=main")
                
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
