"""FFA (Final Fantasy Adventure) の共通設定。

このファイルには、ゲーム本体から参照する設定値だけをまとめています。
保存データのキー名や、既存キャラクターが持つ番号はここで変更しないでください。
特に画像・称号・職業などの番号付きマスターは、配列ではなく整数IDをキーにした
辞書で管理します。途中にデータを追加しても、既存データの番号がずれません。
"""

import os


Config = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================================
# 1. 保存先・実行環境
# ============================================================================
# プレイヤーデータ、排他制御ファイル、Jinjaテンプレートの保存先。
Config["save_dir"] = os.path.join(BASE_DIR, "save_data")
Config["lock_dir"] = os.path.join(BASE_DIR, "lock")
Config["template_dir"] = os.path.join(BASE_DIR, "templates")

# 管理画面のパスワードとセッション署名用秘密鍵。
# 本番環境では必ず環境変数を設定し、既定値のまま公開しないこと。
Config["admin_password"] = os.environ.get("FFA_ADMIN_PASSWORD", "1111")
Config["secret_key"] = os.environ.get(
    "FFA_SECRET_KEY", "ffa_secret_key_vips_ver3"
)

# メンテナンス中はログイン後のゲーム処理を停止する。
Config["maintenance_mode"] = 0  # 1: 有効 / 0: 無効


# ============================================================================
# 2. アカウント・セッション・自動削除
# ============================================================================
# ログインCookieと暗号化セッションの設定。
Config["cookie_name"] = "FFAPYCOOKIE"  # 旧版互換のログインCookie名
Config["session_expiry"] = 1800  # セッション有効期限（秒、30分）

# 長期間プレイされていないキャラクターの自動削除基準。
Config["character_delete_after_days"] = 60  # 最終戦闘から自動削除判定までの日数
Config["active_character_timeout_seconds"] = 120  # 他キャラクターを「現在冒険中」と表示する有効秒数

# 同一IP/ホストからの複数登録制限。
Config["single_account_per_host"] = True
Config["single_account_exempt_ids"] = [
    "test",
]  # 同一IPチェックを免除するテスト用ID

# テストユーザーなど、自動削除・管理画面削除から保護するID。
Config["protected_user_ids"] = [
    "test",
]
Config["protected_user_backup_dir"] = os.path.join(
    Config["save_dir"], "protected_users"
)

# 人間チャンプのデータ。対人戦や宿屋で更新される。
Config["champion_file"] = os.path.join(Config["save_dir"], "champion.json")
# チョコボチャンプのデータ。王者決定戦の結果で更新される。
Config["chocobo_champion_file"] = os.path.join(
    Config["save_dir"], "chocobo_champion.json"
)
# 現在アクセス中のキャラクター一覧。一定時間ごとに古い記録を整理する。
Config["active_characters_file"] = os.path.join(
    Config["save_dir"], "active_characters.json"
)


# ============================================================================
# 3. ゲームルール・上限・進行バランス
# ============================================================================
# キャラクターと所持金の上限。
Config["max_level"] = 99999
Config["max_hp"] = 99999999
Config["max_param"] = 99999  # 力・知能など各能力値の上限
Config["max_gold"] = 999999999999  # 所持金の上限
Config["max_bank"] = 999999999999000  # 銀行預金の上限

# 経験値・報酬・宿屋の基本値。
Config["inn_cost_per_level"] = 10  # 宿泊費のレベル1あたりの係数
Config["battle_reward_factor"] = 500  # 対戦賞金の乱数上限・連勝賞金の係数
Config["pvp_base_exp"] = 30  # 対人戦で得られる基本経験値
Config["level_up_exp_coeff"] = 300  # 次レベルまでの必要経験値に掛ける係数

# 各種行動の再実行待ち時間（秒）。
Config["pvp_race_cooldown_seconds"] = 20  # 対人戦・チョコボレース・天下一武道会
Config["training_cooldown_seconds"] = 20  # モンスター修行・チョコボ訓練・伝説の戦い

