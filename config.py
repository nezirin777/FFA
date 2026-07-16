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
Config["souko_folder"] = "save_data"  # 倉庫データディレクトリの相対パス

Config["admin_password"] = "1111"  # 管理者用パスワード
Config["secret_key"] = "ffa_secret_key_vips_ver3"  # クッキー暗号化・署名用の秘密鍵
Config["maintenance_mode"] = 0  # メンテナンスモード (1: 有効, 0: 無効)
Config["delete_limit_days"] = 60  # 未戦闘によるキャラクター自動削除の制限日数 (日)
Config["active_time"] = 120  # アクティブプレイヤーとしてみなす判定秒数


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
Config["max_param"] = 99999  # 力・魔力などの最大能力値
Config["max_gold"] = 999999999999  # 所持金の最大値
Config["max_bank"] = 999999999999000  # 銀行預金の最大値

Config["inn_cost"] = 10  # 宿屋の宿泊費の基本係数 (レベル乗算用)
Config["prize_money"] = 500  # 対戦で得られる賞金の基本額
Config["base_exp"] = 30  # 戦闘で得られる基本経験値
Config["base_hp"] = 500  # キャラクター作成時の初期HP
Config["level_up_coeff"] = 300  # レベルアップに必要な経験値の係数 (レベル乗算用)

Config["battle_cooldown"] = 30  # 通常対戦(対人)のクールダウン秒数
Config["monster_cooldown"] = 30  # モンスター修行のクールダウン秒数
Config["boss_cooldown"] = 10  # ボス戦のクールダウン秒数

Config["level_diff_limit"] = 15  # 通常戦闘で対戦相手を選べるレベル差制限
Config["battle_limit"] = 9999  # 1日の最大対戦回数制限
Config["max_turns"] = 150  # 1戦闘における最大ターン数 (引き分け判定用)
Config["master_tac_limit"] = 1  # 転職後の戦術（タクティクス）クリア設定 (1: クリアする)
Config["tenka_count"] = 3  # 天下一武道会の最大対戦数

# ==========================================
# 4. 表示・デザイン設定 (Aesthetics & CSS)
# ==========================================

# ヘルプ関連
Config["help_text"] = "html/ffhelp.html"  # ヘルプファイルのパス
Config["help_text_url"] = "ヘルプ"  # ヘルプリンクの表示文字列

Config["main_title"] = "FFA改 Vips Ver 3.00"  # ゲームのメインタイトル

# テンプレート互換用スクリプトエイリアス
Config["script"] = "login.py"
Config["script_pass"] = "login.py?mode=passchange"
Config["script_post"] = "login.py?mode=post_message"
Config["script_select"] = "login.py?mode=select_battle"
Config["scripto"] = "others.py"



