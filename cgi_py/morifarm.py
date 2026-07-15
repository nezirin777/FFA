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
FFA Python/CGI 森の農場 (morifarm.py)
野生チョコボの購入・配合・引退（野に放す）・命名・宿屋での寿命回復を処理します。
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
    mode = in_params.get("mode", "main")
    if mode == "choco":
        mode = "main"
    # ルーティングキー (login.py?mode=morifarm) や不明なmodeで入場した場合はメイン表示へ
    valid_modes = ("main", "choco_shop", "choco_buy", "choco_shopb",
                   "choco_buyb", "choco_sell", "choco_name", "yadoya")
    if mode not in valid_modes:
        mode = "main"
    
    # キャラクターデータのロード
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターデータが見つかりません。ログインし直してください。")
        
    # パスワードチェック (簡易)
    # 実際にはセッションやクッキーでの厳密な検証が望ましいが、既存踏襲
    chara_log = in_params.get("mydata", "")
    
    # チョコボデータのロード
    choco_raw = common.choco_load(user_id)
    has_choco = choco_raw is not None

    # お見合い用・野生用画像ランク
    rank_imgs = [
        "g.gif", "e.gif", "d.gif", "c.gif", "b.gif", "a.gif", "s.gif", "ss.gif"
    ]
    # タイプ一覧
    types = ['普通', '早熟', '晩成', '持続', '超晩成', '超早熟']

    context = {
        "chara": chara,
        "chara_log": chara_log,
        "mode": mode,
        "has_choco": has_choco,
        "rank_imgs": rank_imgs,
        "types": types,
    }

    if mode == "main":
        # === メイン画面表示 ===
        if has_choco:
            # チョコボステータスの補正と表示値の決定
            cwin = choco_raw.get("win", 0)
            
            # クラス名の判定
            if cwin == 0:
                cls = "新馬"
            elif cwin < 5:
                cls = "５００万"
            elif cwin < 15:
                cls = "９００万"
            elif cwin < 30:
                cls = "１６００万"
            elif cwin < 50:
                cls = "オープン"
            elif cwin < 75:
                cls = "グレードⅣ"
            elif cwin < 105:
                cls = "グレードⅢ"
            elif cwin < 140:
                cls = "グレードⅡ"
            else:
                cls = "グレードⅠ"
                
            # タイプ/技の取得
            ctype = choco_raw.get("type", 0)
            waza = types[ctype] if ctype < len(types) else "不明"
            
            # 調子の判定
            clife = choco_raw.get("life", 1000)
            if clife >= 990:
                csta = "寿命近し"
            else:
                status_list = ['最悪', '不調', '普通', '好調', '絶好調']
                life_t = int(clife / 200)
                if life_t >= len(status_list):
                    life_t = len(status_list) - 1
                csta = status_list[life_t]
                
            # 引き取り想定額 (金ゴールド * 100)
            money = choco_raw.get("gold", 0) * 100
            
            # チョコボ画像Noからファイル名を取得
            cno = choco_raw.get("no", 0)
            img_file = config.Config['choco_images'][cno] if cno < len(config.Config['choco_images']) else config.Config['choco_images'][0]
            
            choco_data = {
                "name": choco_raw.get("name", "名無しのチョコボ"),
                "sex": choco_raw.get("sex", 0),
                "cls": cls,
                "waza": waza,
                "run": choco_raw.get("run", 0),
                "win": cwin,
                "max": choco_raw.get("max", 10),
                "life": clife,
                "csta": csta,
                "money": money,
                "img_file": img_file,
                "no": cno
            }
            context["choco"] = choco_data
            
        common.render_template("morifarm.html", context)

    elif mode == "choco_shop":
        # === 野生チョコボ探索・購入画面 ===
        # chocobofile.json をロード
        choco_list = common.choco_list_load("chocobofile")
        
        # ランダムに5頭ほど抽出して表示
        hakken = random.randint(1, 5)
        selected_chocos = []
        if choco_list:
            for _ in range(hakken):
                selected_chocos.append(random.choice(choco_list))
                
        context["choco_list"] = selected_chocos
        common.render_template("morifarm.html", context)

    elif mode == "choco_shopb":
        # === お見合い相手選択画面 ===
        if not has_choco:
            common.show_error("親となるチョコボがいません。")
            
        cfname = choco_raw.get("name", "")
        if not cfname or cfname == "名無しのチョコボ":
            common.show_error("親となるチョコボに名前が付いていません。名前を付けてからお見合いしてください。")
            
        # 性別に応じて相手側のリストを読み込み
        # 自身がオス(1)なら相手はメス(chocoboos)、自身がメス(0)なら相手はオス(chocoboms)
        cfsex = choco_raw.get("sex", 0)
        list_type = "chocoboos" if cfsex == 1 else "chocoboms"
        
        choco_list = common.choco_list_load(list_type)
        
        # お相手候補をランダムに5頭抽出
        hakken = random.randint(1, 5)
        selected_chocos = []
        if choco_list:
            for _ in range(hakken):
                selected_chocos.append(random.choice(choco_list))
                
        # 自身のチョコボ情報
        cno = choco_raw.get("no", 0)
        ctype = choco_raw.get("type", 0)
        waza = types[ctype] if ctype < len(types) else "不明"
        
        choco_info = {
            "no": cno,
            "sex": cfsex,
            "name": cfname,
            "money": choco_raw.get("gold", 0) * 100,
            "run": choco_raw.get("run", 0),
            "win": choco_raw.get("win", 0),
            "max": choco_raw.get("max", 10),
            "waza": waza
        }
        
        context["choco"] = choco_info
        context["choco_list"] = selected_chocos
        common.render_template("morifarm.html", context)

    elif mode == "choco_buy":
        # === 野生チョコボ購入・捕獲処理 ===
        item_no = int(in_params.get("item_no", "-1"))
        
        # 野生チョコボリストから対象のチョコボを検索
        choco_list = common.choco_list_load("chocobofile")
        target_choco = None
        for cy in choco_list:
            if cy.get("no") == item_no:
                target_choco = cy
                break
                
        if not target_choco:
            common.show_error("そのチョコボは存在しません。")
            
        # 新しいチョコボデータの初期作成
        # カラム順に合わせた初期データ辞書を作成
        choco_data = {
            "id": user_id,
            "pass": chara["pass"],
            "breader": chara["name"],
            "name": target_choco.get("name", "名無しのチョコボ"),
            "sex": 0, # 初期はメス(0)
            "blood": target_choco.get("blood", 0),
            "no": target_choco.get("e", 0),
            "maxmax": 70, # 初期限界の限界値
            "type": target_choco.get("waza", 0),
            # max0〜max6 (初期限界値)
            "max0": 10, "max1": 10, "max2": 10, "max3": 10, "max4": 10, "max5": 10, "max6": 10,
            "life": 100, # 寿命
            "train": 0,  # トレーニング回数
            "run": 0,    # 出走回数
            "win": 0,    # 勝利数
            "max": 10,   # 現在の限界値
            # c0〜c6 (現在ステータス)
            "c0": 10, "c1": 10, "c2": 10, "c3": 10, "c4": 10, "c5": 10, "c6": 10,
            "gold": 0,
            # 家系
            "father": target_choco.get("mother", "不明"),
            "fblood": target_choco.get("motherrank", 0),
            "mother": target_choco.get("father", "不明"),
            "mblood": target_choco.get("fatherrank", 0)
        }
        
        # 排他ロックをかけて登録
        common.get_lock(f"choco_{user_id}")
        try:
            common.choco_regist(user_id, choco_data)
        finally:
            common.release_lock(f"choco_{user_id}")
            
        context["mode"] = "main" # メインに戻すための演出
        context["has_choco"] = True
        
        # メイン画面に自動遷移するためのcontext設定
        # ロードし直して渡す
        context["choco"] = {
            "name": choco_data["name"],
            "sex": choco_data["sex"],
            "cls": "新馬",
            "waza": types[choco_data["type"]],
            "run": 0,
            "win": 0,
            "max": 10,
            "life": 100,
            "csta": "最悪",
            "money": 0,
            "img_file": config.Config['choco_images'][choco_data["no"]],
            "no": choco_data["no"]
        }
        
        common.render_template("morifarm.html", context)

    elif mode == "choco_buyb":
        # === 配合（お見合い実行）処理 ===
        if not has_choco:
            common.show_error("親となるチョコボがいません。")
            
        item_no = int(in_params.get("item_no", "-1"))
        
        # 親チョコボ情報
        cfname = choco_raw.get("name", "")
        cfsex = choco_raw.get("sex", 0)
        cfblood = choco_raw.get("blood", 0)
        cfno = choco_raw.get("no", 0)
        cftype = choco_raw.get("type", 0)
        cfwin = choco_raw.get("win", 0)
        cftrain = choco_raw.get("train", 0)
        cffblood = choco_raw.get("fblood", 0)
        cfmblood = choco_raw.get("mblood", 0)
        cffather = choco_raw.get("father", "不明")
        cfmother = choco_raw.get("mother", "不明")
        cfbreader = choco_raw.get("breader", "")
        
        # 相手側リストをロード
        list_type = "chocoboos" if cfsex == 1 else "chocoboms"
        partner_list = common.choco_list_load(list_type)
        partner = None
        for cy in partner_list:
            if cy.get("no") == item_no:
                partner = cy
                break
                
        if not partner:
            common.show_error("お相手のチョコボが見つかりません。")
            
        cy_name = partner.get("name", "")
        cy_blood = partner.get("blood", 0)
        cy_e = partner.get("e", 0)
        cy_waza = partner.get("waza", 0)
        cy_fatherrank = partner.get("fatherrank", 0)
        cy_motherrank = partner.get("motherrank", 0)
        
        # 親の家系の名前定義
        if cfsex:
            father_name = cfname
            mother_name = cy_name
        else:
            father_name = cy_name
            mother_name = cfname
            
        # 子供のステータス計算
        # ランダム血統補正
        cf_ran_hit = False
        cy_ran_hit = False
        if not cfblood:
            cfblood = random.randint(0, 9)
            cf_ran_hit = True
        if not cy_blood:
            cy_blood = random.randint(0, 9)
            cy_ran_hit = True
            
        birth = random.randint(0, max(0, cfblood + cy_blood))
        if cf_ran_hit:
            cfblood = 0
        if cy_ran_hit:
            cy_blood = 0
            
        if cfwin > 50:
            birth += 1
        if cftrain > 1000:
            birth += 1
            
        prebirth = random.randint(0, max(0, cy_fatherrank + cy_motherrank)) + random.randint(0, max(0, cffblood + cfmblood))
        if cfwin > 100:
            prebirth += 2
        if cftrain > 500:
            prebirth += 1
            
        # 血統ランク cblood の算出
        cblood = 0
        if birth >= 14:
            cblood = 7 if prebirth >= 1 else 0
        elif birth == 13:
            if prebirth >= 3: cblood = 7
            elif prebirth >= 1: cblood = 6
            else: cblood = 0
        elif birth >= 12:
            if prebirth >= 7: cblood = 7
            elif prebirth >= 5: cblood = 6
            elif prebirth >= 3: cblood = 5
            elif prebirth >= 1: cblood = 4
            else: cblood = 0
        elif birth >= 11:
            if prebirth >= 9: cblood = 7
            elif prebirth >= 7: cblood = 6
            elif prebirth >= 5: cblood = 5
            elif prebirth >= 3: cblood = 4
            elif prebirth >= 1: cblood = 3
            else: cblood = 0
        elif birth >= 10:
            if prebirth >= 11: cblood = 7
            elif prebirth >= 9: cblood = 6
            elif prebirth >= 7: cblood = 5
            elif prebirth >= 5: cblood = 4
            elif prebirth >= 3: cblood = 3
            elif prebirth >= 1: cblood = 2
            else: cblood = 0
        elif birth >= 9:
            if prebirth >= 13: cblood = 7
            elif prebirth >= 11: cblood = 6
            elif prebirth >= 9: cblood = 5
            elif prebirth >= 7: cblood = 4
            elif prebirth >= 5: cblood = 3
            elif prebirth >= 3: cblood = 2
            elif prebirth >= 1: cblood = 1
            else: cblood = 0
        elif birth >= 8:
            if prebirth >= 15: cblood = 7
            elif prebirth >= 12: cblood = 6
            elif prebirth >= 10: cblood = 5
            elif prebirth >= 8: cblood = 4
            elif prebirth >= 5: cblood = 3
            elif prebirth >= 3: cblood = 2
            elif prebirth >= 1: cblood = 1
            else: cblood = 0
        elif birth >= 7:
            if prebirth >= 17: cblood = 7
            elif prebirth >= 13: cblood = 6
            elif prebirth >= 11: cblood = 5
            elif prebirth >= 9: cblood = 4
            elif prebirth >= 5: cblood = 3
            elif prebirth >= 3: cblood = 2
            elif prebirth >= 1: cblood = 1
            else: cblood = 0
        elif birth >= 6:
            if prebirth >= 19: cblood = 7
            elif prebirth >= 15: cblood = 6
            elif prebirth >= 12: cblood = 5
            elif prebirth >= 9: cblood = 4
            elif prebirth >= 5: cblood = 3
            elif prebirth >= 3: cblood = 2
            elif prebirth >= 1: cblood = 1
            else: cblood = 0
        elif birth >= 5:
            if prebirth >= 21: cblood = 7
            elif prebirth >= 17: cblood = 6
            elif prebirth >= 13: cblood = 5
            elif prebirth >= 9: cblood = 4
            elif prebirth >= 5: cblood = 3
            elif prebirth >= 3: cblood = 2
            elif prebirth >= 1: cblood = 1
            else: cblood = 0
        elif birth >= 4:
            if prebirth >= 23: cblood = 7
            elif prebirth >= 19: cblood = 6
            elif prebirth >= 15: cblood = 5
            elif prebirth >= 9: cblood = 4
            elif prebirth >= 5: cblood = 3
            elif prebirth >= 3: cblood = 2
            elif prebirth >= 1: cblood = 1
            else: cblood = 0
        elif birth >= 3:
            if prebirth >= 25: cblood = 7
            elif prebirth >= 21: cblood = 6
            elif prebirth >= 15: cblood = 5
            elif prebirth >= 13: cblood = 4
            elif prebirth >= 5: cblood = 3
            elif prebirth >= 3: cblood = 2
            elif prebirth >= 1: cblood = 1
            else: cblood = 0
        elif birth >= 2:
            if prebirth >= 27: cblood = 7
            elif prebirth >= 23: cblood = 6
            elif prebirth >= 19: cblood = 5
            elif prebirth >= 14: cblood = 4
            elif prebirth >= 5: cblood = 3
            elif prebirth >= 3: cblood = 2
            elif prebirth >= 1: cblood = 1
            else: cblood = 0
        elif birth >= 1:
            if prebirth >= 28: cblood = 7
            elif prebirth >= 25: cblood = 6
            elif prebirth >= 21: cblood = 5
            elif prebirth >= 15: cblood = 4
            elif prebirth >= 5: cblood = 3
            elif prebirth >= 3: cblood = 2
            elif prebirth >= 1: cblood = 1
            else: cblood = 0
        else:
            if prebirth == 28: cblood = 7
            elif prebirth >= 27: cblood = 6
            elif prebirth >= 25: cblood = 5
            elif prebirth >= 21: cblood = 4
            elif prebirth >= 11: cblood = 3
            elif prebirth >= 7: cblood = 2
            elif prebirth >= 3: cblood = 1
            else: cblood = 0
            
        # 最大限界値 cmaxmax の決定
        if cblood == 7: cmaxmax = 5500 + random.randint(0, 1499)
        elif cblood == 6: cmaxmax = 5500 + random.randint(0, 999)
        elif cblood == 5: cmaxmax = 4500 + random.randint(0, 1999)
        elif cblood == 4: cmaxmax = 3500 + random.randint(0, 2499)
        elif cblood == 3: cmaxmax = 3000 + random.randint(0, 2999)
        elif cblood == 2: cmaxmax = 2500 + random.randint(0, 2999)
        elif cblood == 1: cmaxmax = 2000 + random.randint(0, 3499)
        else: cmaxmax = random.randint(0, 6999)
        
        # 性別決定 (1: オス, 0: メス)
        csex = random.randint(0, 1)
        
        # 画像・タイプの決定
        if random.randint(0, 18) == 1:
            cno = random.randint(0, 7)
            ctype = random.randint(0, 5)
        elif random.randint(0, 1) == 1:
            cno = cy_e
            ctype = cy_waza
        else:
            cno = cfno
            ctype = cftype
            
        # 能力限界値 cmax0〜cmax6 と初期パラメータ c0〜c6 の算出
        cmax_vals = [0] * 7
        c_vals = [0] * 7
        
        # タイプ別補正値マッピング
        # [ [cmax_base, cmax_rand], [c_base, c_rand_mul] ]
        type_params = {
            0: [
                [[950, 100], [750, 100], [950, 100], [650, 100], [550, 100], [850, 100], [550, 100]],
                [[20, 48], [20, 38], [20, 48], [20, 33], [20, 28], [20, 43], [20, 28]]
            ],
            1: [
                [[850, 100], [750, 100], [850, 100], [650, 100], [650, 100], [850, 100], [650, 100]],
                [[20, 43], [20, 38], [20, 43], [20, 38], [20, 33], [20, 38], [20, 33]]
            ],
            2: [
                [[750, 100], [750, 100], [750, 100], [750, 100], [750, 100], [750, 100], [750, 100]],
                [[20, 38], [20, 38], [20, 38], [20, 38], [20, 38], [20, 38], [20, 38]]
            ],
            3: [
                [[650, 100], [650, 100], [750, 100], [850, 100], [850, 100], [650, 100], [850, 100]],
                [[20, 33], [20, 33], [20, 38], [20, 38], [20, 43], [20, 38], [20, 43]]
            ],
            4: [
                [[550, 100], [650, 100], [650, 100], [950, 100], [850, 100], [650, 100], [950, 100]],
                [[20, 28], [20, 33], [20, 33], [20, 38], [20, 43], [20, 43], [20, 48]]
            ],
            5: [
                [[750, 100], [650, 100], [650, 100], [950, 100], [650, 100], [950, 100], [650, 100]],
                [[20, 38], [20, 33], [20, 33], [20, 48], [20, 33], [20, 48], [20, 33]]
            ]
        }
        
        cfg = type_params.get(ctype, type_params[0])
        for idx in range(7):
            cmax_vals[idx] = cfg[0][idx][0] + random.randint(0, cfg[0][idx][1] - 1)
            c_vals[idx] = cfg[1][idx][0] + random.randint(0, cfg[1][idx][1] - 1) * (cblood + 1)
            
        csum = sum(c_vals)
        cmax = int(csum * (1 + random.random() * 2))
        
        if cmax > cmaxmax:
            cmax = cmaxmax
            if csum > cmaxmax:
                wariai = cmaxmax / csum
                for idx in range(7):
                    c_vals[idx] = int(c_vals[idx] * wariai) + 1
                    
        # 新チョコボデータの作成
        new_choco = {
            "id": user_id,
            "pass": chara["pass"],
            "breader": chara["name"],
            "name": "", # 名前は初期空白で命名フォームへ
            "sex": csex,
            "blood": cblood,
            "no": cno,
            "maxmax": cmaxmax,
            "type": ctype,
            "max0": cmax_vals[0], "max1": cmax_vals[1], "max2": cmax_vals[2], "max3": cmax_vals[3], "max4": cmax_vals[4], "max5": cmax_vals[5], "max6": cmax_vals[6],
            "life": 1000,
            "train": 0,
            "run": 0,
            "win": 0,
            "max": cmax,
            "c0": c_vals[0], "c1": c_vals[1], "c2": c_vals[2], "c3": c_vals[3], "c4": c_vals[4], "c5": c_vals[5], "c6": c_vals[6],
            "gold": 0,
            "father": father_name,
            "fblood": cfblood,
            "mother": mother_name,
            "mblood": cy_blood
        }
        
        common.get_lock(f"choco_{user_id}")
        try:
            common.choco_regist(user_id, new_choco)
        finally:
            common.release_lock(f"choco_{user_id}")
            
        # お見合い結果の情報をcontextに格納
        choco_info = {
            "no": cno,
            "waza": types[ctype],
            "father": father_name,
            "fblood": cfblood,
            "mother": mother_name,
            "mblood": cy_blood
        }
        context["choco"] = choco_info
        
        common.render_template("morifarm.html", context)

    elif mode == "choco_sell":
        # === チョコボ引退（野に放す）処理 ===
        if not has_choco:
            common.show_error("引退させるチョコボがいません。")
            
        cfname = choco_raw.get("name", "")
        if not cfname or cfname == "名無しのチョコボ":
            common.show_error("チョコボに名前を付けてから野に放してください。")
            
        # 売却金額 (想定額 = 金ゴールド * 100)
        cfgold = choco_raw.get("gold", 0)
        money = cfgold * 100
        
        cfsex = choco_raw.get("sex", 0)
        cfrun = choco_raw.get("run", 0)
        cfwin = choco_raw.get("win", 0)
        cfblood = choco_raw.get("blood", 0)
        cftype = choco_raw.get("type", 0)
        cffather = choco_raw.get("father", "不明")
        cffblood = choco_raw.get("fblood", 0)
        cfmother = choco_raw.get("mother", "不明")
        cfmblood = choco_raw.get("mblood", 0)
        cfno = choco_raw.get("no", 0)
        cfbreader = choco_raw.get("breader", "")
        
        # 殿堂お見合いリストの更新
        # オスならメスのお見合いリスト(chocoboos)、メスならオスのお見合いリスト(chocoboms)に登録する
        list_type = "chocoboos" if cfsex == 1 else "chocoboms"
        
        common.get_lock(list_type)
        try:
            lines = common.choco_list_load(list_type)
            # no(ID)でソート
            lines.sort(key=lambda x: x.get("no", 0))
            
            # 上書き先の決定 (割り込み処理)
            # 10回ランダム試行して条件に合うものを探す
            warikomi_idx = 0
            hit = False
            for _ in range(10):
                if not lines:
                    break
                idx = random.randint(0, len(lines) - 1)
                target = lines[idx]
                if target.get("win", 0) < 100 and target.get("blood", 0) < 5:
                    warikomi_idx = idx
                    hit = True
                    break
                    
            if not hit and lines:
                warikomi_idx = random.randint(0, len(lines) - 1)
                
            # ID割り当て
            warikomi_no = lines[warikomi_idx]["no"] if lines else random.randint(1, 99)
            
            new_entry = {
                "no": warikomi_no,
                "name": cfname,
                "price": money,
                "run": cfrun,
                "win": cfwin,
                "blood": cfblood,
                "waza": cftype,
                "father": cffather,
                "fatherrank": cffblood,
                "mother": cfmother,
                "motherrank": cfmblood,
                "e": cfno,
                "breader": cfbreader
            }
            
            if hit and warikomi_idx < len(lines):
                lines[warikomi_idx] = new_entry
            else:
                lines.insert(0, new_entry)
                
            common.choco_list_regist(list_type, lines)
        finally:
            common.release_lock(list_type)
            
        # プレイヤー所持金の加算
        chara["gold"] += cfgold
        if chara["gold"] > config.Config['max_gold']:
            chara["gold"] = config.Config['max_gold']
            
        common.get_lock(user_id)
        try:
            common.chara_regist(user_id, chara)
        finally:
            common.release_lock(user_id)
            
        # チョコボデータの物理削除
        common.get_lock(f"choco_{user_id}")
        try:
            path = os.path.join(config.Config['save_dir'], user_id, "chocolog.json")
            if os.path.exists(path):
                os.remove(path)
        finally:
            common.release_lock(f"choco_{user_id}")
            
        # 完了画面表示
        context["choco"] = {
            "breader": cfbreader,
            "no": cfno,
            "name": cfname,
            "money": money,
            "run": cfrun,
            "win": cfwin,
            "waza": types[cftype]
        }
        common.render_template("morifarm.html", context)

    elif mode == "choco_name":
        # === チョコボ命名処理 ===
        st_name = in_params.get("st_name", "").strip()
        if not st_name:
            common.show_error("名前を入力してください。")
            
        # 禁止ワードチェック
        for word in config.Config['ban_words']:
            if word in st_name:
                common.show_error(f"名前に禁止ワード「{word}」が含まれています。")
                
        # 履歴との重複チェック (もし履歴ファイルがあれば)
        rireki_path = os.path.join(config.Config['save_dir'], "rireki.json")
        if os.path.exists(rireki_path):
            with open(rireki_path, "r", encoding="utf-8") as f:
                try:
                    rireki = json.load(f)
                    for r in rireki:
                        if r.get("name") == st_name:
                            common.show_error("その名前は殿堂入りチョコボで既に使われています。別の名前にしてください。")
                except:
                    pass
                    
        if not has_choco:
            common.show_error("チョコボデータが見つかりません。")
            
        # 名前更新して保存
        choco_raw["name"] = st_name
        common.get_lock(f"choco_{user_id}")
        try:
            common.choco_regist(user_id, choco_raw)
        finally:
            common.release_lock(f"choco_{user_id}")
            
        context["mode"] = "main"
        context["has_choco"] = True
        
        # 表示用ステータス再算出
        cwin = choco_raw.get("win", 0)
        if cwin == 0: cls = "新馬"
        elif cwin < 5: cls = "５００万"
        elif cwin < 15: cls = "９００万"
        elif cwin < 30: cls = "１６００万"
        elif cwin < 50: cls = "オープン"
        elif cwin < 75: cls = "グレードⅣ"
        elif cwin < 105: cls = "グレードⅢ"
        elif cwin < 140: cls = "グレードⅡ"
        else: cls = "グレードⅠ"
        
        clife = choco_raw.get("life", 1000)
        if clife >= 990:
            csta = "寿命近し"
        else:
            status_list = ['最悪', '不調', '普通', '好調', '絶好調']
            life_t = int(clife / 200)
            if life_t >= len(status_list): life_t = len(status_list) - 1
            csta = status_list[life_t]
            
        cno = choco_raw.get("no", 0)
        
        context["choco"] = {
            "name": st_name,
            "sex": choco_raw.get("sex", 0),
            "cls": cls,
            "waza": types[choco_raw.get("type", 0)],
            "run": choco_raw.get("run", 0),
            "win": cwin,
            "max": choco_raw.get("max", 10),
            "life": clife,
            "csta": csta,
            "money": choco_raw.get("gold", 0) * 100,
            "img_file": config.Config['choco_images'][cno],
            "no": cno
        }
        
        common.render_template("morifarm.html", context)

    elif mode == "yadoya":
        # === 宿屋（寿命回復）処理 ===
        common.get_lock(user_id)
        try:
            # ギルを消費する
            chara = common.chara_load(user_id) # 最新データを読み込み
            if chara["gold"] < 5000:
                common.show_error("ゴールドが足りません。（5,000ゴールド必要です）")
                
            chara["gold"] -= 5000
            common.chara_regist(user_id, chara)
        finally:
            common.release_lock(user_id)
            
        # チョコボデータ回復
        common.get_lock(f"choco_{user_id}")
        try:
            choco = common.choco_load(user_id)
            if not choco:
                common.show_error("チョコボデータが見つかりません。")
                
            clife = choco.get("life", 1000)
            if clife == 1000:
                common.show_error("チョコボは既に絶好調（体力最大）です。")
                
            # 寿命のランダム回復
            clife += random.randint(200, 499)
            if clife > 1000:
                clife = 1000
                choco["max"] = choco.get("max", 10) + 10
                
            choco["life"] = clife
            choco["train"] = choco.get("train", 0) + 1
            choco["max"] = choco.get("max", 10) + 10
            
            common.choco_regist(user_id, choco)
        finally:
            common.release_lock(f"choco_{user_id}")
            
        common.render_template("morifarm.html", context)

if __name__ == "__main__":
    main()
