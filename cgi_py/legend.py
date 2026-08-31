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
FFA Python/CGI - レジェンドプレイス戦闘スクリプト (legend.py)
"""
import os
import time
import random

# 共通モジュールと設定モジュールのインポート
try:
    import config
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from sub_def import battle_logic
    from sub_def.crypto import get_session, token_check
except ImportError:
    from . import config
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from sub_def import battle_logic
    from sub_def.crypto import get_session, token_check

parse_cookie_user = common.parse_cookie_user
load_monsters = common.load_json_list


def daily_legend_reward_state(chara, now):
    """当日中に通常報酬を受け取ったレジェンド固定敵の一覧を正規化する。"""
    today = time.strftime("%Y-%m-%d", time.localtime(now))
    raw_state = chara.get("legend_reward_history")
    if not isinstance(raw_state, dict) or raw_state.get("date") != today:
        return {"date": today, "rewarded_enemy_keys": []}
    rewarded_keys = raw_state.get("rewarded_enemy_keys", [])
    if not isinstance(rewarded_keys, list):
        rewarded_keys = []
    return {
        "date": today,
        "rewarded_enemy_keys": [str(key) for key in rewarded_keys if isinstance(key, str)],
    }


def get_legend_players():
    """レジェンドプレイスを1階層以上攻略したキャラクターを取得する。"""
    players = []
    save_dir = config.Config["save_dir"]
    if not os.path.exists(save_dir):
        return players
    for user_id in os.listdir(save_dir):
        if not os.path.isdir(os.path.join(save_dir, user_id)):
            continue
        chara = common.chara_load(user_id)
        if not chara or int(chara.get("title_id", 0)) <= 0:
            continue
        title_index = int(chara.get("title_id", 0))
        chara = dict(chara)
        chara["title_name"] = config.Config["titles"].get(title_index, config.Config["titles"][0])
        chara["battle_count"] = int(chara.get("battle_count", 0))
        chara["win_count"] = int(chara.get("win_count", 0))
        players.append(chara)
    players.sort(key=lambda p: (-int(p.get("title_id", 0)), -int(p.get("level", 0)), p.get("name", "")))
    return players
def main():
    # 1. メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    # 2. パラメータの取得
    params = common.decode_params()
    if params.get("view") == "ranking":
        common.render_template("legend_ranking.html", {
            "players": get_legend_players(),
            "chara_img": config.Config["chara_images"]
        })
        return

    if params.get("mode") in ("legend", "boss"):
        token_check(params, get_session())

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

        if c_id != user_id or c_pass != chara["pass"]:
            common.release_lock(user_id)
            common.show_error("パスワード認証に失敗しました。")

        chara["battle_count"] = int(chara.get("battle_count", 0))
        chara["win_count"] = int(chara.get("win_count", 0))

        if int(chara.get("battle_count", 0)) <= 0:
            common.release_lock(user_id)
            common.show_error("一度チャンプに挑戦してください。")

        if chara["battle_limit"] <= 0:
            common.release_lock(user_id)
            common.show_error("これ以上修行はできません（回数制限）。")

        try:
            boss_file_idx = int(boss_file_param)
        except ValueError:
            common.release_lock(user_id)
            common.show_error("無効な階層です。")

        boss_map = {
            0: config.Config['legend_boss_lv1_file'],
            1: config.Config['legend_boss_lv2_file'],
            2: config.Config['legend_boss_lv3_file'],
            3: config.Config['legend_boss_lv4_file']
        }
        if boss_file_idx not in boss_map:
            common.release_lock(user_id)
            common.show_error("無効な階層です。")

        # 称号レベル制限チェック
        if chara["title_id"] < boss_file_idx:
            common.release_lock(user_id)
            common.show_error("この階層に挑戦する資格がありません！")

        # 待機時間（クールダウン）チェック
        now = int(time.time())
        ltime = now - chara["last_time"]
        vtime = config.Config['training_cooldown_seconds'] - ltime
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
        file_path = boss_map[boss_file_idx]
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
        reward_key = f"{boss_file_idx}:{boss_flag}"
        daily_reward_state = daily_legend_reward_state(chara, now)
        is_repeat_reward = reward_key in daily_reward_state["rewarded_enemy_keys"]

        item = common.equipment_load(user_id)
        if not item:
            common.release_lock(user_id)
            common.show_error("アイテムデータが読み込めません。")

        # 3. 戦闘実行 (BattleSimulator)
        simulator = battle_logic.BattleSimulator("boss", chara, item, enemy_data, is_player_enemy=False)
        win, logs = simulator.simulate()

        # 4. 戦闘結果の集計と更新 (legend_sentoukeka相当)
        comment = ""
        gold_gained = 0
        exp_gained = enemy_data["exp_reward"]
        theft_adjustment = (
            int(simulator.state.gold_reward_bonus)
            - int(simulator.state.gold_reward_penalty)
        )

        if win == 1:
            chara["win_count"] += 1
            base_reward = enemy_data["gold_reward"] + random.randrange(max(1, int(enemy_data["gold_reward"]))) + 1
            if is_repeat_reward:
                divisor = max(1, int(config.Config["legend_repeat_reward_divisor"]))
                exp_gained = max(1, int(exp_gained / divisor))
                gold_gained = max(0, int((base_reward + theft_adjustment) / divisor))
                comment += (
                    f'<span class="yellow">この敵の本日2回目以降の撃破です。'
                    f'経験値・ゴールド報酬は 1/{divisor} になります。</span><br>'
                )
            else:
                # 初回撃破の通常報酬を記録し、同日の再撃破だけを減額する。
                daily_reward_state["rewarded_enemy_keys"].append(reward_key)
                chara["legend_reward_history"] = daily_reward_state
                # 盗み分は勝利報酬へ一度だけ合算する。
                gold_gained = max(0, base_reward + theft_adjustment)
            chara["gold"] += gold_gained
            if chara["gold"] > config.Config['max_gold']:
                chara["gold"] = config.Config['max_gold']
                
            chara["boss_flag"] -= 1
            if chara["boss_flag"] <= 0:
                # 階層クリア！
                if chara["title_id"] < boss_file_idx + 1:
                    comment += f'<b><span class="yellow text-large">{chara["name"]} は、レジェンドプレイスを攻略した！！新しい称号が与えられます！！</span></b><br>'
                    chara["title_id"] = boss_file_idx + 1
                    # 全体メッセージは称号が実際に上がる初回攻略時だけ投稿する。
                    # 再挑戦の周回クリアで同じ通知を繰り返さない。
                    common.get_lock("all_message_post")
                    try:
                        all_msgs = common.all_message_load()
                        new_msg = {
                            "id": "sys",
                            "name": "【天の声】",
                            "time": common.get_time_str(),
                            "message": f"{chara['name']}さんが新たにレジェンドプレイスを攻略され、称号が上がりました！",
                            "host": "system"
                        }
                        all_msgs.insert(0, new_msg)
                        common.all_message_regist(all_msgs[:config.Config['all_message_storage_limit']])
                    finally:
                        common.release_lock("all_message_post")
                else:
                    comment += f'<b><span class="yellow text-large">{chara["name"]} は、レジェンドプレイスを攻略した！！</span></b><br>'
                # 完走直後は0を保持する。これにより結果画面では同じ階層へ
                # 連戦するボタンを出さず、街へ戻る操作で次回挑戦用にリセットする。
            else:
                comment += f'<b><font size=5>{chara["name"]} は、戦闘に勝利した！！HPが少し回復した♪ 残り {chara["boss_flag"]} 体・・・</font></b><br>'
        elif win == 2:
            # 引き分け
            exp_gained = int(exp_gained / 2)
            # 引き分けは基礎報酬を支給せず、盗み分だけを反映する。
            gold_gained = theft_adjustment
            chara["gold"] += gold_gained
            if chara["gold"] > config.Config['max_gold']:
                chara["gold"] = config.Config['max_gold']
            if chara["gold"] < 0:
                chara["gold"] = 0

            chara["boss_flag"] = config.Config['legend_progress_reset_value']
            comment += f'<b><font size=5>{chara["name"]} は、逃げ出した・・・♪</font></b><br>'
            if gold_gained > 0:
                comment += f'<span class="green">盗んだお金 {gold_gained} G を獲得しました。</span><br>'
            elif gold_gained < 0:
                comment += f'<span class="red">お金を {abs(gold_gained)} G 失いました。</span><br>'
        else:
            # 敗北
            exp_gained = 1
            chara["boss_flag"] = config.Config['legend_progress_reset_value']
            chara["gold"] = int(chara["gold"] / 100) # ゴールド激減
            comment += f'<b><font size=5>{chara["name"]} は、戦闘に負けた・・・。</font></b><br>'

        # レジェンドは勝敗にかかわらず経験値を得るが、従来は結果画面に
        # 表示していなかった。保存値と結果表示を一致させる。
        comment += f'経験値 {exp_gained} を獲得しました。<br>'

        # 共通処理
        chara["battle_count"] += 1 # 戦闘回数カウンタ
        chara["battle_limit"] -= 1

        # レベルアップ処理
        syoku = common.syoku_load(user_id)
        if syoku is None:
            syoku = {}
        lv_comment, lvup_count = battle_logic.process_levelup(chara, exp_gained, syoku)
        comment += lv_comment

        # Ver2のhp_afterと同じく、レベルアップ後のvit/max_hpを使って
        # 戦闘後HPを回復する。敗北時は現在の最大HPまで回復する。
        restored_hp = simulator.state.khp + random.randint(0, max(0, chara["vit"] - 1))
        if restored_hp > chara["max_hp"]:
            restored_hp = chara["max_hp"]
        if restored_hp <= 0:
            restored_hp = chara["max_hp"]
        chara["hp"] = restored_hp

        # 最終行動時間
        chara["last_time"] = now
        chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")

        # セーブ
        common.save_user_sections(user_id, chara=chara, syoku=syoku)

    finally:
        common.release_lock(user_id)

    # 背景・音楽の調整
    boss_h = int(config.Config['legend_progress_reset_value'] / 2)
    if chara["boss_flag"] == 1:
        media = config.Config["legend_battle_media"]["final"]
    elif chara["boss_flag"] >= boss_h:
        media = config.Config["legend_battle_media"]["high"]
    else:
        media = config.Config["legend_battle_media"]["normal"]
    backgif = media["background"]

    legend_wait_seconds = 0
    if win == 1 and chara["boss_flag"] > 0:
        legend_wait_seconds = max(
            0,
            config.Config["training_cooldown_seconds"]
            - (int(time.time()) - int(chara.get("last_time", 0))),
        )

    # レンダリング
    context = {
        "page_background": backgif,
        "chara": chara,
        "enemy_name": enemy_data["name"],
        "logs": logs,
        "win": win,
        "comment": comment,
        "gold_gained": gold_gained,
        "exp_gained": exp_gained,
        "mode": "boss",
        "boss_file": boss_file_idx,
        "backgif": backgif,
        "legend_wait_seconds": legend_wait_seconds,
    }
    common.render_template("monster_result.html", context)

if __name__ == "__main__":
    main()
