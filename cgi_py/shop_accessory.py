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
FFA Python/CGI - 装飾品店スクリプト (shop_accessory.py)
"""

import os


# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正

def load_available_accessories(job_idx):
    """共通装飾品マスターから、現在の職業が購入可能な商品を抽出します。"""
    return common.master_records_for_job(config.Config["accessory_file"], job_idx)


format_bonus = common.format_accessory_bonus

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    params = common.decode_params()
    mode = params.get("mode", "")
    user_id = params.get("id", "").strip()
    # IDOR対策: 状態変更は本人のみ許可(ロック取得前にチェック)
    common.require_owner(user_id)
    
    if not user_id:
        common.show_error("ユーザーIDが指定されていません。")
        
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        item = common.equipment_load(user_id)
        if not chara or not item:
            common.release_lock(user_id)
            common.show_error("キャラクター情報が見つかりません。")
            
        job_idx = chara["job"]
        job_name = config.Config['chara_jobs'].get(job_idx, "不明な職業")
        accessory_shop_url = f"{config.Config['shop_accessory_script']}&id={user_id}"
        
        # 1. 購入処理
        if mode == "buy":
            item_no = params.get("item_no", "").strip()
            if not item_no:
                common.release_lock(user_id)
                common.redirect_with_flash(accessory_shop_url, "購入する商品が選択されていません。", "error")
                
            accessories = load_available_accessories(job_idx)
            selected_accessory = next(
                (accessory for accessory in accessories if str(accessory["no"]) == item_no),
                None,
            )
            
            if not selected_accessory:
                common.release_lock(user_id)
                common.redirect_with_flash(accessory_shop_url, "指定された商品は販売されていません。", "error")
                
            # 所持金チェック
            if chara["gold"] < selected_accessory["gold"]:
                common.release_lock(user_id)
                common.redirect_with_flash(accessory_shop_url, "所持金が足りません。", "error")
                
            # 倉庫の空きチェック
            souko = common.souko_load(user_id, "accessory")
            if len(souko) >= config.Config['max_accessories']:
                common.release_lock(user_id)
                common.redirect_with_flash(accessory_shop_url, f"装飾品倉庫がいっぱいです！(最大 {config.Config['max_accessories']} 個)", "error")
                
            # 購入処理実行
            chara["gold"] -= selected_accessory["gold"]
            chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            
            # 倉庫に追加
            new_accessory = {
                "id": selected_accessory["no"],
                "name": selected_accessory["name"],
                "gold": selected_accessory["gold"],
                "effect_id": selected_accessory["effect_id"],
                "bonus": selected_accessory["bonus"],
                "hit_rate": selected_accessory["hit_rate"],
                "evasion_rate": selected_accessory["evasion_rate"],
                "special_rate": selected_accessory["special_rate"],
                "description": selected_accessory.get("description", "")
            }
            souko.append(new_accessory)
            
            # 保存
            common.save_user_sections(user_id, chara=chara, souko_accessory=souko)
            common.release_lock(user_id)
            
            # 取引結果はトーストで通知し、装飾品店へ戻す
            common.redirect_with_flash(
                accessory_shop_url,
                f"装飾品 {selected_accessory['name']} を {selected_accessory['gold']} G で購入しました。購入した装飾品は倉庫に送られました。",
                "success",
            )
            return
            
        # 2. 売却（下取り）処理
        elif mode == "sell":
            equipped_id = chara.get("accessory_id", 0)
            if not equipped_id or equipped_id == 0:
                common.release_lock(user_id)
                common.redirect_with_flash(accessory_shop_url, "売却できる装飾品を装備していません。", "error")
                
            # マスタから装飾品の情報を取得して価格を決定
            master_item = common.find_master_record(config.Config["accessory_file"], equipped_id)
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
                "bonus": {"str": 0, "int": 0, "mnd": 0, "vit": 0, "dex": 0, "agi": 0, "cha": 0, "karma": 0},
                "hit_rate": 0,
                "evasion_rate": 0,
                "special_rate": 0,
                "description": ""
            }
            
            # 保存
            common.save_user_sections(user_id, chara=chara, equipment=item)
            common.release_lock(user_id)
            
            # 取引結果はトーストで通知し、装飾品店へ戻す
            common.redirect_with_flash(
                accessory_shop_url,
                f"装備していた装飾品 {master_item['name']} を下取りに出しました。売却額 {sell_gold} G を手に入れました！",
                "success",
            )
            return
            
        # 3. 装飾品店画面表示 (mode == "")
        else:
            common.release_lock(user_id)
            
            # 現在装備中の装飾品情報
            equipped_id = chara.get("accessory_id", 0)
            master_item = common.find_master_record(config.Config["accessory_file"], equipped_id)
            
            if master_item:
                equipped_item = {
                    "id": equipped_id,
                    "name": master_item["name"],
                    "performance": master_item.get("description") or format_bonus(master_item["bonus"]),
                    "sell_gold": int(master_item["gold"] / 3) * 2
                }
            else:
                equipped_item = {
                    "id": 0,
                    "name": "なし",
                    "performance": "効果なし",
                    "sell_gold": 0
                }
                
            # 販売リストの取得
            accessories = load_available_accessories(job_idx)
            catalog_items = []
            for accessory in accessories:
                catalog_items.append({
                    "no": accessory["no"],
                    "name": accessory["name"],
                    "performance": accessory.get("description") or format_bonus(accessory["bonus"]),
                    "gold": accessory["gold"]
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
                "catalog_items": catalog_items,
                "performance_label": "説明",
                "post_url": config.Config['shop_accessory_script']
            }
            common.render_template("shop_trade.html", context)
            
    except Exception as e:
        common.release_lock(user_id)
        common.show_error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
