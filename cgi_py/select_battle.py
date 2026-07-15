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
FFA Python/CGI - 対戦相手選択・バトルスクリプト (select_battle.py)
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

def get_all_players():
    """全プレイヤーのキャラクターデータをロードして返します"""
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

def main():
    # 1. メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    # 2. パラメータの取得
    params = common.decode_params()
    mode = params.get("mode", "log_in") # log_in, sentaku, battle
    # ルーティングキー (login.py?mode=select_battle) で入場した場合や不明なmodeは初期画面へ
    if mode not in ("log_in", "sentaku", "battle"):
        mode = "log_in"
    user_id = params.get("id", "").strip()

    if not user_id:
        common.show_error("ログイン情報が不足しています。")

    # クッキー認証
    cookie_str = common.get_cookie(config.Config['cookie_name'])
    c_id, c_pass = parse_cookie_user(cookie_str)
    
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターが見つかりません。")
        
    if c_id == user_id and c_pass != chara["pass"]:
        common.show_error("パスワード認証に失敗しました。")

    # 3. 各モードの実行
    if mode == "log_in":
        # 対戦選択の初期画面
        context = {
            "chara": chara,
            "mode": mode
        }
        common.render_template("select_battle.html", context)
        return

    elif mode == "sentaku":
        # 対戦相手一覧
        players = get_all_players()
        # 自分自身を除外
        players = [p for p in players if p["id"] != chara["id"]]
        context = {
            "chara": chara,
            "players": players,
            "mode": mode
        }
        common.render_template("select_battle.html", context)
        return

    elif mode == "battle":
        aite_id = params.get("aiteid", "").strip()
        aite_name = params.get("aitename", "").strip()

        # クールダウン時間チェック
        now = int(time.time())
        ltime = now - chara["last_time"]
        if ltime < config.Config['battle_cooldown']:
            common.show_error(f"まだ行動できません！ (あと {config.Config['battle_cooldown'] - ltime} 秒)")

        if not aite_id and not aite_name:
            common.show_error("対戦相手が指定されていません。")

        # 名前で検索する場合
        if not aite_id and aite_name:
            players = get_all_players()
            matched = [p for p in players if p["name"].strip() == aite_name.strip() and p["id"] != chara["id"]]
            if not matched:
                common.show_error(f"対戦相手 「{aite_name}」 が見つかりません。")
            aite_id = matched[0]["id"]

        if aite_id == chara["id"]:
            common.show_error("自分自身と対戦することはできません。")

        # 相手データのロード
        aite_chara = common.chara_load(aite_id)
        if not aite_chara:
            common.show_error("対戦相手のキャラクターデータが見つかりません。")

        aite_item = common.item_load(aite_id)
        if not aite_item:
            common.show_error("対戦相手のアイテムデータが見つかりません。")

        aite_chara["equipped_item"] = aite_item

        # 自プレイヤーのアイテムロード
        item = common.item_load(user_id)
        if not item:
            common.show_error("アイテムデータが読み込めません。")

        # 4. 戦闘シミュレート実行 (練習戦なのでセーブは行わない)
        simulator = battle_logic.BattleSimulator("battle", chara, item, aite_chara, is_player_enemy=True)
        win, logs = simulator.simulate()

        comment = ""
        if win == 1:
            comment = f'<span class="green u-text-large">{aite_chara["name"]} に勝利しました！</span><br>(練習戦のためステータスやゴールドの変動はありません)'
        elif win == 0:
            comment = f'<span class="red u-text-large">{aite_chara["name"]} に敗北しました・・・</span><br>(練習戦のためステータスやゴールドの変動はありません)'
        else:
            comment = f'<span class="yellow u-text-large">引き分けです。</span><br>(練習戦のためステータスやゴールドの変動はありません)'

        # 5. 戦闘結果画面の描画 (monster_result.html を再利用)
        context = {
            "chara": chara,
            "enemy_name": aite_chara["name"],
            "logs": logs,
            "win": win,
            "comment": comment,
            "gold_gained": 0,
            "exp_gained": 0,
            "mode": "battle"
        }
        common.render_template("monster_result.html", context)
        return

    else:
        common.show_error("無効なモードです。")

if __name__ == "__main__":
    main()
