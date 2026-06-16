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

import os
import sys


# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正

def get_item_master(item_id, item_type):
    """マスタファイルから特定の装備品情報を取得します。"""
    if item_type == "item":
        path = os.path.join(common.BASE_DIR, config.Config['item_file'])
    elif item_type == "def":
        path = os.path.join(common.BASE_DIR, config.Config['def_file'])
    else: # acs
        path = os.path.join(common.BASE_DIR, config.Config['acs_file'])
        
    if not os.path.exists(path):
        return None
        
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("<>")
            if parts and parts[0] == str(item_id):
                def get_val(lst, idx, default=""):
                    return lst[idx] if idx < len(lst) else default
                
                if item_type == "acs":
                    return {
                        "id": int(parts[0]),
                        "name": parts[1],
                        "gold": int(parts[2]),
                        "effect_id": int(get_val(parts, 3, 0)),
                        "bonus": {
                            "str": int(get_val(parts, 4, 0)),
                            "int": int(get_val(parts, 5, 0)),
                            "dex": int(get_val(parts, 6, 0)),
                            "vit": int(get_val(parts, 7, 0)),
                            "agi": int(get_val(parts, 8, 0)),
                            "mnd": int(get_val(parts, 9, 0)),
                            "lck": int(get_val(parts, 10, 0)),
                            "lp": int(get_val(parts, 11, 0))
                        },
                        "attrib": int(get_val(parts, 12, 0)),
                        "spare1": int(get_val(parts, 13, 0)),
                        "spare2": int(get_val(parts, 14, 0)),
                        "spare3": int(get_val(parts, 15, 0))
                    }
                else:
                    return {
                        "id": int(parts[0]),
                        "name": parts[1],
                        "power": int(parts[2]),
                        "gold": int(parts[3]),
                        "effect": int(get_val(parts, 4, 0))
                    }
    return None