# 伝説の戦いの進行フラグを「挑戦可能」に戻す保存値。時間ではない。
Config["legend_progress_reset_value"] = 10

# 戦闘回数と戦闘処理の上限。
Config["training_battle_limit"] = 9999  # モンスター修行・伝説戦の残り回数初期値／補充値
Config["max_turns"] = 150  # 1戦闘の最大ターン数
Config["tenka_count"] = 3  # 天下一武道会の最大対戦数

# 旧版 wbattle.pl から引き継いだ戦闘判定値。
# 計算式と保存データの互換性に関わるため、意味を確認せず変更しないこと。
Config["counterattack_level_gap"] = 15  # 初手逆転必殺判定に必要なレベル差
Config["counterattack_damage_multiplier"] = 100  # 初手逆転必殺時のダメージ倍率

# 転職後の戦術クリア設定。1の場合、転職後に戦術を未習得へ戻す。
Config["reset_tactics_on_job_change"] = 1  # 転職時に戦術を未習得へ戻す

# 通常モンスターの難易度を切り替えるキャラクターレベル境界。
Config["monster_level_threshold_lv2"] = 100  # これ未満は初級、それ以上は中級候補
Config["monster_level_threshold_lv3"] = 500  # これ未満は中級、それ以上は上級候補
Config["monster_level_threshold_lv4"] = 1000  # これ未満は上級、それ以上は最上級
Config["isekai_level"] = 300  # 異世界へ入場できる最低レベル


# ============================================================================
# 4. 表示・お知らせ・入力制限
# ============================================================================
Config["main_title"] = "FFA改 Vips Ver 3.00"  # サイト・ページの基本タイトル
Config["manual_path"] = "html/manual.html"  # 遊び方・職業説明マニュアルのURL
Config["manual_link_label"] = "プレイマニュアル"  # マニュアルリンクの表示名

# 画面上部のテロップと公開トップのお知らせ。admin_messageはHTMLを含む。
Config["telop_message"] = (
    "<font color=yellow>ごゆっくりお楽しみください</font>管理人より♪"
)
Config["admin_message"] = (
    "<font color=red>\n"
    "・１人で２人以上のキャラクターの登録を禁止します。<br>\n"
    "・ブラウザの更新ボタン等を押すことを禁止します。<br>\n"
    "・上記に該当するキャラクターは連絡等をなしに管理人の独断により削除することがあります。</font><br>"
)

# キャラクター名・コメントなどへの入力禁止ワード。
Config["ban_words"] = [
    "あほ",
    "馬鹿",
    "SEX",
    "ダイヤルQ2",
    "キチガイ",
    "ウンコ",
    "チンポ",
]


# ============================================================================
# 5. URL・CGIルーティング
# ============================================================================
# 入口となるCGIスクリプト。
Config["login_script"] = "login.py"
Config["chara_make_script"] = "chara_make.py"
Config["admin_script"] = "admin.py"
Config["others_script"] = "others.py"

# 街・キャラクター設定・システム一覧。
Config["main_script"] = "login.py?mode=main"
Config["status_script"] = "login.py?mode=sts"
Config["tactics_script"] = "login.py?mode=tac_change"
Config["passchange_script"] = "login.py?mode=passchange"
Config["tensyoku_script"] = "login.py?mode=tensyoku"
Config["system_script"] = "login.py"  # modeパラメータを後ろに付けて使用
Config["ranking_script"] = "login.py?mode=rank"
Config["character_image_list_script"] = "login.py?mode=img_list"

# ショップ・施設。
Config["shop_item_script"] = "login.py?mode=shop_item"
Config["shop_def_script"] = "login.py?mode=shop_def"
Config["shop_acs_script"] = "login.py?mode=shop_acs"
Config["bank_script"] = "login.py?mode=bank"
Config["souko_script"] = "login.py?mode=souko"

