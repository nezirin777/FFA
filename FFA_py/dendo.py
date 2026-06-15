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
#------------------------------------------------------#
# チョコボ牧場 edit by いく (http://www.eriicu.com)
# FFA いく改ver2.00 edit by いく
# FFA Emilia Ver1.01 remodeled by Classic (閉鎖)
# FF Battle De I v3.06 remodeling by jun-k (http://www.mj-world.jp/) (更新停止中)
# FF ADVENTURE(改) v1.040 remodeled by GUN (http://www.gun-online.com)
# FF ADVENTURE v0.43 edit by D.Takamiya(CUMRO) 現配布元(管理者ma-ti) (http://www5c.biglobe.ne.jp/~ma-ti/)
#------------------------------------------------------#
"""
FFA Python/CGI 殿堂入り登録・一覧 (dendo.py)
重賞を3勝以上したチョコボを殿堂入り登録し、殿堂入りチョコボの一覧を表示・対戦スロットに登録します。
"""

import os
import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')
import json

# 共通モジュールのインポート
try:
    import common
    import config
except ImportError:
    from . import common
    from . import config

# Windows等で標準出力をUTF-8にするための設定
def main():
    # CGIパラメータ解析
    in_params = common.decode_params()
    user_id = in_params.get("id", "")
    chara_log = in_params.get("mydata", "")
    mode = in_params.get("mode", "")

    # キャラクターデータのロード
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターデータが見つかりません。")
        
    # 重賞レース名のマッピング
    RACE_NAMES = {
        "r1": "チョコボダービー", "r2": "チョコボスタリオン", "r3": "チョコボカップ",
        "r4": "ジェイドカップ", "r5": "BBA賞", "r6": "チョコボ春賞", "r7": "チョコボ秋賞",
        "r8": "チョコボキング", "r9": "チョコボステークス", "r10": "キングスカップ", "r11": "クイーンカップ",
        "r12": "シルバーカップ", "r13": "新潟アドバンス", "r14": "チコスダービー",
        "r15": "チョコボードカップ", "r16": "チョコボエプソム", "r17": "チョコボ王",
        "r18": "ブリーダーズカップ", "r19": "ゴールドカップ", "r20": "プラチナカップ",
        "r21": "チョコボオークス", "r22": "チョコボキングス"
    }

    registered_msg = ""

    # === 殿堂登録処理 ===
    if mode == "dendo":
        # チョコボデータのロード
        choco = common.choco_load(user_id)
        if not choco:
            common.show_error("登録するチョコボがいません。")
            
        cname = choco.get("name", "")
        if not cname or cname == "名無しのチョコボ":
            common.show_error("名前の無いチョコボは登録できません。")
            
        # 個人重賞履歴のロード
        g1_raw = common.choco_g1_load(user_id)
        trophies_count = 0
        my_trophies = []
        if g1_raw:
            for k in RACE_NAMES.keys():
                if g1_raw.get(k, 0) > 0:
                    trophies_count += 1
                    my_trophies.append(RACE_NAMES[k])
                    
        # 3冠チェック
        if trophies_count < 3:
            common.show_error(f"重賞(G1/G2)タイトルを3つ以上獲得していません。(現在: {trophies_count}個)")

        # 殿堂リストをロード
        common.get_lock("dendo_list")
        try:
            dendo_list = common.choco_list_load("denchoco")
            
            # すでに登録されているかチェック (IDと名前で判定)
            hit_idx = -1
            for idx, dc in enumerate(dendo_list):
                if dc.get("id") == user_id and dc.get("name") == cname:
                    hit_idx = idx
                    break
                    
            # 登録用チョコボデータの整形
            dendo_entry = {
                "id": user_id,
                "breader": chara["name"],
                "name": cname,
                "sex": choco.get("sex", 0),
                "blood": choco.get("blood", 0),
                "no": choco.get("no", 0),
                "maxmax": choco.get("maxmax", 70),
                "type": choco.get("type", 0),
                # ステータス
                "c0": choco.get("c0", 10),
                "c1": choco.get("c1", 10),
                "c2": choco.get("c2", 10),
                "c3": choco.get("c3", 10),
                "c4": choco.get("c4", 10),
                "c5": choco.get("c5", 10),
                "c6": choco.get("c6", 10),
                "life": choco.get("life", 1000),
                "train": choco.get("train", 0),
                "run": choco.get("run", 0),
                "win": choco.get("win", 0),
                "max": choco.get("max", 10),
                "gold": choco.get("gold", 0),
                "father": choco.get("father", "不明"),
                "fblood": choco.get("fblood", 0),
                "mother": choco.get("mother", "不明"),
                "mblood": choco.get("mblood", 0),
                # 獲得したトロフィーリストを埋め込む
                "trophies": my_trophies
            }
            
            if hit_idx != -1:
                # 上書き
                dendo_list[hit_idx] = dendo_entry
                registered_msg = f"「{cname}」の殿堂データを更新しましたクポ！"
            else:
                # 新規挿入
                dendo_list.insert(0, dendo_entry)
                registered_msg = f"祝！「{cname}」が殿堂入りチョコボとして登録されましたクポ！"
                
            common.choco_list_regist("denchoco", dendo_list)
        finally:
            common.release_lock("dendo_list")

    # === 一覧表示処理 ===
    # 殿堂リストロード
    dendo_list = common.choco_list_load("denchoco")
    
    # テンプレート表示用にデータを整形
    rank_imgs = [
        "e.gif", "d.gif", "c.gif", "c.gif", "b.gif", "b.gif", "a.gif", "a.gif", "s.gif", "s.gif", "ss.gif", "ss.gif", "ss.gif", "ss.gif", "ss.gif"
    ]
    types = ['普通', '早熟', '晩成', '持続', '超晩成', '超早熟']
    
    formatted_dendo = []
    for dc in dendo_list:
        # トロフィー文字列
        trophy_list = dc.get("trophies", [])
        if trophy_list:
            # G1(赤)とG2(青)を色分けして表示するための文字列生成
            trophy_elements = []
            for t_name in trophy_list:
                # G1/G2の判定 (RACE_NAMES のキー r1..r11 は G1、r12..r22 は G2)
                is_g1 = False
                for r_key, r_name in RACE_NAMES.items():
                    if r_name == t_name:
                        is_g1 = int(r_key[1:]) <= 11
                        break
                color = "red" if is_g1 else "blue"
                trophy_elements.append(f'<span style="color:{color};">● {t_name}</span>')
            trophy_str = "  ".join(trophy_elements)
        else:
            trophy_str = "なし"
            
        formatted_dendo.append({
            "name": dc.get("name", "名無し"),
            "breader": dc.get("breader", "不明"),
            "no": dc.get("no", 0),
            "sex": dc.get("sex", 0),
            "type": dc.get("type", 0),
            "run": dc.get("run", 0),
            "win": dc.get("win", 0),
            "train": dc.get("train", 0),
            "max": dc.get("max", 10),
            "gold": dc.get("gold", 0),
            "father": dc.get("father", "不明"),
            "mother": dc.get("mother", "不明"),
            "c0_t": min(len(rank_imgs) - 1, int(dc.get("c0", 10) / 100)),
            "c1_t": min(len(rank_imgs) - 1, int(dc.get("c1", 10) / 100)),
            "c2_t": min(len(rank_imgs) - 1, int(dc.get("c2", 10) / 100)),
            "c3_t": min(len(rank_imgs) - 1, int(dc.get("c3", 10) / 100)),
            "c4_t": min(len(rank_imgs) - 1, int(dc.get("c4", 10) / 100)),
            "c5_t": min(len(rank_imgs) - 1, int(dc.get("c5", 10) / 100)),
            "c6_t": min(len(rank_imgs) - 1, int(dc.get("c6", 10) / 100)),
            "trophy_str": trophy_str
        })

    context = {
        "chara": chara,
        "chara_log": chara_log,
        "dendo_list": formatted_dendo,
        "rank_imgs": rank_imgs,
        "types": types,
        "registered_msg": registered_msg
    }

    common.render_template("dendo.html", context)

if __name__ == "__main__":
    main()
