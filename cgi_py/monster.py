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
FFA Python/CGI - モンスター修行・幻影・異世界スクリプト (monster.py)
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
            return common.decode_html_entities(json.load(f))
    except Exception:
        return []

def main():
    # 1. メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    # 2. パラメータの取得
    params = common.decode_params()
    mode = params.get("mode", "monster") # monster, genei, isekiai
    user_id = params.get("id", "").strip()
    mons_file_param = params.get("mons_file", "monster0")

    if not user_id:
        common.show_error("ログイン情報が不足しています。")

    # クッキーによるログイン認証
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

        # 3. 待機時間（クールダウン）チェック
        now = int(time.time())
        ltime = now - chara["last_time"]
        if ltime < config.Config['training_cooldown_seconds']:
            common.release_lock(user_id)
            common.show_error(f"まだ行動できません！ (あと {config.Config['training_cooldown_seconds'] - ltime} 秒)")

        # 4. 各モード固有のチェックとモンスターファイルの選択
        enemy_list = []
        is_genei = False
        is_isekiai = False

        if mode == "monster":
            # 修行
            if chara["battle_limit"] <= 0:
                common.release_lock(user_id)
                common.show_error("これ以上修行はできません（回数制限）。")
            
            # mons_file のマッピング
            mons_map = {
                "monster0": config.Config['monster_lv1_file'],
                "monster1": config.Config['monster_lv2_file'],
                "monster2": config.Config['monster_lv3_file'],
                "monster3": config.Config['monster_lv4_file']
            }
            file_key = mons_file_param
            if file_key not in mons_map:
                file_key = "monster0"
            enemy_list = load_monsters(mons_map[file_key])

        elif mode == "genei":
            # 幻影の城
            is_genei = True
            if int(chara.get("battle_count", 0)) <= 0:
                common.release_lock(user_id)
                common.show_error("一度チャンプに挑戦してください。")
            # 最終行動時間 (last_time) が5の倍数でなければエラー
            if chara["last_time"] % 5 != 0:
                common.release_lock(user_id)
                common.show_error("もう消えてしまって行けませんでした。")
            
            # レベルによる切り替え
            lvl = chara["level"]
            if lvl < config.Config['monster_level_threshold_lv2']:
                target_file = config.Config['monster_lv1_file']
            elif lvl < config.Config['monster_level_threshold_lv3']:
                target_file = config.Config['monster_lv2_file']
            elif lvl < config.Config['monster_level_threshold_lv4']:
                target_file = config.Config['monster_lv3_file']
            else:
                target_file = config.Config['monster_lv4_file']
            enemy_list = load_monsters(target_file)

        elif mode == "isekiai":
            # 異世界
            is_isekiai = True
            if chara["level"] < config.Config['isekai_level']:
                common.release_lock(user_id)
                common.show_error(f"異世界に行くにはレベル {config.Config['isekai_level']} 以上必要です。")
            enemy_list = load_monsters(config.Config['isekai_file'])

        else:
            common.release_lock(user_id)
            common.show_error("無効な戦闘モードです。")

        if not enemy_list:
            common.release_lock(user_id)
            common.show_error("対戦相手モンスターデータが見つかりません。")

        # 対戦相手の決定 (重み付きランダム選択)
        # モンスターデータ内の "weight"（出現重み）を基準に抽選を行います。
        # 旧仕様において「データの多重登録（通常モンスターは3回、えりりん等のレアモンスターは1回定義）」
        # で遭遇率を調整していた挙動を正確に引き継ぐため、以下の重みで動作します：
        # - 通常モンスター: weight = 3
        # - えりりん等のレアモンスター: weight = 1 (通常モンスターの1/3の遭遇率)
        # - weightキーを持たないデータ: weight = 1 (一律均等)
        weights = [enemy.get("weight", 1) for enemy in enemy_list]
        enemy_data = random.choices(enemy_list, weights=weights, k=1)[0]

        # 所持アイテム・装備のロード
        item = common.equipment_load(user_id)
        if not item:
            common.release_lock(user_id)
            common.show_error("アイテムデータが読み込めません。")

        # 5. 戦闘実行 (BattleSimulator)
        simulator = battle_logic.BattleSimulator(mode, chara, item, enemy_data, is_player_enemy=False)
        if is_genei:
            # 旧版どおり、乱数分に基礎SPの2倍を加える。
            monster_hp = random.randrange(max(1, enemy_data["rand"])) + enemy_data["sp"] * 2
            simulator.state.mhp = simulator.state.mhp_flg = monster_hp
        
        # 戦闘シミュレート開始
        win, logs = simulator.simulate()

        # 6. 戦闘結果の集計とキャラクターデータの更新
        comment = ""
        gold_gained = 0
        exp_gained = 0

        # 戦闘後の残りHP復元 (hp_after)
        restored_hp = simulator.state.khp + random.randint(0, max(0, chara["vit"] - 1))
        if restored_hp > chara["max_hp"]:
            restored_hp = chara["max_hp"]
        if restored_hp <= 0:
            restored_hp = chara["max_hp"]
        chara["hp"] = restored_hp

        # 勝敗処理
        if win == 1:
            # 旧版 sentoukeka 相当: 基本報酬 + 1〜基本報酬の範囲。
            base_gold = max(0, int(enemy_data["gold"]))
            gold_gained = base_gold + random.randrange(max(1, base_gold)) + 1
            gold_gained += simulator.state.gold_reward_bonus
            gold_gained = max(0, gold_gained - simulator.state.gold_reward_penalty)
            exp_gained = enemy_data["ex"]
            
            # 幻影の城のお宝追加判定
            if is_genei:
                if random.randrange(3) == 0:
                    otakara = (random.randrange(1000) + 1) * enemy_data["gold"]
                    gold_gained += otakara
                    comment += f'<br><b><span class="red u-text-large">財宝({otakara}Ｇ)を発見した！！！！</span></b><br>'
                else:
                    comment += '<br><b><span class="gray u-text-large">辺りに財宝は見つからなかった・・・。</span></b><br>'

            chara["gold"] += gold_gained
            if chara["gold"] > config.Config['max_gold']:
                chara["gold"] = config.Config['max_gold']
            if chara["gold"] < 0:
                chara["gold"] = 0
            
            comment += f'<span class="green u-text-large">戦闘に勝利しました！</span><br>'
            comment += f'経験値 {exp_gained} と {gold_gained} ゴールドを獲得しました。<br>'
        elif win == 0:
            # 旧版の敗北時処理は所持金を1%にする。
            chara["gold"] = int(chara["gold"] / 100)
            comment += f'<span class="red u-text-large">戦闘に敗北しました・・・</span><br>'
        else:
            comment += f'<span class="yellow u-text-large">時間切れ引き分けです。</span><br>'

        # 旧版 mbattle.pl の sentoukeka と同じく、通常修行・幻影の城・異世界を
        # 挟んだ場合はレジェンドプレイスの連続攻略を終了する。
        # レジェンドを続ける場合だけ、結果画面の「さらに奥へ進む」から
        # legend.py を直接呼び出して boss_flag を保持する。
        chara["boss_flag"] = config.Config["legend_progress_reset_value"]

        # 旧版では通常修行・幻影の城・異世界のいずれも戦闘回数へ集計する。
        chara["battle_count"] = int(chara.get("battle_count", 0)) + 1
        if win == 1:
            chara["win_count"] = int(chara.get("win_count", 0)) + 1

        # レベルアップ処理
        syoku = common.syoku_load(user_id)
        if syoku is None:
            syoku = {}
        
        lv_comment, lvup_count = battle_logic.process_levelup(chara, exp_gained, syoku)
        comment += lv_comment

        # バトル回数を減算
        if chara["battle_limit"] > 0:
            chara["battle_limit"] -= 1

        # 最終行動時間を更新
        chara["last_time"] = now
        chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")

        # セーブ
        common.chara_regist(user_id, chara)
        common.syoku_regist(user_id, syoku)

    finally:
        common.release_lock(user_id)

    # 7. 結果画面のレンダリング
    context = {
        "chara": chara,
        "enemy_name": enemy_data["name"],
        "logs": logs,
        "win": win,
        "comment": comment,
        "gold_gained": gold_gained,
        "exp_gained": exp_gained,
        "mode": mode
    }
    common.render_template("monster_result.html", context)

if __name__ == "__main__":
    main()
