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
FFA Python/CGI - ログイン前トップ・その他メニュー表示スクリプト (others.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')
import os
import time

# 共通モジュールと設定モジュールのインポート
import config
import common

def parse_cookie_user(cookie_str):
    if not cookie_str:
        return None, None
    id_val = None
    pass_val = None
    pairs = cookie_str.split(",")
    for pair in pairs:
        if "<>" in pair:
            k, v = pair.split("<>", 1)
            if k == "id":
                id_val = v
            elif k == "pass":
                pass_val = v
    return id_val, pass_val

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
    winner_path = os.path.join(common.BASE_DIR, config.Config['winner_file'])
    if not os.path.exists(winner_path):
        return parse_winner_data("sys<>サイト<>URL<>無名の剣士<>1<>0<>10<>10<>10<>10<>10<>10<>10<>0<>0<>1000<>1000<>1<>0<>0<>無名<>素手<>0<>0<>衣服<>0<>0<>なし<>0<>0<>0<>0<>0<>0<>0<>0<>0<>127.0.0.1<>0<>sys<>無名の剣士<>サイト<>URL<>0<>0<>sys<>無名の剣士<>サイト<>URL<>100<>0<>0<>0<>")
    try:
        with open(winner_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return parse_winner_data("sys<>サイト<>URL<>無名の剣士<>1<>0<>10<>10<>10<>10<>10<>10<>10<>0<>0<>1000<>1000<>1<>0<>0<>無名<>素手<>0<>0<>衣服<>0<>0<>なし<>0<>0<>0<>0<>0<>0<>0<>0<>0<>127.0.0.1<>0<>sys<>無名の剣士<>サイト<>URL<>0<>0<>sys<>無名の剣士<>サイト<>URL<>100<>0<>0<>0<>")
    return parse_winner_data(content)

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    # クッキーからログイン情報取得
    cookie_str = common.get_cookie(config.Config['cookie_name'])
    c_id, c_pass = parse_cookie_user(cookie_str)
    
    # テストプレイ制限チェック (10分=600秒)
    now = int(time.time())
    test_playable = False
    test_chara = common.chara_load("test")
    if test_chara:
        last_time = test_chara.get("last_time", 0)
        if last_time + 600 < now:
            test_playable = True
            
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
    # winnerの総戦闘回数（Perlの$winner[18]に相当するもの。parse_winner_dataでのlevelが総戦闘回数として使われている可能性があります。）
    # Perlの$winner[18]は通常 level です。勝率の式： $ritu = int(($winner[19] / $winner[18]) * 100);
    # ここでの $winner[19] は win_count ですが、winner_char["level"] が総戦闘回数。
    total_count = winner["level"]
    if total_count > 0:
        win_ratio = int((win_count / total_count) * 100)
    else:
        win_ratio = 0
        
    # バーのピクセル幅計算
    divpm = int(config.Config['max_param'] / 100)
    if divpm <= 0:
        divpm = 1
        
    def get_bar_width(val):
        w = int(val / divpm)
        return min(max(w, 1), 100)
        
    # 基本特性値バーの幅
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
    
    # 武器命中補正、防具回避補正など (Perlでは $winner[23] は武器命中率上昇、$winner[26] は防具回避率上昇など。)
    # parse_winner_data で：
    # parts[23] = 武器効果 (effect)
    # parts[26] = 防具効果 (effect)
    # parts[35] = アクセサリー補正 (lp) or 必殺補正？
    # Perlコードでは：
    # $winner[23] は武器の命中率補正。
    # $winner[26] は防具の回避率補正。
    # $winner[35] は必殺補正。
    # ここでは raw_parts から読み込んだ値を使います。
    # winner["equipped_item"]["weapon"]["effect"] 等
    weapon_effect = winner["equipped_item"]["weapon"]["effect"]
    armor_effect = winner["equipped_item"]["armor"]["effect"]
    acs_lp = winner["equipped_item"]["accessory"]["bonus"]["lp"] # カルマ/必殺補正
    
    bw_hit = int(0.5 * (hit_base + weapon_effect))
    bw_kaihi = int(0.5 * (kaihi_base + armor_effect))
    bw_waza = int(waza_base + acs_lp)
    
    bw["hit"] = min(max(bw_hit, 1), 100)
    bw["kaihi"] = min(max(bw_kaihi, 1), 100)
    bw["waza"] = min(max(bw_waza, 1), 100)
    
    # 現在の冒険者一覧HTML取得
    guests_html = common.update_and_get_guests("", "")
    
    # テンプレートレンダリング
    context = {
        "c_id": c_id or "",
        "c_pass": c_pass or "",
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
    common.render_template("others.html", context)

if __name__ == "__main__":
    main()
