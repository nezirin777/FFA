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
    # IDOR対策: 状態変更は本人のみ許可(ロック取得前にチェック)
    common.require_owner(user_id)
    chara_log = in_params.get("mydata", "")
    mode = in_params.get("mode", "")

    if mode == "dendo":
        from sub_def.crypto import get_session, token_check
        token_check(in_params, get_session())

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
        my_trophies = []
        if g1_raw:
            for k in RACE_NAMES.keys():
                if g1_raw.get(k, 0) > 0:
                    my_trophies.append(RACE_NAMES[k])

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
    types = config.Config["chocobo_types"]
    
    formatted_dendo = []

    def class_name_from_wins(win_count):
        if win_count == 0:
            return "新馬"
        if win_count < 5:
            return "５００万"
        if win_count < 15:
            return "９００万"
        if win_count < 30:
            return "１６００万"
        if win_count < 50:
            return "オープン"
        if win_count < 75:
            return "グレードⅣ"
        if win_count < 105:
            return "グレードⅢ"
        if win_count < 140:
            return "グレードⅡ"
        return "グレードⅠ"

    ability_labels = ("スピード", "スタミナ", "粘り", "落ち着き", "闘争心", "賢さ", "反射神経")
    image_files = config.Config["choco_images"]

    for dc in dendo_list:
        trophy_data = []
        for trophy_name in dc.get("trophies", []):
            race_key = next((key for key, name in RACE_NAMES.items() if name == trophy_name), "")
            trophy_data.append({
                "name": trophy_name,
                "is_g1": bool(race_key and int(race_key[1:]) <= 11),
            })

        win_count = common.to_int(dc.get("win"), 0)
        ability_values = [common.to_int(dc.get(f"c{index}"), 10) for index in range(7)]
        image_id = common.to_int(dc.get("no"), 0)
        formatted_dendo.append({
            "name": dc.get("name", "名無し"),
            "breader": dc.get("breader", "不明"),
            "image": image_files.get(image_id, image_files.get(0, "")),
            "sex_label": "オス" if common.to_int(dc.get("sex"), 0) == 1 else "メス",
            "type_label": types.get(common.to_int(dc.get("type"), 0), "不明"),
            "run": common.to_int(dc.get("run"), 0),
            "win": win_count,
            "train": common.to_int(dc.get("train"), 0),
            "max": common.to_int(dc.get("max"), 10),
            "maxmax": common.to_int(dc.get("maxmax"), common.to_int(dc.get("max"), 0)),
            "money": common.to_int(dc.get("gold"), 0) * 100,
            "father": dc.get("father", "不明"),
            "mother": dc.get("mother", "不明"),
            "abilities": [
                {
                    "label": label,
                    "value": value,
                    "rank_idx": min(len(rank_imgs) - 1, max(0, value // 100)),
                }
                for label, value in zip(ability_labels, ability_values)
            ],
            "class_name": class_name_from_wins(win_count),
            "trophies": trophy_data,
        })

    context = {
        "page_background": config.Config["chocobo_farm_background"],
        "chara": chara,
        "chara_log": chara_log,
        "dendo_list": formatted_dendo,
        "legends": formatted_dendo,
        "rank_imgs": rank_imgs,
        "types": types,
        "registered_msg": registered_msg
    }

    common.render_template("dendo.html", context)

if __name__ == "__main__":
    main()
