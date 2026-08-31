#!D:\Python\Python314\python.exe
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
#    いかなる損害に対して作者は一切の責任を负いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#
"""
FFA Python/CGI - 新規キャラクター登録スクリプト (chara_make.py)
"""

import sys
import os
import time
import random

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
Config = config.Config

def random_asset_id(assets):
    """ID付きアセットから既存の番号をランダムに選びます。"""
    return random.choice(tuple(assets))

def validate_input(params):
    """入力値のバリデーションを行います。エラーがある場合はエラーメッセージを返します。"""
    user_id = params.get("id", "").strip()
    user_pass = params.get("pass", "").strip()
    passchange = params.get("passchange", "").strip()
    c_name = params.get("c_name", "").strip()
    sex_str = params.get("sex", "").strip()
    syoku_str = params.get("syoku", "").strip()
    
    # IDのバリデーション（半角英数字、4〜8文字）
    from sub_def.validation import validate_user_id
    id_err = validate_user_id(user_id)
    if id_err:
        return id_err
        
    # パスワードのバリデーション（4〜8文字の半角英数字・記号）
    from sub_def.validation import validate_game_password
    pass_err = validate_game_password(user_pass)
    if pass_err:
        return pass_err
        
    # キャラクター名のバリデーション（予約語・制御文字・Shift-JIS互換性）
    from sub_def.validation import validate_username
    name_err = validate_username(c_name)
    if name_err:
        return name_err
        
    if not passchange:
        return "パスワード変更用単語が入力されていません。"
    if not sex_str:
        return "性別が選択されていません。"
    if not syoku_str:
        return "初期職業が選択されていません。"
        
    try:
        sex = int(sex_str)
        if sex not in (0, 1):
            return "性別の指定が不正です。"
    except ValueError:
        return "性別の指定が不正です。"
        
    try:
        syoku = int(syoku_str)
        if syoku < 0 or syoku > 3:
            return "職業の指定が不正です。"
    except ValueError:
        return "職業の指定が不正です。"
        
    # IDの重複チェック
    if common.chara_load(user_id) is not None:
        return "そのIDはすでに使用されています。"
        
    # 名前の重複チェック
    all_players = common.get_all_players()
    for player in all_players:
        if player.get("name") == c_name:
            return "同一名のキャラクターが既に存在します。"

    # 同一IP/ホストからの複数登録チェック（旧版互換）
    if Config.get("single_account_per_host", True):
        remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
        exempt_ids = set(Config.get("single_account_exempt_ids", ["test"]))
        for player in all_players:
            if player.get("id") in exempt_ids:
                continue
            if player.get("host") == remote_addr:
                return "同一IPから登録されたキャラクターがすでに存在します。"
            
    return None

