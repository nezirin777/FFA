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
FFA Python/CGI - メイン・ステータス画面表示スクリプト (ffadventure.py)
"""
import os
import time
import json

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正

parse_cookie_user = common.parse_cookie_user

def get_winner():
    """
    王者データを読み込み、辞書として返します。
    """
    winner_path = os.path.join(common.BASE_DIR, config.Config['champion_file'])
    default_winner = {
        "id": "sys", "name": "無名の剣士", "img": 0, "hp": 1000, "max_hp": 1000, "win_count": 0
    }
    if not os.path.exists(winner_path):
        return default_winner
    try:
        with open(winner_path, "r", encoding="utf-8") as f:
            data = common.decode_html_entities(json.load(f))
        return {
            "id": data.get("id", "sys"),
            "name": data.get("name", "無名の剣士"),
            "img": data.get("img", 0),
            "hp": data.get("hp", 1000),
            "max_hp": data.get("max_hp", 1000),
            "win_count": data.get("win_count", 0)
        }
    except Exception:
        return default_winner

def main():
    # 1. メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    # 2. パラメータの取得
    params = common.decode_params()
    user_id = params.get("id", "").strip()
    
    # 3. ユーザー認証（クッキーチェックを含む）
    # クッキーからログイン情報を取得
    cookie_str = common.get_cookie(config.Config['cookie_name'])
    c_id, c_pass = parse_cookie_user(cookie_str)
    
    if not user_id:
        # パラメータで ID が渡されていない場合は、クッキーの ID を使用
        if c_id:
            user_id = c_id
        else:
            common.show_error("ログイン情報がありません。再度ログインしてください。")
            
    # キャラクターデータロード
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターが存在しないか、データが破損しています。")
        
    # パスワード検証（IDOR対策: ログイン中の本人のみ自分のホーム画面を表示できる）
    if c_id != user_id or c_pass != chara["pass"]:
        common.show_error("認証に失敗しました。再度ログインしてください。")

    # レジェンド攻略結果・待機画面からの明示中断はCSRFを検証する。
    if params.get("legend_cancel") == "1":
        if os.environ.get("REQUEST_METHOD", "GET").upper() != "POST":
            common.show_error("不正な中断リクエストです。画面のボタンから操作してください。")
        from sub_def.crypto import get_session, token_check
        token_check(params, get_session())

    # Ver2と同様、街へ戻った時点でレジェンドの途中進行は破棄する。
    # 戦闘結果画面からの連戦は街を経由しないため、同じ階層内では継続できる。
    legend_reset_value = config.Config["legend_progress_reset_value"]
    if common.to_int(chara.get("boss_flag", legend_reset_value), legend_reset_value) != legend_reset_value:
        common.get_lock(user_id)
        try:
            latest_chara = common.chara_load(user_id)
            if latest_chara:
                if common.to_int(latest_chara.get("boss_flag", legend_reset_value), legend_reset_value) != legend_reset_value:
                    latest_chara["boss_flag"] = legend_reset_value
                    common.chara_regist(user_id, latest_chara)
                chara = latest_chara
        finally:
            common.release_lock(user_id)
        
    # 4. 所持アイテムのロード
    item = common.equipment_load(user_id)
    if not item:
        # 初期装備の設定（ロード失敗時の安全策）
        item = common.default_equipment()
        
    # 5. 王者データの取得
    winner = get_winner()
    # チョコボチャンプは人間側のチャンプとは別の共有セーブデータです。
    choco_winner = common.chocobo_champion_view()
    
    # 6. 行動制限時間・待機時間の計算
    now = int(time.time())
    ltime = now - chara["last_time"]
    vtime = config.Config['pvp_race_cooldown_seconds'] - ltime
    ztime = vtime + 1 if vtime >= 0 else 0

    # 性別表記
    esex = "男" if chara["sex"] else "女"
    
    # レベルアップ必要経験値
    next_ex = chara["level"] * config.Config['level_up_exp_coeff']
    
    # 称号
    title_idx = chara["title_id"]
    syou = config.Config['titles'].get(title_idx, config.Config['titles'][0])
    
    # 宿屋代金の計算
    yado_daix = int(config.Config['inn_cost_per_level'] * chara["level"])
    
    # 職業名の取得
    job_idx = chara["job"]
    job_name = config.Config['chara_jobs'].get(job_idx, "不明な職業")

    # Ver2のclassと同じく、現職の熟練度を10刻みでクラス表示する。
    class_marks = ("■□□□□□", "■■□□□□", "■■■□□□", "■■■■□□", "■■■■■□", "■■■■■■", "★★★★★★")
    class_names = ("Beginner", "Charanger", "LowClass", "NormalClass", "HighClass", "TopClass", "Master")
    class_index = min(6, max(0, int(chara.get("job_level", 0)) // 10))
    job_class_mark = class_marks[class_index]
    job_class_name = class_names[class_index]
    
    # HPパーセンテージ計算
    if chara["max_hp"] > 0:
        hp_percent = int(chara["hp"] / chara["max_hp"] * 100)
    else:
        hp_percent = 0
    if hp_percent > 100:
        hp_percent = 100
        
    # 銀行預金 (Perl の $chara[34] に相当)
    chara["bank"] = chara.get("bank", chara.get("unused33", 0)) # 移行スクリプトで key に bank が無ければ default 0
    if "bank" not in chara:
        # キーが無い場合は追加
        chara["bank"] = chara.get("unused33", 0)
        
    # 7. アクティブキャラクター一覧の更新・取得
    active_characters_html = common.update_and_get_active_characters(user_id, chara["name"])
    
    # 8. 掲示板の取得
    bbs_posts = common.bbs_load()[:config.Config['bbs_display_limit']]
    all_messages = common.all_message_load()[:config.Config['all_message_display_limit']]
    accessory_description = common.accessory_description(item.get("accessory", {}), chara.get("accessory_id", 0))

    # 街の基本能力値欄でも、旧版と同じく装備補正を併記する。
    accessory = item.get("accessory", {})
    hit_ritu = min(150, int(chara.get("dex", 10) / 10) + 51)
    kaihi_ritu = min(50, int(chara.get("agi", 10) / 20))
    waza_ritu = min(75, int(chara.get("karma", 0) / 15) + 10 + chara.get("job_level", 0))
    ci_plus = item.get("weapon", {}).get("hit_rate", 0) + accessory.get("hit_rate", 0)
    cd_plus = item.get("armor", {}).get("evasion_rate", 0) + accessory.get("evasion_rate", 0)
    waza_plus = accessory.get("special_rate", 0)

    # 街の能力値欄にも、ステータス詳細と同じ表示用バーを渡す。
    divpm = int(config.Config["max_param"] / 100) if config.Config["max_param"] > 0 else 100
    if divpm <= 0:
        divpm = 100

    def get_visible_bar_width(value):
        return min(100, max(1, int(value)))

    bar_widths = {
        "str": get_visible_bar_width(0.5 * (chara.get("str", 10) / divpm)),
        "int": get_visible_bar_width(0.5 * (chara.get("int", 10) / divpm)),
        "mnd": get_visible_bar_width(0.5 * (chara.get("mnd", 10) / divpm)),
        "vit": get_visible_bar_width(0.5 * (chara.get("vit", 10) / divpm)),
        "dex": get_visible_bar_width(0.5 * (chara.get("dex", 10) / divpm)),
        "agi": get_visible_bar_width(0.5 * (chara.get("agi", 10) / divpm)),
        "cha": get_visible_bar_width(0.5 * (chara.get("cha", 10) / divpm)),
        "karma": get_visible_bar_width(0.5 * (chara.get("karma", 0) / divpm)),
        "hit": get_visible_bar_width((hit_ritu + ci_plus) * 0.5),
        "kaihi": get_visible_bar_width((kaihi_ritu + cd_plus) * 0.5),
        "waza": get_visible_bar_width(waza_ritu + waza_plus),
    }
    
    # 9. 画面描画
    context = {
        "chara": chara,
        "equipment": item,
        "winner": winner,
        "choco_winner": choco_winner,
        "ztime": ztime,
        "esex": esex,
        "next_ex": next_ex,
        "syou": syou,
        "yado_daix": yado_daix,
        "job_name": job_name,
        "job_class_mark": job_class_mark,
        "job_class_name": job_class_name,
        "hp_percent": hp_percent,
        "active_characters_html": active_characters_html,
        "bbs_posts": bbs_posts,
        "all_messages": all_messages,
        "chara_img": config.Config['chara_images'],
        "accessory_description": accessory_description,
        "hit_ritu": hit_ritu,
        "kaihi_ritu": kaihi_ritu,
        "waza_ritu": waza_ritu,
        "ci_plus": ci_plus,
        "cd_plus": cd_plus,
        "waza_plus": waza_plus,
        "bar_widths": bar_widths,
    }
    
    common.render_template("ffadventure.html", context)

if __name__ == "__main__":
    main()
