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
FFA Python/CGI チョコボトレーニング (ctrain.py)
自身のチョコボをトレーニングし、能力値を上昇させます。
"""

import os
import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')
import random
import time
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
    mode = in_params.get("mode", "race0")

    # キャラクターデータのロード
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターデータが見つかりません。")
        
    # チョコボデータのロード
    choco = common.choco_load(user_id)
    if not choco:
        common.show_error("トレーニングするチョコボを飼育していません。")
        
    cname = choco.get("name", "名無しのチョコボ")
    clife = choco.get("life", 1000)
    
    # 戻るフォーム
    backform_html = f"""
    <form action="{config.Config['chocofarm_script']}" method="post">
      <input type="hidden" name="id" value="{user_id}">
      <input type="hidden" name="mydata" value="{chara_log}">
      <input type="submit" class="btn-farm btn-secondary" value="牧場に戻る">
    </form>
    """
    
    # 体力チェック (200未満なら不可)
    if clife < 200:
        common.show_error(f"チョコボの体力が足りません。宿屋で休ませてください。<br>{backform_html}")

    # トレーニング種類の設定
    # 0: 瞬発力(c0), 1: 持久力(c1), 2: 粘り強さ(c2), 3: 落ち着き(c3), 4: 闘争心(c4), 5: 知力(c5), 6: 切れ味(c6)
    syurui_map = {
        "race0": (0, "バーベルあげ"),
        "race1": (1, "砂浜走り"),
        "race2": (2, "スイミング"),
        "race3": (3, "瞑想"),
        "race4": (4, "猛特訓"),
        "race5": (5, "お勉強"),
        "race6": (6, "坂道ダッシュ")
    }
    
    syurui, subject = syurui_map.get(mode, (0, "バーベルあげ"))

    # キャラクターの時間制限チェック
    now = int(time.time())
    last_time = chara.get("last_time", 0)
    ltime = now - last_time
    if ltime < config.Config['monster_cooldown']:
        wait_sec = config.Config['monster_cooldown'] - ltime
        common.show_error(f"まだトレーニングできません。あと {wait_sec} 秒お待ちください。<br>{backform_html}")

    # アクション時間を更新
    chara["last_time"] = now

    # === 20ターンのトレーニング実行 ===
    turn = 20
    success = 0
    lose = 0
    turns_data = []

    for i in range(1, turn + 1):
        is_success = random.randint(1, 4) != 1 # 3/4の確率で成功
        
        # メッセージの決定
        msg = ""
        if syurui == 0: # 瞬発力
            msg = '<span style="color:#ff5555; font-weight:bold;">重すぎてあがらないクポ！</span>' if not is_success else '<span style="color:#55ff55; font-weight:bold;">バーベルがあがったクポ！</span>'
        elif syurui == 1: # 持久力
            msg = '<span style="color:#ff5555; font-weight:bold;">砂浜で遊んでしまっているクポ...</span>' if not is_success else '<span style="color:#55ff55; font-weight:bold;">砂浜を走りきったクポ！</span>'
        elif syurui == 2: # 粘り強さ
            msg = '<span style="color:#ff5555; font-weight:bold;">おぼれそうになっているクポ！</span>' if not is_success else '<span style="color:#55ff55; font-weight:bold;">スイスイ泳ぎきったクポ！</span>'
        elif syurui == 3: # 落ち着き
            msg = '<span style="color:#ff5555; font-weight:bold;">目の前を通る虫に気を取られているクポ...</span>' if not is_success else '<span style="color:#55ff55; font-weight:bold;">あらゆる雑念を振り払ったクポ！</span>'
        elif syurui == 4: # 闘争心
            msg = '<span style="color:#ff5555; font-weight:bold;">サボっているクポ...</span>' if not is_success else '<span style="color:#55ff55; font-weight:bold;">闘志がみなぎっているクポ！</span>'
        elif syurui == 5: # 知力
            if not is_success:
                msg = '<span style="color:#ff5555; font-weight:bold;">居眠りしているクポ...</span>'
            else:
                mae = random.randint(10, 99)
                usiro = random.randint(10, 99)
                kotae = mae * usiro
                msg = f'<span style="color:#55ff55; font-weight:bold;">難解な問題を解いたクポ！ ({mae} × {usiro} = {kotae})</span>'
        elif syurui == 6: # 切れ味
            msg = '<span style="color:#ff5555; font-weight:bold;">坂道から転げ落ちているクポ！</span>' if not is_success else '<span style="color:#55ff55; font-weight:bold;">疾風のように駆け上がったクポ！</span>'

        if is_success:
            success += 1
        else:
            lose += 1
            
        turns_data.append({
            "success": is_success,
            "msg": msg
        })

    # === 能力値増減の計算 ===
    agari = ""
    senzai = ""
    rousui = ""
    genkai = ""
    
    # チョコボステータスの展開
    c0 = choco.get("c0", 10)
    c1 = choco.get("c1", 10)
    c2 = choco.get("c2", 10)
    c3 = choco.get("c3", 10)
    c4 = choco.get("c4", 10)
    c5 = choco.get("c5", 10)
    c6 = choco.get("c6", 10)
    
    cmax0 = choco.get("max0", 10)
    cmax1 = choco.get("max1", 10)
    cmax2 = choco.get("max2", 10)
    cmax3 = choco.get("max3", 10)
    cmax4 = choco.get("max4", 10)
    cmax5 = choco.get("max5", 10)
    cmax6 = choco.get("max6", 10)
    
    cmax = choco.get("max", 10)
    cmaxmax = choco.get("maxmax", 70)
    cblood = choco.get("blood", 0)
    ctrain = choco.get("train", 0)
    crun = choco.get("run", 0)

    # 1. 成功・失敗が共にある場合
    if success > 0 and lose > 0:
        if syurui == 0:
            c0 += int(success * 2 / 3 + 1)
            c6 -= int(lose / 2 + 1)
            if cmax0 > c0:
                agari = "瞬発力が上がりましたクポ！しかし少し切れ味が鈍ったクポ。"
            else:
                cmax0 += 3
                c0 = cmax0
                agari = f"{cname}の瞬発力は限界のようクポ。しかし強引に限界を突破したクポ！<br>少し切れ味が鈍ったクポ。"
        elif syurui == 1:
            c1 += int(success * 2 / 3 + 1)
            c5 -= int(lose / 2 + 1)
            if cmax1 > c1:
                agari = "持久力が上がりましたクポ！しかし少し知力が低下したクポ。"
            else:
                cmax1 += 3
                c1 = cmax1
                agari = f"{cname}の持久力は限界のようクポ。しかし強引に限界を突破したクポ！<br>少し知力が低下したクポ。"
        elif syurui == 2:
            c2 += int(success / 2)
            if cmax2 > c2:
                agari = "粘り強さが上がりましたクポ！"
            else:
                cmax2 += 3
                c2 = cmax2
                agari = f"{cname}の粘り強さは限界のようクポ。しかし強引に限界を突破したクポ！"
        elif syurui == 3:
            c3 += int(success * 2 / 3 + 1)
            c4 -= int(lose / 2 + 1)
            if cmax3 > c3:
                agari = "落ち着きが上がりましたクポ！しかし少し闘争心が低下したクポ。"
            else:
                cmax3 += 3
                c3 = cmax3
                agari = f"{cname}の落ち着きは限界のようクポ。しかし強引に限界を突破したクポ！<br>少し闘争心が低下したクポ。"
        elif syurui == 4:
            c4 += int(success * 2 / 3 + 1)
            c3 -= int(lose / 2 + 1)
            if cmax4 > c4:
                agari = "闘争心が上がりましたクポ！しかし少し落ち着きが低下したクポ。"
            else:
                cmax4 += 3
                c4 = cmax4
                agari = f"{cname}の闘争心は限界のようクポ。しかし強引に限界を突破したクポ！<br>少し落ち着きが低下したクポ。"
        elif syurui == 5:
            c5 += int(success * 2 / 3 + 1)
            c1 -= int(lose / 2 + 1)
            if cmax5 > c5:
                agari = "知力が上がりましたクポ！しかし少し持久力が低下したクポ。"
            else:
                cmax5 += 3
                c5 = cmax5
                agari = f"{cname}の知力は限界のようクポ。しかし強引に限界を突破したクポ！<br>少し持久力が低下したクポ。"
        elif syurui == 6:
            c6 += int(success * 2 / 3 + 1)
            c0 -= int(lose / 2 + 1)
            if cmax6 > c6:
                agari = "切れ味が上がりましたクポ！しかし少し瞬発力が低下したクポ。"
            else:
                cmax6 += 3
                c6 = cmax6
                agari = f"{cname}の切れ味は限界のようクポ。しかし強引に限界を突破したクポ！<br>少し瞬発力が低下したクポ。"
                
    # 2. 成功のみ（大成功）の場合
    elif success > 0:
        if syurui == 0:
            c0 += int(success * 2 / 3 + 1)
            if cmax0 > c0:
                agari = "大成功クポ！瞬発力が大きく上がりましたクポ！"
            else:
                cmax0 += 5
                c0 = cmax0
                agari = f"大成功クポ！{cname}の瞬発力は限界のようクポが、大きく限界を突破したクポ！"
        elif syurui == 1:
            c1 += int(success * 2 / 3 + 1)
            if cmax1 > c1:
                agari = "大成功クポ！持久力が大きく上がりましたクポ！"
            else:
                cmax1 += 5
                c1 = cmax1
                agari = f"大成功クポ！{cname}の持久力は限界のようクポが、大きく限界を突破したクポ！"
        elif syurui == 2:
            c2 += int(success / 2)
            if cmax2 > c2:
                agari = "大成功クポ！粘り強さが大きく上がりましたクポ！"
            else:
                cmax2 += 5
                c2 = cmax2
                agari = f"大成功クポ！{cname}の粘り強さは限界のようクポが、大きく限界を突破したクポ！"
        elif syurui == 3:
            c3 += int(success * 2 / 3 + 1)
            if cmax3 > c3:
                agari = "大成功クポ！落ち着きが大きく上がりましたクポ！"
            else:
                cmax3 += 5
                c3 = cmax3
                agari = f"大成功クポ！{cname}の落ち着きは限界のようクポが、大きく限界を突破したクポ！"
        elif syurui == 4:
            c4 += int(success * 2 / 3 + 1)
            if cmax4 > c4:
                agari = "大成功クポ！闘争心が大きく上がりましたクポ！"
            else:
                cmax4 += 5
                c4 = cmax4
                agari = f"大成功クポ！{cname}の闘争心は限界のようクポが、大きく限界を突破したクポ！"
        elif syurui == 5:
            c5 += int(success * 2 / 3 + 1)
            if cmax5 > c5:
                agari = "大成功クポ！知力が大きく上がりましたクポ！"
            else:
                cmax5 += 5
                c5 = cmax5
                agari = f"大成功クポ！{cname}の知力は限界のようクポが、大きく限界を突破したクポ！"
        elif syurui == 6:
            c6 += int(success * 2 / 3 + 1)
            if cmax6 > c6:
                agari = "大成功クポ！切れ味が大きく上がりましたクポ！"
            else:
                cmax6 += 5
                c6 = cmax6
                agari = f"大成功クポ！{cname}の切れ味は限界のようクポが、大きく限界を突破したクポ！"
                
    # 3. 失敗のみの場合
    else:
        if syurui == 0:
            c6 -= int(lose / 2 + 1)
            agari = "すべて失敗クポ……切れ味が鈍ってしまったクポ。"
        elif syurui == 1:
            c5 -= int(lose / 2 + 1)
            agari = "すべて失敗クポ……知力が低下してしまったクポ。"
        elif syurui == 2:
            agari = "すべて失敗クポ……何の成果も得られなかったクポ。"
        elif syurui == 3:
            c4 -= int(lose / 2 + 1)
            agari = "すべて失敗クポ……闘争心が低下してしまったクポ。"
        elif syurui == 4:
            c3 -= int(lose / 2 + 1)
            agari = "すべて失敗クポ……落ち着きが低下してしまったクポ。"
        elif syurui == 5:
            c1 -= int(lose / 2 + 1)
            agari = "すべて失敗クポ……持久力が低下してしまったクポ。"
        elif syurui == 6:
            c0 -= int(lose / 2 + 1)
            agari = "すべて失敗クポ……瞬発力が低下してしまったクポ。"

    # パラメータの下限チェック (マイナスなら 1 にして最大限界値を -5)
    c_vals = [c0, c1, c2, c3, c4, c5, c6]
    c_names = ["瞬発力", "持久力", "粘り強さ", "落ち着き", "闘争心", "知力", "切れ味"]
    for idx in range(7):
        if c_vals[idx] < 0:
            genkai += f"{c_names[idx]}が低下しすぎて、チョコボがひねくれてしまったクポ！（最大能力限界 -5）<br>"
            c_vals[idx] = 1
            cmaxmax -= 5
            
    c0, c1, c2, c3, c4, c5, c6 = c_vals

    # 老衰チェック
    ctrain += 1
    if ctrain + crun > 1000:
        cmaxmax = int(cmaxmax * 0.99)
        rousui = f"あぁ、もう{cname}の体は限界のようですクポ。<br>よくこれまで育ててくれたと思いますクポ。<br>そろそろお見合い（引退）の時期ではないでしょうかクポ。"

    # パラメータ上限クランプ
    cmax0_v = max(cmax0, 1)
    cmax1_v = max(cmax1, 1)
    cmax2_v = max(cmax2, 1)
    cmax3_v = max(cmax3, 1)
    cmax4_v = max(cmax4, 1)
    cmax5_v = max(cmax5, 1)
    cmax6_v = max(cmax6, 1)
    
    if c0 > cmax0_v:
        genkai += "瞬発力の個別の限界に達したクポ！<br>"
        c0 = cmax0_v
    if c1 > cmax1_v:
        genkai += "持久力の個別の限界に達したクポ！<br>"
        c1 = cmax1_v
    if c2 > cmax2_v:
        genkai += "粘り強さの個別の限界に達したクポ！<br>"
        c2 = cmax2_v
    if c3 > cmax3_v:
        genkai += "落ち着きの個別の限界に達したクポ！<br>"
        c3 = cmax3_v
    if c4 > cmax4_v:
        genkai += "闘争心の個別の限界に達したクポ！<br>"
        c4 = cmax4_v
    if c5 > cmax5_v:
        genkai += "知力の個別の限界に達したクポ！<br>"
        c5 = cmax5_v
    if c6 > cmax6_v:
        genkai += "切れ味の個別の限界に達したクポ！<br>"
        c6 = cmax6_v

    # 寿命・限界値の計算
    clife -= 50
    cmax += 5
    
    # 総合限界判定
    c_sum = c0 + c1 + c2 + c3 + c4 + c5 + c6
    if cmax > cmaxmax:
        cmax = cmaxmax
        if c_sum > cmax:
            senzai = f"{cname}の能力は総合的な限界に達したクポ。これ以上の成長は見込めないクポ。<br>"
            # 1/3の確率で最大限界を+2
            if random.randint(1, 3) == 1:
                cmaxmax += 2
                senzai += "しかし！今回の頑張りで最大能力限界が +2 突破したクポ！<br>"
                
            # 比率クランプ
            wariai = cmax / c_sum
            c0 = int(c0 * wariai) + 1
            c1 = int(c1 * wariai) + 1
            c2 = int(c2 * wariai) + 1
            c3 = int(c3 * wariai) + 1
            c4 = int(c4 * wariai) + 1
            c5 = int(c5 * wariai) + 1
            c6 = int(c6 * wariai) + 1
        else:
            senzai = "最大能力限界には達しているが、まだ成長の余地はあるクポ。<br>"
    elif c_sum > cmax:
        # トレーニング限界（出走して潜在を引き出す必要あり）
        wariai = cmax / c_sum
        c0 = int(c0 * wariai) + 1
        c1 = int(c1 * wariai) + 1
        c2 = int(c2 * wariai) + 1
        c3 = int(c3 * wariai) + 1
        c4 = int(c4 * wariai) + 1
        c5 = int(c5 * wariai) + 1
        c6 = int(c6 * wariai) + 1
        senzai = f"トレーニングのみでの成長限界に達したクポ。<br>レースに出て潜在能力を開放するクポ！<br>"

    # === データの保存 ===
    # チョコボデータの更新
    choco["c0"] = c0; choco["c1"] = c1; choco["c2"] = c2
    choco["c3"] = c3; choco["c4"] = c4; choco["c5"] = c5; choco["c6"] = c6
    choco["max0"] = cmax0; choco["max1"] = cmax1; choco["max2"] = cmax2
    choco["max3"] = cmax3; choco["max4"] = cmax4; choco["max5"] = cmax5; choco["max6"] = cmax6
    choco["life"] = clife
    choco["max"] = cmax
    choco["maxmax"] = cmaxmax
    choco["train"] = ctrain

    # キャラクターとチョコボの排他保存
    common.get_lock(user_id)
    try:
        common.chara_regist(user_id, chara)
    finally:
        common.release_lock(user_id)

    common.get_lock(f"choco_{user_id}")
    try:
        common.choco_regist(user_id, choco)
    finally:
        common.release_lock(f"choco_{user_id}")

    # テンプレートへの受け渡しコンテキスト
    context = {
        "chara": chara,
        "chara_log": chara_log,
        "choco": choco,
        "subject": subject,
        "success": success,
        "lose": lose,
        "agari": agari,
        "senzai": senzai,
        "genkai": genkai,
        "rousui": rousui,
        "turns_json": json.dumps(turns_data)
    }

    common.render_template("ctrain.html", context)

if __name__ == "__main__":
    main()
