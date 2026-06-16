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
FFA Python/CGI - 通常王者バトルスクリプト (battle.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
import os
import time
import random

# 共通モジュールと設定モジュールのインポート
try:
    import config
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from sub_def import battle_logic
except ImportError:
    from . import config
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from sub_def import battle_logic

def parse_cookie_user(cookie_str):
    """クッキー文字列からIDとパスワードを抽出します"""
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

def parse_winner_data(winner_str):
    """王者ファイルデータを解析し、キャラクター辞書と生partsを返します"""
    parts = winner_str.strip().split("<>")
    if parts and parts[-1] == "":
        parts = parts[:-1]
        
    def get_val(lst, idx, default=""):
        return lst[idx] if idx < len(lst) else default
        
    def to_i(val):
        try: return int(val)
        except: return 0

    winner_char = {
        "id": get_val(parts, 0, "sys"),
        "site": get_val(parts, 1),
        "url": get_val(parts, 2),
        "name": get_val(parts, 3, "無名の剣士"),
        "sex": to_i(get_val(parts, 4)),
        "img": to_i(get_val(parts, 5)),
        "str": to_i(get_val(parts, 6)),
        "int": to_i(get_val(parts, 7)),
        "dex": to_i(get_val(parts, 8)),
        "vit": to_i(get_val(parts, 9)),
        "agi": to_i(get_val(parts, 10)),
        "mnd": to_i(get_val(parts, 11)),
        "lck": to_i(get_val(parts, 12)),
        "lp": to_i(get_val(parts, 13)),
        "job": to_i(get_val(parts, 14)),
        "hp": to_i(get_val(parts, 15)),
        "max_hp": to_i(get_val(parts, 16)),
        "level": to_i(get_val(parts, 17)),
        "comment": get_val(parts, 20),
        "host": get_val(parts, 37),
        "job_level": to_i(get_val(parts, 38)),
        "win_count": to_i(get_val(parts, 43)),
        "max_win_count": to_i(get_val(parts, 44)),
        "max_win_id": get_val(parts, 45),
        "max_win_name": get_val(parts, 46),
        "gold": to_i(get_val(parts, 49)), # 賞金
    }
    
    winner_item = {
        "weapon": {
            "name": get_val(parts, 21, "素手"),
            "dmg": to_i(get_val(parts, 22)),
            "effect": to_i(get_val(parts, 23))
        },
        "armor": {
            "name": get_val(parts, 24, "衣服"),
            "def": to_i(get_val(parts, 25)),
            "effect": to_i(get_val(parts, 26))
        },
        "accessory": {
            "name": get_val(parts, 27, "なし"),
            "effect_id": to_i(get_val(parts, 50)),
            "bonus": {
                "str": to_i(get_val(parts, 28)),
                "int": to_i(get_val(parts, 29)),
                "dex": to_i(get_val(parts, 30)),
                "vit": to_i(get_val(parts, 31)),
                "agi": to_i(get_val(parts, 32)),
                "mnd": to_i(get_val(parts, 33)),
                "lck": to_i(get_val(parts, 34)),
                "lp": to_i(get_val(parts, 35)),
            },
            "attrib": to_i(get_val(parts, 51)),
            "spare1": to_i(get_val(parts, 52)),
            "spare2": to_i(get_val(parts, 53)),
            "spare3": 0
        }
    }
    
    winner_char["equipped_item"] = winner_item
    return winner_char, parts

def main():
    # 1. メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    # 2. パラメータの取得
    params = common.decode_params()
    user_id = params.get("id", "").strip()

    if not user_id:
        common.show_error("ログイン情報が不足しています。")

    # クッキー認証
    cookie_str = common.get_cookie(config.Config['cookie_name'])
    c_id, c_pass = parse_cookie_user(cookie_str)
    
    # 挑戦者（自分）のデータをロックしてロード
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        if not chara:
            common.release_lock(user_id)
            common.show_error("キャラクターが見つかりません。")
            
        if c_id == user_id and c_pass != chara["pass"]:
            common.release_lock(user_id)
            common.show_error("パスワード認証に失敗しました。")

        # 待機時間（クールダウン）チェック
        now = int(time.time())
        ltime = now - chara["last_time"]
        if ltime < config.Config['battle_cooldown']:
            common.release_lock(user_id)
            common.show_error(f"まだ行動できません！ (あと {config.Config['battle_cooldown'] - ltime} 秒)")

        # 王者データのロックを取得してロード
        common.get_lock("winner")
        try:
            winner_path = os.path.join(common.BASE_DIR, config.Config['winner_file'])
            if not os.path.exists(winner_path):
                # デフォルトのダミー王者データ
                winner_raw = "sys<>サイト<>URL<>無名の剣士<>1<>0<>10<>10<>10<>10<>10<>10<>10<>0<>0<>1000<>1000<>1<>0<>0<>無名<>素手<>0<>0<>衣服<>0<>0<>なし<>0<>0<>0<>0<>0<>0<>0<>0<>0<>127.0.0.1<>0<>sys<>無名の剣士<>サイト<>URL<>0<>0<>sys<>無名の剣士<>サイト<>URL<>100<>0<>0<>0<>"
            else:
                with open(winner_path, "r", encoding="utf-8") as f:
                    winner_raw = f.read()
            
            winner, raw_parts = parse_winner_data(winner_raw)
            
            if winner["id"] == chara["id"]:
                common.release_lock("winner")
                common.release_lock(user_id)
                common.show_error("自身が王者のため、挑戦できません。")

            # 所持アイテム・装備のロード
            item = common.item_load(user_id)
            if not item:
                common.release_lock("winner")
                common.release_lock(user_id)
                common.show_error("アイテムデータが読み込めません。")

            # 3. 戦闘実行 (BattleSimulator - 対人戦)
            simulator = battle_logic.BattleSimulator("battle", chara, item, winner, is_player_enemy=True)
            win, logs = simulator.simulate()

            # 4. 戦闘結果の集計と更新
            comment = ""
            gold_gained = 0
            exp_gained = 0

            # 戦闘後の残りHP復元
            restored_hp = simulator.state.khp + random.randint(0, max(0, chara["vit"] - 1))
            if restored_hp > chara["max_hp"]:
                restored_hp = chara["max_hp"]
            if restored_hp <= 0:
                restored_hp = chara["max_hp"] # 敗北時は全回復
            chara["hp"] = restored_hp

            restored_whp = simulator.state.mhp + random.randint(0, max(0, winner["vit"] - 1))
            if restored_whp > winner["max_hp"]:
                restored_whp = winner["max_hp"]
            if restored_whp <= 0:
                restored_whp = winner["max_hp"]
            winner["hp"] = restored_whp

            gold_gained = winner["gold"]
            exp_gained = config.Config['base_exp'] # 対人戦の基本経験値

            if win == 1 or win == 2:
                # 挑戦者の勝利または引き分け ➔ 挑戦者が新しい王者になる！
                chara["gold"] += gold_gained
                if chara["gold"] > config.Config['max_gold']:
                    chara["gold"] = config.Config['max_gold']

                # 新しい王者レコードを組み立てる
                new_parts = [
                    chara["id"], chara["site"], chara["url"], chara["name"], str(chara["sex"]), str(chara["img"]),
                    str(chara["str"]), str(chara["int"]), str(chara["dex"]), str(chara["vit"]), str(chara["agi"]),
                    str(chara["mnd"]), str(chara["lck"]), str(chara["lp"]), str(chara["job"]), str(chara["hp"]),
                    str(chara["max_hp"]), str(chara["level"]), str(chara["unused21"]), str(chara["unused22"]), chara["comment"],
                    item["weapon"]["name"], str(item["weapon"]["dmg"]), str(item["weapon"]["effect"]),
                    item["armor"]["name"], str(item["armor"]["def"]), str(item["armor"]["effect"]),
                    item["accessory"]["name"], str(item["accessory"]["bonus"]["str"]), str(item["accessory"]["bonus"]["int"]),
                    str(item["accessory"]["bonus"]["dex"]), str(item["accessory"]["bonus"]["vit"]), str(item["accessory"]["bonus"]["agi"]),
                    str(item["accessory"]["bonus"]["mnd"]), str(item["accessory"]["bonus"]["lck"]), str(item["accessory"]["bonus"]["lp"]),
                    str(chara["unused30"]), chara["host"], str(chara["job_level"]),
                    winner["id"], winner["name"], winner["site"], winner["url"],
                    "1", # 連勝回数を1にリセット
                    str(winner["max_win_count"]), winner["max_win_id"], winner["max_win_name"],
                    winner.get("max_win_site", "不明"), winner.get("max_win_url", ""),
                    str(gold_gained),
                    str(item["accessory"]["effect_id"]), str(item["accessory"]["attrib"]), str(item["accessory"]["spare1"])
                ]
                new_winner_str = "<>".join(new_parts) + "<>\n"
                
                comment += f'<font color="{config.Config['color_green']}" size=5>見事に勝利し、新王者になりました！</font><br>'
                comment += f'経験値 {exp_gained} と賞金 {gold_gained} ゴールドを獲得しました。<br>'
            else:
                # 挑戦者の敗北 ➔ 王者の防衛成功
                winner["win_count"] += 1
                
                if winner["win_count"] > winner["max_win_count"]:
                    winner["max_win_count"] = winner["win_count"]
                    winner["max_win_id"] = winner["id"]
                    winner["max_win_name"] = winner["name"]
                
                # 防衛成功につき、王者のHPを最大HPの10%分回復
                winner["hp"] += int(winner["max_hp"] / 10)
                if winner["hp"] > winner["max_hp"]:
                    winner["hp"] = winner["max_hp"]
                    
                # 最後の挑戦者情報として自分を記録
                raw_parts[15] = str(winner["hp"])
                raw_parts[43] = str(winner["win_count"])
                raw_parts[44] = str(winner["max_win_count"])
                raw_parts[45] = winner["max_win_id"]
                raw_parts[46] = winner["max_win_name"]
                
                raw_parts[40] = chara["id"]
                raw_parts[41] = chara["name"]
                raw_parts[42] = chara["site"]
                raw_parts[43] = chara["url"]
                
                new_winner_str = "<>".join(raw_parts) + "<>\n"
                
                comment += f'<font color="{config.Config['color_red']}" size=5>王者の防衛に阻まれ、敗北しました・・・</font><br>'
                comment += f'経験値 {exp_gained} を獲得しました。<br>'

            # 王者データの保存
            with open(winner_path, "w", encoding="utf-8") as f:
                f.write(new_winner_str)

        finally:
            common.release_lock("winner")

        # レベルアップ処理
        syoku = common.syoku_load(user_id)
        if syoku is None:
            syoku = {}
        lv_comment, lvup_count = battle_logic.process_levelup(chara, exp_gained, syoku)
        comment += lv_comment

        # 最終行動時間を更新
        chara["last_time"] = now
        chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")

        # セーブ
        common.chara_regist(user_id, chara)
        common.syoku_regist(user_id, syoku)

    finally:
        common.release_lock(user_id)

    # 5. 結果画面のレンダリング
    context = {
        "chara": chara,
        "enemy_name": winner["name"],
        "logs": logs,
        "win": win,
        "comment": comment,
        "gold_gained": gold_gained if win in [1, 2] else 0,
        "exp_gained": exp_gained,
        "mode": "battle"
    }
    common.render_template("monster_result.html", context)

if __name__ == "__main__":
    main()