# ==========================================
# 5. メッセージ・お知らせ設定 (Notices & Messages)
# ==========================================
Config["telop_message"] = (
    "<font color=yellow>ごゆっくりお楽しみください</font>管理人より♪"  # 画面上部テロップメッセージ
)
Config["admin_message"] = (  # ログイン画面の管理者お知らせ事項 (HTML)
    "<font color=red>\n"
    "・１人で２人以上のキャラクターの登録を禁止します。<br>\n"
    "・違法サイトのＵＲＬのキャラクターの登録は禁止します。<br>\n"
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
Config["post_message_script"] = "login.py?mode=post_message"
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
Config["winner_file"] = "data/winner.json"  # 王者（チャンプ）データファイル
Config["syoku_file"] = "data/syoku.json"  # 職業マスタデータファイル
Config["tac_file"] = "data/tac/tac.json"  # 戦術マスタデータファイル
Config["tac_folder"] = "data/tac"  # 戦術データフォルダ

# ショップ商品マスタ
Config["item_file"] = "data/item/item.json"  # 武器マスタ
Config["item_folder"] = "data/item"
Config["max_items"] = 8

Config["def_file"] = "data/def/def.json"  # 防具マスタ
Config["def_folder"] = "data/def"
Config["max_defenses"] = 8

Config["acs_file"] = "data/acs/acs.json"  # 装飾品マスタ
Config["acs_folder"] = "data/acs"
Config["max_accessories"] = 8

# モンスター・ボス出現マスタ
Config["monster0_file"] = "data/lowmons.json"  # 初級モンスター
Config["monster1_file"] = "data/normalmons.json"  # 中級モンスター
Config["monster2_file"] = (
    "data/highmons.json"  # 上級モンスター (※現在高難易度用で未使用)
)
Config["monster3_file"] = "data/spmons.json"  # 特殊モンスター

Config["isekai_file"] = "data/isekaimons.json"  # 異世界モンスター
Config["isekai_level"] = 300  # 異世界侵入の制限レベル

Config["boss0_file"] = "data/bossmons0.json"  # 伝説の地ボス層0
Config["boss1_file"] = "data/bossmons1.json"  # 伝説の地ボス層1
Config["boss2_file"] = "data/bossmons2.json"  # 伝説の地ボス層2
Config["boss3_file"] = "data/bossmons3.json"  # 伝説の地ボス層3

# ==========================================
# 9. リスト・ゲームマスタ定義 (Assets & Game Masters)
# ==========================================
# キャラクター立ち絵リスト
Config["chara_images"] = [
    "ana.gif",
    "arce.gif",
    "arlon.gif",
    "balt.gif",
    "bea.gif",
    "bellmayl.gif",
    "c_zoro.gif",
    "corza.gif",
    "dr_kureha.gif",
    "elly.gif",
    "emerada.gif",
    "fei.gif",
    "karuu.gif",
    "kuina.gif",
    "kuro.gif",
    "kurokoda.gif",
    "kuzya.gif",
    "maru.gif",
    "meso-s.gif",
    "mini-aerith.gif",
    "mini-auron.gif",
    "mini-baku.gif",
    "mini-barret.gif",
    "mini-blank.gif",
    "mini-braska.gif",
    "mini-buricid.gif",
    "mini-cait.gif",
    "mini-cid.gif",
    "mini-cid10.gif",
    "mini-cid7.gif",
    "mini-cinna.gif",
    "mini-cloud.gif",
    "mini-edea.gif",
    "mini-eiko.gif",
    "mini-el.gif",
    "mini-ff9-01.gif",
    "mini-ff9-02.gif",
    "mini-ff9-03.gif",
    "mini-ff9-04.gif",
    "mini-ff9-05.gif",
    "mini-ff9-06.gif",
    "mini-ff9-07.gif",
    "mini-flatley.gif",
    "mini-freija.gif",
    "mini-fuujin.gif",
    "mini-garnet.gif",
    "mini-jecht.gif",
    "mini-kerocid.gif",
    "mini-kimari.gif",
    "mini-kiros.gif",
    "mini-laguna.gif",
    "mini-lani.gif",
    "mini-lulu.gif",
    "mini-marcus.gif",
    "mini-mikoto.gif",
    "mini-quina.gif",
    "mini-quistis.gif",
    "mini-raijin.gif",
    "mini-red.gif",
    "mini-rikku.gif",
    "mini-rinoa.gif",
    "mini-ruby.gif",
    "mini-salamander.gif",
    "mini-seif.gif",
    "mini-selphie.gif",
    "mini-sephi.gif",
    "mini-seymore.gif",
    "mini-shelinda.gif",
    "mini-squall.gif",
    "mini-steiner.gif",
    "mini-tidus.gif",
    "mini-tifa.gif",
    "mini-vin.gif",
    "mini-vivi.gif",
    "mini-wakka.gif",
    "mini-ward.gif",
    "mini-yuffie.gif",
    "mini-yuna.gif",
    "mini-yunalesca.gif",
    "mini-zell.gif",
    "mini-zidane.gif",
    "mog.gif",
    "mr2.gif",
    "ms_gw.gif",
    "munba.gif",
    "nami.gif",
    "pel.gif",
    "rufi.gif",
    "sanji.gif",
    "sarama.gif",
    "shitan.gif",
    "smoker.gif",
    "syancs.gif",
    "tashi.gif",
    "usausa.gif",
    "vivi.gif",
    "zoro.gif",
    # --- 追加キャラアイコン (既存のimg indexを崩さないよう末尾に追加) ---
    "chop.gif",
    "gf-efreet.gif",
    "gf-karban.gif",
    "gf-leviathan.gif",
    "gf-siren.gif",
    "ikon_m_c.gif",
    "ikon_m_e.gif",
    "ikon_m_f.gif",
    "ikon_m_g.gif",
    "ikon_m_m.gif",
    "ikon_m_q.gif",
    "ikon_m_sa.gif",
    "ikon_m_st.gif",
    "ikon_m_v.gif",
    "ikon_m_z.gif",
]

# チョコボアイコン・アセット
Config["choco_images"] = [
    "cho-ml.gif",
    "cho-gl.gif",
    "cho-yl.gif",
    "cho-kl.gif",
    "cho-bl.gif",
    "cho-wl.gif",
    "cho-rl.gif",
    "cho-pl.gif",
]
Config["img_farm"] = "images/chara/choco"
Config["img_path"] = "images/chara"
Config["farm_back"] = "images/farm.jpg"
Config["crace_back"] = "images/farm.jpg"


# レベル進行段階・タイトル・職業一覧
Config["titles"] = ["駆け出し", "プチ", "超", "極", "超極の殿堂"]
Config["chara_jobs"] = [
    "見習い戦士",
    "戦士",
    "ナイト",
    "シーフ",
    "竜騎士",
    "赤魔道士",
    "バード",
    "忍者",
    "召喚士",
    "ビショップ",
    "聖騎士",
    "モンク",
    "暗黒騎士",
    "魔人",
    "蒼魔道士",
    "時魔道士",
    "マシーナリー",
    "グラディエーター",
    "学者",
    "バーサーカー",
    "風水士",
    "召喚術士",
    "管理者",
    "ものまね士",
    "アニマルテイマー",
    "アサシン",
    "剣聖",
    "バトルマスター",
    "ホーリーナイト",
    "歌姫",
    "ナイトメアマイスター",
]
Config["jobs_html_path"] = "html/syokugyou.html"

# 幻影闘技場レベル制限
Config["genei_level_low"] = 100
Config["genei_level_high"] = 500
Config["genei_level_max"] = 1000

# メッセージログ表示限界数・その他
Config["max_lines"] = 5
Config["max_messages"] = 20
Config["max_all_lines"] = 5
Config["max_all_messages"] = 20
Config["comeback_factor"] = 100
Config["all_data_file"] = "alldata.json"

# Mapped aliases for compatibility with legacy templates
Config["chara_syoku"] = Config["chara_jobs"]
Config["chara_img"] = Config["chara_images"]

