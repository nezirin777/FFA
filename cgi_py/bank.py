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
FFA Python/CGI - 銀行取引スクリプト (bank.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
import os

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正

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

def main():
    # メンテナンスチェック
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
            
        # 銀行預金初期化 (もしなければ0)
        if "bank" not in chara:
            chara["bank"] = 0
            
        # 1. 預け入れ (bank_sell)
        if mode == "bank_sell":
            azuke_str = params.get("azuke", "").strip()
            if azuke_str == "":
                common.release_lock(user_id)
                common.show_error("金額を入力してください。")
                
            if not azuke_str.isdigit():
                common.release_lock(user_id)
                common.show_error("金額は半角数値で入力してください。")
                
            azuke_val = int(azuke_str)
            if azuke_val <= 0:
                common.release_lock(user_id)
                common.show_error("マイナスの値は預け入れできません。")
                
            azukeru_gold = azuke_val * 1000
            if azukeru_gold > chara["gold"]:
                common.release_lock(user_id)
                common.show_error("所持金を超えています。")
                
            if azukeru_gold + chara["bank"] > config.Config['max_bank']:
                common.release_lock(user_id)
                common.show_error(f"銀行の最大預金上限（{config.Config['max_bank']}ゴールド）を超えてしまいます。")
                
            # ゴールド更新
            chara["bank"] += azukeru_gold
            chara["gold"] -= azukeru_gold
            
            # ホスト名取得
            remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            chara["host"] = remote_addr
            
            # 保存
            common.chara_regist(user_id, chara)
            
            # 結果表示
            context = {
                "chara": chara,
                "msg": f"{azukeru_gold}ゴールドお預かりいたしました。",
                "user_id": user_id
            }
            common.render_template("bank_result.html", context)
            
        # 2. 引き出し (bank_buy)
        elif mode == "bank_buy":
            dasu_str = params.get("dasu", "").strip()
            if dasu_str == "":
                common.release_lock(user_id)
                common.show_error("金額を入力してください。")
                
            if not dasu_str.isdigit():
                common.release_lock(user_id)
                common.show_error("金額は半角数値で入力してください。")
                
            dasu_val = int(dasu_str)
            if dasu_val <= 0:
                common.release_lock(user_id)
                common.show_error("マイナスの値は引き出しできません。")
                
            dasuru_gold = dasu_val * 1000
            if dasuru_gold > chara["bank"]:
                common.release_lock(user_id)
                common.show_error("預金額を超えています。")
                
            if dasuru_gold + chara["gold"] > config.Config['max_gold']:
                common.release_lock(user_id)
                common.show_error(f"所持金の最大上限（{config.Config['max_gold']}ゴールド）を超えてしまいます。")
                
            # ゴールド更新
            chara["bank"] -= dasuru_gold
            chara["gold"] += dasuru_gold
            
            # ホスト名取得
            remote_addr = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            chara["host"] = remote_addr
            
            # 保存
            common.chara_regist(user_id, chara)
            
            # 結果表示
            context = {
                "chara": chara,
                "msg": f"{dasuru_gold}ゴールドお引き出しいたしました。",
                "user_id": user_id
            }
            common.render_template("bank_result.html", context)
            
        # 3. 銀行初期画面 (表示)
        else:
            # 預け入れ可能額（1,000ゴールド単位）
            if config.Config['max_bank'] < chara["bank"] + chara["gold"]:
                bank_max_in = int((config.Config['max_bank'] - chara["bank"]) / 1000)
            else:
                bank_max_in = int(chara["gold"] / 1000)
            if bank_max_in < 0:
                bank_max_in = 0
                
            # 引き出し可能額（1,000ゴールド単位）
            if config.Config['max_gold'] < chara["bank"] + chara["gold"]:
                bank_max_out = int((config.Config['max_gold'] - chara["gold"]) / 1000)
            else:
                bank_max_out = int(chara["bank"] / 1000)
            if bank_max_out < 0:
                bank_max_out = 0
                
            context = {
                "chara": chara,
                "user_id": user_id,
                "bank_max_in": bank_max_in,
                "bank_max_out": bank_max_out,
                "bank_max": config.Config['max_bank']
            }
            common.render_template("bank.html", context)
            
    finally:
        common.release_lock(user_id)

if __name__ == "__main__":
    main()
