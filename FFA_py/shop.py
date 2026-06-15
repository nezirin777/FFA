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
FFA Python/CGI - 宿屋スクリプト (shop.py)
"""

import os
import sys


# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')
# 共通モジュールと設定モジュールのインポート
import config
import common

def update_winner_hp(user_id, max_hp):
    """
    王者が宿屋に泊まった場合、王者ファイル(winner.ini)の現在HPを最大HPに回復させて保存します。
    """
    winner_path = os.path.join(common.BASE_DIR, config.Config['winner_file'])
    if not os.path.exists(winner_path):
        return
        
    common.get_lock("winner")
    try:
        with open(winner_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        parts = content.strip().split("<>")
        if parts and parts[-1] == "":
            parts = parts[:-1]
            
        # 王者IDが一致する場合、現在HP(インデックス15)を最大HP(インデックス16)に書き換える
        if len(parts) > 16 and parts[0] == user_id:
            parts[15] = str(max_hp)
            
            # 再度連結して保存 (Perl互換のため末尾に <> を付与)
            new_content = "<>".join(parts) + "<>\n"
            with open(winner_path, "w", encoding="utf-8") as f:
                f.write(new_content)
    finally:
        common.release_lock("winner")

def main():
    # 1. メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待たせします。")
        
    # 2. パラメータの取得
    params = common.decode_params()
    mode = params.get("mode", "")
    user_id = params.get("id", "").strip()
    
    if mode != "yado" or not user_id:
        common.show_error("不正なパラメータです。")
        
    # 3. キャラクター情報のロード(排他制御ロック付)
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        if not chara:
            common.release_lock(user_id)
            common.show_error("キャラクターが見つかりません。")
            
        # 4. 宿代の計算
        yado_daix = int(config.Config['inn_cost'] * chara["level"])
        
        # 5. 所持金不足チェック
        if chara["gold"] < yado_daix:
            common.release_lock(user_id)
            common.show_error("宿代が足りません！")
            
        # 6. 回復処理と所持金減算
        chara["hp"] = chara["max_hp"]
        chara["gold"] -= yado_daix
        chara["boss_flag"] = config.Config['boss_cooldown']  # ボスフラグを回復
        
        # 7. データの保存
        common.chara_regist(user_id, chara)
    finally:
        common.release_lock(user_id)
        
    # 8. 王者HPの更新 (王者が宿に泊まった場合)
    update_winner_hp(user_id, chara["max_hp"])
    
    # 9. 画面描画
    context = {
        "chara": chara,
        "yado_daix": yado_daix
    }
    common.render_template("shop.html", context)

if __name__ == "__main__":
    main()
