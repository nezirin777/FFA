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

# CGIが受け取るPOST本文の上限。旧版と同じ50KiBに制限し、意図しない
# 大きなリクエストをアプリケーション側でも受け取らない。
Config["max_post_body_bytes"] = 50 * 1024

# 異常終了で残ったロックを自動解除するまでの秒数。通常の保存や日次バックアップが
# この時間を超える運用では値を上げる。0以下にすると自動解除を無効化する。
Config["lock_stale_seconds"] = 300

# 日次セーブバックアップ。save_dataの外に置き、バックアップ自身を再コピーしない。
Config["backup_dir"] = os.path.join(BASE_DIR, "backups")
Config["backup_enabled"] = True
Config["backup_retention_days"] = 40

# 管理画面のパスワードとセッション署名用秘密鍵。
# 本番環境では必ず環境変数を設定し、既定値のまま公開しないこと。
Config["admin_password"] = os.environ.get("FFA_ADMIN_PASSWORD", "1111")
Config["secret_key"] = os.environ.get("FFA_SECRET_KEY", "ffa_secret_key_vips_ver3")

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
Config["active_character_timeout_seconds"] = (
    120  # 他キャラクターを「現在冒険中」と表示する有効秒数
)

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

# モンスター戦の盗み報酬上限。引き分け時も盗み分を支給するため、
# 1戦で何度も成功しても報酬が無制限に増えないようにする。
Config["monster_steal_max_successes"] = 3  # 1戦あたりの盗み成功回数上限
Config["monster_steal_reward_cap_multiplier"] = 2  # 通常勝利報酬の最大値（基準報酬×2）

# 旧版 wbattle.pl から引き継いだ戦闘判定値。
# 計算式と保存データの互換性に関わるため、意味を確認せず変更しないこと。
Config["counterattack_level_gap"] = 15  # 初手逆転必殺判定に必要なレベル差
Config["counterattack_damage_multiplier"] = 100  # 初手逆転必殺時のダメージ倍率

# マスター済みの別職業の戦術を選択候補へ含めるか。Ver2の $master_tac に対応。
Config["master_tactics_enabled"] = 1
# 転職後の選択中戦術を解除するか。戦術候補の範囲とは独立している。
Config["reset_tactics_on_job_change"] = 1

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
Config["shop_weapon_script"] = "login.py?mode=shop_weapon"
Config["shop_armor_script"] = "login.py?mode=shop_armor"
Config["shop_accessory_script"] = "login.py?mode=shop_accessory"
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
Config["wild_chocobo_file"] = (
    "data/chocobo/chocobofile.json"  # 購入候補となる野生チョコボ
)
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


