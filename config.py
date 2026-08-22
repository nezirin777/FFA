"""
FFA (Final Fantasy Adventure) 設定ファイル
"""

import os

Config = {}

# ==========================================
# 1. システム・ディレクトリ設定 (System & Directories)
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Config["save_dir"] = os.path.join(BASE_DIR, "save_data")  # ユーザーデータの保存先
Config["lock_dir"] = os.path.join(BASE_DIR, "lock")  # 排他制御用ロックディレクトリ
Config["template_dir"] = os.path.join(
    BASE_DIR, "templates"
)  # HTMLテンプレートディレクトリ

# 管理者パスワード・秘密鍵は環境変数から取得することを推奨（本番では必ず設定すること）。
# 環境変数が未設定の場合は下記の既定値にフォールバックする（開発用。公開運用では変更必須）。
Config["admin_password"] = os.environ.get(
    "FFA_ADMIN_PASSWORD", "1111"
)  # 管理者用パスワード
Config["secret_key"] = os.environ.get(
    "FFA_SECRET_KEY", "ffa_secret_key_vips_ver3"
)  # クッキー暗号化・署名用の秘密鍵
Config["maintenance_mode"] = 0  # メンテナンスモード (1: 有効, 0: 無効)
Config["delete_limit_days"] = 60  # 未戦闘によるキャラクター自動削除の制限日数 (日)
Config["single_account_per_host"] = (
    True  # 同一IP/ホストからの複数キャラクター登録を禁止する
)
Config["single_account_exempt_ids"] = ["test"]  # 同一IPチェックの対象外にする特殊ID
# テスト・検証用として自動削除と通常の管理画面削除から保護するID
Config["protected_user_ids"] = ["test"]
Config["protected_user_backup_dir"] = os.path.join(
    Config["save_dir"], "protected_users"
)
Config["active_time"] = 120  # アクティブプレイヤーとしてみなす判定秒数
# チャンプデータはプレイ中に更新されるセーブデータとして保存する。
Config["winner_file"] = os.path.join(Config["save_dir"], "winner.json")


# ==========================================
# 2. セッション & セキュリティ設定 (Session & Security)
# ==========================================
Config["cookie_name"] = "FFAPYCOOKIE"  # ログインID記憶用などのレガシーCookie名
Config["session_expiry"] = 1800  # 暗号化セッション(FFAPY_SESSION)の有効期限 (秒: 30分)

# ==========================================
# 3. ゲームルール・数値設計 (Game Balance & Limits)
# ==========================================
Config["max_level"] = 99999  # キャラクターの最大レベル
Config["max_hp"] = 99999999  # キャラクターの最大HP
Config["max_param"] = 99999  # 力・知能などの最大能力値
Config["max_gold"] = 999999999999  # 所持金の最大値
Config["max_bank"] = 999999999999000  # 銀行預金の最大値

Config["inn_cost"] = 10  # 宿屋の宿泊費の基本係数 (レベル乗算用)
Config["prize_money"] = 500  # 対戦で得られる賞金の基本額
Config["base_exp"] = 30  # 戦闘で得られる基本経験値
Config["level_up_coeff"] = 300  # レベルアップに必要な経験値の係数 (レベル乗算用)

Config["battle_cooldown"] = 20  # 通常対戦(対人)のクールダウン秒数
Config["monster_cooldown"] = 20  # モンスター修行のクールダウン秒数
Config["boss_cooldown"] = 10  # ボス戦のクールダウン秒数

Config["battle_limit"] = 9999  # 1日の最大対戦回数制限
Config["max_turns"] = 150  # 1戦闘における最大ターン数 (引き分け判定用)
# 旧版 wbattle.pl の初手逆転必殺判定
Config["level_sa"] = 15
Config["gyakuten"] = 100
Config["master_tac_limit"] = 1  # 転職後の戦術（タクティクス）クリア設定 (1: クリアする)
Config["tenka_count"] = 3  # 天下一武道会の最大対戦数

# ==========================================
# 4. 表示・デザイン設定 (Aesthetics & CSS)
# ==========================================

# ヘルプ関連
Config["help_text"] = "html/manual.html"  # ヘルプ(遊び方マニュアル)のパス
Config["help_text_url"] = "プレイマニュアル"  # ヘルプリンクの表示文字列

Config["main_title"] = "FFA改 Vips Ver 3.00"  # ゲームのメインタイトル

# テンプレート互換用スクリプトエイリアス
Config["script"] = "login.py"
Config["script_pass"] = "login.py?mode=passchange"
Config["script_select"] = "login.py?mode=select_battle"
Config["scripto"] = "others.py"


