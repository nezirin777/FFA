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
FFA Python/CGI - パスワード変更スクリプト (passchange.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
import os
import time

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
from sub_def.crypto import hash_password

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

def get_pass_change_path(user_id):
    return os.path.join(config.Config['save_dir'], user_id, "pass_change.json")

def load_pass_change(user_id):
    path = get_pass_change_path(user_id)
    if not os.path.exists(path):
        return None
    try:
        import json
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def save_pass_change(user_id, data):
    path = get_pass_change_path(user_id)
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
            
        if user_id == "test":
            common.release_lock(user_id)
            common.show_error("テストキャラクターはパスワードを変更できません。")
            
        pass_change = load_pass_change(user_id)
        
        # 1. パスワード変更用単語の新規設定 (passset)
        # ※サブ動作名を "passchange" にするとルーティングキー (login.py?mode=passchange) と
        #   衝突し、入場時のGETでもこの分岐に入ってしまうため別名にしている
        if mode == "passset":
            pass_confirm = params.get("pass", "").strip()
            word = params.get("passchange", "").strip()

            # 保存値はハッシュのため、入力値もハッシュ化して比較する
            if hash_password(pass_confirm) != chara["pass"]:
                common.release_lock(user_id)
                common.show_error("現在のパスワードが間違っています。")

            if pass_change:
                common.release_lock(user_id)
                common.show_error("パスワード変更用単語はすでに設定されています。")
                
            if not word:
                common.release_lock(user_id)
                common.show_error("パスワード変更用単語を入力してください。")
                
            now = int(time.time())
            remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            
            pass_change_data = {
                "pass": chara["pass"],
                "passchange": word,
                "created_at": now,
                "host": remote_addr
            }
            save_pass_change(user_id, pass_change_data)
            
            context = {
                "chara": chara,
                "user_id": user_id,
                "word": word
            }
            common.render_template("passchange_set_done.html", context)
            
        # 2. パスワード変更実行 (passchan)
        elif mode == "passchan":
            pass_confirm = params.get("pass", "").strip()
            word = params.get("passchange", "").strip()
            npass = params.get("npass", "").strip()
            nkpass = params.get("nkpass", "").strip()

            # 保存値はハッシュのため、入力値もハッシュ化して比較する
            if hash_password(pass_confirm) != chara["pass"]:
                common.release_lock(user_id)
                common.show_error("現在のパスワードが間違っています。")
                
            if not pass_change:
                common.release_lock(user_id)
                common.show_error("変更用単語が設定されていません。")
                
            if word != pass_change["passchange"]:
                common.release_lock(user_id)
                common.show_error("パスワード変更用単語が間違っています。")
                
            if not npass:
                common.release_lock(user_id)
                common.show_error("新しいパスワードを入力してください。")
                
            if npass != nkpass:
                common.release_lock(user_id)
                common.show_error("新しいパスワードと確認入力が一致しません。")
                
            if not npass.isalnum() or len(npass) < 4 or len(npass) > 8:
                common.release_lock(user_id)
                common.show_error("新しいパスワードは4〜8文字の半角英数字で設定してください。")
                
            now = int(time.time())
            remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            
            # 更新 (保存・クッキーともにハッシュ値を用いる)
            hashed_npass = hash_password(npass)
            chara["pass"] = hashed_npass
            common.chara_regist(user_id, chara)

            # パスワード変更ファイルも更新
            pass_change["pass"] = hashed_npass
            pass_change["created_at"] = now
            pass_change["host"] = remote_addr
            save_pass_change(user_id, pass_change)

            # クッキーのヘッダーを返すためのクッキー値変更
            # ログインセッションを維持するため、クッキーを書き換えます
            cookie_value = f"id<>{user_id},pass<>{hashed_npass}"
            cookie_header = common.set_cookie_header(config.Config['cookie_name'], cookie_value)
            
            context = {
                "chara": chara,
                "user_id": user_id
            }
            common.render_template("passchange_done.html", context, extra_headers=[cookie_header])
            
        # 3. 初期表示
        else:
            time_str = ""
            host_str = ""
            if pass_change:
                time_str = common.get_time_str(pass_change.get("created_at", 0))
                host_str = pass_change.get("host", "不明")
                
            context = {
                "chara": chara,
                "user_id": user_id,
                "has_words": pass_change is not None,
                "last_time": time_str,
                "last_host": host_str
            }
            common.render_template("passchange.html", context)
            
    finally:
        common.release_lock(user_id)

if __name__ == "__main__":
    main()