# 対人戦・モンスター戦・ボス戦。
Config["select_battle_script"] = "login.py?mode=select_battle"
Config["battle_script"] = "login.py?mode=battle"
Config["monster_script"] = "login.py?mode=monster"
Config["legend_script"] = "login.py?mode=legend"

# チョコボ牧場・レース。
Config["chocofarm_script"] = "login.py?mode=chocofarm"
Config["mori_farm_script"] = "login.py?mode=morifarm"
Config["crace_script"] = "login.py?mode=crace"
Config["ctrain_script"] = "login.py?mode=ctrain"
Config["dendo_script"] = "login.py?mode=dendo"
Config["chocorank_script"] = "login.py?mode=chocorank"
Config["farmrace_script"] = "login.py?mode=farmrace"

# 掲示板・天下一武道会。
Config["bbs_script"] = "login.py?mode=bbs"
Config["tenka_script"] = "login.py?mode=tenka"


# ============================================================================
# 6. マスターデータ・データファイル
# ============================================================================
# 職業と戦術のマスター。
Config["syoku_file"] = "data/syoku.json"
Config["tac_file"] = "data/tac.json"  # 職業別の使用条件はjob_idsで管理

# 装備マスター。購入・装備可能職業は各JSONのjob_idsで管理する。
Config["weapon_file"] = "data/weapon.json"
Config["armor_file"] = "data/armor.json"
Config["accessory_file"] = "data/accessory.json"

# プレイヤー1人あたりの倉庫上限。
Config["max_weapons"] = 8
Config["max_armors"] = 8
Config["max_accessories"] = 8

# チョコボ牧場の補助マスター。
Config["hint_file"] = "data/hint.json"
Config["wild_chocobo_file"] = "data/chocobo/chocobofile.json"  # 購入候補となる野生チョコボ
Config["chocobo_race_data_dir"] = "data/chocobo"  # チョコボレースのライバルデータ格納先
Config["chocobo_rival_files"] = {
    0: "ribal0.json",
    1: "ribal1.json",
    2: "ribal2.json",
    3: "ribal3.json",
    4: "ribal4.json",
    5: "ribal5.json",
    6: "ribal6.json",
    7: "ribal7.json",
    8: "ribal8.json",
}  # チョコボレースのライバルマスター（レース番号別）

# 通常戦・異世界戦で使用するモンスター。
Config["monster_lv1_file"] = "data/monsters/mons_lv1.json"  # 初級
Config["monster_lv2_file"] = "data/monsters/mons_lv2.json"  # 中級
Config["monster_lv3_file"] = "data/monsters/mons_lv3.json"  # 上級
Config["monster_lv4_file"] = "data/monsters/mons_lv4.json"  # 最上級
Config["isekai_file"] = "data/monsters/mons_isekai.json"

# 伝説の戦いで階層ごとに使用するボス。
Config["legend_boss_lv1_file"] = "data/monsters/legend_boss_lv1.json"
Config["legend_boss_lv2_file"] = "data/monsters/legend_boss_lv2.json"
Config["legend_boss_lv3_file"] = "data/monsters/legend_boss_lv3.json"
Config["legend_boss_lv4_file"] = "data/monsters/legend_boss_lv4.json"

# 伝説の戦いの難易度に応じた背景画像。
Config["legend_battle_media"] = {
    "final": {
        "background": "images/last_boss_back.gif",
    },
    "high": {
        "background": "images/boss_back.gif",
    },
    "normal": {
        "background": "images/boss2_back.gif",
    },
}

# 旧版のfarm_back/crace_backに相当する牧場・レース背景。
# 牧場系画面のデザインを変更しても、背景差し替え箇所は設定で管理する。
Config["chocobo_farm_background"] = "images/farm.jpg"
Config["chocobo_race_background"] = "images/farm.jpg"


