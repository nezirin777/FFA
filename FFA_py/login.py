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
FFA Python/CGI - ログイン処理スクリプト (login.py)
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

def main():
    # 1. メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    # 2. パラメータの取得
    params = common.decode_params()
    user_id = params.get("id", "").strip()
    user_pass = params.get("pass", "").strip()
    
    # 3. 入力チェック
    if not user_id:
        common.show_error("IDが入力されていません。")
        
    # 4. キャラクターデータのロード
    chara = common.chara_load(user_id)
    if not chara:
        # 復元画面（hukugen.cgi）への遷移エラーを表示（元CGIに準拠）
        err_msg = (
            "キャラクターデータが読み込めません。<br>"
            "データが存在しないか、破損している可能性があります。<br>"
            f'<form action="hukugen.py" method="post">'
            f'<input type="hidden" name="id" value="{user_id}">'
            f'<input type="hidden" name="mode" value="log_in">'
            f'<input type="submit" value="復元を試みる" style="margin-top:10px; padding:3px 10px;">'
            f'</form>'
        )
        common.show_error(err_msg)
        
    # 5. アクセス制限 (ホストIPチェック)
    remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
    for shut_ip in config.Config['shut_hosts']:
        # ワイルドカードを正規表現などに変換してチェックすることも可能だが、簡易的に前方一致や完全一致で判定
        shut_prefix = shut_ip.replace("*", "")
        if remote_addr.startswith(shut_prefix):
            common.show_error("アクセスが制限されています。")
            
    # 6. ログイン履歴 (login_log.json) の処理
    # ロックを取得してログイン履歴を記録
    lock_name = f"login{user_id}"
    common.get_lock(lock_name)
    
    try:
        login_logs = common.login_log_load(user_id)
        
        # 履歴件数の制限 (最大15件)
        if len(login_logs) >= 15:
            login_logs = login_logs[:14] # 最新14件を残す
            
        get_time_str = common.get_time_str()
        
        # パスワード不一致チェック
        if user_pass != chara["pass"]:
            # 失敗ログを追加 (failed=1)
            new_log = {
                "pass": user_pass,
                "host": remote_addr,
                "time": get_time_str,
                "failed": 1
            }
            login_logs.insert(0, new_log)
            common.login_log_regist(user_id, login_logs)
            common.release_lock(lock_name)
            common.show_error("パスワードが間違っています。")
            
        # 成功ログを追加 (failed=0)
        new_log = {
            "pass": user_pass,
            "host": remote_addr,
            "time": get_time_str,
            "failed": 0
        }
        login_logs.insert(0, new_log)
        common.login_log_regist(user_id, login_logs)
        
    finally:
        # ロック解除
        common.release_lock(lock_name)
        
    # 7. 成功/失敗ログの整形
    success_logs = [log for log in login_logs if log["failed"] == 0][:5] # 最新の成功5件を表示
    error_logs = [log for log in login_logs if log["failed"] == 1][:5]   # 最新の失敗5件を表示
    
    # 8. クッキーの設定
    # "id<>userid,pass<>userpass" 形式でクッキーを発行
    cookie_value = f"id<>{user_id},pass<>{chara['pass']}"
    cookie_header = common.set_cookie_header(config.Config['cookie_name'], cookie_value)
    
    # 9. 冒険者リストの更新と取得
    guest_list_html = common.update_and_get_guests(user_id, chara["name"])
    
    # 10. メッセージデータのロード
    personal_messages = common.message_load(user_id)[:config.Config['max_lines']]
    global_messages = common.all_message_load()[:config.Config['max_all_lines']]
    
    # 11. Jinja2テンプレートでの画面描画
    context = {
        "chara": chara,
        "success_logs": success_logs,
        "error_logs": error_logs,
        "guest_list_html": guest_list_html,
        "personal_messages": personal_messages,
        "global_messages": global_messages
    }
    
    common.render_template("login.html", context, extra_headers=[cookie_header])

if __name__ == "__main__":
    main()