# ==========================================
# 5. メッセージ・お知らせ設定 (Notices & Messages)
# ==========================================
Config["telop_message"] = (
    "<font color=yellow>ごゆっくりお楽しみください</font>管理人より♪"  # 画面上部テロップメッセージ
)
Config["admin_message"] = (  # 公開トップの管理者お知らせ事項 (HTML)
    "<font color=red>\n"
    "・１人で２人以上のキャラクターの登録を禁止します。<br>\n"
    "・ブラウザの更新ボタン等を押すことを禁止します。<br>\n"
    "・上記に該当するキャラクターは連絡等をなしに管理人の独断により削除することがあります。</font><br>"
)
Config["ban_words"] = [
    "あほ",
    "馬鹿",
    "SEX",
    "ダイヤルQ2",
    "キチガイ",
    "ウンコ",
    "チンポ",
]  # 禁止ワードリスト

# ==========================================
# 6. スクリプト・URLルーティング (Scripts & Routing)
# ==========================================
# メイン・システム
Config["login_script"] = "login.py"
Config["chara_make_script"] = "chara_make.py"
Config["admin_script"] = "admin.py"
Config["others_script"] = "others.py"

# プレイヤー画面・設定
Config["main_script"] = "login.py?mode=main"
Config["status_script"] = "login.py?mode=sts"
Config["tactics_script"] = "login.py?mode=tac_change"
Config["passchange_script"] = "login.py?mode=passchange"
Config["tensyoku_script"] = "login.py?mode=tensyoku"
Config["system_script"] = (
    "login.py"  # 共通サブ画面エントリ (後方に?mode=ranking等を動的付与)
)

# ショップ・施設
Config["shop_item_script"] = "login.py?mode=shop_item"
Config["shop_def_script"] = "login.py?mode=shop_def"
Config["shop_acs_script"] = "login.py?mode=shop_acs"
Config["bank_script"] = "login.py?mode=bank"
Config["souko_script"] = "login.py?mode=souko"

# 戦闘・修行
Config["select_battle_script"] = "login.py?mode=select_battle"
Config["battle_script"] = "login.py?mode=battle"
Config["monster_script"] = "login.py?mode=monster"
Config["legend_script"] = "login.py?mode=legend"

# チョコボ・育成
Config["chocofarm_script"] = "login.py?mode=chocofarm"
Config["mori_farm_script"] = "login.py?mode=morifarm"
Config["crace_script"] = "login.py?mode=crace"
Config["ctrain_script"] = "login.py?mode=ctrain"
Config["dendo_script"] = "login.py?mode=dendo"
Config["chocorank_script"] = "login.py?mode=chocorank"
Config["farmrace_script"] = "login.py?mode=farmrace"

# コミュニケーション・ランキング
Config["bbs_script"] = "login.py?mode=bbs"  # プレイヤー掲示板
Config["max_bbs_posts"] = 50  # 掲示板に保持する最大投稿数
Config["ranking_script"] = "login.py?mode=rank"
Config["img_all_list"] = "login.py?mode=img_list"

# 天下一武道会
Config["tenka_script"] = "login.py?mode=tenka"

# ==========================================
# 7. 外部掲示板・投票リンク設定 (External BBS & Votes)
# ==========================================
Config["vote_image"] = "アイコン一覧"

# ==========================================
# 8. マスタデータ・定義ファイル設定 (Master Data Files)
# ==========================================
Config["syoku_file"] = "data/syoku.json"  # 職業マスタデータファイル
Config["tac_file"] = "data/tac.json"  # 全戦術マスター（職業別使用条件はjob_idsで管理）

# ショップ商品マスタ
Config["weapon_file"] = "data/weapon.json"  # 武器マスタ
Config["max_weapons"] = 8

Config["armor_file"] = "data/armor.json"  # 防具マスタ
Config["max_armors"] = 8

Config["accessory_file"] = "data/accessory.json"  # 装飾品マスタ
Config["hint_file"] = "data/hint.json"  # チョコボ牧場のヒントマスター
Config["chocobo_file"] = "data/chocobo/chocobofile.json"  # 野生チョコボのマスターデータ
Config["chocobo_data_dir"] = "data/chocobo"  # チョコボ関連マスターデータの保存先
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
}  # チョコボレースのライバルマスター
Config["max_accessories"] = 8

# モンスター・ボス出現マスタ
Config["monster_lv1_file"] = "data/monsters/mons_lv1.json"  # 初級モンスター
Config["monster_lv2_file"] = "data/monsters/mons_lv2.json"  # 中級モンスター
Config["monster_lv3_file"] = "data/monsters/mons_lv3.json"  # 上級モンスター
Config["monster_lv4_file"] = "data/monsters/mons_lv4.json"  # 最上級モンスター

Config["isekai_file"] = "data/monsters/mons_isekai.json"  # 異世界モンスター
Config["isekai_level"] = 300  # 異世界侵入の制限レベル

