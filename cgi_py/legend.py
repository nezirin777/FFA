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
FFA Python/CGI - 伝説の戦い・ボス戦闘スクリプト (legend.py)
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

def load_monsters(file_path):
    """モンスターファイルからモンスター一覧を読み込みます(JSON)"""
    full_path = os.path.join(common.BASE_DIR, file_path)
    if not os.path.exists(full_path):
        return []
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def main():
    # 1. メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    # 2. パラメータの取得
    params = common.decode_params()
    user_id = params.get("id", "").strip()
    boss_file_param = params.get("boss_file", "0")

    if not user_id:
        common.show_error("ログイン情報が不足しています。")

    # クッキー認証
    cookie_str = common.get_cookie(config.Config['cookie_name'])
    c_id, c_pass = parse_cookie_user(cookie_str)
    
    # キャラクターロード (排他ロック付き)
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        if not chara:
            common.release_lock(user_id)
            common.show_error("キャラクターが見つかりません。")
            
        if c_id == user_id and c_pass != chara["pass"]:
            common.release_lock(user_id)
            common.show_error("パスワード認証に失敗しました。")

        if chara["battle_limit"] <= 0:
            common.release_lock(user_id)
            common.show_error("これ以上修行はできません（回数制限）。")

        try:
            boss_file_idx = int(boss_file_param)
        except ValueError:
            boss_file_idx = 0

        # 称号レベル制限チェック
        if chara["title"] < boss_file_idx:
            common.release_lock(user_id)
            common.show_error("この階層に挑戦する資格がありません！")

        # 待機時間（クールダウン）チェック
        now = int(time.time())
        ltime = now - chara["last_time"]
        vtime = config.Config['monster_cooldown'] - ltime
        if vtime > 0:
            # 待機時間エラー
            common.release_lock(user_id)
            context = {
                "chara": chara,
                "vtime": vtime,
                "boss_file": boss_file_idx
            }
            common.render_template("legend_error.html", context)
            return

        # ボスデータのロード
        boss_map = {
            0: config.Config['boss0_file'],
            1: config.Config['boss1_file'],
            2: config.Config['boss2_file'],
            3: config.Config['boss3_file']
        }
        file_path = boss_map.get(boss_file_idx, config.Config['boss0_file'])
        enemy_list = load_monsters(file_path)
        if not enemy_list:
            common.release_lock(user_id)
            common.show_error("ボスデータが見つかりません。")

        # boss_flag 番目のボスを選択
        boss_flag = chara["boss_flag"]
        if boss_flag < 0 or boss_flag >= len(enemy_list):
            boss_flag = len(enemy_list) - 1
            chara["boss_flag"] = boss_flag
            
        enemy_data = enemy_list[boss_flag]

        item = common.item_load(user_id)
        if not item:
            common.release_lock(user_id)
            common.show_error("アイテムデータが読み込めません。")

        # 3. 戦闘実行 (BattleSimulator)
        simulator = battle_logic.BattleSimulator("boss", chara, item, enemy_data, is_player_enemy=False)
        win, logs = simulator.simulate()

        # 4. 戦闘結果の集計と更新 (legend_sentoukeka相当)
        comment = ""
        gold_gained = 0
        exp_gained = enemy_data["ex"]

        if win == 1:
            chara["unused22"] += 1
            gold_gained = enemy_data["gold"] + random.randint(0, enemy_data["gold"]) + 1
            chara["gold"] += gold_gained
            if chara["gold"] > config.Config['max_gold']:
                chara["gold"] = config.Config['max_gold']
                
            chara["boss_flag"] -= 1
            if chara["boss_flag"] <= 0:
                # 階層クリア！
                comment += f'<b><span class="yellow" style="font-size: 1.25em;">{chara["name"]} は伝説のプレイスを攻略しました！新称号を獲得しました！</span></b><br>'
                
                # 全体メッセージに投稿
                all_msgs = common.all_message_load()
                new_msg = {
                    "id": "sys",
                    "name": "【天の声】",
                    "time": common.get_time_str(),
                    "message": f"{chara['name']} が伝説のプレイス (エリア {boss_file_idx}) をクリアし、新たな称号を獲得しました！",
                    "host": "system"
                }
                all_msgs.insert(0, new_msg)
                common.all_message_regist(all_msgs[:config.Config['max_all_messages']])
                
                if chara["title"] < boss_file_idx + 1:
                    chara["title"] = boss_file_idx + 1
                chara["boss_flag"] = config.Config['boss_cooldown']
            else:
                comment += f'<b><font size=5>{chara["name"]} は勝利しました！残り {chara["boss_flag"]} 体・・・</font></b><br>'
        elif win == 2:
            # 引き分け
            exp_gained = int(exp_gained / 2)
            chara["boss_flag"] = config.Config['boss_cooldown']
            comment += f'<b><font size=5>{chara["name"]} は引き分けました。ボス攻略は最初からやり直しです。</font></b><br>'
        else:
            # 敗北
            exp_gained = 1
            chara["boss_flag"] = config.Config['boss_cooldown']
            chara["gold"] = int(chara["gold"] / 100) # ゴールド激減
            comment += f'<b><font size=5>{chara["name"]} は敗北しました。ボス攻略は最初からやり直しです。</font></b><br>'

        # 戦闘後の残りHP復元
        restored_hp = simulator.state.khp + random.randint(0, max(0, chara["vit"] - 1))
        if restored_hp > chara["max_hp"]:
            restored_hp = chara["max_hp"]
        if restored_hp <= 0:
            restored_hp = chara["max_hp"]
        chara["hp"] = restored_hp

        # 共通処理
        chara["unused21"] += 1 # 戦闘回数カウンタ
        chara["battle_limit"] -= 1

        # レベルアップ処理
        syoku = common.syoku_load(user_id)
        if syoku is None:
            syoku = {}
        lv_comment, lvup_count = battle_logic.process_levelup(chara, exp_gained, syoku)
        comment += lv_comment

        # 最終行動時間
        chara["last_time"] = now
        chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")

        # セーブ
        common.chara_regist(user_id, chara)
        common.syoku_regist(user_id, syoku)

    finally:
        common.release_lock(user_id)

    # 背景・音楽の調整
    boss_h = int(config.Config['boss_cooldown'] / 2)
    if chara["boss_flag"] == 1:
        backgif = "images/last_boss_back.gif"
        midi = "data/last_boss.mid"
    elif chara["boss_flag"] >= boss_h:
        backgif = "images/boss_back.gif"
        midi = "data/boss1.mid"
    else:
        backgif = "images/boss2_back.gif"
        midi = "data/boss2.mid"

    # レンダリング
    context = {
        "chara": chara,
        "enemy_name": enemy_data["name"],
        "logs": logs,
        "win": win,
        "comment": comment,
        "gold_gained": gold_gained,
        "exp_gained": exp_gained,
        "mode": "boss",
        "boss_file": boss_file_idx
    }
    common.render_template("monster_result.html", context)

if __name__ == "__main__":
    main()
