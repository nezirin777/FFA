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
FFA Python/CGI - メイン・ステータス画面表示スクリプト (ffadventure.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
import os
import time
import json

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正

def parse_cookie_user(cookie_str):
    """
    クッキー文字列 "id<>user_id,pass<>password" からIDとパスワードを抽出します。
    """
    if not cookie_str:
        return None, None
    id_val = None
    pass_val = None
    # カンマで分割
    pairs = cookie_str.split(",")
    for pair in pairs:
        if "<>" in pair:
            k, v = pair.split("<>", 1)
            if k == "id":
                id_val = v
            elif k == "pass":
                pass_val = v
    return id_val, pass_val

def get_winner():
    """
    王者データを読み込み、辞書として返します。
    """
    winner_path = os.path.join(common.BASE_DIR, config.Config['winner_file'])
    default_winner = {
        "id": "sys", "name": "無名の剣士", "img": 0, "hp": 1000, "max_hp": 1000, "win_count": 0
    }
    if not os.path.exists(winner_path):
        return default_winner
    try:
        with open(winner_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "id": data.get("id", "sys"),
            "name": data.get("name", "無名の剣士"),
            "img": data.get("img", 0),
            "hp": data.get("hp", 1000),
            "max_hp": data.get("max_hp", 1000),
            "win_count": data.get("win_count", 0)
        }
    except Exception:
        return default_winner

def main():
    # 1. メンテナンスチェック
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    # 2. パラメータの取得
    params = common.decode_params()
    user_id = params.get("id", "").strip()
    
    # 3. ユーザー認証（クッキーチェックを含む）
    # クッキーからログイン情報を取得
    cookie_str = common.get_cookie(config.Config['cookie_name'])
    c_id, c_pass = parse_cookie_user(cookie_str)
    
    if not user_id:
        # パラメータで ID が渡されていない場合は、クッキーの ID を使用
        if c_id:
            user_id = c_id
        else:
            common.show_error("ログイン情報がありません。再度ログインしてください。")
            
    # キャラクターデータロード
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターが存在しないか、データが破損しています。")
        
    # パスワード検証（IDOR対策: ログイン中の本人のみ自分のホーム画面を表示できる）
    if c_id != user_id or c_pass != chara["pass"]:
        common.show_error("認証に失敗しました。再度ログインしてください。")
        
    # 4. 所持アイテムのロード
    item = common.item_load(user_id)
    if not item:
        # 初期装備の設定（ロード失敗時の安全策）
        item = {
            "weapon": {"name": "素手", "dmg": 0, "effect": 0},
            "armor": {"name": "衣服", "def": 0, "effect": 0},
            "accessory": {
                "name": "なし", "effect_id": 0,
                "bonus": {"str": 0, "int": 0, "dex": 0, "vit": 0, "agi": 0, "mnd": 0, "lck": 0, "lp": 0},
                "attrib": 0, "spare1": 0, "spare2": 0, "spare3": 0
            }
        }
        
    # 5. 王者データの取得
    winner = get_winner()
    
    # 6. 行動制限時間・待機時間の計算
    now = int(time.time())
    ltime = now - chara["last_time"]
    vtime = config.Config['battle_cooldown'] - ltime
    ztime = vtime + 1 if vtime >= 0 else 0
    
    # ボスフラグ進行度の調整
    if chara["boss_flag"] < config.Config['boss_cooldown']:
        chara["boss_flag"] = 0
        
    # 性別表記
    esex = "男" if chara["sex"] else "女"
    
    # レベルアップ必要経験値
    next_ex = chara["level"] * config.Config['level_up_coeff']
    
    # 称号
    title_idx = chara["title"]
    if title_idx < 0 or title_idx >= len(config.Config['titles']):
        title_idx = 0
    syou = config.Config['titles'][title_idx]
    
    # 宿屋代金の計算
    yado_daix = int(config.Config['inn_cost'] * chara["level"])
    
    # 職業名の取得
    job_idx = chara["job"]
    if job_idx < 0 or job_idx >= len(config.Config['chara_jobs']):
        job_idx = 0
    job_name = config.Config['chara_jobs'][job_idx]
    
    # HPパーセンテージ計算
    if chara["max_hp"] > 0:
        hp_percent = int(chara["hp"] / chara["max_hp"] * 100)
    else:
        hp_percent = 0
    if hp_percent > 100:
        hp_percent = 100
        
    # 銀行預金 (Perl の $chara[34] に相当)
    chara["bank"] = chara.get("bank", chara.get("unused33", 0)) # 移行スクリプトで key に bank が無ければ default 0
    if "bank" not in chara:
        # キーが無い場合は追加
        chara["bank"] = chara.get("unused33", 0)
        
    # 7. オンラインゲスト更新・取得
    guest_list_html = common.update_and_get_guests(user_id, chara["name"])
    
    # 8. 個人メッセージの取得
    personal_messages = common.message_load(user_id)[:config.Config['max_lines']]
    
    # 9. 画面描画
    context = {
        "chara": chara,
        "item": item,
        "winner": winner,
        "ztime": ztime,
        "esex": esex,
        "next_ex": next_ex,
        "syou": syou,
        "yado_daix": yado_daix,
        "job_name": job_name,
        "hp_percent": hp_percent,
        "guest_list_html": guest_list_html,
        "personal_messages": personal_messages
    }
    
    common.render_template("ffadventure.html", context)

if __name__ == "__main__":
    main()
