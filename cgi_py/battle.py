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

parse_cookie_user = common.parse_cookie_user

DEFAULT_WINNER = {
    "id": "sys",
    "name": "無名の剣士",
    "sex": 1,
    "img": 0,
    "str": 10,
    "int": 10,
    "mnd": 10,
    "vit": 10,
    "dex": 10,
    "agi": 10,
    "cha": 10,
    "karma": 0,
    "job": 0,
    "hp": 1000,
    "max_hp": 1000,
    "level": 1,
    "battle_count": 0,
    "battle_win_count": 0,
    "comment": "無名",
    "equipped_item": {
        "weapon": { "name": "素手", "atk": 0, "hit_rate": 0 },
        "armor": { "name": "衣服", "defense": 0, "evasion_rate": 0 },
        "accessory": {
            "name": "なし",
            "effect_id": 0,
            "bonus": {
                "str": 0, "int": 0, "mnd": 0, "vit": 0, "dex": 0, "agi": 0, "cha": 0, "karma": 0
            },
            "hit_rate": 0,
            "evasion_rate": 0,
            "special_rate": 0,
            "description": ""
        }
    },
    "tactic_id": 0,
    "host": "127.0.0.1",
    "job_level": 0,
    "last_challenger": {
        "id": "sys",
        "name": "無名の剣士"
    },
    "win_count": 0,
    "max_win_count": 0,
    "max_win_id": "sys",
    "max_win_name": "無名の剣士",
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
            
        if c_id != user_id or c_pass != chara["pass"]:
            common.release_lock(user_id)
            common.show_error("パスワード認証に失敗しました。")

        # 待機時間（クールダウン）チェック
        now = int(time.time())
        ltime = now - chara["last_time"]
        if ltime < config.Config['pvp_race_cooldown_seconds']:
            common.release_lock(user_id)
            common.show_error(f"まだ行動できません！ (あと {config.Config['pvp_race_cooldown_seconds'] - ltime} 秒)")

        # 王者データのロックを取得してロード
        common.get_lock("winner")
        try:
            winner_path = os.path.join(common.BASE_DIR, config.Config['champion_file'])
            if not os.path.exists(winner_path):
                winner = DEFAULT_WINNER
            else:
                try:
                    with open(winner_path, "r", encoding="utf-8") as f:
                        winner = common.decode_html_entities(json.load(f))
                        winner.pop("site", None)
                        winner.pop("url", None)
                        winner.pop("max_win_site", None)
                        winner.pop("max_win_url", None)
                        if isinstance(winner.get("last_challenger"), dict):
                            winner["last_challenger"].pop("site", None)
                            winner["last_challenger"].pop("url", None)
                except Exception:
                    winner = DEFAULT_WINNER
            
            if winner["id"] == chara["id"]:
                common.release_lock("winner")
                common.release_lock(user_id)
                common.show_error("自身が王者のため、挑戦できません。")

            # 所持アイテム・装備のロード
            item = common.equipment_load(user_id)
            if not item:
                common.release_lock("winner")
                common.release_lock(user_id)
                common.show_error("アイテムデータが読み込めません。")

            # 3. 戦闘実行 (BattleSimulator - 対人戦)
            simulator = battle_logic.BattleSimulator("battle", chara, item, winner, is_player_enemy=True)
            # 対人戦の賞金は旧版 winner[50]。盗み技の基準額にする。
            simulator.state.gold_base = max(0, int(winner.get("gold", 0)))
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

            gold_gained = int(winner["gold"]) + simulator.state.gold_reward_bonus
            gold_gained = max(0, gold_gained - simulator.state.gold_reward_penalty)

            # 旧版 wbattle.pl の経験値計算。
            # 勝利・引き分けは相手レベル×基本値、敗北時は相手レベルそのもの。
            opponent_level = max(1, int(winner.get("level", 1)))
            if win in (1, 2):
                exp_gained = opponent_level * config.Config["pvp_base_exp"]
            else:
                exp_gained = opponent_level

            # 旧版の対人戦績は結果分岐より先に挑戦者へ反映する。
            chara["battle_count"] = int(chara.get("battle_count", 0)) + 1
            if win == 1:
                chara["win_count"] = int(chara.get("win_count", 0)) + 1

            # 旧版の battle.cgi と同じく、チャンプ戦を終えたら
            # レジェンドプレイスの挑戦権を新しい攻略開始状態へ戻す。
            # これがないと、途中階層で街へ戻った後にチャンプへ挑戦しても
            # boss_flag が残り、レジェンドプレイスへ再入場できなくなる。
            chara["boss_flag"] = config.Config["legend_progress_reset_value"]

            # 旧版 battle.cgi と同じく、対人戦終了後は修行回数を補充する。
            chara["battle_limit"] = config.Config["training_battle_limit"]

            if win == 1 or win == 2:
                # 挑戦者の勝利または引き分け ➔ 挑戦者が新しい王者になる！
                chara["gold"] += gold_gained
                if chara["gold"] > config.Config['max_gold']:
                    chara["gold"] = config.Config['max_gold']
                if chara["gold"] < 0:
                    chara["gold"] = 0

                # 旧版は新王者の賞金を、旧王者の連勝数・挑戦者レベル・賞金係数から再計算する。
                new_winner_gold = int(
                    winner.get("win_count", 0)
                    * chara.get("level", 1)
                    * config.Config["battle_reward_factor"]
                )

                # 新しい王者レコードを組み立てる
                winner = {
                    "id": chara["id"],
                    "name": chara["name"],
                    "sex": int(chara["sex"]),
                    "img": int(chara["img"]),
                    "str": int(chara["str"]),
                    "int": int(chara["int"]),
                    "mnd": int(chara["mnd"]),
                    "vit": int(chara["vit"]),
                    "dex": int(chara["dex"]),
                    "agi": int(chara["agi"]),
                    "cha": int(chara["cha"]),
                    "karma": int(chara["karma"]),
                    "job": int(chara["job"]),
                    "hp": int(chara["hp"]),
                    "max_hp": int(chara["max_hp"]),
                    "level": int(chara["level"]),
                    "battle_count": int(chara.get("battle_count", 0)),
                    "battle_win_count": int(chara.get("win_count", 0)),
                    "comment": chara["comment"],
                    "equipped_item": {
                        "weapon": {
                            "name": item["weapon"]["name"],
                            "atk": int(item["weapon"]["atk"]),
                            "hit_rate": int(item["weapon"]["hit_rate"])
                        },
                        "armor": {
                            "name": item["armor"]["name"],
                            "defense": int(item["armor"]["defense"]),
                            "evasion_rate": int(item["armor"]["evasion_rate"])
                        },
                        "accessory": {
                            "name": item["accessory"]["name"],
                            "effect_id": int(item["accessory"].get("effect_id", 0)),
                            "bonus": {
                                "str": int(item["accessory"]["bonus"]["str"]),
                                "int": int(item["accessory"]["bonus"]["int"]),
                                "mnd": int(item["accessory"]["bonus"]["mnd"]),
                                "vit": int(item["accessory"]["bonus"]["vit"]),
                                "dex": int(item["accessory"]["bonus"]["dex"]),
                                "agi": int(item["accessory"]["bonus"]["agi"]),
                                "cha": int(item["accessory"]["bonus"]["cha"]),
                                "karma": int(item["accessory"]["bonus"]["karma"])
                            },
                            "hit_rate": int(item["accessory"].get("hit_rate", 0)),
                            "evasion_rate": int(item["accessory"].get("evasion_rate", 0)),
                            "special_rate": int(item["accessory"].get("special_rate", 0)),
                            "description": common.accessory_description(item.get("accessory", {}), chara.get("accessory_id", 0))
                        }
                    },
                    "tactic_id": int(chara.get("tactic_id", 0)),
                    "host": chara["host"],
                    "job_level": int(chara["job_level"]),
                    "last_challenger": {
                        "id": winner.get("id", "sys"),
                        "name": winner.get("name", "無名の剣士")
                    },
                    "win_count": 1, # 連勝回数を1にリセット
                    "max_win_count": int(winner.get("max_win_count", 0)),
                    "max_win_id": winner.get("max_win_id", "sys"),
                    "max_win_name": winner.get("max_win_name", "無名の剣士"),
                    "gold": new_winner_gold
                }
                
                comment += f'<span class="green u-text-large">見事に勝利し、新王者になりました！</span><br>'
                comment += f'経験値 {exp_gained} と賞金 {gold_gained} ゴールドを獲得しました。<br>'
            else:
                # 挑戦者の敗北 ➔ 王者の防衛成功
                # 旧版の敗北時処理は挑戦者の所持金を半分にする。
                chara["gold"] = max(0, int(chara["gold"] / 2))
                winner["win_count"] += 1
                
                if winner["win_count"] > winner["max_win_count"]:
                    winner["max_win_count"] = winner["win_count"]
                    winner["max_win_id"] = winner["id"]
                    winner["max_win_name"] = winner["name"]
                
                # 防衛成功につき、王者のHPを最大HPの10%分回復
                winner["hp"] += int(winner["max_hp"] / 10)
                if winner["hp"] > winner["max_hp"]:
                    winner["hp"] = winner["max_hp"]

                # 防衛成功時は王者側の次回賞金を連勝数分だけ積み上げる。
                winner["gold"] = int(winner.get("gold", 0)) + int(
                    winner["win_count"]
                    * chara.get("level", 1)
                    * config.Config["battle_reward_factor"]
                )
                    
                # 最後の挑戦者情報として自分を記録
                winner["last_challenger"] = {
                    "id": chara["id"],
                    "name": chara["name"]
                }
                
                comment += f'<span class="red u-text-large">王者の防衛に阻まれ、敗北しました・・・</span><br>'
                comment += f'経験値 {exp_gained} を獲得しました。<br>'

            # 王者データの保存
            from sub_def.file_ops import save_data_atomically
            save_data_atomically(winner, winner_path, "champion")

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
        common.save_user_sections(user_id, chara=chara, syoku=syoku)

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