# ============================================================================
# 7. 画像・表示マスター（番号は保存データと対応）
# ============================================================================
# キャラクター立ち絵。既存画像のIDは変更・再採番しないこと。
Config["chara_images"] = {
    0: "ana.gif", 1: "arce.gif", 2: "arlon.gif", 3: "balt.gif",
    4: "bea.gif", 5: "bellmayl.gif", 6: "c_zoro.gif", 7: "corza.gif",
    8: "dr_kureha.gif", 9: "elly.gif", 10: "emerada.gif", 11: "fei.gif",
    12: "karuu.gif", 13: "kuina.gif", 14: "kuro.gif", 15: "kurokoda.gif",
    16: "kuzya.gif", 17: "maru.gif", 18: "meso-s.gif", 19: "mini-aerith.gif",
    20: "mini-auron.gif", 21: "mini-baku.gif", 22: "mini-barret.gif", 23: "mini-blank.gif",
    24: "mini-braska.gif", 25: "mini-buricid.gif", 26: "mini-cait.gif", 27: "mini-cid.gif",
    28: "mini-cid10.gif", 29: "mini-cid7.gif", 30: "mini-cinna.gif", 31: "mini-cloud.gif",
    32: "mini-edea.gif", 33: "mini-eiko.gif", 34: "mini-el.gif", 35: "mini-ff9-01.gif",
    36: "mini-ff9-02.gif", 37: "mini-ff9-03.gif", 38: "mini-ff9-04.gif", 39: "mini-ff9-05.gif",
    40: "mini-ff9-06.gif", 41: "mini-ff9-07.gif", 42: "mini-flatley.gif", 43: "mini-freija.gif",
    44: "mini-fuujin.gif", 45: "mini-garnet.gif", 46: "mini-jecht.gif", 47: "mini-kerocid.gif",
    48: "mini-kimari.gif", 49: "mini-kiros.gif", 50: "mini-laguna.gif", 51: "mini-lani.gif",
    52: "mini-lulu.gif", 53: "mini-marcus.gif", 54: "mini-mikoto.gif", 55: "mini-quina.gif",
    56: "mini-quistis.gif", 57: "mini-raijin.gif", 58: "mini-red.gif", 59: "mini-rikku.gif",
    60: "mini-rinoa.gif", 61: "mini-ruby.gif", 62: "mini-salamander.gif", 63: "mini-seif.gif",
    64: "mini-selphie.gif", 65: "mini-sephi.gif", 66: "mini-seymore.gif", 67: "mini-shelinda.gif",
    68: "mini-squall.gif", 69: "mini-steiner.gif", 70: "mini-tidus.gif", 71: "mini-tifa.gif",
    72: "mini-vin.gif", 73: "mini-vivi.gif", 74: "mini-wakka.gif", 75: "mini-ward.gif",
    76: "mini-yuffie.gif", 77: "mini-yuna.gif", 78: "mini-yunalesca.gif", 79: "mini-zell.gif",
    80: "mini-zidane.gif", 81: "mog.gif", 82: "mr2.gif", 83: "ms_gw.gif",
    84: "munba.gif", 85: "nami.gif", 86: "pel.gif", 87: "rufi.gif",
    88: "sanji.gif", 89: "sarama.gif", 90: "shitan.gif", 91: "smoker.gif",
    92: "syancs.gif", 93: "tashi.gif", 94: "usausa.gif", 95: "vivi.gif",
    96: "zoro.gif",
    # 追加画像は必ず新しいIDを割り当て、既存IDの意味を変えないこと。
    97: "chop.gif", 98: "gf-efreet.gif", 99: "gf-karban.gif", 100: "gf-leviathan.gif",
    101: "gf-siren.gif", 102: "ikon_m_c.gif", 103: "ikon_m_e.gif", 104: "ikon_m_f.gif",
    105: "ikon_m_g.gif", 106: "ikon_m_m.gif", 107: "ikon_m_q.gif", 108: "ikon_m_sa.gif",
    109: "ikon_m_st.gif", 110: "ikon_m_v.gif", 111: "ikon_m_z.gif",
}