def main():
    # メンテナンスチェック
    if Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    params = common.decode_params()
    mode = params.get("mode", "").strip()
    
    # 登録制限チェック
    chara_stop = getattr(config, "chara_stop", 0)
    if chara_stop:
        common.show_error("現在キャラクターの新規作成は停止しています。")

    # セッション/CSRF管理モジュールインポート
    from sub_def.crypto import get_session, save_session, token_generate, token_check, hash_password
    from sub_def.file_ops import save_user_all
    from sub_def.utils import redirect
    
    session = get_session()

    # 1. 登録確認画面 (make_pre)
    if mode == "make_pre":
        # POST / 画面遷移の CSRF トークン検証
        token_check(params, session)
        
        err = validate_input(params)
        if err:
            common.show_error(err)
            
        # 画像番号のチェック
        chara_img_idx_str = params.get("chara", "").strip()
        try:
            chara_img_idx = int(chara_img_idx_str)
            if chara_img_idx not in Config['chara_images']:
                chara_img_idx = random_asset_id(Config['chara_images'])
        except ValueError:
            chara_img_idx = random_asset_id(Config['chara_images'])
            
        # 次の make_end フォーム送信用の新しい CSRF トークン生成
        csrf_token = token_generate(session)
        cookie_header = save_session(session)
        
        context = {
            "csrf_token": csrf_token,
            "in": params,
            "c_name": params.get("c_name", "").strip(),
            "sex": int(params.get("sex", "1")),
            "syoku": int(params.get("syoku", "0")),
            "chara": chara_img_idx,
            "passchange": params.get("passchange", "").strip(),
            "intgold": 5000,
            "chara_img_name": Config['chara_images'][chara_img_idx]
        }
        common.render_template("chara_make_pre.html", context, extra_headers=[cookie_header])
        
    # 2. 登録完了処理 (make_end)
    elif mode == "make_end":
        # POST 送信の CSRF トークン検証
        token_check(params, session)
        
        err = validate_input(params)
        if err:
            common.show_error(err)
            
        user_id = params.get("id", "").strip()
        user_pass = params.get("pass", "").strip()
        passchange = params.get("passchange", "").strip()
        c_name = params.get("c_name", "").strip()
        sex = int(params.get("sex", "1"))
        syoku = int(params.get("syoku", "0"))
        
        chara_img_idx_str = params.get("chara", "").strip()
        try:
            chara_img_idx = int(chara_img_idx_str)
            if chara_img_idx not in Config['chara_images']:
                chara_img_idx = random_asset_id(Config['chara_images'])
        except ValueError:
            chara_img_idx = random_asset_id(Config['chara_images'])
            
        # 職業ごとの初期ステータス割り振り
        if syoku == 1: # 黒魔道士
            n_str, n_int, n_mnd, n_vit, n_dex, n_agi, n_cha = 9, 14, 10, 9, 11, 8, 10
            karma = 5
        elif syoku == 2: # 白魔道士
            n_str, n_int, n_mnd, n_vit, n_dex, n_agi, n_cha = 9, 10, 12, 9, 11, 8, 12
            karma = 5
        elif syoku == 3: # シーフ
            n_str, n_int, n_mnd, n_vit, n_dex, n_agi, n_cha = 11, 8, 8, 11, 13, 8, 12
            karma = 5
        else: # ソルジャー
            n_str, n_int, n_mnd, n_vit, n_dex, n_agi, n_cha = 13, 8, 8, 13, 11, 10, 8
            karma = 5
            
        now = int(time.time())
        remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
        
        # セキュリティ向上のため、パスワードを PBKDF2 ハッシュ化して保存
        hashed_pass = hash_password(user_pass)
        
        # 1. chara データ構築
        new_chara = {
            "id": user_id,
            "pass": hashed_pass,
            "name": c_name,
            "img": chara_img_idx,
            "sex": sex,
            "level": 1,
            "max_hp": 500,
            "hp": 500,
            "str": n_str,
            "int": n_int,
            "mnd": n_mnd,
            "vit": n_vit,
            "dex": n_dex,
            "agi": n_agi,
            "cha": n_cha,
            "karma": karma,
            "job": syoku,
            "job_level": 1,
            "exp": 0,
            "gold": 5000,
            "bank": 0,
            "weapon_id": 0,
            "armor_id": 0,
            "accessory_id": 0,
            "battle_count": 0,
            "win_count": 0,
            "battle_limit": Config['training_battle_limit'],
            "boss_flag": Config['legend_progress_reset_value'],
            "comment": "よろしくお願いします！",
            "host": remote_addr,
            "last_time": now,
            "title_id": 0,
            "tactic_id": 0,
        }
        
        # 2. item データ構築
        new_item = {
            "weapon": {
                "name": "素手",
                "atk": 0,
                "hit_rate": 0
            },
            "armor": {
                "name": "衣服",
                "defense": 0,
                "evasion_rate": 0
            },
            "accessory": {
                "name": "なし",
                "effect_id": 0,
                "bonus": {
                    "str": 0, "int": 0, "mnd": 0, "vit": 0, "dex": 0, "agi": 0, "cha": 0, "karma": 0
                },
                "hit_rate": 0,
                "evasion_rate": 0,
                "special_rate": 0,
                "description": ""
            }
        }
        
        # 3. syoku データ構築
        new_syoku = {str(i): 0 for i in range(31)}
        
        # 4. パスワード変更用単語の保存内容を準備する。
        # 実際の保存はID・名前・ホストの再確認と同じ排他区間で行う。
        pass_change_data = {
            "pass": hashed_pass,
            "passchange": passchange,
            "created_at": now,
            "host": remote_addr
        }
            
        # user_all.json 統合データ辞書の一本化構造の組み立てとアトミック保存
        user_data = {
            "chara": new_chara,
            "equipment": new_item,
            "syoku": new_syoku,
            "login_log": [],
            "souko_weapon": [],
            "souko_armor": [],
            "souko_accessory": [],
            "choco": {},
            "choco_g1": {},
            "choco_race_history": [],
        }
        # 確認画面を複数タブで送信された場合でも、チェック直後の登録まで
        # 直列化して同一ID・同一名・同一ホストの競合登録を防ぐ。
        registration_error = None
        common.get_lock("character_creation")
        try:
            registration_error = validate_input(params)
            if registration_error is None:
                user_dir = os.path.join(Config['save_dir'], user_id)
                os.makedirs(user_dir, exist_ok=True)

                from sub_def.file_ops import save_data_atomically
                save_data_atomically(
                    pass_change_data,
                    os.path.join(user_dir, "pass_change.json"),
                    f"pass_change_{user_id}",
                )

                save_user_all(user_id, user_data)
        finally:
            common.release_lock("character_creation")

        if registration_error:
            common.show_error(registration_error)
        
        # 5. 全体システムニュースへの登録。
        # キャラ作成が同時に行われても、既存ニュースを取りこぼさないよう共有ロックを使う。
        common.get_lock("all_message_post")
        try:
            all_msgs = common.all_message_load()
            new_msg = {
                "id": "system",
                "name": "システム",
                "time": common.get_time_str(now),
                "message": f"{c_name}さんが新たに冒険者として登録されました！皆さんよろしく！",
                "host": "system"
            }
            all_msgs.insert(0, new_msg)
            common.all_message_regist(all_msgs[:Config['all_message_storage_limit']])
        finally:
            common.release_lock("all_message_post")
        
        # 登録完了時、自動的に暗号化セッションを発行してメイン画面へダイレクトログイン (F5多重送信防止)
        session_data = {
            "user_id": user_id,
            "password_hash": hashed_pass,
            "csrf_token": session.get("csrf_token")
        }
        cookie_header = save_session(session_data)
        redirect("login.py?mode=main", extra_headers=[cookie_header])
        
    # 3. 初期フォーム画面 (表示)
    else:
        csrf_token = token_generate(session)
        cookie_header = save_session(session)

        # 確認画面の「修正する」から戻った場合は、パスワード以外の入力を
        # 再表示する。パスワードはHTMLへ戻さず、利用者に再入力させる。
        selected_sex = params.get("sex", "1").strip()
        if selected_sex not in ("0", "1"):
            selected_sex = "1"
        selected_job = params.get("syoku", "0").strip()
        if selected_job not in {str(job_id) for job_id in Config["initial_job_ids"]}:
            selected_job = "0"
        
        context = {
            "csrf_token": csrf_token,
            "chara_img_list": [
                {"id": image_id, "file": image_file}
                for image_id, image_file in Config['chara_images'].items()
            ],
            "chara_syoku_list": [
                {"id": job_id, "name": Config['chara_jobs'][job_id]}
                for job_id in Config['initial_job_ids']
            ],
            "character_image_list_url": Config['character_image_list_script'],
            "character_image_list_label": Config['character_image_list_label'],
            "form_values": {
                "id": params.get("id", "").strip(),
                "passchange": params.get("passchange", "").strip(),
                "c_name": params.get("c_name", "").strip(),
                "sex": selected_sex,
                "chara": params.get("chara", "").strip(),
                "syoku": selected_job,
            },
        }
        common.render_template("chara_make.html", context, extra_headers=[cookie_header])

if __name__ == "__main__":
    main()