def format_bonus(bonus_dict):
    """アクセサリーの能力値上昇を表示用の文字列に変換します。"""
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
    item_no_str = params.get("item_no", "").strip()
    
    if not user_id:
        common.show_error("ユーザーIDが指定されていません。")
        
    # ロック取得
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        item = common.item_load(user_id)
        if not chara or not item:
            common.release_lock(user_id)
            common.show_error("キャラクター情報が見つかりません。")
            
        # 倉庫データのロード
        souko_item = common.souko_load(user_id, "item")
        souko_def = common.souko_load(user_id, "def")
        souko_acs = common.souko_load(user_id, "acs")
        
        # 処理実行フラグ (保存が必要か)
        modified = False
        
        # 1. 武器の外し・装備・破棄
        if mode == "item_hazusi":
            equipped_id = chara.get("weapon_id", 0)
            if equipped_id and equipped_id != 0:
                if len(souko_item) >= config.Config['max_items']:
                    common.release_lock(user_id)
                    common.show_error("武器倉庫がいっぱいです！外せません。")
                
                master = get_item_master(equipped_id, "item")
                if not master:
                    master = {"id": equipped_id, "name": item["weapon"]["name"], "power": item["weapon"]["dmg"], "gold": 0, "effect": 0}
                    
                # 倉庫へ追加
                souko_item.append({
                    "id": master["id"],
                    "name": master["name"],
                    "power": master["power"],
                    "gold": master["gold"],
                    "effect": master.get("effect", 0)
                })
                # 装備リセット
                chara["weapon_id"] = 0
                item["weapon"] = {"name": "素手", "dmg": 0, "effect": 0}
                modified = True
                
        elif mode == "item_soubi" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_item):
                # 倉庫から取り出し
                target = souko_item.pop(idx)
                
                # 現在の装備を外して倉庫へ戻す
                equipped_id = chara.get("weapon_id", 0)
                if equipped_id and equipped_id != 0:
                    master = get_item_master(equipped_id, "item")
                    if not master:
                        master = {"id": equipped_id, "name": item["weapon"]["name"], "power": item["weapon"]["dmg"], "gold": 0, "effect": 0}
                    souko_item.append({
                        "id": master["id"],
                        "name": master["name"],
                        "power": master["power"],
                        "gold": master["gold"],
                        "effect": master.get("effect", 0)
                    })
                
                # 新しい装備を適用
                chara["weapon_id"] = target["id"]
                item["weapon"] = {
                    "name": target["name"],
                    "dmg": target["power"],
                    "effect": target.get("effect", 0)
                }
                modified = True
                
        elif mode == "item_delete" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_item):
                souko_item.pop(idx)
                modified = True
                
        # 2. 防具の外し・装備・破棄
        elif mode == "def_hazusi":
            equipped_id = chara.get("armor_id", 0)
            if equipped_id and equipped_id != 0:
                if len(souko_def) >= config.Config['max_defenses']:
                    common.release_lock(user_id)
                    common.show_error("防具倉庫がいっぱいです！外せません。")
                
                master = get_item_master(equipped_id, "def")
                if not master:
                    master = {"id": equipped_id, "name": item["armor"]["name"], "power": item["armor"]["def"], "gold": 0, "effect": 0}
                    
                souko_def.append({
                    "id": master["id"],
                    "name": master["name"],
                    "power": master["power"],
                    "gold": master["gold"],
                    "effect": master.get("effect", 0)
                })
                chara["armor_id"] = 0
                item["armor"] = {"name": "衣服", "def": 0, "effect": 0}
                modified = True
                
        elif mode == "def_soubi" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_def):
                target = souko_def.pop(idx)
                
                equipped_id = chara.get("armor_id", 0)
                if equipped_id and equipped_id != 0:
                    master = get_item_master(equipped_id, "def")
                    if not master:
                        master = {"id": equipped_id, "name": item["armor"]["name"], "power": item["armor"]["def"], "gold": 0, "effect": 0}
                    souko_def.append({
                        "id": master["id"],
                        "name": master["name"],
                        "power": master["power"],
                        "gold": master["gold"],
                        "effect": master.get("effect", 0)
                    })
                
                chara["armor_id"] = target["id"]
                item["armor"] = {
                    "name": target["name"],
                    "def": target["power"],
                    "effect": target.get("effect", 0)
                }
                modified = True
                
        elif mode == "def_delete" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_def):
                souko_def.pop(idx)
                modified = True
                
        # 3. 装飾品の外し・装備・破棄
        elif mode == "acs_hazusi":
            equipped_id = chara.get("accessory_id", 0)
            if equipped_id and equipped_id != 0:
                if len(souko_acs) >= config.Config['max_accessories']:
                    common.release_lock(user_id)
                    common.show_error("装飾品倉庫がいっぱいです！外せません。")
                
                master = get_item_master(equipped_id, "acs")
                if not master:
                    master = {
                        "id": equipped_id, "name": item["accessory"]["name"], "gold": 0, "effect_id": 0,
                        "bonus": item["accessory"]["bonus"], "attrib": item["accessory"]["attrib"],
                        "spare1": item["accessory"]["spare1"], "spare2": item["accessory"]["spare2"], "spare3": item["accessory"]["spare3"]
                    }
                    
                souko_acs.append(master)
                chara["accessory_id"] = 0
                item["accessory"] = {
                    "name": "なし",
                    "effect_id": 0,
                    "bonus": {"str": 0, "int": 0, "dex": 0, "vit": 0, "agi": 0, "mnd": 0, "lck": 0, "lp": 0},
                    "attrib": 0, "spare1": 0, "spare2": 0, "spare3": 0
                }
                modified = True
                
        elif mode == "acs_soubi" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_acs):
                target = souko_acs.pop(idx)
                
                equipped_id = chara.get("accessory_id", 0)
                if equipped_id and equipped_id != 0:
                    master = get_item_master(equipped_id, "acs")
                    if not master:
                        master = {
                            "id": equipped_id, "name": item["accessory"]["name"], "gold": 0, "effect_id": 0,
                            "bonus": item["accessory"]["bonus"], "attrib": item["accessory"]["attrib"],
                            "spare1": item["accessory"]["spare1"], "spare2": item["accessory"]["spare2"], "spare3": item["accessory"]["spare3"]
                        }
                    souko_acs.append(master)
                
                chara["accessory_id"] = target["id"]
                item["accessory"] = {
                    "name": target["name"],
                    "effect_id": target["effect_id"],
                    "bonus": target["bonus"],
                    "attrib": target["attrib"],
                    "spare1": target["spare1"],
                    "spare2": target["spare2"],
                    "spare3": target["spare3"]
                }
                modified = True
                
        elif mode == "acs_delete" and item_no_str:
            idx = int(item_no_str)
            if 0 <= idx < len(souko_acs):
                souko_acs.pop(idx)
                modified = True
                
        # 4. データ保存
        if modified:
            common.chara_regist(user_id, chara)
            common.item_regist(user_id, item)
            common.souko_regist(user_id, "item", souko_item)
            common.souko_regist(user_id, "def", souko_def)
            common.souko_regist(user_id, "acs", souko_acs)
            
        common.release_lock(user_id)
        
        # 5. 画面描画
        # 装飾品ボーナスの表示整形
        acs_bonus_str = format_bonus(item["accessory"]["bonus"])
        
        # 倉庫アクセサリーリストの上昇ステータス文字列化
        for a in souko_acs:
            a["bonus_str"] = format_bonus(a["bonus"])
            
        context = {
            "chara": chara,
            "item": item,
            "acs_bonus_str": acs_bonus_str,
            "souko_item": souko_item,
            "souko_def": souko_def,
            "souko_acs": souko_acs
        }
        common.render_template("souko.html", context)
        
    except Exception as e:
        common.release_lock(user_id)
        common.show_error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