# チョコボ画像。チョコボデータのnoと対応する。
Config["choco_images"] = {
    0: "cho-ml.gif",
    1: "cho-gl.gif",
    2: "cho-yl.gif",
    3: "cho-kl.gif",
    4: "cho-bl.gif",
    5: "cho-wl.gif",
    6: "cho-rl.gif",
    7: "cho-pl.gif",
}
Config["character_image_path"] = "images/chara"  # キャラクター画像のURL基準
Config["chocobo_image_path"] = "images/chara/choco"  # チョコボ画像のURL基準

# チョコボの成長タイプ。チョコボデータのtypeと対応する。
Config["chocobo_types"] = {
    0: "普通",
    1: "早熟",
    2: "晩成",
    3: "持続",
    4: "超晩成",
    5: "超早熟",
}


# ============================================================================
# 8. 職業・称号マスター（番号は保存データと対応）
# ============================================================================
# キャラクターの伝説攻略段階に対応する称号。
Config["titles"] = {
    0: "駆け出し",
    1: "プチ",
    2: "超",
    3: "極",
    4: "超極の殿堂",
}

# 職業IDは職業マスター、キャラクター、装備、戦術データから参照される。
# 既存のIDを変更せず、新しい職業は末尾に新規IDを追加すること。
Config["chara_jobs"] = {
    0: "見習い戦士",
    1: "戦士",
    2: "ナイト",
    3: "シーフ",
    4: "竜騎士",
    5: "赤魔道士",
    6: "バード",
    7: "忍者",
    8: "召喚士",
    9: "ビショップ",
    10: "聖騎士",
    11: "モンク",
    12: "暗黒騎士",
    13: "魔人",
    14: "蒼魔道士",
    15: "時魔道士",
    16: "マシーナリー",
    17: "グラディエーター",
    18: "学者",
    19: "バーサーカー",
    20: "風水士",
    21: "召喚術士",
    22: "管理者",
    23: "ものまね士",
    24: "アニマルテイマー",
    25: "アサシン",
    26: "剣聖",
    27: "バトルマスター",
    28: "ホーリーナイト",
    29: "歌姫",
    30: "ナイトメアマイスター",
}

# キャラクター作成時に選択できる職業ID。職業マスター全体とは別に管理する。
Config["initial_job_ids"] = (0, 1, 2, 3)
Config["jobs_html_path"] = "html/manual.html#jobs"  # 職業説明へのリンク


# ============================================================================
# 9. 表示件数・コミュニケーション上限・外部リンク
# ============================================================================
Config["bbs_display_limit"] = 20  # 街に表示する掲示板投稿数
Config["max_all_messages"] = 20  # 全体ニュースの最大保持・表示件数
Config["bbs_storage_limit"] = 50  # 掲示板ファイルに保持する投稿数
Config["chocobo_partner_list_limit"] = 100  # お見合い候補として保持する最大件数
Config["character_image_list_label"] = "アイコン一覧"  # キャラクター画像一覧リンクの表示名


# ============================================================================
# 10. 起動時検証
# ============================================================================
def _validate_id_maps():
    """番号付きマスターが誤って配列へ戻らないよう検証する。"""
    id_maps = (
        "chara_images",
        "choco_images",
        "chocobo_types",
        "titles",
        "chara_jobs",
    )
    for map_name in id_maps:
        values = Config[map_name]
        if not isinstance(values, dict) or any(
            not isinstance(key, int) for key in values
        ):
            raise ValueError(f"{map_name} は整数IDをキーにした辞書で定義してください")

    if not set(Config["initial_job_ids"]).issubset(Config["chara_jobs"]):
        raise ValueError("initial_job_ids に未定義の職業IDが含まれています")


_validate_id_maps()
