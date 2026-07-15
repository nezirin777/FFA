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
FFA Python/CGI チョコボ王者戦 (farmrace.py)
現在の王者チョコボと1対1で対戦し、勝てば新王者として登録されます。
"""

import os
import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
import random
import time
import json

# 共通モジュールのインポート
try:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    import config
except ImportError:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from . import config

# Windows等で標準出力をUTF-8にするための設定
def main():
    # CGIパラメータ解析
    in_params = common.decode_params()
    user_id = in_params.get("id", "")
    chara_log = in_params.get("mydata", "")

    # キャラクターデータのロード
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターデータが見つかりません。")
        
    # チョコボデータのロード
    choco = common.choco_load(user_id)
    if not choco:
        common.show_error("レースに出走させるチョコボを飼育していません。")
        
    cname = choco.get("name", "名無しのチョコボ")
    clife = choco.get("life", 1000)
    cwin = choco.get("win", 0)
    crun = choco.get("run", 0)
    ctrain = choco.get("train", 0)
    
    # 戻るフォーム (error.html 側で最新のCSRFトークン付きで描画される)
    back_ctx = {
        "back_action": config.Config['chocofarm_script'],
        "back_params": {"id": user_id, "mydata": chara_log},
        "back_label": "牧場に戻る",
    }

    # バリデーション
    if not cname or cname == "名無しのチョコボ":
        common.show_error("チョコボに名前を付けてからレースに出走させてください。", back_ctx)
    if clife < 400:
        common.show_error("チョコボの体力が足りません。宿屋で休ませてから出走させてください。", back_ctx)

    # 時間制限チェック (30秒間隔)
    now = int(time.time())
    last_time = chara.get("last_time", 0)
    ltime = now - last_time
    if ltime < config.Config['battle_cooldown']:
        wait_sec = config.Config['battle_cooldown'] - ltime
        common.show_error(f"まだレースに出走できません。あと {wait_sec} 秒お待ちください。", back_ctx)

    # 王者データのロード
    winner = common.farm_winner_load()
    if not winner:
        # 初期王者設定
        winner = {
            "id": "admin",
            "pass": "",
            "breader": "管理者",
            "site": "",
            "url": "",
            "name": "ゴールドボコ",
            "no": 1,
            "type": 0,
            "run": 0,
            "win": 0,
            "max": 1000,
            "c0": 200, "c1": 200, "c2": 200, "c3": 200, "c4": 200, "c5": 200, "c6": 200,
            "ren": 0,
            "lname": "なし",
            "lsite": "",
            "lurl": "",
            "lbreader": "なし",
            "father": "不明",
            "mother": "不明"
        }

    # すでに王者かどうかのチェック
    if winner.get("id") == user_id and winner.get("name") == cname:
        common.show_error("現在あなたのチョコボが王者なので、挑戦レースはできません。", back_ctx)

    # アクション時間更新
    chara["last_time"] = now

    # === レース進行シミュレーション ===
    # パラメータの取得
    c0 = choco.get("c0", 10); wc0 = winner.get("c0", 10)
    c1 = choco.get("c1", 10); wc1 = winner.get("c1", 10)
    c2 = choco.get("c2", 10); wc2 = winner.get("c2", 10)
    c3 = choco.get("c3", 10); wc3 = winner.get("c3", 10)
    c4 = choco.get("c4", 10); wc4 = winner.get("c4", 10)
    c5 = choco.get("c5", 10); wc5 = winner.get("c5", 10)
    c6 = choco.get("c6", 10); wc6 = winner.get("c6", 10)
    
    wcren = winner.get("ren", 0)
    wcmax = winner.get("max", 10)
    wcname = winner.get("name", "ゴールドボコ")
    wcbreader = winner.get("breader", "管理者")
    
    # 基礎比率算出
    heri = (c2 + wc2) / 4000
    nebari = int((c2 + wc2) / 2)
    kisyou = int((c3 + wc3) / 2)
    seriai = int((c4 + wc4) / 2)
    tiryoku = int((c5 + wc5) / 2)
    
    tyousei = 2000 / max(1, c0 + wc0)
    kinryoku = int((c0 + wc0) / 2)
    
    lastspart = int(((c0 + wc0) / 3 + (c6 + wc6)) / 60)
    if lastspart <= 0:
        lastspart = 1

    total_dist = 2400
    knokori = total_dist # あなたの残り
    wnokori = total_dist # 王者の残り
    
    khp_flg = c1
    whp_flg = wc1
    
    turns_data = []
    step = 0
    win = False
    syasin = False
    
    while step < 100:
        step += 1
        step_comment = ""
        kdmg = 0
        wdmg = 0
        
        # 1. スタート処理
        if step == 1:
            # プレイヤーのスタートダッシュ
            if random.randint(0, kisyou) <= random.randint(0, int(c3 * 2 / 3)):
                kdmg = int(random.randint(0, int(c0 / (tyousei * 4))) + c0 / (tyousei * 4))
                step_comment += f'<span class="red">{cname}はスタートで出遅れましたクポ！</span> '
                ksyoumou = heri * kdmg * 3 * (kisyou / max(1, c3)) * (c2 / max(1, nebari))
            elif random.randint(0, tiryoku) <= random.randint(0, int(c5 * 2 / 3)):
                kdmg = int(random.randint(0, int(c0 * 1.5 / tyousei)))
                step_comment += f'<span class="green">{cname}は好スタート！</span> '
                ksyoumou = heri * (kdmg / 2) * (kisyou / max(1, c3)) * (c2 / max(1, nebari))
            else:
                kdmg = int(random.randint(0, int(c0 / (tyousei * 2))) + c0 / (tyousei * 2))
                ksyoumou = heri * kdmg * (kisyou / max(1, c3)) * (c2 / max(1, nebari))
                
            # 王者のスタートダッシュ
            if random.randint(0, kisyou) <= random.randint(0, int(wc3 * 2 / 3)):
                wdmg = int(random.randint(0, int(wc0 / (tyousei * 4))) + wc0 / (tyousei * 4))
                step_comment += f'<span class="red-light">王者{wcname}はスタートで出遅れたクポ！</span> '
                wsyoumou = heri * wdmg * 3 * (kisyou / max(1, wc3)) * (wc2 / max(1, nebari))
            elif random.randint(0, tiryoku) <= random.randint(0, int(wc5 * 2 / 3)):
                wdmg = int(random.randint(0, int(wc0 * 1.5 / tyousei)))
                step_comment += f'<span class="yellow">王者{wcname}は好スタートを切ったクポ！</span> '
                wsyoumou = heri * (wdmg / 2) * (kisyou / max(1, wc3)) * (wc2 / max(1, nebari))
            else:
                wdmg = int(random.randint(0, int(wc0 / (tyousei * 2))) + wc0 / (tyousei * 2))
                wsyoumou = heri * wdmg * (kisyou / max(1, wc3)) * (wc2 / max(1, nebari))
                
            ksyoumou = ksyoumou / 2
            wsyoumou = wsyoumou / 2
            
            knokori -= kdmg
            wnokori -= wdmg
            khp_flg -= ksyoumou
            whp_flg -= wsyoumou
            
            if knokori < wnokori:
                step_comment += f"<br>スタート！先頭は {cname} クポ！"
            else:
                step_comment += f"<br>スタート！王者 {wcname} がハナを奪うクポ！"

        # 2. 中盤・終盤の移動
        else:
            # プレイヤーの移動力
            kdmg = (random.randint(0, c0) + random.randint(0, c6) + random.randint(0, c6) + random.randint(0, c6)) / lastspart
            ksyoumou = heri * kdmg * (kisyou / max(1, c3)) * (c2 / max(1, nebari))
            
            if khp_flg <= 0:
                if random.randint(0, nebari) < random.randint(0, c2):
                    kdmg = kdmg * 1.2
                    ksyoumou = ksyoumou * 0.5
                else:
                    kdmg = kdmg / 3
                    if step % 4 == 0:
                        step_comment += f'<span class="red">{cname}はバテています...</span> '
            elif (random.randint(0, seriai) < random.randint(0, c4)) or (khp_flg / max(1, c1) >= 0.4):
                ksyoumou = ksyoumou * 2
                kdmg = kdmg * 2.2
                if step % 4 == 0:
                    step_comment += f'<span class="green">{cname}のラストスパート！</span> '
                    
            kdmg = int(kdmg)
            
            # 王者の移動力
            wdmg = (random.randint(0, wc0) + random.randint(0, wc6) + random.randint(0, wc6) + random.randint(0, wc6)) / lastspart
            wsyoumou = heri * wdmg * (kisyou / max(1, wc3)) * (wc2 / max(1, nebari))
            
            if whp_flg <= 0:
                if random.randint(0, nebari) < random.randint(0, wc2):
                    wdmg = wdmg * 1.2
                    wsyoumou = wsyoumou * 0.5
                else:
                    wdmg = wdmg / 3
                    if step % 4 == 0:
                        step_comment += f'<span class="red-light">王者{wcname}がバテてきたクポ！</span> '
            elif (random.randint(0, seriai) < random.randint(0, wc4)) or (whp_flg / max(1, wc1) >= 0.4):
                wsyoumou = wsyoumou * 2
                wdmg = wdmg * 2.2
                if step % 4 == 0:
                    step_comment += f'<span class="yellow">王者{wcname}のラストスパート！</span> '
                    
            wdmg = int(wdmg)
            
            knokori -= kdmg
            wnokori -= wdmg
            khp_flg -= ksyoumou
            whp_flg -= wsyoumou
            
            lead = wnokori - knokori
            if lead > 200:
                step_comment += f"{cname}が大きくリードしているクポ！"
            elif lead < -200:
                step_comment += f"王者{wcname}がぐんぐんと突き放すクポ！"
            else:
                if abs(lead) < 15:
                    step_comment += "二頭が完全に並んだデッドヒートクポ！"
                elif lead > 0:
                    step_comment += f"{cname}がわずかにリードクポ！"
                else:
                    step_comment += f"王者{wcname}がわずかに先頭クポ！"

        # ターン記録
        turns_data.append({
            "step": step,
            "pos0": max(0, knokori),
            "pos1": max(0, wnokori),
            "comment": step_comment
        })
        
        # ゴール判定
        if knokori < 0 and wnokori < 0:
            syasin = True
            break
        elif knokori < 0:
            win = True
            break
        elif wnokori < 0:
            win = False
            break

    # 写真判定
    if syasin:
        if random.randint(0, c0) > random.randint(0, wc0):
            win = True
        else:
            win = False

    # === 結果・報酬処理 ===
    agari = ""
    senzai = ""
    genkai = ""
    rousui = ""
    comment = ""
    
    # チョコボステータスの限界・現在値を取得
    choco_c0 = choco.get("c0", 10)
    choco_c1 = choco.get("c1", 10)
    choco_c2 = choco.get("c2", 10)
    choco_c3 = choco.get("c3", 10)
    choco_c4 = choco.get("c4", 10)
    choco_c5 = choco.get("c5", 10)
    choco_c6 = choco.get("c6", 10)
    
    choco_max = choco.get("max", 10)
    choco_maxmax = choco.get("maxmax", 70)
    
    if win:
        crun += 1
        cwin += 1
        
        # 新王者のデータを生成して保存
        new_winner = {
            "id": user_id,
            "pass": chara["pass"],
            "breader": chara["name"],
            "site": chara.get("site", ""),
            "url": chara.get("url", ""),
            "name": cname,
            "no": choco.get("no", 0),
            "type": choco.get("type", 0),
            "run": crun,
            "win": cwin,
            "max": choco_max + 80, # 限界値を+80した値
            "c0": choco_c0, "c1": choco_c1, "c2": choco_c2, "c3": choco_c3, "c4": choco_c4, "c5": choco_c5, "c6": choco_c6,
            "ren": 1,
            "lname": wcname,
            "lsite": winner.get("site", ""),
            "lurl": winner.get("url", ""),
            "lbreader": wcbreader,
            "father": choco.get("father", "不明"),
            "mother": choco.get("mother", "不明")
        }
        
        # パラメータ上昇
        choco_max += 80
        c0_up = random.randint(1, 6)
        c1_up = random.randint(1, 6)
        c2_up = random.randint(1, 6)
        c3_up = random.randint(1, 6)
        c4_up = random.randint(1, 6)
        c5_up = random.randint(1, 6)
        c6_up = random.randint(1, 6)
        
        choco_c0 += c0_up
        choco_c1 += c1_up
        choco_c2 += c2_up
        choco_c3 += c3_up
        choco_c4 += c4_up
        choco_c5 += c5_up
        choco_c6 += c6_up
        
        # 奪取賞金：王者の最大値 * 王者連勝数 * 10,000 G
        gold = max(1, wcmax) * max(1, wcren) * 10000
        
        comment = f"<strong>🏆 見事に勝利し、新王者になりましたクポ！</strong><br>{cname}は見事王座を勝ち取りました！"
        agari = f"新王者ボーナス：能力値が大きく上昇しました！<br>（瞬発力+{c0_up}, 持久力+{c1_up}, 粘り強さ+{c2_up}, 落ち着き+{c3_up}, 闘争心+{c4_up}, 知力+{c5_up}, 切れ味+{c6_up}）"
        
        # 全体メッセージに流す
        common.get_lock("all_message")
        try:
            all_msgs = common.all_message_load()
            new_msg = {
                "id": "system",
                "name": "モーグリ実況",
                "time": common.get_time_str(),
                "message": f"👑 【新王者誕生】{chara['name']}の愛馬 {cname} が、王者 {wcname} を倒し、サブウッドチョコボの新王者になりましたクポ！連勝記録がスタートするクポ！"
            }
            all_msgs.insert(0, new_msg)
            if len(all_msgs) > config.Config['max_all_messages']:
                all_msgs = all_msgs[:config.Config['max_all_messages']]
            common.all_message_regist(all_msgs)
        finally:
            common.release_lock("all_message")
            
    else:
        # 防衛された場合
        wcren += 1
        
        # 王者データを防衛分更新して上書き
        winner["ren"] = wcren
        winner["lname"] = cname
        winner["lsite"] = chara.get("site", "")
        winner["lurl"] = chara.get("url", "")
        winner["lbreader"] = chara["name"]
        new_winner = winner
        
        crun += 1
        choco_max += 20
        choco_c0 += 1
        choco_c1 += 1
        choco_c2 += 1
        choco_c3 += 1
        choco_c4 += 1
        choco_c5 += 1
        choco_c6 += 1
        
        # 参加賞：王者の最大値 * 王者連勝数 / 1,000 G
        gold = int(max(1, wcmax) * max(1, wcren) / 1000)
        if gold < 10:
            gold = 10
            
        comment = f"<strong>👑 王者{wcname}が防衛しました。</strong><br>あと一歩及びませんでしたクポ……防衛されて悔しいクポ！"
        agari = "参加賞：能力値が全体的に +1 上昇しましたクポ。"

    # 寿命の減少 (200消費)
    clife -= 200
    
    # 老衰チェック
    if ctrain + crun > 1000:
        choco_maxmax = int(choco_maxmax * 0.99)
        rousui = f"あぁ、もう{cname}の体は限界のようですクポ。<br>よくこれまで育ててくれたと思いますクポ。<br>そろそろお見合い（引退）の時期ではないでしょうかクポ。"

    # 能力上限クランプ
    cmax0 = choco.get("max0", 10)
    cmax1 = choco.get("max1", 10)
    cmax2 = choco.get("max2", 10)
    cmax3 = choco.get("max3", 10)
    cmax4 = choco.get("max4", 10)
    cmax5 = choco.get("max5", 10)
    cmax6 = choco.get("max6", 10)
    
    cmax0_v = max(cmax0, 1)
    cmax1_v = max(cmax1, 1)
    cmax2_v = max(cmax2, 1)
    cmax3_v = max(cmax3, 1)
    cmax4_v = max(cmax4, 1)
    cmax5_v = max(cmax5, 1)
    cmax6_v = max(cmax6, 1)
    
    if choco_c0 > cmax0_v:
        genkai += "瞬発力の限界に達しましたクポ。<br>"
        choco_c0 = cmax0_v
    if choco_c1 > cmax1_v:
        genkai += "持久力の限界に達しましたクポ。<br>"
        choco_c1 = cmax1_v
    if choco_c2 > cmax2_v:
        genkai += "粘り強さの限界に達しましたクポ。<br>"
        choco_c2 = cmax2_v
    if choco_c3 > cmax3_v:
        genkai += "落ち着きの限界に達しましたクポ。<br>"
        choco_c3 = cmax3_v
    if choco_c4 > cmax4_v:
        genkai += "闘争心の限界に達しましたクポ。<br>"
        choco_c4 = cmax4_v
    if choco_c5 > cmax5_v:
        genkai += "知力の限界に達しましたクポ。<br>"
        choco_c5 = cmax5_v
    if choco_c6 > cmax6_v:
        genkai += "切れ味の限界に達しましたクポ。<br>"
        choco_c6 = cmax6_v

    # 総合限界比率クランプ
    c_sum = choco_c0 + choco_c1 + choco_c2 + choco_c3 + choco_c4 + choco_c5 + choco_c6
    if choco_max > choco_maxmax:
        choco_max = choco_maxmax
        if c_sum > choco_max:
            senzai = f"{cname}の能力は総合的な限界に達したクポ。<br>"
            wariai = choco_max / c_sum
            choco_c0 = int(choco_c0 * wariai) + 1
            choco_c1 = int(choco_c1 * wariai) + 1
            choco_c2 = int(choco_c2 * wariai) + 1
            choco_c3 = int(choco_c3 * wariai) + 1
            choco_c4 = int(choco_c4 * wariai) + 1
            choco_c5 = int(choco_c5 * wariai) + 1
            choco_c6 = int(choco_c6 * wariai) + 1
    elif c_sum > choco_max:
        wariai = choco_max / c_sum
        choco_c0 = int(choco_c0 * wariai) + 1
        choco_c1 = int(choco_c1 * wariai) + 1
        choco_c2 = int(choco_c2 * wariai) + 1
        choco_c3 = int(choco_c3 * wariai) + 1
        choco_c4 = int(choco_c4 * wariai) + 1
        choco_c5 = int(choco_c5 * wariai) + 1
        choco_c6 = int(choco_c6 * wariai) + 1
        senzai = f"トレーニング限界に達しましたクポ。一般レースや王者戦で潜在を引き出すクポ！<br>"

    # プレイヤーの所持金加算
    chara["gold"] += gold
    if chara["gold"] > config.Config['max_gold']:
        chara["gold"] = config.Config['max_gold']
        
    # チョコボ自身のゴールド価値加算
    choco["gold"] = choco.get("gold", 0) + int(gold / 100)
    
    # チョコボデータ更新
    choco["c0"] = choco_c0; choco["c1"] = choco_c1; choco["c2"] = choco_c2
    choco["c3"] = choco_c3; choco["c4"] = choco_c4; choco["c5"] = choco_c5; choco["c6"] = choco_c6
    choco["run"] = crun
    choco["win"] = cwin
    choco["life"] = clife
    choco["max"] = choco_max
    choco["maxmax"] = choco_maxmax

    # データの保存
    # プレイヤー
    common.get_lock(user_id)
    try:
        common.chara_regist(user_id, chara)
    finally:
        common.release_lock(user_id)
        
    # チョコボ
    common.get_lock(f"choco_{user_id}")
    try:
        common.choco_regist(user_id, choco)
    finally:
        common.release_lock(f"choco_{user_id}")

    # 王者データの保存
    common.get_lock("farm_winner")
    try:
        common.farm_winner_regist(new_winner)
    finally:
        common.release_lock("farm_winner")

    # 完了画面用 context
    context = {
        "chara": chara,
        "chara_log": chara_log,
        "choco": choco,
        "winner": winner,
        "turns_json": json.dumps(turns_data),
        "comment": comment + f"<br>{chara['name']}は <b>{gold}</b> ギルを獲得しました！",
        "agari": agari,
        "senzai": senzai,
        "genkai": genkai,
        "rousui": rousui,
        "win_js": "true" if win else "false"
    }

    common.render_template("farmrace.html", context)

if __name__ == "__main__":
    main()
