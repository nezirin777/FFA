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
FFA Python/CGI - メッセージ送受信（郵便局）スクリプト (post_message.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')
import os
import time

# 共通モジュールと設定モジュールのインポート
import config
import common

# リスト設定モードの判定用定数 (O(1) メンバーシップテスト用、線形探索を回避して高速化)
_POST_MODES: frozenset[str] = frozenset({"ban", "friend"})

def parse_cookie_user(cookie_str):
    if not cookie_str:
        return None, None
    id_val = None
    pass_val = None
    pairs = cookie_str.split(",")
    for pair in pairs:
        if "<>" in pair:
            k, v = pair.split("<>", 1)
            if k == "id":
                id_val = v
            elif k == "pass":
                pass_val = v
    return id_val, pass_val

def get_all_players():
    """全プレイヤーデータを取得します (レベル順ソート)"""
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
    # レベル降順でソート
    players.sort(key=lambda x: x.get("level", 1), reverse=True)
    return players

# === 拒否・友達データの読み書き ===
def load_message_ban(user_id):
    path = os.path.join(config.Config['save_dir'], user_id, "message_ban.json")
    if not os.path.exists(path):
        return {"all_limit": False, "list": []}
    try:
        import json
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"all_limit": False, "list": []}

def save_message_ban(user_id, data):
    path = os.path.join(config.Config['save_dir'], user_id, "message_ban.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

# === 送信済みメッセージの読み書き ===
def load_message_sent(user_id):
    path = os.path.join(config.Config['save_dir'], user_id, "message_sent.json")
    if not os.path.exists(path):
        return []
    try:
        import json
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_message_sent(user_id, data):
    path = os.path.join(config.Config['save_dir'], user_id, "message_sent.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    params = common.decode_params()
    mode = params.get("mode", "").strip()
    user_id = params.get("id", "").strip()
    
    # ユーザー認証
    cookie_str = common.get_cookie(config.Config['cookie_name'])
    c_id, c_pass = parse_cookie_user(cookie_str)
    
    if not user_id:
        if c_id:
            user_id = c_id
        else:
            common.show_error("ログイン情報がありません。再度ログインしてください。")
            
    # ロック取得
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        if not chara:
            common.release_lock(user_id)
            common.show_error("キャラクター情報が見つかりません。")
            
        # パスワードチェック
        if c_id == user_id and c_pass != chara["pass"]:
            common.release_lock(user_id)
            common.show_error("ログインパスワードが一致しません。")
            
        # 1. メッセージ送信処理 (message)
        if mode == "message":
            mes = params.get("mes", "").strip()
            mesid = params.get("mesid", "").strip()
            mesname = params.get("mesname", "").strip()
            
            if not mes:
                common.release_lock(user_id)
                common.show_error("メッセージを入力してください。")
                
            if not mesid and not mesname:
                common.release_lock(user_id)
                common.show_error("送信相手（IDまたは名前）を入力してください。")
                
            if user_id == "test":
                common.release_lock(user_id)
                common.show_error("テストキャラクターはメッセージを送信できません。")
                
            # 相手を検索
            aite_chara = None
            all_players = get_all_players()
            for player in all_players:
                if (mesid and player["id"] == mesid) or (mesname and player["name"] == mesname):
                    aite_chara = player
                    break
                    
            if not aite_chara:
                common.release_lock(user_id)
                common.show_error("指定された相手が見つかりません。")
                
            aite_id = aite_chara["id"]
            if aite_id == user_id:
                common.release_lock(user_id)
                common.show_error("自分宛てにメッセージは送信できません。")
                
            # 禁止ワードチェック
            for ban_w in config.Config['ban_words']:
                if ban_w in mes:
                    common.release_lock(user_id)
                    common.show_error("メッセージ内容に不適切な表現が含まれています。")
                    
            # 文字数制限チェック (1000文字以内)
            if len(mes) > 1000:
                common.release_lock(user_id)
                common.show_error(f"メッセージが長すぎます（現在 {len(mes)} 文字、最大 1000 文字）。")
                
            # 相手の受信制限チェック
            aite_ban = load_message_ban(aite_id)
            
            # 送信者が相手から拒否 (status==1) されているか
            is_banned = False
            is_friend = False
            for b_item in aite_ban.get("list", []):
                if b_item["id"] == user_id:
                    if b_item["status"] == 1:
                        is_banned = True
                    elif b_item["status"] == 2:
                        is_friend = True
                        
            # 受信制限 (受信凍結) かつ 友達でない場合
            if aite_ban.get("all_limit", False) and not is_friend:
                common.release_lock(user_id)
                common.show_error("相手が友達以外からのメッセージ受信を制限しているため、送信できません。")
                
            if is_banned or aite_id == "test":
                common.release_lock(user_id)
                common.show_error("相手から受信制限を受けているため、送信できません。")
                
            now = int(time.time())
            remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            
            # メッセージ構築
            msg_item = {
                "id": user_id,
                "name": chara["name"],
                "time": common.get_time_str(now),
                "message": mes,
                "host": remote_addr
            }
            
            # 相手の受信箱に登録
            common.get_lock(aite_id)
            try:
                aite_msgs = common.message_load(aite_id)
                aite_msgs.insert(0, msg_item)
                # 上限カット
                aite_msgs = aite_msgs[:config.Config['max_messages']]
                common.message_regist(aite_id, aite_msgs)
            finally:
                common.release_lock(aite_id)
                
            # 自分の送信済み箱に登録
            sent_msg_item = {
                "id": aite_id,
                "name": aite_chara["name"],
                "time": common.get_time_str(now),
                "message": mes,
                "host": remote_addr
            }
            my_sent_msgs = load_message_sent(user_id)
            my_sent_msgs.insert(0, sent_msg_item)
            my_sent_msgs = my_sent_msgs[:config.Config['max_messages']]
            save_message_sent(user_id, my_sent_msgs)
            
            context = {
                "chara": chara,
                "user_id": user_id,
                "aite_name": aite_chara["name"]
            }
            common.render_template("post_message_sent_done.html", context)
            
        # 2. 受信制限（受信凍結）の設定 (limit & limit_do)
        elif mode == "limit":
            my_ban = load_message_ban(user_id)
            context = {
                "chara": chara,
                "user_id": user_id,
                "all_limit": my_ban.get("all_limit", False)
            }
            common.render_template("post_message_limit.html", context)
            
        elif mode == "limit_do":
            bansts_str = params.get("bansts", "").strip()
            my_ban = load_message_ban(user_id)
            
            if bansts_str == "1":
                my_ban["all_limit"] = True
                msg = "受信制限を【制限中】に設定しました。"
            else:
                my_ban["all_limit"] = False
                msg = "受信制限を【解除】しました。"
                
            save_message_ban(user_id, my_ban)
            
            context = {
                "chara": chara,
                "user_id": user_id,
                "msg": msg
            }
            common.render_template("post_message_action_done.html", context)
            
        # 3. 拒否・友達リストへの追加・解除 (ban & friend & ban_do) (O(1) frozenset ルックアップで判定)
        elif mode in _POST_MODES:
            my_ban = load_message_ban(user_id)
            status_filter = 1 if mode == "ban" else 2
            
            # リストから対象ステータスの人物を抽出
            list_filtered = [item for item in my_ban.get("list", []) if item["status"] == status_filter]
            
            context = {
                "chara": chara,
                "user_id": user_id,
                "mode": mode,
                "list": list_filtered
            }
            common.render_template("post_message_list_setting.html", context)
            
        elif mode == "ban_do":
            mesid = params.get("mesid", "").strip()
            mesname = params.get("mesname", "").strip()
            bansts_str = params.get("bansts", "").strip() # 0: 解除, 1: 拒否, 2: 友達
            
            try:
                bansts = int(bansts_str)
            except ValueError:
                common.release_lock(user_id)
                common.show_error("設定ステータスが不正です。")
                
            if not mesid and not mesname:
                common.release_lock(user_id)
                common.show_error("相手を指定してください。")
                
            # 相手を検索
            aite_chara = None
            all_players = get_all_players()
            for player in all_players:
                if (mesid and player["id"] == mesid) or (mesname and player["name"] == mesname):
                    aite_chara = player
                    break
                    
            if not aite_chara:
                common.release_lock(user_id)
                common.show_error("指定された相手が見つかりません。")
                
            aite_id = aite_chara["id"]
            if aite_id == user_id:
                common.release_lock(user_id)
                common.show_error("自分自身は設定できません。")
                
            my_ban = load_message_ban(user_id)
            
            # 解除/追加
            lst = my_ban.get("list", [])
            # すでに登録されている同一IDを削除
            lst = [item for item in lst if item["id"] != aite_id]
            
            action_name = "設定を解除"
            if bansts == 1:
                lst.append({"id": aite_id, "name": aite_chara["name"], "status": 1})
                action_name = "拒否リストに登録"
            elif bansts == 2:
                lst.append({"id": aite_id, "name": aite_chara["name"], "status": 2})
                action_name = "友達リストに登録"
                
            my_ban["list"] = lst
            save_message_ban(user_id, my_ban)
            
            context = {
                "chara": chara,
                "user_id": user_id,
                "msg": f"{aite_chara['name']} さんを {action_name} しました。"
            }
            common.render_template("post_message_action_done.html", context)
            
        # 4. 全ユーザー一覧から相手選択 (all_list)
        elif mode == "all_list":
            players = get_all_players()
            # 自分を除外
            players = [p for p in players if p["id"] != user_id]
            context = {
                "chara": chara,
                "user_id": user_id,
                "players": players
            }
            common.render_template("post_message_select_user.html", context)
            
        # 5. メッセージの返信作成補助 (res)
        elif mode == "res":
            res_id = params.get("mesid", "").strip()
            res_name = params.get("mesname", "").strip()
            res_content = params.get("mes", "").strip()
            
            context = {
                "chara": chara,
                "user_id": user_id,
                "res_id": res_id,
                "res_name": res_name,
                "res_content": res_content
            }
            common.render_template("post_message_reply.html", context)
            
        # 6. メッセージ（郵便局）初期画面
        else:
            msgs_received = common.message_load(user_id)
            msgs_sent = load_message_sent(user_id)
            
            context = {
                "chara": chara,
                "user_id": user_id,
                "msgs_received": msgs_received,
                "msgs_sent": msgs_sent
            }
            common.render_template("post_message.html", context)
            
    finally:
        common.release_lock(user_id)

if __name__ == "__main__":
    main()
