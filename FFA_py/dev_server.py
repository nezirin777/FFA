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
FFA Python/CGI ローカルテストサーバー (dev_server.py)
親ディレクトリ(FFA)をルートとして起動し、静的ファイル(images/, html/)の配信と
FFA_py/ 配下の .py CGIスクリプトの実行をサポートします。
"""

import os
import sys
import http.server
import socketserver

# 親ディレクトリ (FFA) をカレントディレクトリにする
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(base_dir)

PORT = 8000

class FFA_CGIHandler(http.server.CGIHTTPRequestHandler):
    def is_cgi(self):
        """
        リクエストパスが /FFA_py/ 配下の .py ファイルである場合、CGIとして処理します。
        """
        # クエリパラメータを取り除く
        path_no_query = self.path.split('?')[0]
        
        # Windowsのパス区切りに対応
        normalized_path = path_no_query.replace('\\', '/')
        
        if normalized_path.startswith("/FFA_py/") and normalized_path.endswith(".py"):
            # cgi_infoを設定: (ディレクトリ部分, スクリプトファイル名)
            # 例: ("FFA_py", "login.py")
            parts = normalized_path.lstrip("/").split("/")
            dir_part = "/".join(parts[:-1])
            file_part = parts[-1]
            self.cgi_info = (dir_part, file_part)
            return True
            
        return False

# CGIを実行可能に設定
FFA_CGIHandler.cgi_directories = ["/FFA_py"]

print(f"==================================================")
print(f" FFA Python/CGI Local Dev Server")
print(f" Web Root: {os.getcwd()}")
print(f" Server URL: http://localhost:{PORT}/FFA_py/login.py")
print(f"==================================================")
print("起動中... (終了するには Ctrl+C を押してください)")

# アドレス再利用を有効にするためのカスタムHTTPServer
class ReusableHTTPServer(http.server.HTTPServer):
    allow_reuse_address = True

try:
    with ReusableHTTPServer(("", PORT), FFA_CGIHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nサーバーを停止しました。")
except Exception as e:
    print(f"\nエラーが発生しました: {e}")
