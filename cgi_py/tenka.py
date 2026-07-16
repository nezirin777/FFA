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
FFA Python/CGI - 天下一武道会 (tenka.py)
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
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    import config
    from sub_def import battle_logic
except ImportError:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from . import config
    from sub_def import battle_logic

# Windows等で標準出力をUTF-8にする設定
def get_all_players():
    """全プレイヤーデータを取得します"""
    players = []
    save_dir = config.Config['save_dir']
    if not os.path.exists(save_dir):
        return players
        
    for user_id in os.listdir(save_dir):
        user_path = os.path.join(save_dir, user_id)
        if os.path.isdir(user_path):
            chara = common.chara_load(user_id)
            if chara:
                players.append(chara)
    return players

def update_tenka_members():
    """天下一武道会メンバーリスト(all_tenka)を更新します"""
    tenka_path = os.path.join(config.Config['save_dir'], "all_tenka.json")
    now = int(time.time())
    
    # 全プレイヤーをロードしてレベル順にソート
    players = get_all_players()
    sorted_players = sorted(players, key=lambda x: x.get("level", 1), reverse=True)
    
    # 上位 tenka_su 名を抽出
    tenka_su = config.Config['tenka_count']
    members = sorted_players[:tenka_su]
    
    tenka_data = {
        "last_updated": now,
        "members": members
    }
    
    with open(tenka_path, "w", encoding="utf-8") as f:
        json.dump(tenka_data, f, ensure_ascii=False, indent=2)
        
    return tenka_data

def get_tenka_data():
    """天下一武道会メンバーリストのキャッシュを取得、または再構築します"""
    tenka_path = os.path.join(config.Config['save_dir'], "all_tenka.json")
    now = int(time.time())
    tenka_data = None
    
    if os.path.exists(tenka_path):
        try:
            with open(tenka_path, "r", encoding="utf-8") as f:
                tenka_data = json.load(f)
        except:
            pass
            
    # 24時間キャッシュ
    if not tenka_data or now - tenka_data.get("last_updated", 0) > 86400:
        common.get_lock("tenka_members")
        try:
            # 重複防止再確認
            if os.path.exists(tenka_path):
                try:
                    with open(tenka_path, "r", encoding="utf-8") as f:
                        tenka_data = json.load(f)
                except:
                    pass
            if not tenka_data or now - tenka_data.get("last_updated", 0) > 86400:
                tenka_data = update_tenka_members()
        finally:
            common.release_lock("tenka_members")
            
    return tenka_data

def load_aite_equipped_item(aite_id):
    """対戦相手の装備データをロードします。無ければ初期装備を返します。"""
    item = common.item_load(aite_id)
    if not item:
        item = {
            "weapon": {"name": "素手", "dmg": 0, "effect": 0},
            "armor": {"name": "衣服", "def": 0, "effect": 0},
            "accessory": {
                "name": "なし", "effect_id": 0,
                "bonus": {"str": 0, "int": 0, "dex": 0, "vit": 0, "agi": 0, "mnd": 0, "lck": 0, "lp": 0},
                "attrib": 0, "spare1": 0, "spare2": 0, "spare3": 0
            }
        }
    return item

def load_tenka_logs():
    """最近の制覇者履歴をロードします"""
    log_path = os.path.join(config.Config['save_dir'], "tenka_log.json")
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []

