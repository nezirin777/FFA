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
FFA Python/CGI - 装飾品店スクリプト (shop_acs.py)
"""

import os
import sys
import json


# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正

def get_acs_master(acs_id):
    """装飾品マスタ(acs.json)から特定の装飾品情報を取得します。"""
    path = os.path.join(common.BASE_DIR, config.Config['acs_file'])
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            if item.get("no") == int(acs_id):
                return {
                    "id": item["no"],
                    "name": item["name"],
                    "gold": item["gold"],
                    "effect_id": item.get("effect_id", 0),
                    "bonus": {
                        "str": item.get("bonus", {}).get("str", 0),
                        "int": item.get("bonus", {}).get("int", 0),
                        "dex": item.get("bonus", {}).get("dex", 0),
                        "vit": item.get("bonus", {}).get("vit", 0),
                        "agi": item.get("bonus", {}).get("agi", 0),
                        "mnd": item.get("bonus", {}).get("mnd", 0),
                        "lck": item.get("bonus", {}).get("lck", 0),
                        "lp": item.get("bonus", {}).get("lp", 0)
                    },
                    "attrib": item.get("attrib", 0),
                    "spare1": item.get("spare1", 0),
                    "spare2": item.get("spare2", 0),
                    "spare3": 0
                }
    except Exception:
        pass
    return None

def load_shop_items(job_idx):
    """現在の職業に対応する装飾品店の商品リストを読み込みます。"""
    path = os.path.join(common.BASE_DIR, f"{config.Config['acs_folder']}/acs{job_idx}.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            item["spare3"] = 0
        return items
    except Exception:
        return []

def format_bonus(bonus_dict):
    """ステータス上昇ボーナスを表示用に文字列化します。"""
    parts = []
    keys = [("str", "力"), ("int", "魔"), ("dex", "技"), ("vit", "体"), 
            ("agi", "速"), ("mnd", "精"), ("lck", "運"), ("lp", "魅")]
    for k, name in keys:
        val = bonus_dict.get(k, 0)
        if val != 0:
            sign = "+" if val > 0 else ""
            parts.append(f"{name}{sign}{val}")
    return " ".join(parts) if parts else "効果なし"

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    params = common.decode_params()
    mode = params.get("mode", "")
    user_id = params.get("id", "").strip()
    
    if not user_id:
        common.show_error("ユーザーIDが指定されていません。")
        
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        item = common.item_load(user_id)
        if not chara or not item:
            common.release_lock(user_id)
            common.show_error("キャラクター情報が見つかりません。")
            
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
            souko = common.souko_load(user_id, "acs")
            if len(souko) >= config.Config['max_accessories']:
                common.release_lock(user_id)
                common.show_error(f"装飾品倉庫がいっぱいです！(最大 {config.Config['max_accessories']} 個)")
                
            # 購入処理実行
            chara["gold"] -= selected_item["gold"]
            chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            
            # 倉庫に追加
            new_acs = {
                "id": selected_item["no"],
                "name": selected_item["name"],
                "gold": selected_item["gold"],
                "effect_id": selected_item["effect_id"],
                "bonus": selected_item["bonus"],
                "attrib": selected_item["attrib"],
                "spare1": selected_item["spare1"],
                "spare2": selected_item["spare2"],
                "spare3": selected_item["spare3"]
            }
            souko.append(new_acs)
            
            # 保存
            common.chara_regist(user_id, chara)
            common.souko_regist(user_id, "acs", souko)
            common.release_lock(user_id)
            
            # 取引結果表示
            result_msg = (
                f"装飾品 <b>{selected_item['name']}</b> を <b>{selected_item['gold']}</b> G で購入しました！<br>"
                "購入した装飾品は倉庫に送られました。ステータス画面から装備を整えてください。"
            )
            common.render_template("shop_result.html", {
                "chara": chara,
                "result_msg": result_msg,
                "back_url": config.Config['shop_acs_script']
            })
            return
            
        # 2. 売却（下取り）処理
        elif mode == "sell":
            equipped_id = chara.get("accessory_id", 0)
            if not equipped_id or equipped_id == 0:
                common.release_lock(user_id)
                common.show_error("売却できる装飾品を装備していません。")
                
            # マスタから装飾品の情報を取得して価格を決定
            master_item = get_acs_master(equipped_id)
            if not master_item:
                master_item = {"name": item["accessory"]["name"], "gold": 0}
                
            sell_gold = int(master_item["gold"] / 3) * 2
            
            chara["gold"] += sell_gold
            if chara["gold"] > config.Config['max_gold']:
                chara["gold"] = config.Config['max_gold']
                
            # 装備をリセット
            chara["accessory_id"] = 0
            item["accessory"] = {
                "name": "なし",
                "effect_id": 0,
                "bonus": {"str": 0, "int": 0, "dex": 0, "vit": 0, "agi": 0, "mnd": 0, "lck": 0, "lp": 0},
                "attrib": 0,
                "spare1": 0,
                "spare2": 0,
                "spare3": 0
            }
            
            # 保存
            common.chara_regist(user_id, chara)
            common.item_regist(user_id, item)
            common.release_lock(user_id)
            
            # 取引結果表示
            result_msg = (
                f"装備していた装飾品 <b>{master_item['name']}</b> を下取りに出しました。<br>"
                f"売却額 <b>{sell_gold}</b> G を手に入れました！"
            )
            common.render_template("shop_result.html", {
                "chara": chara,
                "result_msg": result_msg,
                "back_url": config.Config['shop_acs_script']
            })
            return
            
        # 3. 装飾品店画面表示 (mode == "")
        else:
            common.release_lock(user_id)
            
            # 現在装備中の装飾品情報
            equipped_id = chara.get("accessory_id", 0)
            master_item = get_acs_master(equipped_id) if equipped_id != 0 else None
            
            if master_item:
                equipped_item = {
                    "id": equipped_id,
                    "name": master_item["name"],
                    "power": format_bonus(master_item["bonus"]),
                    "sell_gold": int(master_item["gold"] / 3) * 2
                }
            else:
                equipped_item = {
                    "id": 0,
                    "name": "なし",
                    "power": "効果なし",
                    "sell_gold": 0
                }
                
            # 販売リストの取得
            raw_shop_items = load_shop_items(job_idx)
            shop_items = []
            for r_item in raw_shop_items:
                shop_items.append({
                    "no": r_item["no"],
                    "name": r_item["name"],
                    "power": format_bonus(r_item["bonus"]),
                    "gold": r_item["gold"]
                })
            
            # メッセージの構築
            shop_msg = (
                "「いらっしゃいませ！旅を彩り、能力を呼び覚ます装飾品店へようこそ。<br>"
                f"現在の職業 <b>{job_name}</b> の秘められた力を引き出す指輪やアミュレットだよ。<br>"
                "お気に入りの一品を身につけて、冒険を有利に進めてね！」"
            )
            
            context = {
                "chara": chara,
                "shop_title": "装飾品店",
                "shop_msg": shop_msg,
                "equipped_item": equipped_item,
                "shop_items": shop_items,
                "post_url": config.Config['shop_acs_script']
            }
            common.render_template("shop_trade.html", context)
            
    except Exception as e:
        common.release_lock(user_id)
        common.show_error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
