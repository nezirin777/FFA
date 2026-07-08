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
import json

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

DEFAULT_WINNER = {
    "id": "sys",
    "site": "サイト",
    "url": "URL",
    "name": "無名の剣士",
    "sex": 1,
    "img": 0,
    "str": 10,
    "int": 10,
    "dex": 10,
    "vit": 10,
    "agi": 10,
    "mnd": 10,
    "lck": 10,
    "lp": 0,
    "job": 0,
    "hp": 1000,
    "max_hp": 1000,
    "level": 1,
    "unused21": 0,
    "unused22": 0,
    "comment": "無名",
    "equipped_item": {
        "weapon": { "name": "素手", "dmg": 0, "effect": 0 },
        "armor": { "name": "衣服", "def": 0, "effect": 0 },
        "accessory": {
            "name": "なし",
            "effect_id": 0,
            "bonus": {
                "str": 0, "int": 0, "dex": 0, "vit": 0, "agi": 0, "mnd": 0, "lck": 0, "lp": 0
            },
            "attrib": 0,
            "spare1": 0,
            "spare2": 0,
            "spare3": 0
        }
    },
    "unused30": 0,
    "host": "127.0.0.1",
    "job_level": 0,
    "last_challenger": {
        "id": "sys",
        "name": "無名の剣士",
        "site": "サイト",
        "url": "URL"
    },
    "win_count": 0,
    "max_win_count": 0,
    "max_win_id": "sys",
    "max_win_name": "無名の剣士",
    "max_win_site": "サイト",
    "max_win_url": "URL",
    "gold": 100
}

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
                winner = DEFAULT_WINNER
            else:
                try:
                    with open(winner_path, "r", encoding="utf-8") as f:
                        winner = json.load(f)
                except Exception:
                    winner = DEFAULT_WINNER
            
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
                winner = {
                    "id": chara["id"],
                    "site": chara["site"],
                    "url": chara["url"],
                    "name": chara["name"],
                    "sex": int(chara["sex"]),
                    "img": int(chara["img"]),
                    "str": int(chara["str"]),
                    "int": int(chara["int"]),
                    "dex": int(chara["dex"]),
                    "vit": int(chara["vit"]),
                    "agi": int(chara["agi"]),
                    "mnd": int(chara["mnd"]),
                    "lck": int(chara["lck"]),
                    "lp": int(chara["lp"]),
                    "job": int(chara["job"]),
                    "hp": int(chara["hp"]),
                    "max_hp": int(chara["max_hp"]),
                    "level": int(chara["level"]),
                    "unused21": int(chara.get("unused21", 0)),
                    "unused22": int(chara.get("unused22", 0)),
                    "comment": chara["comment"],
                    "equipped_item": {
                        "weapon": {
                            "name": item["weapon"]["name"],
                            "dmg": int(item["weapon"]["dmg"]),
                            "effect": int(item["weapon"]["effect"])
                        },
                        "armor": {
                            "name": item["armor"]["name"],
                            "def": int(item["armor"]["def"]),
                            "effect": int(item["armor"]["effect"])
                        },
                        "accessory": {
                            "name": item["accessory"]["name"],
                            "effect_id": int(item["accessory"].get("effect_id", 0)),
                            "bonus": {
                                "str": int(item["accessory"]["bonus"]["str"]),
                                "int": int(item["accessory"]["bonus"]["int"]),
                                "dex": int(item["accessory"]["bonus"]["dex"]),
                                "vit": int(item["accessory"]["bonus"]["vit"]),
                                "agi": int(item["accessory"]["bonus"]["agi"]),
                                "mnd": int(item["accessory"]["bonus"]["mnd"]),
                                "lck": int(item["accessory"]["bonus"]["lck"]),
                                "lp": int(item["accessory"]["bonus"]["lp"])
                            },
                            "attrib": int(item["accessory"].get("attrib", 0)),
                            "spare1": int(item["accessory"].get("spare1", 0)),
                            "spare2": int(item["accessory"].get("spare2", 0)),
                            "spare3": 0
                        }
                    },
                    "unused30": int(chara.get("unused30", 0)),
                    "host": chara["host"],
                    "job_level": int(chara["job_level"]),
                    "last_challenger": {
                        "id": winner.get("id", "sys"),
                        "name": winner.get("name", "無名の剣士"),
                        "site": winner.get("site", "サイト"),
                        "url": winner.get("url", "URL")
                    },
                    "win_count": 1, # 連勝回数を1にリセット
                    "max_win_count": int(winner.get("max_win_count", 0)),
                    "max_win_id": winner.get("max_win_id", "sys"),
                    "max_win_name": winner.get("max_win_name", "無名の剣士"),
                    "max_win_site": winner.get("max_win_site", "不明"),
                    "max_win_url": winner.get("max_win_url", ""),
                    "gold": gold_gained
                }
                
                comment += f'<span class="green" style="font-size: 1.25em;">見事に勝利し、新王者になりました！</span><br>'
                comment += f'経験値 {exp_gained} と賞金 {gold_gained} ゴールドを獲得しました。<br>'
            else:
                # 挑戦者の敗北 ➔ 王者の防衛成功
                winner["win_count"] += 1
                
                if winner["win_count"] > winner["max_win_count"]:
                    winner["max_win_count"] = winner["win_count"]
                    winner["max_win_id"] = winner["id"]
                    winner["max_win_name"] = winner["name"]
                    winner["max_win_site"] = winner.get("site", "不明")
                    winner["max_win_url"] = winner.get("url", "")
                
                # 防衛成功につき、王者のHPを最大HPの10%分回復
                winner["hp"] += int(winner["max_hp"] / 10)
                if winner["hp"] > winner["max_hp"]:
                    winner["hp"] = winner["max_hp"]
                    
                # 最後の挑戦者情報として自分を記録
                winner["last_challenger"] = {
                    "id": chara["id"],
                    "name": chara["name"],
                    "site": chara["site"],
                    "url": chara["url"]
                }
                
                comment += f'<span class="red" style="font-size: 1.25em;">王者の防衛に阻まれ、敗北しました・・・</span><br>'
                comment += f'経験値 {exp_gained} を獲得しました。<br>'

            # 王者データの保存
            with open(winner_path, "w", encoding="utf-8") as f:
                json.dump(winner, f, ensure_ascii=False, indent=2)

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
