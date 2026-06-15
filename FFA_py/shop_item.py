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
FFA Python/CGI - 武器屋スクリプト (shop_item.py)
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

def get_item_master(item_id):
    """武器マスタ(item.ini)から特定の武器情報を取得します。"""
    path = os.path.join(common.BASE_DIR, config.Config['item_file'])
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("<>")
            if parts and parts[0] == str(item_id):
                return {
                    "id": int(parts[0]),
                    "name": parts[1],
                    "power": int(parts[2]),
                    "gold": int(parts[3])
                }
    return None

def load_shop_items(job_idx):
    """現在の職業に対応する武器屋の商品リストを読み込みます。"""
    path = os.path.join(common.BASE_DIR, f"{config.Config['item_folder']}/item{job_idx}.ini")
    items = []
    if not os.path.exists(path):
        return items
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("<>")
            if len(parts) >= 4:
                items.append({
                    "no": int(parts[0]),
                    "name": parts[1],
                    "power": int(parts[2]),
                    "gold": int(parts[3]),
                    "hit": int(parts[4]) if len(parts) > 4 else 0
                })
    return items

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    params = common.decode_params()
    mode = params.get("mode", "")
    user_id = params.get("id", "").strip()
    
    if not user_id:
        common.show_error("ユーザーIDが指定されていません。")
        
    # 宿屋などと同様、処理開始時にロックを取得
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        item = common.item_load(user_id)
        if not chara or not item:
            common.release_lock(user_id)
            common.show_error("キャラクター情報が見つかりません。")
            
        # 共通情報
        job_idx = chara["job"]
        job_name = config.Config['chara_jobs'][job_idx]
        
        # 1. 購入処理
        if mode == "buy":
            item_no = params.get("item_no", "").strip()
            if not item_no:
                common.release_lock(user_id)
                common.show_error("購入する商品が選択されていません。")
                
            shop_items = load_shop_items(job_idx)
            selected_item = next((i for i in shop_items if str(i["no"]) == item_no), None)
            
            if not selected_item:
                common.release_lock(user_id)
                common.show_error("指定された商品は販売されていません。")
                
            # 所持金チェック
            if chara["gold"] < selected_item["gold"]:
                common.release_lock(user_id)
                common.show_error("所持金が足りません。")
                
            # 倉庫の空きチェック
            souko = common.souko_load(user_id, "item")
            if len(souko) >= config.Config['max_items']:
                common.release_lock(user_id)
                common.show_error(f"武器倉庫がいっぱいです！(最大 {config.Config['max_items']} 個)")
                
            # 購入処理実行
            chara["gold"] -= selected_item["gold"]
            chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            
            # 倉庫に追加
            new_weapon = {
                "id": selected_item["no"],
                "name": selected_item["name"],
                "power": selected_item["power"],
                "gold": selected_item["gold"],
                "effect": selected_item["hit"]
            }
            souko.append(new_weapon)
            
            # 保存
            common.chara_regist(user_id, chara)
            common.souko_regist(user_id, "item", souko)
            common.release_lock(user_id)
            
            # 取引結果表示
            result_msg = (
                f"武器 <b>{selected_item['name']}</b> を <b>{selected_item['gold']}</b> G で購入しました！<br>"
                "購入した武器は倉庫に送られました。ステータス画面から装備を整えてください。"
            )
            common.render_template("shop_result.html", {
                "chara": chara,
                "result_msg": result_msg,
                "back_url": "shop_item.py"
            })
            return
            
        # 2. 売却（下取り）処理
        elif mode == "sell":
            equipped_id = chara.get("weapon_id", 0)
            if not equipped_id or equipped_id == 0:
                common.release_lock(user_id)
                common.show_error("売却できる武器を装備していません。")
                
            # マスタから武器の情報を取得して価格を決定
            master_item = get_item_master(equipped_id)
            if not master_item:
                # マスタに見つからない場合はデフォルト価格で下取り
                master_item = {"name": item["weapon"]["name"], "gold": 0}
                
            sell_gold = int(master_item["gold"] / 3) * 2
            
            chara["gold"] += sell_gold
            if chara["gold"] > config.Config['max_gold']:
                chara["gold"] = config.Config['max_gold']
                
            # 装備をリセット
            chara["weapon_id"] = 0
            item["weapon"] = {"name": "素手", "dmg": 0, "effect": 0}
            
            # 保存
            common.chara_regist(user_id, chara)
            common.item_regist(user_id, item)
            common.release_lock(user_id)
            
            # 取引結果表示
            result_msg = (
                f"装備していた武器 <b>{master_item['name']}</b> を下取りに出しました。<br>"
                f"売却額 <b>{sell_gold}</b> G を手に入れました！"
            )
            common.render_template("shop_result.html", {
                "chara": chara,
                "result_msg": result_msg,
                "back_url": "shop_item.py"
            })
            return
            
        # 3. 武器屋画面表示 (mode == "")
        else:
            common.release_lock(user_id)
            
            # 現在装備中の武器情報
            equipped_id = chara.get("weapon_id", 0)
            master_item = get_item_master(equipped_id) if equipped_id != 0 else None
            
            if master_item:
                equipped_item = {
                    "id": equipped_id,
                    "name": master_item["name"],
                    "power": master_item["power"],
                    "sell_gold": int(master_item["gold"] / 3) * 2
                }
            else:
                equipped_item = {
                    "id": 0,
                    "name": "素手",
                    "power": 0,
                    "sell_gold": 0
                }
                
            # 販売リストの取得
            shop_items = load_shop_items(job_idx)
            
            # メッセージの構築
            shop_msg = (
                "「いらっしゃい！武器を揃えにきたのかい？<br>"
                f"今のあんたの職業は <b>{job_name}</b> だな。<br>"
                f"それなら、この <b>{job_name}用</b> の武器がおすすめだよ。<br>"
                "ゆっくり見ていってくれな！」"
            )
            
            context = {
                "chara": chara,
                "shop_title": "武器屋",
                "shop_msg": shop_msg,
                "equipped_item": equipped_item,
                "shop_items": shop_items,
                "post_url": "shop_item.py"
            }
            common.render_template("shop_trade.html", context)
            
    except Exception as e:
        common.release_lock(user_id)
        common.show_error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