Config["legend_boss_lv1_file"] = "data/monsters/legend_boss_lv1.json"  # 伝説の地ボス・レベル1
Config["legend_boss_lv2_file"] = "data/monsters/legend_boss_lv2.json"  # 伝説の地ボス・レベル2
Config["legend_boss_lv3_file"] = "data/monsters/legend_boss_lv3.json"  # 伝説の地ボス・レベル3
Config["legend_boss_lv4_file"] = "data/monsters/legend_boss_lv4.json"  # 伝説の地ボス・レベル4
Config["legend_battle_media"] = {
    "final": {
        "background": "images/last_boss_back.gif",
        "midi": "data/last_boss.mid",
    },
    "high": {
        "background": "images/boss_back.gif",
        "midi": "data/boss1.mid",
    },
    "normal": {
        "background": "images/boss2_back.gif",
        "midi": "data/boss2.mid",
    },
}  # 伝説の戦いの背景・BGM

# ==========================================
# 9. リスト・ゲームマスタ定義 (Assets & Game Masters)
# ==========================================
# キャラクター立ち絵リスト（保存済みの画像番号を変更しない）
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
    # 追加画像は既存番号を崩さないよう末尾へ追加する。
    97: "chop.gif", 98: "gf-efreet.gif", 99: "gf-karban.gif", 100: "gf-leviathan.gif",
    101: "gf-siren.gif", 102: "ikon_m_c.gif", 103: "ikon_m_e.gif", 104: "ikon_m_f.gif",
    105: "ikon_m_g.gif", 106: "ikon_m_m.gif", 107: "ikon_m_q.gif", 108: "ikon_m_sa.gif",
    109: "ikon_m_st.gif", 110: "ikon_m_v.gif", 111: "ikon_m_z.gif",
}

# チョコボアイコン・アセット
Config["choco_images"] = {
    0: "cho-ml.gif", 1: "cho-gl.gif", 2: "cho-yl.gif", 3: "cho-kl.gif",
    4: "cho-bl.gif", 5: "cho-wl.gif", 6: "cho-rl.gif", 7: "cho-pl.gif",
}
Config["chocobo_types"] = {
    0: "普通", 1: "早熟", 2: "晩成", 3: "持続", 4: "超晩成", 5: "超早熟",
}
Config["img_farm"] = "images/chara/choco"
Config["img_path"] = "images/chara"
Config["farm_back"] = "images/farm.jpg"
Config["crace_back"] = "images/farm.jpg"


# レベル進行段階・タイトル・職業一覧
Config["titles"] = {
    0: "駆け出し", 1: "プチ", 2: "超", 3: "極", 4: "超極の殿堂",
}
Config["chara_jobs"] = {
    0: "見習い戦士", 1: "戦士", 2: "ナイト", 3: "シーフ",
    4: "竜騎士", 5: "赤魔道士", 6: "バード", 7: "忍者",
    8: "召喚士", 9: "ビショップ", 10: "聖騎士", 11: "モンク",
    12: "暗黒騎士", 13: "魔人", 14: "蒼魔道士", 15: "時魔道士",
    16: "マシーナリー", 17: "グラディエーター", 18: "学者", 19: "バーサーカー",
    20: "風水士", 21: "召喚術士", 22: "管理者", 23: "ものまね士",
    24: "アニマルテイマー", 25: "アサシン", 26: "剣聖", 27: "バトルマスター",
    28: "ホーリーナイト", 29: "歌姫", 30: "ナイトメアマイスター",
}
Config["initial_job_ids"] = (0, 1, 2, 3)  # キャラ作成時に選択できる初期職業
Config["jobs_html_path"] = (
    "html/manual.html#jobs"  # 職業説明(統合マニュアルの職業セクションへ)
)

# 幻影闘技場レベル制限
Config["genei_level_low"] = 100
Config["genei_level_high"] = 500
Config["genei_level_max"] = 1000

# メッセージログ表示限界数・その他
Config["max_lines"] = 20
Config["max_all_messages"] = 20
Config["max_choco_partner_list"] = 100  # お見合い候補リストの最大件数

# Mapped aliases for compatibility with legacy templates
Config["chara_syoku"] = Config["chara_jobs"]
Config["chara_img"] = Config["chara_images"]


def _validate_id_maps():
    """番号付きマスターが誤って配列へ戻らないよう起動時に検証します。"""
    id_maps = (
        "chara_images",
        "choco_images",
        "chocobo_types",
        "titles",
        "chara_jobs",
    )
    for map_name in id_maps:
        values = Config[map_name]
        if not isinstance(values, dict) or any(not isinstance(key, int) for key in values):
            raise ValueError(f"{map_name} は整数IDをキーにした辞書で定義してください")

    if not set(Config["initial_job_ids"]).issubset(Config["chara_jobs"]):
        raise ValueError("initial_job_ids に未定義の職業IDが含まれています")


_validate_id_maps()
