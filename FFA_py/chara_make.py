#!D:\Python\Python314\python.exe
# -*- coding: utf-8 -*-
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
FFA Python/CGI - 新規キャラクター登録スクリプト (chara_make.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')
import os
import time
import random

# 共通モジュールと設定モジュールのインポート
import config
import common

def get_all_players():
    """全プレイヤーデータをロードしてリストで返します"""
    players = []
    save_dir = config.Config['save_dir']
    if not os.path.exists(save_dir):
        return players
    for user_id in os.listdir(save_dir):
        user_path = os.path.join(save_dir, user_id)
        if os.path.isdir(user_path):
            chara = common.chara_load(user_id)
            if chara:
                players.append(chara)
    return players

def validate_input(params):
    """入力値のバリデーションを行います。エラーがある場合はエラーメッセージを返します。"""
    user_id = params.get("id", "").strip()
    user_pass = params.get("pass", "").strip()
    passchange = params.get("passchange", "").strip()
    c_name = params.get("c_name", "").strip()
    sex_str = params.get("sex", "").strip()
    syoku_str = params.get("syoku", "").strip()
    
    if not user_id.isalnum():
        return "IDは半角英数字で入力してください。"
    if len(user_id) < 4 or len(user_id) > 8:
        return "IDは4文字以上8文字以下で入力してください。"
        
    if not user_pass.isalnum():
        return "パスワードは半角英数字で入力してください。"
    if len(user_pass) < 4 or len(user_pass) > 8:
        return "パスワードは4文字以上8文字以下で入力してください。"
        
    if not passchange:
        return "パスワード変更用単語が入力されていません。"
    if not c_name:
        return "キャラクターの名前が入力されていません。"
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
        
    # 名前の重複チェック（管理者以外の通常時、config.name_banが有効なら）
    # 通常は重複禁止のためチェックします
    all_players = get_all_players()
    for player in all_players:
        if player["name"] == c_name:
            return "同一名のキャラクターが既に存在します。"
            
    # 同一IPからの重複登録制限 (config.ip_banチェック。今回は簡易的に省略するか、IPのチェックを必要に応じて有効化)
    remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
    # テストアカウント以外で同一IPからの重複登録を禁止する場合
    # for player in all_players:
    #     if player.get("host") == remote_addr and player["id"] != "test":
    #         return "同一IPから登録されたキャラクターが既に存在します。"

    return None

def main():
    # メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    params = common.decode_params()
    mode = params.get("mode", "").strip()
    
    # 登録制限チェック
    # config.chara_stop が 1 の場合は新規登録停止
    chara_stop = getattr(config, "chara_stop", 0)
    if chara_stop:
        common.show_error("現在キャラクターの新規作成は停止しています。")

    # 1. 登録確認画面 (make_pre)
    if mode == "make_pre":
        err = validate_input(params)
        if err:
            common.show_error(err)
            
        site = params.get("site", "").strip() or "オススメのHP"
        url = params.get("url", "").strip() or "http://www.eriicu.com"
        
        # 画像番号のチェック
        chara_img_idx_str = params.get("chara", "").strip()
        try:
            chara_img_idx = int(chara_img_idx_str)
            if chara_img_idx < 0 or chara_img_idx >= len(config.Config['chara_images']):
                chara_img_idx = random.randint(0, len(config.Config['chara_images']) - 1)
        except ValueError:
            chara_img_idx = random.randint(0, len(config.Config['chara_images']) - 1)
            
        context = {
            "in": params,
            "c_name": params.get("c_name", "").strip(),
            "sex": int(params.get("sex", "1")),
            "syoku": int(params.get("syoku", "0")),
            "chara": chara_img_idx,
            "site": site,
            "url": url,
            "passchange": params.get("passchange", "").strip(),
            "intgold": 5000,
            "chara_img_name": config.Config['chara_images'][chara_img_idx]
        }
        common.render_template("chara_make_pre.html", context)
        
    # 2. 登録完了処理 (make_end)
    elif mode == "make_end":
        err = validate_input(params)
        if err:
            common.show_error(err)
            
        user_id = params.get("id", "").strip()
        user_pass = params.get("pass", "").strip()
        passchange = params.get("passchange", "").strip()
        c_name = params.get("c_name", "").strip()
        sex = int(params.get("sex", "1"))
        syoku = int(params.get("syoku", "0"))
        
        site = params.get("site", "").strip() or "オススメのHP"
        url = params.get("url", "").strip() or "http://www.eriicu.com"
        
        chara_img_idx_str = params.get("chara", "").strip()
        try:
            chara_img_idx = int(chara_img_idx_str)
            if chara_img_idx < 0 or chara_img_idx >= len(config.Config['chara_images']):
                chara_img_idx = random.randint(0, len(config.Config['chara_images']) - 1)
        except ValueError:
            chara_img_idx = random.randint(0, len(config.Config['chara_images']) - 1)
            
        # 職業ごとの初期ステータス割り振り
        if syoku == 1: # 戦士
            n_str, n_int, n_dex, n_vit, n_agi, n_mnd, n_lck = 9, 14, 10, 9, 11, 8, 10
            lp = 5
        elif syoku == 2: # ナイト
            n_str, n_int, n_dex, n_vit, n_agi, n_mnd, n_lck = 9, 10, 12, 9, 11, 8, 12
            lp = 5
        elif syoku == 3: # シーフ
            n_str, n_int, n_dex, n_vit, n_agi, n_mnd, n_lck = 11, 8, 8, 11, 13, 8, 12
            lp = 5
        else: # 見習い戦士
            n_str, n_int, n_dex, n_vit, n_agi, n_mnd, n_lck = 13, 8, 8, 13, 11, 10, 8
            lp = 5
            
        now = int(time.time())
        remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
        
        # 1. chara.json 構築
        new_chara = {
            "id": user_id,
            "pass": user_pass,
            "site": site,
            "url": url,
            "name": c_name,
            "sex": sex,
            "img": chara_img_idx,
            "str": n_str,
            "int": n_int,
            "dex": n_dex,
            "vit": n_vit,
            "agi": n_agi,
            "mnd": n_mnd,
            "lck": n_lck,
            "job": syoku,
            "hp": 500,
            "max_hp": 500,
            "exp": 0,
            "level": 1,
            "gold": 5000,
            "lp": lp,
            "unused21": 0,
            "unused22": 0,
            "comment": "よろしくお願いします！",
            "weapon_id": 0,
            "battle_limit": config.Config['battle_limit'],
            "host": remote_addr,
            "last_time": now,
            "boss_flag": config.Config['boss_cooldown'],
            "armor_id": 0,
            "unused30": 0,
            "accessory_id": 0,
            "title": 0,
            "job_level": 1,
            "bank": 0
        }
        
        # 2. item.json 構築 (初期装備)
        new_item = {
            "weapon": {
                "name": "素手",
                "dmg": 0,
                "effect": 0
            },
            "armor": {
                "name": "衣服",
                "def": 0,
                "effect": 0
            },
            "accessory": {
                "name": "なし",
                "effect_id": 0,
                "bonus": {
                    "str": 0, "int": 0, "dex": 0, "vit": 0, "agi": 0, "mnd": 0, "lck": 0, "lp": 0
                },
                "attrib": 0,
                "spare1": 0,
                "spare2": 0,
                "spare3": 0
            }
        }
        
        # 3. syoku.json 構築 (初期熟練度。見習い戦士など初期職業の熟練度を少し上げるなどの処理はないか。Perl版では特になし。)
        new_syoku = {str(i): 0 for i in range(31)}
        
        # パスワード変更用単語（重要データ）の保存。
        # Perlでは password フォルダに {id}.cgi として "pass<>passchange<>date<>host<>" のように保存していました。
        # Python版では `save_data/{user_id}/pass_change.json` にまとめて保存しましょう。
        user_dir = os.path.join(config.Config['save_dir'], user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        pass_change_data = {
            "pass": user_pass,
            "passchange": passchange,
            "created_at": now,
            "host": remote_addr
        }
        with open(os.path.join(user_dir, "pass_change.json"), "w", encoding="utf-8") as f:
            import json
            json.dump(pass_change_data, f, ensure_ascii=False, indent=2)
            
        # ディレクトリロックを取りながら一括保存
        common.save_user_all(user_id, new_chara, new_item, new_syoku)
        
        # 4. 全体システムニュースへの登録
        all_msgs = common.all_message_load()
        new_msg = {
            "id": "system",
            "name": "システム",
            "time": common.get_time_str(now),
            "message": f"{c_name}さんが新たに冒険者として登録されました！皆さんよろしく！",
            "host": "system"
        }
        all_msgs.insert(0, new_msg)
        common.all_message_regist(all_msgs[:config.Config['max_all_messages']])
        
        # 登録完了画面をレンダリング
        context = {
            "chara": new_chara,
            "chara_img_name": config.Config['chara_images'][chara_img_idx],
            "chara_syoku_name": config.Config['chara_jobs'][syoku],
            "passchange": passchange
        }
        common.render_template("chara_make_end.html", context)
        
    # 3. 初期フォーム画面 (表示)
    else:
        # キャラクター画像の選択肢を渡すための情報
        context = {
            "chara_img_list": config.Config['chara_images'],
            "chara_syoku_list": config.Config['chara_jobs'][:4], # 初期職業の4つ (0..3)
            "img_all_list": config.Config['img_all_list'],
            "vote_gazou": config.Config['vote_image']
        }
        common.render_template("chara_make.html", context)

if __name__ == "__main__":
    main()
