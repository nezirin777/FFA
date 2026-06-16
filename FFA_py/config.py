"""
FFA (Final Fantasy Adventure) 設定ファイル
"""
import os

Config = {}

# === 1. 移行した共通設定 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Config['save_dir'] = os.path.join(BASE_DIR, "save_data")
Config['lock_dir'] = os.path.join(BASE_DIR, "lock")
Config['template_dir'] = os.path.join(BASE_DIR, "templates")
Config['admin_password'] = '1111'
Config['secret_key'] = 'ffa_secret_key_vips_ver3'

# === 2. 既存の設定 ===
Config['acs_file'] = 'data/acs/acs.ini'
Config['acs_folder'] = 'data/acs'
Config['max_accessories'] = 8
Config['shop_acs_script'] = 'login.py?mode=shop_acs'
Config['alink_color'] = '#ff5500'
Config['all_data_file'] = 'alldata.json'
Config['max_all_lines'] = 5
Config['max_all_messages'] = 20
Config['all_tenka_script'] = 'all_tenka.py'
Config['body_size'] = '100%'
Config['battle_cooldown'] = 30
Config['bg_gif'] = ''
Config['ban_words'] = ['あほ', '馬鹿', 'SEX', 'ダイヤルQ2', 'キチガイ', 'ウンコ', 'チンポ']
Config['max_bank'] = 999999999999000
Config['bbs_url'] = 'http://localhost:8000'
Config['bbs_title'] = '掲示板'
Config['bg_color'] = '#0b0b14'
Config['color_blue'] = '#60a5fa'
Config['boss_cooldown'] = 10
Config['boss0_file'] = 'data/bossmons0.ini'
Config['boss1_file'] = 'data/bossmons1.ini'
Config['boss2_file'] = 'data/bossmons2.ini'
Config['boss3_file'] = 'data/bossmons3.ini'
Config['chara_images'] = ['ana.gif', 'arce.gif', 'arlon.gif', 'balt.gif', 'bea.gif', 'bellmayl.gif', 'c_zoro.gif', 'corza.gif', 'dr_kureha.gif', 'elly.gif', 'emerada.gif', 'fei.gif', 'karuu.gif', 'kuina.gif', 'kuro.gif', 'kurokoda.gif', 'kuzya.gif', 'maru.gif', 'meso-s.gif', 'mini-aerith.gif', 'mini-auron.gif', 'mini-baku.gif', 'mini-barret.gif', 'mini-blank.gif', 'mini-braska.gif', 'mini-buricid.gif', 'mini-cait.gif', 'mini-cid.gif', 'mini-cid10.gif', 'mini-cid7.gif', 'mini-cinna.gif', 'mini-cloud.gif', 'mini-edea.gif', 'mini-eiko.gif', 'mini-el.gif', 'mini-ff9-01.gif', 'mini-ff9-02.gif', 'mini-ff9-03.gif', 'mini-ff9-04.gif', 'mini-ff9-05.gif', 'mini-ff9-06.gif', 'mini-ff9-07.gif', 'mini-flatley.gif', 'mini-freija.gif', 'mini-fuujin.gif', 'mini-garnet.gif', 'mini-jecht.gif', 'mini-kerocid.gif', 'mini-kimari.gif', 'mini-kiros.gif', 'mini-laguna.gif', 'mini-lani.gif', 'mini-lulu.gif', 'mini-marcus.gif', 'mini-mikoto.gif', 'mini-quina.gif', 'mini-quistis.gif', 'mini-raijin.gif', 'mini-red.gif', 'mini-rikku.gif', 'mini-rinoa.gif', 'mini-ruby.gif', 'mini-salamander.gif', 'mini-seif.gif', 'mini-selphie.gif', 'mini-sephi.gif', 'mini-seymore.gif', 'mini-shelinda.gif', 'mini-squall.gif', 'mini-steiner.gif', 'mini-tidus.gif', 'mini-tifa.gif', 'mini-vin.gif', 'mini-vivi.gif', 'mini-wakka.gif', 'mini-ward.gif', 'mini-yuffie.gif', 'mini-yuna.gif', 'mini-yunalesca.gif', 'mini-zell.gif', 'mini-zidane.gif', 'mog.gif', 'mr2.gif', 'ms_gw.gif', 'munba.gif', 'nami.gif', 'pel.gif', 'rufi.gif', 'sanji.gif', 'sarama.gif', 'shitan.gif', 'smoker.gif', 'syancs.gif', 'tashi.gif', 'usausa.gif', 'vivi.gif', 'zoro.gif']
Config['chara_make_script'] = 'chara_make.py'
Config['chara_jobs'] = ['見習い戦士', '戦士', 'ナイト', 'シーフ', '竜騎士', '赤魔道士', 'バード', '忍者', '召喚士', 'ビショップ', '聖騎士', 'モンク', '暗黒騎士', '魔人', '蒼魔道士', '時魔道士', 'マシーナリー', 'グラディエーター', '学者', 'バーサーカー', '風水士', '召喚術士', '管理者', 'ものまね士', 'アニマルテイマー', 'アサシン', '剣聖', 'バトルマスター', 'ホーリーナイト', '歌姫', 'ナイトメアマイスター']
Config['max_hp'] = 99999999
Config['max_level'] = 99999
Config['max_param'] = 99999
Config['choco_images'] = ['cho-ml.gif', 'cho-gl.gif', 'cho-yl.gif', 'cho-kl.gif', 'cho-bl.gif', 'cho-wl.gif', 'cho-rl.gif', 'cho-pl.gif']
Config['choco_css'] = 'html/choco.css'
Config['crace_back'] = 'images/farm.jpg'
Config['color_dark'] = '#1e1b4b'
Config['def_file'] = 'data/def/def.ini'
Config['def_folder'] = 'data/def'
Config['max_defenses'] = 8
Config['shop_def_script'] = 'login.py?mode=shop_def'
Config['farm_back'] = 'images/farm.jpg'
Config['farm_midi'] = ''
Config['cookie_name'] = 'FFAPYCOOKIE'
Config['font_name'] = 'ＭＳ Ｐゴシック'
Config['genei_level_high'] = 500
Config['genei_level_low'] = 100
Config['genei_level_max'] = 1000
Config['max_gold'] = 999999999999
Config['color_green'] = '#34d399'
Config['comeback_factor'] = 100
Config['help_text'] = 'html/ffhelp.html'
Config['help_text_url'] = 'ヘルプ'
Config['img_all_list'] = 'login.py?mode=img_list'  # login.py 経由の画像一覧ルーティングへ統一
Config['img_farm'] = 'images/chara/choco'
Config['img_path'] = 'images/chara'
Config['isekai_level'] = 300
Config['isekai_file'] = 'data/isekaimons.ini'
Config['item_file'] = 'data/item/item.ini'
Config['item_folder'] = 'data/item'
Config['max_items'] = 8
Config['shop_item_script'] = 'login.py?mode=shop_item'
Config['admin_message'] = '<font color=red>\n・１人で２人以上のキャラクターの登録を禁止します。<br>\n・違法サイトのＵＲＬのキャラクターの登録は禁止します。<br>\n・ブラウザの更新ボタン等を押すことを禁止します。<br>\n・上記に該当するキャラクターは連絡等をなしに管理人の独断により削除することがあります。</font><br>'
Config['base_exp'] = 30
Config['base_hp'] = 500
Config['level_diff_limit'] = 15
Config['delete_limit_days'] = 60
Config['link_color'] = '#60a5fa'
Config['login_script'] = 'login.py'
Config['level_up_coeff'] = 300
Config['monster_cooldown'] = 30
Config['main_title'] = 'FFA改 Vips Ver 3.00'
Config['master_tac_limit'] = 1
Config['max_lines'] = 5
Config['maintenance_mode'] = 0
Config['max_messages'] = 20
Config['monster0_file'] = 'data/lowmons.ini'
Config['monster1_file'] = 'data/normalmons.ini'
Config['monster2_file'] = 'data/highmons.ini'
Config['monster3_file'] = 'data/spmons.ini'
Config['ranking_script'] = 'login.py?mode=rank'  # login.py 経由の能力別ランキングルーティングへ統一
Config['color_red'] = '#f87171'
Config['active_time'] = 120
Config['sub_bbs_url'] = ''
Config['sub_bbs_title'] = ''
Config['main_script'] = 'login.py?mode=main'
Config['bank_script'] = 'login.py?mode=bank'
Config['chocofarm_script'] = 'login.py?mode=chocofarm'
Config['crace_script'] = 'login.py?mode=crace'
Config['legend_script'] = 'login.py?mode=legend'
Config['mori_farm_script'] = 'login.py?mode=morifarm'
Config['passchange_script'] = 'login.py?mode=passchange'
Config['post_message_script'] = 'login.py?mode=post_message'
Config['select_battle_script'] = 'login.py?mode=select_battle'
Config['souko_script'] = 'login.py?mode=souko'
Config['tenka_script'] = 'login.py?mode=tenka'
Config['tensyoku_script'] = 'login.py?mode=tensyoku'
Config['system_script'] = 'login.py'  # 多重の?を防ぐため login.py に変更し、呼び出し側で ?mode=ranking 等を追加可能にする
Config['battle_script'] = 'login.py?mode=battle'
Config['admin_script'] = 'admin.py'
Config['monster_script'] = 'login.py?mode=monster'
Config['others_script'] = 'others.py'
Config['tactics_script'] = 'login.py?mode=tac_change'
Config['status_script'] = 'login.py?mode=sts'
Config['shop_script'] = 'login.py?mode=shop'
Config['battle_limit'] = 9999
Config['titles'] = ['駆け出し', 'プチ', '超', '極', '超極の殿堂']
Config['shut_hosts'] = ['999.999.999', '999.999.999', '999.999.999']
Config['souko_folder'] = 'save_data'
Config['syoku_file'] = 'data/syoku.ini'
Config['jobs_html_path'] = 'html/syokugyou.html'
Config['prize_money'] = 500
Config['tac_file'] = 'data/tac/tac.ini'
Config['tac_folder'] = 'data/tac'
Config['telop_message'] = '<font color=yellow>ごゆっくりお楽しみください</font>管理人より♪'
Config['tenka_log_script'] = 'tenka_log.py'
Config['tenka_count'] = 3
Config['text_color'] = '#d1d5db'
Config['max_turns'] = 150
Config['vlink_color'] = '#9ca3af'
Config['vote_url'] = ''
Config['vote_image'] = 'アイコン一覧'
Config['vote_title'] = ''
Config['color_white'] = '#ffffff'
Config['winner_file'] = 'data/winner.ini'
Config['inn_cost'] = 10
Config['color_yellow'] = '#fbbf24'