def save_tenka_logs(logs):
    """制覇者履歴を保存します"""
    log_path = os.path.join(config.Config['save_dir'], "tenka_log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在バージョンアップ中です。しばらくお待ちください。")
        
    in_params = common.decode_params()
    user_id = in_params.get("id", "")
    # IDOR対策: 状態変更は本人のみ許可(ロック取得前にチェック)
    common.require_owner(user_id)
    chara_log = in_params.get("mydata", "")
    mode = in_params.get("mode", "")

    # ログインキャラのロード
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターデータが見つかりません。ログインし直してください。")
        
    # 天下一データロード
    tenka_data = get_tenka_data()
    members = tenka_data.get("members", [])
    
    if mode == "battle":
        # === 戦闘開始処理 ===
        now = int(time.time())
        last_time = chara.get("last_time", 0)
        time_diff = now - last_time
        
        # 戦闘制限時間チェック (b_time秒)
        if time_diff < config.Config['battle_cooldown']:
            left_time = config.Config['battle_cooldown'] - time_diff
            context = {
                "chara": chara,
                "chara_log": chara_log,
                "left_time": left_time,
                "no": in_params.get("no", "1")
            }
            common.render_template("tenka_error.html", context)
            return

        # 対戦相手の決定
        # current_round = int(in_params.get("no", 1))
        # aite_idx = config.Config['tenka_count'] + chara["boss_flag"] - config.Config['boss_cooldown'] - 1
        boss_flag = chara.get("boss_flag", 0)
        aite_idx = config.Config['tenka_count'] + boss_flag - config.Config['boss_cooldown'] - 1
        
        if aite_idx < 0 or aite_idx >= len(members):
            common.show_error("キャラデータ不整合、または対戦相手が見つかりません。")
            
        winner = members[aite_idx]
        winner_id = winner["id"]
        
        # 対戦相手の装備ロードし結合
        winner["equipped_item"] = load_aite_equipped_item(winner_id)
        
        # 自分の装備ロード
        item = common.item_load(user_id)
        if not item:
            item = load_aite_equipped_item(user_id)
            
        # 賞金決定
        gold_reward = random.randint(1, config.Config['prize_money']) * int(winner.get("level", 1))
        
        # シミュレータ起動
        # 対人戦なので is_player_enemy=True に設定
        simulator = battle_logic.BattleSimulator("battle", chara, item, winner, is_player_enemy=True)
        win, battle_logs = simulator.simulate() # 1: プレイヤー勝利, 0: プレイヤー敗北, 2: 引き分け
        
        # 残りHP、経験値計算
        restored_hp = simulator.state.khp + random.randint(0, max(0, chara.get("vit", 10) - 1))
        if restored_hp > chara["max_hp"]:
            restored_hp = chara["max_hp"]
        if restored_hp <= 0:
            restored_hp = chara["max_hp"] # 敗北時は全回復
        chara["hp"] = restored_hp

        comment = ""
        exp_gained = 0
        
        if win == 1:
            # 勝利
            exp_gained = max(10, int(winner.get("level", 1) * 2))
            chara["gold"] += gold_reward
            if chara["gold"] > config.Config['max_gold']:
                chara["gold"] = config.Config['max_gold']
                
            chara["boss_flag"] = boss_flag - 1 # 1段階勝ち抜け
            chara["battle_limit"] = config.Config['battle_limit']
            
            # レベルアップ処理
            syoku = common.syoku_load(user_id) or {}
            lv_comment, lvup_count = battle_logic.process_levelup(chara, exp_gained, syoku)
            comment += lv_comment
            
            # 武道会制覇の判定
            next_winner = chara["boss_flag"] + config.Config['tenka_count'] - config.Config['boss_cooldown']
            if next_winner == 0:
                # 制覇達成
                comment += f"<br><span class='yellow'>🏆 見事に天下一武道会で優勝したクポ！おめでとうクポ！</span>"
                
                # 履歴保存
                common.get_lock("tenka_logs")
                try:
                    logs = load_tenka_logs()
                    logs.insert(0, {
                        "id": user_id,
                        "name": chara["name"],
                        "level": chara["level"],
                        "time": common.get_time_str()
                    })
                    # 20件までに制限
                    if len(logs) > config.Config['max_all_messages']:
                        logs = logs[:config.Config['max_all_messages']]
                    save_tenka_logs(logs)
                finally:
                    common.release_lock("tenka_logs")
                    
                # 全体メッセージに制覇通知を流す
                common.get_lock("all_message_post")
                try:
                    all_msgs = common.all_message_load()
                    new_msg = {
                        "id": "system",
                        "name": "天下一実況",
                        "time": common.get_time_str(),
                        "message": f"🎉 【天下一制覇】{chara['name']}さんが見事に天下一武道会を制覇し、最強の座に輝かれましたクポ！"
                    }
                    all_msgs.insert(0, new_msg)
                    if len(all_msgs) > config.Config['max_all_messages']:
                        all_msgs = all_msgs[:config.Config['max_all_messages']]
                    common.all_message_regist(all_msgs)
                finally:
                    common.release_lock("all_message_post")
            else:
                comment += f"<br>戦闘勝利！次の対戦に進めるクポ。"
        else:
            # 敗北または引き分け
            exp_gained = max(5, int(winner.get("level", 1) * 0.5))
            chara["gold"] = int(chara["gold"] / 2) # お金半分
            
            # レベルアップ処理
            syoku = common.syoku_load(user_id) or {}
            lv_comment, lvup_count = battle_logic.process_levelup(chara, exp_gained, syoku)
            comment += lv_comment
            
            comment += f"<br><span class='red'>敗北しましたクポ・・・お金が半分になってしまいました。</span>"

        # 最終行動時間更新
        chara["last_time"] = now
        chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")
        
        # セーブ
        common.get_lock(user_id)
        try:
            common.chara_regist(user_id, chara)
            if win == 1:
                common.syoku_regist(user_id, syoku)
        finally:
            common.release_lock(user_id)
            
        next_winner = chara["boss_flag"] + config.Config['tenka_count'] - config.Config['boss_cooldown']
        juni = config.Config['tenka_count'] - common.to_int(in_params.get("no", "1"), 1) + 1
        
        context = {
            "chara": chara,
            "chara_log": chara_log,
            "winner": winner,
            "round_no": in_params.get("no", "1"),
            "next_round_no": str(common.to_int(in_params.get("no", "1"), 1) + 1),
            "juni": juni,
            "win": win,
            "next_winner": next_winner,
            "gold_reward": gold_reward,
            "exp_gained": exp_gained,
            "battle_logs": battle_logs,
            "comment": comment
        }
        common.render_template("tenka_result.html", context)

    else:
        # === 武道会ロビー表示 (log_in) ===
        # 1. ボス撃破フラグのチェック
        # ボス撃破フラグが config.Config['boss_cooldown'] (10) 未満、またはそれに一致しない
        # Perlでは $chara[28] != $boss のとき「チャンプに挑戦して下さい」となる
        can_challenge = True
        challenge_error_msg = ""
        
        if chara.get("boss_flag", 0) < config.Config['boss_cooldown']:
            can_challenge = False
            challenge_error_msg = "天下一武道会に挑戦するには、まず通常のボス(10階)を撃破しておく必要がありますクポ。"
            
        # 2. メンバー数が足りているか
        # Perl: $tenka_su > $tenka_ninzu のときは「人数が足りません」
        tenka_hit = len(members) >= config.Config['tenka_count']
        if not tenka_hit:
            can_challenge = False
            challenge_error_msg = "現在の登録者数が不足しているため、武道会を開催できませんクポ。"

        # 履歴ロード
        logs = load_tenka_logs()
        
        # 更新時間文字列
        update_time_str = common.get_time_str(tenka_data["last_updated"])
        
        # opponents, chara_rank, limit_count, winner_info の算出
        players = get_all_players()
        sorted_players = sorted(players, key=lambda x: x.get("level", 1), reverse=True)
        chara_rank = 999
        for idx, p in enumerate(sorted_players):
            if p["id"] == user_id:
                chara_rank = idx + 1
                break

        limit_count = chara.get("boss_flag", 0) + config.Config['tenka_count'] - config.Config['boss_cooldown']
        limit_count = max(0, limit_count)

        opponents = []
        if limit_count > 0 and len(members) >= config.Config['tenka_count']:
            # 現在戦う相手のインデックス
            boss_flag = chara.get("boss_flag", 0)
            aite_idx = config.Config['tenka_count'] + boss_flag - config.Config['boss_cooldown'] - 1
            if 0 <= aite_idx < len(members):
                op_chara = members[aite_idx]
                opponents.append({
                    "name": op_chara.get("name", "名無し"),
                    "rank": aite_idx + 1,
                    "level": op_chara.get("level", 1),
                    "job": op_chara.get("job", 0),
                    "hp": op_chara.get("hp", 100),
                    "max_hp": op_chara.get("max_hp", 100)
                })

        winner_info = None
        if len(members) > 0:
            winner_chara = members[0]
            winner_info = {
                "name": winner_chara.get("name", "ゴールドボコ"),
                "win_count": winner_chara.get("ren", 0),
                "hp": winner_chara.get("hp", 100),
                "max_hp": winner_chara.get("max_hp", 100)
            }

        context = {
            "chara": chara,
            "chara_log": chara_log,
            "members": members,
            "logs": logs,
            "update_time": update_time_str,
            "can_challenge": can_challenge,
            "challenge_error_msg": challenge_error_msg,
            "tenka_su": config.Config['tenka_count'],
            "chara_rank": chara_rank,
            "limit_count": limit_count,
            "opponents": opponents,
            "winner": winner_info
        }
        common.render_template("tenka.html", context)

if __name__ == "__main__":
    main()
