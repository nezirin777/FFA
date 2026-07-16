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
FFA Python/CGI チョコボレース (crace.py)
一般レース、G1/G2重賞レース、殿堂レースのシミュレーションと結果処理を行います。
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

# 重賞レースのモード (O(1) メンバーシップテスト用定数、線形探索を回避して高速化)
_HEAVY_RACES: frozenset[str] = frozenset({"race7", "race8"})

# Windows等で標準出力をUTF-8にするための設定
def load_rivals(ribal_path, count=4):
    """ライバルファイルを読み込み、ランダムに count 頭取得します。"""
    # 殿堂データ(json)か、通常のiniファイル(CSV)かを判定してロードする
    rivals = []
    if not os.path.exists(ribal_path):
        return rivals
        
    if ribal_path.endswith('.json'):
        with open(ribal_path, "r", encoding="utf-8") as f:
            try:
                rivals = json.load(f)
            except:
                pass
    else:
        # CSV (.ini) ロード
        try:
            with open(ribal_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except:
            with open(ribal_path, "r", encoding="shift-jis", errors='ignore') as f:
                lines = f.readlines()
                
        for line in lines:
            if not line.strip():
                continue
            parts = line.strip().split("<>")
            if parts and parts[-1] == "":
                parts = parts[:-1]
            if len(parts) >= 12:
                rivals.append({
                    "breader": parts[0],
                    "name": parts[1],
                    "no": int(parts[2]),
                    "type": int(parts[3]),
                    "max": int(parts[4]),
                    "c0": int(parts[5]),
                    "c1": int(parts[6]),
                    "c2": int(parts[7]),
                    "c3": int(parts[8]),
                    "c4": int(parts[9]),
                    "c5": int(parts[10]),
                    "c6": int(parts[11])
                })
                
    # ランダムに抽出
    selected = []
    if rivals:
        for _ in range(count):
            selected.append(random.choice(rivals))
    else:
        # 予備のダミーライバル
        for idx in range(count):
            selected.append({
                "breader": "管理者",
                "name": f"コボタロウ-{idx+1}",
                "no": 0,
                "type": 0,
                "max": 10,
                "c0": 10, "c1": 10, "c2": 10, "c3": 10, "c4": 10, "c5": 10, "c6": 10
            })
            
    return selected

def main():
    # CGIパラメータ解析
    in_params = common.decode_params()
    user_id = in_params.get("id", "")
    # IDOR対策: 状態変更は本人のみ許可(ロック取得前にチェック)
    common.require_owner(user_id)
    chara_log = in_params.get("mydata", "")
    mode = in_params.get("mode", "")
    race_id = common.to_int(in_params.get("race", "0"), 0)

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
    csex = choco.get("sex", 0)
    
    # 戻るフォーム (error.html 側で最新のCSRFトークン付きで描画される)
    back_ctx = {
        "back_action": config.Config['chocofarm_script'],
        "back_params": {"id": user_id, "mydata": chara_log},
        "back_label": "牧場に戻る",
    }

    # 出走レースの検証 (無選択のまま新馬戦が暗黙実行されるのを防ぐ)
    valid_modes = {"race0", "race1", "race2", "race3", "race4", "race5",
                   "race6", "race7", "race8", "race_dendo"}
    if mode not in valid_modes:
        common.show_error("出走するレースが選択されていません。牧場のレース選択から出走してください。", back_ctx)

    # バリデーション
    if not cname or cname == "名無しのチョコボ":
        common.show_error("チョコボに名前を付けてからレースに出走させてください。", back_ctx)
    if clife < 400:
        common.show_error("チョコボの体力が足りません。宿屋で休ませてから出走させてください。", back_ctx)

    # クラス条件判定
    win_min = 0
    win_limit = 100000
    ribal_file = "ribal0.json"
    racename = "新馬戦"
    
    # レースモード判定
    if mode == "race0":
        win_min, win_limit, ribal_file, racename = 0, 1, "ribal0.json", "新馬戦"
    elif mode == "race1":
        win_min, win_limit, ribal_file, racename = 1, 5, "ribal1.json", "５００万以下"
    elif mode == "race2":
        win_min, win_limit, ribal_file, racename = 5, 15, "ribal2.json", "９００万以下"
    elif mode == "race3":
        win_min, win_limit, ribal_file, racename = 15, 30, "ribal3.json", "１６００万以下"
    elif mode == "race4":
        win_min, win_limit, ribal_file, racename = 30, 80, "ribal4.json", "オープン特別"
    elif mode == "race5":
        win_min, win_limit, ribal_file, racename = 50, 100, "ribal5.json", "グレードⅢ(G3)"
    elif mode == "race6":
        win_min, win_limit, ribal_file, racename = 75, 130, "ribal6.json", "グレードⅡ(G2)"
    elif mode == "race7":
        # G1 レース
        win_min = 30
        ribal_file = "ribal7.json"
        g1_names = {
            1: "チョコボダービー", 2: "チョコボスタリオン", 3: "チョコボカップ",
            4: "ジェイドカップ", 5: "BBA賞", 6: "チョコボ春賞", 7: "チョコボ秋賞",
            8: "チョコボキング", 9: "チョコボステークス", 10: "キングスカップ", 11: "クイーンカップ"
        }
        racename = g1_names.get(race_id, "G1重賞")
        # 周期チェック
        if (crun + ctrain) % 40 != 0:
            common.show_error("現在はそのG1レースの開催日ではありません。", back_ctx)
    elif mode == "race8":
        # G2（海外）レース
        win_min = 30
        ribal_file = "ribal8.json"
        g2_names = {
            12: "シルバーカップ", 13: "新潟アドバンス", 14: "チコスダービー",
            15: "チョコボードカップ", 16: "チョコボエプソム", 17: "チョコボ王",
            18: "ブリーダーズカップ", 19: "ゴールドカップ", 20: "プラチナカップ",
            21: "チョコボオークス", 22: "チョコボキングス"
        }
        racename = g2_names.get(race_id, "海外重賞")
        # 周期チェック
        if (crun + ctrain) % 60 != 0:
            common.show_error("現在はその海外レースの開催日ではありません。", back_ctx)
    elif mode == "race_dendo":
        # 殿堂レース
        win_min = 30
        ribal_file = "denchoco.json" # 殿堂データ
        racename = "殿堂レジェンドレース"
        
    if cwin < win_min or cwin >= win_limit:
        common.show_error(f"勝利数がクラス制限に合致しません。現在の勝利数: {cwin}", back_ctx)

    # 時間制限チェック
    now = int(time.time())
    last_time = chara.get("last_time", 0)
    ltime = now - last_time
    if ltime < config.Config['battle_cooldown']:
        wait_sec = config.Config['battle_cooldown'] - ltime
        common.show_error(f"まだレースに出走できません。あと {wait_sec} 秒お待ちください。", back_ctx)

    # アクション時間更新
    chara["last_time"] = now

    # === ライバルたちのロード ===
    # ribal0〜8.json はマスタデータ (data/)、denchoco.json は殿堂データ (save_data/)
    if ribal_file.startswith("ribal"):
        ribal_path = os.path.join(common.BASE_DIR, "data", ribal_file)
    else:
        ribal_path = os.path.join(config.Config['save_dir'], ribal_file)
        
    rivals = load_rivals(ribal_path, count=4)

    # 出走メンバーのパラメータ配列構築
    # インデックス 0: プレイヤー自身, 1..4: ライバル
    names = [cname]
    nos = [choco.get("no", 0)]
    wazas = [choco.get("type", 0)]
    breaders = [chara["name"]]
    
    # 各能力値
    c0 = [choco.get("c0", 10)]
    c1 = [choco.get("c1", 10)]
    c2 = [choco.get("c2", 10)]
    c3 = [choco.get("c3", 10)]
    c4 = [choco.get("c4", 10)]
    c5 = [choco.get("c5", 10)]
    c6 = [choco.get("c6", 10)]
    
    for r in rivals:
        names.append(r["name"])
        nos.append(r["no"])
        wazas.append(r["type"])
        breaders.append(r["breader"])
        c0.append(r["c0"])
        c1.append(r["c1"])
        c2.append(r["c2"])
        c3.append(r["c3"])
        c4.append(r["c4"])
        c5.append(r["c5"])
        c6.append(r["c6"])

    # 基礎変数計算
    c2_sum = sum(c2)
    c3_sum = sum(c3)
    c4_sum = sum(c4)
    c5_sum = sum(c5)
    c0_sum = sum(c0)
    c6_sum = sum(c6)
    
    heri = c2_sum / 10000
    nebari = int(c2_sum / 5)
    kisyou = int(c3_sum / 5)
    seriai = int(c4_sum / 5)
    tiryoku = int(c5_sum / 5)
    
    tyousei = 5000 / c0_sum
    kinryoku = int(c0_sum / 5)
    
    # ラストスパート減衰係数
    lastspart = int(((c0_sum / 3) + c6_sum) / 150)
    if lastspart <= 0:
        lastspart = 1

    # === レース進行シミュレーション ===
    total_dist = 2400
    positions = [total_dist] * 5
    hp_flg = [val for val in c1] # 現在スタミナ
    
    turns_data = []
    nuki = 0
    near = 0
    hitoritabi = False
    
    types_str = ['普通', '早熟', '晩成', '持続', '超晩成', '超早熟']

    # レースのループ
    step = 0
    winner_idx = -1
    
    while step < 100: # 最大100ステップで必ずゴールする設計にする
        step += 1
        step_comment = ""
        
        # 1. 毎ターンの移動量(dmg)を算出
        dmg = [0] * 5
        syoumou = [0] * 5
        
        if step == 1:
            # === スタートダッシュ ===
            for n in range(5):
                # 出遅れ判定
                if random.randint(0, kisyou) <= random.randint(0, int(c3[n] * 2 / 3)):
                    dmg[n] = int(random.randint(0, int(c0[n] / (tyousei * 4))) + c0[n] / (tyousei * 4))
                    if n == 0:
                        step_comment += f'<span class="red">{names[n]}はスタートで出遅れましたクポ！</span> '
                    syoumou[n] = heri * dmg[n] * 3 * (kisyou / max(1, c3[n])) * (c2[n] / max(1, nebari))
                # 好スタート判定
                elif random.randint(0, tiryoku) <= random.randint(0, int(c5[n] * 2 / 3)):
                    dmg[n] = int(random.randint(0, int(c0[n] * 1.5 / tyousei)))
                    if n == 0:
                        step_comment += f'<span class="green">{names[n]}は素晴らしいスタートを切りましたクポ！</span> '
                    syoumou[n] = heri * (dmg[n] / 2) * (kisyou / max(1, c3[n])) * (c2[n] / max(1, nebari))
                # 普通スタート
                else:
                    dmg[n] = int(random.randint(0, int(c0[n] / (tyousei * 2))) + c0[n] / (tyousei * 2))
                    syoumou[n] = heri * dmg[n] * (kisyou / max(1, c3[n])) * (c2[n] / max(1, nebari))
                    
                syoumou[n] = syoumou[n] / 2
                positions[n] = total_dist - dmg[n]
                hp_flg[n] -= syoumou[n]
                
            # スタート後の順位
            sorted_runners = sorted(range(5), key=lambda x: positions[x])
            step_comment += f"<br>スタート！先頭は {names[sorted_runners[0]]} クポ！"
            
        else:
            # === 中盤・終盤の移動 ===
            for n in range(5):
                # 基礎移動力
                base_dmg = (random.randint(0, c0[n]) + random.randint(0, c6[n]) + random.randint(0, c6[n]) + random.randint(0, c6[n])) / lastspart
                syoumou_base = heri * base_dmg * (kisyou / max(1, c3[n])) * (c2[n] / max(1, nebari))
                
                # スタミナ切れ（バテ）の判定
                if hp_flg[n] <= 0:
                    # 粘り強さでカバーできるか
                    if random.randint(0, nebari) < random.randint(0, c2[n]):
                        base_dmg = base_dmg * 1.2
                        syoumou_base = syoumou_base * 0.5
                    else:
                        base_dmg = base_dmg / 3
                        if n == 0 and step % 4 == 0:
                            step_comment += f'<span class="red">{names[n]}は完全にバテていますクポ...</span> '
                # ラストスパート（終盤かつ闘争心/スタミナで加速）
                elif (random.randint(0, seriai) < random.randint(0, c4[n])) or (hp_flg[n] / max(1, c1[n]) >= 0.4):
                    syoumou_base = syoumou_base * 2
                    base_dmg = base_dmg * 2.2
                    if n == 0 and step % 4 == 0:
                        step_comment += f'<span class="yellow">{names[n]}のラストスパートクポ！</span> '
                        
                dmg[n] = int(base_dmg)
                positions[n] = max(0, positions[n] - dmg[n])
                hp_flg[n] -= syoumou_base

            # 順位ソート
            sorted_runners = sorted(range(5), key=lambda x: positions[x])
            
            # 実況メッセージの作成
            lead_dist = positions[sorted_runners[1]] - positions[sorted_runners[0]]
            if lead_dist > 300:
                step_comment += f"{names[sorted_runners[0]]}が完全に独走状態クポ！引き離しにかかっているクポ！"
            elif lead_dist > 100:
                step_comment += f"{names[sorted_runners[0]]}が一頭抜け出しているクポ！"
            else:
                if positions[sorted_runners[1]] - positions[sorted_runners[0]] < 15:
                    step_comment += f"{names[sorted_runners[0]]}と{names[sorted_runners[1]]}が激しく並んで競り合っているクポ！"
                else:
                    step_comment += f"先頭は{names[sorted_runners[0]]}！すぐ後ろに{names[sorted_runners[1]]}がピタリと追うクポ！"
                    
        # 現在のステップログを格納
        turns_data.append({
            "step": step,
            "positions": [pos for pos in positions],
            "comment": step_comment
        })
        
        # ゴール判定
        if any(pos <= 0 for pos in positions):
            # 誰かがゴールイン
            # 最も残り距離が少ない（またはマイナスが大きい）ものを勝者とする
            winner_idx = sorted_runners[0]
            break

    # === 勝敗判定と結果処理 ===
    win = (winner_idx == 0)
    agari = ""
    senzai = ""
    genkai = ""
    rousui = ""
    comment = ""
    
    # 現在のチョコボステータスの限界・現在値を取得
    choco_c0 = choco.get("c0", 10)
    choco_c1 = choco.get("c1", 10)
    choco_c2 = choco.get("c2", 10)
    choco_c3 = choco.get("c3", 10)
    choco_c4 = choco.get("c4", 10)
    choco_c5 = choco.get("c5", 10)
    choco_c6 = choco.get("c6", 10)
    
    choco_max = choco.get("max", 10)
    choco_maxmax = choco.get("maxmax", 70)
    
    # 勝利時の処理
    if win:
        crun += 1
        cwin += 1
        choco_max += 80
        
        # 全ステータスが 1〜6 上昇
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
        
        # 賞金計算
        # X = choco_max / 1000 + 1。Xの1.3乗 * 1000 G
        gold_factor = (int(choco_max / 1000) + 1) ** 1.3
        gold = int(gold_factor * 1000)
        
        comment = f"<strong>🏆 見事に1着でゴールインクポ！</strong><br>{names[0]}は見事な走りでしたクポ！さすがクポ！"
        agari = f"勝利ボーナス：能力値が全体的に上昇しましたクポ！<br>（瞬発力+{c0_up}, 持久力+{c1_up}, 粘り強さ+{c2_up}, 落ち着き+{c3_up}, 闘争心+{c4_up}, 知力+{c5_up}, 切れ味+{c6_up}）"
        
        # 重賞レース(G1/G2)勝利の記録 (O(1) frozenset ルックアップで判定)
        if mode in _HEAVY_RACES and race_id > 0:
            # 個人トロフィー記録の更新
            g1_data = common.choco_g1_load(user_id)
            if not g1_data:
                g1_data = {
                    "id": user_id,
                    "pass": chara["pass"],
                    "name": cname,
                    "father": choco.get("father", "不明"),
                    "mother": choco.get("mother", "不明"),
                    "breader": chara["name"]
                }
            g1_data[f"r{race_id}"] = 1
            
            common.get_lock(f"g1_{user_id}")
            try:
                common.choco_g1_regist(user_id, g1_data)
            finally:
                common.release_lock(f"g1_{user_id}")
                
            # 全体重賞勝利履歴 (rireki.json) の更新
            rireki_path = os.path.join(config.Config['save_dir'], "rireki.json")
            common.get_lock("rireki")
            try:
                rireki_data = []
                if os.path.exists(rireki_path):
                    try:
                        with open(rireki_path, "r", encoding="utf-8") as f:
                            rireki_data = json.load(f)
                    except:
                        pass
                
                # 該当チョコボが履歴に既に存在するかチェック (チョコボ名で判定)
                found = False
                for r in rireki_data:
                    if r.get("name") == cname:
                        r[f"r{race_id}"] = 1
                        found = True
                        break
                
                if not found:
                    # 新規追加
                    new_rireki = {
                        "id": user_id,
                        "name": cname,
                        "father": choco.get("father", "不明"),
                        "mother": choco.get("mother", "不明"),
                        "breader": chara["name"]
                    }
                    # r1〜r22を初期化
                    for idx in range(1, 23):
                        new_rireki[f"r{idx}"] = 0
                    new_rireki[f"r{race_id}"] = 1
                    # 先頭に追加 (最新の勝利順)
                    rireki_data.insert(0, new_rireki)
                else:
                    # 既存更新されたものを先頭に移動する (最新勝利順を維持するため)
                    # ただし単純に要素を取り出して先頭にする
                    target_idx = -1
                    for idx, r in enumerate(rireki_data):
                        if r.get("name") == cname:
                            target_idx = idx
                            break
                    if target_idx != -1:
                        target_item = rireki_data.pop(target_idx)
                        rireki_data.insert(0, target_item)
                
                with open(rireki_path, "w", encoding="utf-8") as f:
                    json.dump(rireki_data, f, ensure_ascii=False, indent=2)
            finally:
                common.release_lock("rireki")
                
            # 全体メッセージに流す
            common.get_lock("all_message_post")
            try:
                all_msgs = common.all_message_load()
                new_msg = {
                    "id": "system",
                    "name": "モーグリ実況",
                    "time": common.get_time_str(),
                    "message": f"🎉 【重賞制覇】{chara['name']}の愛馬 {cname} が、伝統ある重賞「{racename}」を制覇しましたクポ！大歓声クポ！"
                }
                all_msgs.insert(0, new_msg)
                if len(all_msgs) > config.Config['max_all_messages']:
                    all_msgs = all_msgs[:config.Config['max_all_messages']]
                common.all_message_regist(all_msgs)
            finally:
                common.release_lock("all_message_post")
                
            comment += f'<br><span class="gold u-text-large">🎉 【重賞制覇】「{racename}」のタイトルを獲得しました！</span>'
            
    # 敗北時の処理
    else:
        crun += 1
        choco_max += 20
        
        # 全ステータスが 1 上昇
        choco_c0 += 1
        choco_c1 += 1
        choco_c2 += 1
        choco_c3 += 1
        choco_c4 += 1
        choco_c5 += 1
        choco_c6 += 1
        
        # 参加賞
        gold = int(choco_max / 1000)
        if gold < 10:
            gold = 10
            
        winner_name = names[winner_idx]
        comment = f"<strong>🏁 {winner_name}が1着でゴールイン。</strong><br>{names[0]}は敗れてしまいましたクポ……次こそは頑張るクポ！"
        agari = "参加賞：能力値が全体的に +1 上昇しましたクポ。"

    # 寿命の減少（200消費）
    clife -= 200
    
    # 老衰チェック
    if ctrain + crun > 1000:
        choco_maxmax = int(choco_maxmax * 0.99)
        rousui = f"あぁ、もう{cname}の体は限界のようですクポ。<br>よくこれまで育ててくれたと思いますクポ。<br>そろそろお見合い（引退）の時期ではないでしょうかクポ。"

    # 個別パラメータ上限クランプ
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

    # 総合限界判定と比率クランプ
    c_sum = choco_c0 + choco_c1 + choco_c2 + choco_c3 + choco_c4 + choco_c5 + choco_c6
    if choco_max > choco_maxmax:
        choco_max = choco_maxmax
        if c_sum > choco_max:
            senzai = f"{cname}の能力は限界に達したクポ。<br>"
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
        senzai = f"トレーニングのみでの限界に達しましたクポ。<br>レースに出て潜在能力を開放するクポ！<br>"

    # プレイヤーの所持金加算
    chara["gold"] += gold
    if chara["gold"] > config.Config['max_gold']:
        chara["gold"] = config.Config['max_gold']
        
    # チョコボ自身のゴールド価値加算 (gold/100)
    choco["gold"] = choco.get("gold", 0) + int(gold / 100)

    # === データの保存 ===
    # チョコボデータ更新
    choco["c0"] = choco_c0; choco["c1"] = choco_c1; choco["c2"] = choco_c2
    choco["c3"] = choco_c3; choco["c4"] = choco_c4; choco["c5"] = choco_c5; choco["c6"] = choco_c6
    choco["run"] = crun
    choco["win"] = cwin
    choco["life"] = clife
    choco["max"] = choco_max
    choco["maxmax"] = choco_maxmax
    
    # 保存
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

    # フロントエンド用出走者データ
    runners_data = []
    for idx in range(5):
        runners_data.append({
            "name": names[idx],
            "no": nos[idx]
        })

    # テンプレートに渡す
    context = {
        "chara": chara,
        "chara_log": chara_log,
        "choco": choco,
        "racename": racename,
        "runners": runners_data,
        "runners_json": json.dumps(runners_data),
        "turns": turns_data,
        "turns_json": json.dumps(turns_data),
        "comment": comment,
        "agari": agari,
        "senzai": senzai,
        "genkai": genkai,
        "rousui": rousui,
        "win_js": "true" if win else "false"
    }

    common.render_template("crace.html", context)

if __name__ == "__main__":
    main()
