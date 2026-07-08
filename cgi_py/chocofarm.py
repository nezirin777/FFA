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
FFA Python/CGI チョコボ農場 (chocofarm.py)
自身のチョコボのステータス確認、トレーニング、レースへの出走を管理します。
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
        common.show_error("キャラクターデータが見つかりません。ログインし直してください。")
        
    # アイテムデータのロード
    item = common.item_load(user_id)
    
    # チョコボデータのロード
    choco_raw = common.choco_load(user_id)
    has_choco = choco_raw is not None

    # 重賞履歴のロード
    g1_raw = common.choco_g1_load(user_id)
    
    # 歴代王者データのロード
    winner_raw = common.farm_winner_load()
    if not winner_raw:
        # 初期ダミー王者
        winner_raw = {
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
            "max": 10,
            "c0": 10, "c1": 10, "c2": 10, "c3": 10, "c4": 10, "c5": 10, "c6": 10,
            "ren": 0,
            "lname": "なし",
            "lsite": "",
            "lurl": "",
            "lbreader": "なし"
        }

    # アルファベット能力ランク画像
    rank_imgs = [
        "e.gif", "d.gif", "c.gif", "c.gif", "b.gif", "b.gif", "a.gif", "a.gif", "s.gif", "s.gif", "ss.gif", "ss.gif", "ss.gif", "ss.gif", "ss.gif"
    ]
    # タイプ一覧
    types = ['普通', '早熟', '晩成', '持続', '超晩成', '超早熟']

    # === トロフィー（重賞勝利履歴）の抽出 ===
    G1_RACES = {
        "r1": "チョコボダービー", "r2": "チョコボスタリオン", "r3": "チョコボカップ",
        "r4": "ジェイドカップ", "r5": "BBA賞", "r6": "チョコボ春賞", "r7": "チョコボ秋賞",
        "r8": "チョコボキング", "r9": "チョコボステークス", "r10": "キングスカップ", "r11": "クイーンカップ"
    }
    G2_RACES = {
        "r12": "シルバーカップ", "r13": "新潟アドバンス", "r14": "チコスダービー",
        "r15": "チョコボードカップ", "r16": "チョコボエプソム", "r17": "チョコボ王",
        "r18": "ブリーダーズカップ", "r19": "ゴールドカップ", "r20": "プラチナカップ",
        "r21": "チョコボオークス", "r22": "チョコボキングス"
    }
    
    trophies = []
    if g1_raw:
        for k, v in G1_RACES.items():
            if g1_raw.get(k, 0) > 0:
                trophies.append({"name": v, "is_g1": True})
        for k, v in G2_RACES.items():
            if g1_raw.get(k, 0) > 0:
                trophies.append({"name": v, "is_g1": False})

    # === 時間制限の判定 ===
    now = int(time.time())
    last_time = chara.get("last_time", 0)
    ltime = now - last_time
    
    train_wait = config.Config['monster_cooldown'] - ltime
    race_wait = config.Config['battle_cooldown'] - ltime
    
    time_limits = {
        "train_ok": train_wait <= 0,
        "train_wait": max(0, train_wait),
        "race_ok": race_wait <= 0,
        "race_wait": max(0, race_wait)
    }

    # === 王者かどうかの判定 ===
    is_king = (winner_raw.get("id") == user_id and winner_raw.get("name") == (choco_raw.get("name", "") if has_choco else ""))

    # === モーグリのアドバイスの取得 ===
    hint_path = os.path.join(common.BASE_DIR, "data", "hint.json")
    mog_advice = "頑張って育てるクポ！"
    if os.path.exists(hint_path):
        try:
            with open(hint_path, "r", encoding="utf-8") as f:
                hints = json.load(f)
            if hints:
                mog_advice = random.choice(hints)
        except:
            pass

    # === チョコボ情報と一般・重賞レースの算出 ===
    choco_info = None
    race_classes = []
    g1_race = None
    g1_nokori = 0
    g2_race = None
    g2_nokori = 0
    
    if has_choco:
        cwin = choco_raw.get("win", 0)
        crun = choco_raw.get("run", 0)
        ctrain = choco_raw.get("train", 0)
        csex = choco_raw.get("sex", 0)
        
        # クラス名
        if cwin == 0: cls = "新馬"
        elif cwin < 5: cls = "５００万"
        elif cwin < 15: cls = "９００万"
        elif cwin < 30: cls = "１６００万"
        elif cwin < 50: cls = "オープン"
        elif cwin < 75: cls = "グレードⅣ"
        elif cwin < 105: cls = "グレードⅢ"
        elif cwin < 140: cls = "グレードⅡ"
        else: cls = "グレードⅠ"
        
        # 調子
        clife = choco_raw.get("life", 1000)
        if clife >= 990:
            csta = "寿命近し"
        else:
            status_list = ['最悪', '不調', '普通', '好調', '絶好調']
            life_t = int(clife / 200)
            if life_t >= len(status_list): life_t = len(status_list) - 1
            csta = status_list[life_t]
            
        choco_info = {
            "no": choco_raw.get("no", 0),
            "name": choco_raw.get("name", "名無しのチョコボ"),
            "sex": csex,
            "run": crun,
            "win": cwin,
            "waza": types[choco_raw.get("type", 0)] if choco_raw.get("type", 0) < len(types) else "不明",
            "cls": cls,
            "train": ctrain,
            "max": choco_raw.get("max", 10),
            "life": clife,
            "csta": csta,
            "money": choco_raw.get("gold", 0) * 100,
            "father": choco_raw.get("father", "不明"),
            "mother": choco_raw.get("mother", "不明"),
            # 能力値の画像ランク用
            "c0_t": min(len(rank_imgs) - 1, int(choco_raw.get("c0", 10) / 100)),
            "c1_t": min(len(rank_imgs) - 1, int(choco_raw.get("c1", 10) / 100)),
            "c2_t": min(len(rank_imgs) - 1, int(choco_raw.get("c2", 10) / 100)),
            "c3_t": min(len(rank_imgs) - 1, int(choco_raw.get("c3", 10) / 100)),
            "c4_t": min(len(rank_imgs) - 1, int(choco_raw.get("c4", 10) / 100)),
            "c5_t": min(len(rank_imgs) - 1, int(choco_raw.get("c5", 10) / 100)),
            "c6_t": min(len(rank_imgs) - 1, int(choco_raw.get("c6", 10) / 100)),
        }
        
        # 一般出走クラスの決定
        if cwin >= 75 and cwin <= 130:
            race_classes.append({"value": "race6", "name": "グレードⅡ"})
        if cwin >= 50 and cwin <= 100:
            race_classes.append({"value": "race5", "name": "グレードⅢ"})
        if cwin >= 30 and cwin <= 80:
            race_classes.append({"value": "race4", "name": "オープン"})
        if cwin >= 15 and cwin < 30:
            race_classes.append({"value": "race3", "name": "１６００万"})
        if cwin >= 5 and cwin < 15:
            race_classes.append({"value": "race2", "name": "９００万"})
        if cwin >= 1 and cwin < 5:
            race_classes.append({"value": "race1", "name": "５００万"})
        if cwin == 0:
            race_classes.append({"value": "race0", "name": "新馬"})
            
        # G1開催情報の計算 (40ターン周期)
        turn_sum = crun + ctrain
        g1_idx = -1
        if turn_sum % 400 == 0: g1_idx = 1
        elif (turn_sum + 360) % 400 == 0: g1_idx = 2
        elif (turn_sum + 320) % 400 == 0: g1_idx = 3
        elif (turn_sum + 280) % 400 == 0: g1_idx = 4
        elif (turn_sum + 240) % 400 == 0: g1_idx = 5
        elif (turn_sum + 200) % 400 == 0: g1_idx = 6
        elif (turn_sum + 160) % 400 == 0: g1_idx = 7
        elif (turn_sum + 120) % 400 == 0: g1_idx = 8
        elif (turn_sum + 80) % 400 == 0: g1_idx = 9
        elif (turn_sum + 40) % 400 == 0:
            g1_idx = 10 if csex == 1 else 11
            
        if g1_idx != -1:
            g1_name = G1_RACES[f"r{g1_idx}"]
            g1_race = {"value": g1_idx, "name": g1_name}
        else:
            g1_nokori = 40 - turn_sum % 40
            
        # G2（海外）開催情報の計算 (60ターン周期、重賞3勝以上)
        g2_idx = -1
        if turn_sum % 600 == 0: g2_idx = 12
        elif (turn_sum + 540) % 600 == 0: g2_idx = 13
        elif (turn_sum + 480) % 600 == 0: g2_idx = 14
        elif (turn_sum + 420) % 600 == 0: g2_idx = 15
        elif (turn_sum + 360) % 600 == 0: g2_idx = 16
        elif (turn_sum + 300) % 600 == 0: g2_idx = 17
        elif (turn_sum + 240) % 600 == 0: g2_idx = 18
        elif (turn_sum + 180) % 600 == 0: g2_idx = 19
        elif (turn_sum + 120) % 600 == 0: g2_idx = 20
        elif (turn_sum + 60) % 600 == 0:
            g2_idx = 22 if csex == 1 else 21
            
        if g2_idx != -1:
            g2_name = G2_RACES[f"r{g2_idx}"]
            g2_race = {"value": g2_idx, "name": g2_name}
        else:
            g2_nokori = 60 - turn_sum % 60

    # テンプレート（chocofarm.html）が直接参照する変数群を context に追加
    choco_name = ""
    choco_class = ""
    choco_type = ""
    choco_love = 0
    choco_speed = 0
    choco_stamina = 0
    choco_win = 0
    choco_age = 0
    
    if has_choco and choco_info:
        choco_name = choco_info.get("name", "")
        choco_class = choco_info.get("cls", "")
        choco_type = choco_info.get("waza", "")
        choco_love = choco_raw.get("love", 0)
        choco_speed = choco_raw.get("c0", 0)
        choco_stamina = choco_raw.get("c1", 0)
        choco_win = choco_info.get("win", 0)
        choco_age = choco_raw.get("age", 0)

    winner_name = winner_raw.get("name", "なし")
    winner_win = winner_raw.get("ren", 0)
    
    wwin = winner_raw.get("win", 0)
    if wwin == 0: winner_class = "新馬"
    elif wwin < 5: winner_class = "５００万"
    elif wwin < 15: winner_class = "９００万"
    elif wwin < 30: winner_class = "１６００万"
    elif wwin < 50: winner_class = "オープン"
    elif wwin < 75: winner_class = "グレードⅣ"
    elif wwin < 105: winner_class = "グレードⅢ"
    elif wwin < 140: winner_class = "グレードⅡ"
    else: winner_class = "グレードⅠ"
    
    winner_kyori = winner_raw.get("max", 0)
    
    winner_img = ""
    w_img_idx = winner_raw.get("no", 0)
    if 0 <= w_img_idx < len(config.Config.get('choco_images', [])):
        winner_img = config.Config['choco_images'][w_img_idx]

    trophy_names = []
    if trophies:
        for t in trophies:
            if isinstance(t, dict):
                trophy_names.append(t.get("name", ""))
            else:
                trophy_names.append(str(t))

    # ゲスト表示更新
    update_and_get_guests = common.update_and_get_guests(user_id, chara["name"])

    context = {
        "chara": chara,
        "chara_log": chara_log,
        "item": item,
        "has_choco": has_choco,
        "choco": choco_info,
        "winner": winner_raw,
        "trophies": trophy_names,
        "trophies_count": len(trophy_names),
        "rank_imgs": rank_imgs,
        "time_limits": time_limits,
        "is_king": is_king,
        "race_classes": race_classes,
        "g1_race": g1_race,
        "g1_nokori": g1_nokori,
        "g2_race": g2_race,
        "g2_nokori": g2_nokori,
        "mog_advice": mog_advice,
        "update_and_get_guests": update_and_get_guests,
        
        "choco_name": choco_name,
        "choco_class": choco_class,
        "choco_type": choco_type,
        "choco_love": choco_love,
        "choco_speed": choco_speed,
        "choco_stamina": choco_stamina,
        "choco_win": choco_win,
        "choco_age": choco_age,
        
        "winner_name": winner_name,
        "winner_win": winner_win,
        "winner_class": winner_class,
        "winner_kyori": winner_kyori,
        "winner_img": winner_img
    }

    common.render_template("chocofarm.html", context)

if __name__ == "__main__":
    main()
