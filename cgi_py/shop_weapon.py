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
FFA Python/CGI - 武器屋スクリプト (shop_weapon.py)
"""

import os


# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正

def load_available_weapons(job_idx):
    """共通武器マスターから、現在の職業が購入可能な商品を抽出します。"""
    return common.master_records_for_job(config.Config["weapon_file"], job_idx)

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
        
    # 宿屋などと同様、処理開始時にロックを取得
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        item = common.equipment_load(user_id)
        if not chara or not item:
            common.release_lock(user_id)
            common.show_error("キャラクター情報が見つかりません。")
            
        # 共通情報
        job_idx = chara["job"]
        job_name = config.Config['chara_jobs'].get(job_idx, "不明な職業")
        weapon_shop_url = f"{config.Config['shop_weapon_script']}&id={user_id}"
        
        # 1. 購入処理
        if mode == "buy":
            item_no = params.get("item_no", "").strip()
            if not item_no:
                common.release_lock(user_id)
                common.redirect_with_flash(weapon_shop_url, "購入する商品が選択されていません。", "error")
                
            weapons = load_available_weapons(job_idx)
            selected_weapon = next((weapon for weapon in weapons if str(weapon["no"]) == item_no), None)
            
            if not selected_weapon:
                common.release_lock(user_id)
                common.redirect_with_flash(weapon_shop_url, "指定された商品は販売されていません。", "error")
                
            # 所持金チェック
            if chara["gold"] < selected_weapon["gold"]:
                common.release_lock(user_id)
                common.redirect_with_flash(weapon_shop_url, "所持金が足りません。", "error")
                
            # 倉庫の空きチェック
            souko = common.souko_load(user_id, "weapon")
            if len(souko) >= config.Config['max_weapons']:
                common.release_lock(user_id)
                common.redirect_with_flash(weapon_shop_url, f"武器倉庫がいっぱいです！(最大 {config.Config['max_weapons']} 個)", "error")
                
            # 購入処理実行
            chara["gold"] -= selected_weapon["gold"]
            chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            
            # 倉庫に追加
            new_weapon = {
                "id": selected_weapon["no"],
                "name": selected_weapon["name"],
                "atk": selected_weapon["atk"],
                "gold": selected_weapon["gold"],
                "hit_rate": selected_weapon["hit_rate"]
            }
            souko.append(new_weapon)
            
            # 保存
            common.save_user_sections(user_id, chara=chara, souko_weapon=souko)
            common.release_lock(user_id)
            
            # 取引結果はトーストで通知し、武器屋へ戻す
            common.redirect_with_flash(
                weapon_shop_url,
                f"武器 {selected_weapon['name']} を {selected_weapon['gold']} G で購入しました。購入した武器は倉庫に送られました。",
                "success",
            )
            return
            
        # 2. 売却（下取り）処理
        elif mode == "sell":
            equipped_id = chara.get("weapon_id", 0)
            if not equipped_id or equipped_id == 0:
                common.release_lock(user_id)
                common.redirect_with_flash(weapon_shop_url, "売却できる武器を装備していません。", "error")
                
            # マスタから武器の情報を取得して価格を決定
            master_item = common.find_master_record(config.Config["weapon_file"], equipped_id)
            if not master_item:
                # マスタに見つからない場合はデフォルト価格で下取り
                master_item = {"name": item["weapon"]["name"], "gold": 0}
                
            sell_gold = int(master_item["gold"] / 3) * 2
            
            chara["gold"] += sell_gold
            if chara["gold"] > config.Config['max_gold']:
                chara["gold"] = config.Config['max_gold']
                
            # 装備をリセット
            chara["weapon_id"] = 0
            item["weapon"] = {"name": "素手", "atk": 0, "hit_rate": 0}
            
            # 保存
            common.save_user_sections(user_id, chara=chara, equipment=item)
            common.release_lock(user_id)
            
            # 取引結果はトーストで通知し、武器屋へ戻す
            common.redirect_with_flash(
                weapon_shop_url,
                f"装備していた武器 {master_item['name']} を下取りに出しました。売却額 {sell_gold} G を手に入れました！",
                "success",
            )
            return
            
        # 3. 武器屋画面表示 (mode == "")
        else:
            common.release_lock(user_id)
            
            # 現在装備中の武器情報
            equipped_id = chara.get("weapon_id", 0)
            master_item = common.find_master_record(config.Config["weapon_file"], equipped_id)
            
            if master_item:
                equipped_item = {
                    "id": equipped_id,
                    "name": master_item["name"],
                    "performance": master_item["atk"],
                    "sell_gold": int(master_item["gold"] / 3) * 2
                }
            else:
                equipped_item = {
                    "id": 0,
                    "name": "素手",
                    "performance": 0,
                    "sell_gold": 0
                }
                
            # 販売リストの取得
            catalog_items = [
                {
                    "no": weapon["no"],
                    "name": weapon["name"],
                    "performance": weapon["atk"],
                    "gold": weapon["gold"],
                }
                for weapon in load_available_weapons(job_idx)
            ]
            
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
                "catalog_items": catalog_items,
                "post_url": config.Config['shop_weapon_script']
            }
            common.render_template("shop_trade.html", context)
            
    except Exception as e:
        common.release_lock(user_id)
        common.show_error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