# ============================================================================
# 7. 画像・表示マスター（番号は保存データと対応）
# ============================================================================
# キャラクター立ち絵。保存データのimg値と対応するため、並び順を変更しないこと。
Config["chara_images"] = {
    0: "FF7_クラウド.gif",
    1: "FF7_ティファ.gif",
    2: "FF7_エアリス.gif",
    3: "FF7_ユフィ.gif",
    4: "FF7_バレット.gif",
    5: "FF7_ケット・シー.gif",
    6: "FF7_シド.gif",
    7: "FF7_セフィロス.gif",
    8: "FF7_レッド.gif",
    9: "FF7_ヴィンセント.gif",
    10: "FF8_スコール.gif",
    11: "FF8_スコールうさぎ.gif",
    12: "FF8_ラグナ.gif",
    13: "FF8_リノア.gif",
    14: "FF8_ゼル.gif",
    15: "FF8_アーヴァイン.gif",
    16: "FF8_イデア.gif",
    17: "FF8_ウォード.gif",
    18: "FF8_エルオーネ.gif",
    19: "FF8_キスティス.gif",
    20: "FF8_キロス.gif",
    21: "FF8_サイファー.gif",
    22: "FF8_シド.gif",
    23: "FF8_セルフィ.gif",
    24: "FF8_ムンバ.gif",
    25: "FF8_風神.gif",
    26: "FF8_雷神.gif",
    27: "FF9_ジタン.gif",
    28: "FF9_ガーネット.gif",
    29: "FF9_ビビ.gif",
    30: "FF9_クイナ.gif",
    31: "FF9_エーコ.gif",
    32: "FF9_アデルバート.gif",
    33: "FF9_クジャ.gif",
    34: "FF9_バクー.gif",
    35: "FF9_フラットレイ.gif",
    36: "FF9_フライヤ.gif",
    37: "FF9_サラマンダー.gif",
    38: "FF9_ブランク.gif",
    39: "FF9_ブリ虫シド.gif",
    40: "FF9_カエルシド.gif",
    41: "FF9_シナ.gif",
    42: "FF9_ベアトリクス .gif",
    43: "FF9_マーカス.gif",
    44: "FF9_ミコト.gif",
    45: "FF9_ラニ.gif",
    46: "FF9_ルビィ.gif",
    47: "FF10_ティーダ.gif",
    48: "FF10_ユウナ.gif",
    49: "FF10_ワッカ.gif",
    50: "FF10_ルールー.gif",
    51: "FF10_リュック.gif",
    52: "FF10_アーロン.gif",
    53: "FF10_キマリ.gif",
    54: "FF10_ブラスカ.gif",
    55: "FF10_シーモア.gif",
    56: "FF10_ジェクト.gif",
    57: "FF10_ユウナレスカ.gif",
    58: "FF10_シド.gif",
    59: "FF10_シェリンダ .gif",
    60: "FF_イフリート.gif",
    61: "FF_カーバンクル.gif",
    62: "FF_セイレーン.gif",
    63: "FF_モーグリ.gif",
    64: "FF_リヴァイアサン.gif",
    65: "めそ.gif",
    66: "ゼノギアス_エメラダ.gif",
    67: "ゼノギアス_エリィ.gif",
    68: "ゼノギアス_バルト.gif",
    69: "ゼノギアス_フェイ.gif",
    70: "ゼノギアス_シタン.gif",
    71: "ゼノギアス_マルー.gif",
    72: "ワンピ_ルフィ.gif",
    73: "ワンピ_Mr2.gif",
    74: "ワンピ_くいな.gif",
    75: "ワンピ_たしぎ.gif",
    76: "ワンピ_ゾロ.gif",
    77: "ワンピ_ゾロ2.gif",
    78: "ワンピ_サンジ.gif",
    79: "ワンピ_ナミ.gif",
    80: "ワンピ_チョッパー.gif",
    81: "ワンピ_ビビ.gif",
    82: "ワンピ_カル―.gif",
    83: "ワンピ_アーロン.gif",
    84: "ワンピ_エース.gif",
    85: "ワンピ_クレハ.gif",
    86: "ワンピ_クロ.gif",
    87: "ワンピ_クロコダイル.gif",
    88: "ワンピ_コーザ.gif",
    89: "ワンピ_シャンクス.gif",
    90: "ワンピ_スモーカー.gif",
    91: "ワンピ_ベルメール.gif",
    92: "ワンピ_ペル.gif",
    93: "ワンピ_ミスGW.gif",
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
Config["chocobo_image_path"] = "images/choco"  # チョコボ画像のURL基準

# チョコボの成長タイプ。チョコボデータのtypeと対応する。
Config["chocobo_types"] = {
    0: "普通",
    1: "早熟",
    2: "晩成",
    3: "持続",
    4: "超晩成",
    5: "超早熟",
}


# 旧版のfarm_back/crace_backに相当する牧場・レース背景。
# 牧場系画面のデザインを変更しても、背景差し替え箇所は設定で管理する。
Config["chocobo_farm_background"] = ""
Config["chocobo_race_background"] = ""
Config["chocobo_race_announcer_image"] = (
    "images/choco/アナウンサー.gif"  # レース実況欄のアナウンサー画像
)

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
    0: "ソルジャー",
    1: "黒魔道士",
    2: "白魔道士",
    3: "シーフ",
    4: "時魔道士",
    5: "赤魔道士",
    6: "バード",
    7: "召喚士",
    8: "竜騎士",
    9: "ビショップ",
    10: "ナイト",
    11: "侍",
    12: "モンク",
    13: "忍者",
    14: "暗黒騎士",
    15: "魔法剣士",
    16: "マシナリー",
    17: "幻獣師",
    18: "皇帝",
    19: "Ｓｅｅｄ",
    20: "占い師",
    21: "ものまね師",
    22: "管理人",
    23: "たまねぎ剣士",
    24: "アニマルテイマー",
    25: "アサシン",
    26: "聖者",
    27: "バトルマスター",
    28: "ホーリーナイト",
    29: "勇者",
    30: "グランドマスター",
}

# キャラクター作成時に選択できる職業ID。職業マスター全体とは別に管理する。
Config["initial_job_ids"] = (0, 1, 2, 3)
Config["jobs_html_path"] = "html/manual.html#jobs"  # 職業説明へのリンク


# ============================================================================
# 9. 表示件数・コミュニケーション上限・外部リンク
# ============================================================================
Config["bbs_display_limit"] = 100  # 街のスクロール枠に読み込む掲示板投稿数
Config["bbs_storage_limit"] = 100  # 掲示板ファイルに保持する投稿数
Config["all_message_display_limit"] = 20  # 街のスクロール枠に読み込む全体ニュース件数
Config["all_message_storage_limit"] = 20  # 全体ニュースファイルに保持する件数
Config["all_message_input_limit"] = (
    500  # 管理画面から投稿できる全体ニュース本文の最大文字数
)
Config["tenka_log_limit"] = 20  # 天下一武道会の制覇履歴表示・保存件数
Config["chocobo_partner_list_limit"] = 100  # お見合い候補として保持する最大件数
Config["character_image_list_label"] = (
    "アイコン一覧"  # キャラクター画像一覧リンクの表示名
)


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
