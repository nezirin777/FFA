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
FFA Python/CGI - 倉庫管理スクリプト (souko.py)
"""

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
from sub_def.crypto import get_session, token_check

def get_item_master(item_id, item_type):
    """種別に対応する装備マスターを共通読込処理で検索します。"""
    master_file = {
        "weapon": config.Config["weapon_file"],
        "armor": config.Config["armor_file"],
        "accessory": config.Config["accessory_file"],
    }.get(item_type)
    return common.find_master_record(master_file, item_id) if master_file else None


format_bonus = common.format_accessory_bonus

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    params = common.decode_params()
    mode = params.get("mode", "")
    state_changing_modes = {
        "weapon_remove", "weapon_equip", "weapon_delete",
        "armor_remove", "armor_equip", "armor_delete",
        "accessory_remove", "accessory_equip", "accessory_delete",
    }
    if mode in state_changing_modes:
        token_check(params, get_session())
    user_id = params.get("id", "").strip()
    # IDOR対策: 状態変更は本人のみ許可(ロック取得前にチェック)
    common.require_owner(user_id)
    item_no_str = params.get("item_no", "").strip()
    
    if not user_id:
        common.show_error("ユーザーIDが指定されていません。")
        
    # ロック取得
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        item = common.equipment_load(user_id)
        if not chara or not item:
            common.release_lock(user_id)
            common.show_error("キャラクター情報が見つかりません。")
            
        # 倉庫データのロード
        souko_weapon = common.souko_load(user_id, "weapon")
        souko_armor = common.souko_load(user_id, "armor")
        souko_accessory = common.souko_load(user_id, "accessory")
        souko_url = f"{config.Config['souko_script']}&id={user_id}"
        
        # 処理実行フラグ (保存が必要か)
        modified = False
        
        # 1. 武器の外し・装備・破棄
        if mode == "weapon_remove":
            equipped_id = chara.get("weapon_id", 0)
            if equipped_id and equipped_id != 0:
                if len(souko_weapon) >= config.Config['max_weapons']:
                    common.release_lock(user_id)
                    common.redirect_with_flash(souko_url, "武器倉庫がいっぱいです！外せません。", "error")
                
                master = get_item_master(equipped_id, "weapon")
                if not master:
                    master = {"id": equipped_id, "name": item["weapon"]["name"], "atk": item["weapon"]["atk"], "gold": 0, "hit_rate": 0}
                    
                # 倉庫へ追加
                souko_weapon.append({
                    "id": master["id"],
                    "name": master["name"],
                    "atk": master["atk"],
                    "gold": master["gold"],
                    "hit_rate": master.get("hit_rate", 0)
                })
                # 装備リセット
                chara["weapon_id"] = 0
                item["weapon"] = {"name": "素手", "atk": 0, "hit_rate": 0}
                modified = True
                
        elif mode == "weapon_equip" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_weapon):
                # 倉庫から取り出し
                target = souko_weapon.pop(idx)
                
                # 現在の装備を外して倉庫へ戻す
                equipped_id = chara.get("weapon_id", 0)
                if equipped_id and equipped_id != 0:
                    master = get_item_master(equipped_id, "weapon")
                    if not master:
                        master = {"id": equipped_id, "name": item["weapon"]["name"], "atk": item["weapon"]["atk"], "gold": 0, "hit_rate": 0}
                    souko_weapon.append({
                        "id": master["id"],
                        "name": master["name"],
                        "atk": master["atk"],
                        "gold": master["gold"],
                        "hit_rate": master.get("hit_rate", 0)
                    })
                
                # 新しい装備を適用
                chara["weapon_id"] = target["id"]
                item["weapon"] = {
                    "name": target["name"],
                    "atk": target["atk"],
                    "hit_rate": target.get("hit_rate", 0)
                }
                modified = True
                
        elif mode == "weapon_delete" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_weapon):
                souko_weapon.pop(idx)
                modified = True
                
        # 2. 防具の外し・装備・破棄
        elif mode == "armor_remove":
            equipped_id = chara.get("armor_id", 0)
            if equipped_id and equipped_id != 0:
                if len(souko_armor) >= config.Config['max_armors']:
                    common.release_lock(user_id)
                    common.redirect_with_flash(souko_url, "防具倉庫がいっぱいです！外せません。", "error")
                
                master = get_item_master(equipped_id, "armor")
                if not master:
                    master = {"id": equipped_id, "name": item["armor"]["name"], "defense": item["armor"]["defense"], "gold": 0, "evasion_rate": 0}
                    
                souko_armor.append({
                    "id": master["id"],
                    "name": master["name"],
                    "defense": master["defense"],
                    "gold": master["gold"],
                    "evasion_rate": master.get("evasion_rate", 0)
                })
                chara["armor_id"] = 0
                item["armor"] = {"name": "衣服", "defense": 0, "evasion_rate": 0}
                modified = True
                
        elif mode == "armor_equip" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_armor):
                target = souko_armor.pop(idx)
                
                equipped_id = chara.get("armor_id", 0)
                if equipped_id and equipped_id != 0:
                    master = get_item_master(equipped_id, "armor")
                    if not master:
                        master = {"id": equipped_id, "name": item["armor"]["name"], "defense": item["armor"]["defense"], "gold": 0, "evasion_rate": 0}
                    souko_armor.append({
                        "id": master["id"],
                        "name": master["name"],
                        "defense": master["defense"],
                        "gold": master["gold"],
                        "evasion_rate": master.get("evasion_rate", 0)
                    })
                
                chara["armor_id"] = target["id"]
                item["armor"] = {
                    "name": target["name"],
                    "defense": target["defense"],
                    "evasion_rate": target.get("evasion_rate", 0)
                }
                modified = True
                
        elif mode == "armor_delete" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_armor):
                souko_armor.pop(idx)
                modified = True
                
        # 3. 装飾品の外し・装備・破棄
        elif mode == "accessory_remove":
            equipped_id = chara.get("accessory_id", 0)
            if equipped_id and equipped_id != 0:
                if len(souko_accessory) >= config.Config['max_accessories']:
                    common.release_lock(user_id)
                    common.redirect_with_flash(souko_url, "装飾品倉庫がいっぱいです！外せません。", "error")
                
                master = get_item_master(equipped_id, "accessory")
                if not master:
                    master = {
                        "id": equipped_id, "name": item["accessory"]["name"], "gold": 0, "effect_id": 0,
                        "bonus": item["accessory"]["bonus"], "hit_rate": item["accessory"]["hit_rate"],
                        "evasion_rate": item["accessory"]["evasion_rate"], "special_rate": item["accessory"]["special_rate"],
                        "description": item["accessory"].get("description", "")
                    }
                    
                souko_accessory.append(master)
                chara["accessory_id"] = 0
                item["accessory"] = {
                    "name": "なし",
                    "effect_id": 0,
                    "bonus": {"str": 0, "int": 0, "mnd": 0, "vit": 0, "dex": 0, "agi": 0, "cha": 0, "karma": 0},
                    "hit_rate": 0, "evasion_rate": 0, "special_rate": 0, "description": ""
                }
                modified = True
                
        elif mode == "accessory_equip" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_accessory):
                target = souko_accessory.pop(idx)
                
                equipped_id = chara.get("accessory_id", 0)
                if equipped_id and equipped_id != 0:
                    master = get_item_master(equipped_id, "accessory")
                    if not master:
                        master = {
                            "id": equipped_id, "name": item["accessory"]["name"], "gold": 0, "effect_id": 0,
                            "bonus": item["accessory"]["bonus"], "hit_rate": item["accessory"]["hit_rate"],
                            "evasion_rate": item["accessory"]["evasion_rate"], "special_rate": item["accessory"]["special_rate"],
                            "description": item["accessory"].get("description", "")
                        }
                    souko_accessory.append(master)
                
                chara["accessory_id"] = target["id"]
                target_description = target.get("description") or common.accessory_description(target, target.get("id"))
                item["accessory"] = {
                    "name": target["name"],
                    "effect_id": target.get("effect_id", 0),
                    "bonus": target["bonus"],
                    "hit_rate": target.get("hit_rate", 0),
                    "evasion_rate": target.get("evasion_rate", 0),
                    "special_rate": target.get("special_rate", 0),
                    "description": target_description
                }
                modified = True
                
        elif mode == "accessory_delete" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_accessory):
                souko_accessory.pop(idx)
                modified = True
                
        # 4. データ保存
        if modified:
            common.save_user_sections(
                user_id,
                chara=chara,
                equipment=item,
                souko_weapon=souko_weapon,
                souko_armor=souko_armor,
                souko_accessory=souko_accessory,
            )
            
        common.release_lock(user_id)
        
        # 5. 画面描画
        # 装飾品ボーナスの表示整形
        acs_bonus_str = common.accessory_description(item["accessory"], chara.get("accessory_id", 0)) or format_bonus(item["accessory"]["bonus"])
        
        # 倉庫アクセサリーリストの上昇ステータス文字列化
        for a in souko_accessory:
            a["bonus_str"] = common.accessory_description(a, a.get("id", 0)) or format_bonus(a["bonus"])
            
        context = {
            "chara": chara,
            "equipment": item,
            "acs_bonus_str": acs_bonus_str,
            "souko_weapon": souko_weapon,
            "souko_armor": souko_armor,
            "souko_accessory": souko_accessory
        }
        common.render_template("souko.html", context)
        
    except Exception as e:
        common.release_lock(user_id)
        common.show_error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
