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
#------------------------------------------------------#
# チョコボ牧場 edit by いく (http://www.eriicu.com)
# FFA いく改ver2.00 edit by いく
# FFA Emilia Ver1.01 remodeled by Classic (閉鎖)
# FF Battle De I v3.06 remodeling by jun-k (http://www.mj-world.jp/) (更新停止中)
# FF ADVENTURE(改) v1.040 remodeled by GUN (http://www.gun-online.com)
# FF ADVENTURE v0.43 edit by D.Takamiya(CUMRO) 現配布元(管理者ma-ti) (http://www5c.biglobe.ne.jp/~ma-ti/)
#------------------------------------------------------#
"""
FFA Python/CGI - チョコボランキング・重賞履歴表示 (chocorank.py)
"""

import sys

import os
import time
import json


RANK_CACHE_VERSION = 2

# 共通モジュールのインポート
try:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    import config
except ImportError:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from . import config

# Windows等で標準出力をUTF-8にする設定
def get_all_chocobos():
    """全ユーザーのフォルダからチョコボデータを取得します"""
    chocobos = []
    save_dir = config.Config['save_dir']
    if not os.path.exists(save_dir):
        return chocobos
        
    for user_id in os.listdir(save_dir):
        user_path = os.path.join(save_dir, user_id)
        if os.path.isdir(user_path):
            choco = common.choco_load(user_id)
            if choco:
                chocobos.append(choco)
    return chocobos


def ability_rank_index(value):
    """Ver2と同じ能力ランク画像の境界値を返します。"""
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = 0

    # Ver2は各境界を「より大きい」で判定している。
    if value > 1000:
        return 10  # SS
    if value > 800:
        return 8   # S
    if value > 600:
        return 6   # A
    if value > 400:
        return 4   # B
    if value > 200:
        return 2   # C
    if value > 100:
        return 1   # D
    return 0       # E


def build_rankings(chocobos):
    """各部門のTop 10を作成します"""
    
    def extract_top(lst, sort_key, val_key=None, mul=1):
        sorted_lst = sorted(lst, key=lambda x: x.get(sort_key, 0), reverse=True)
        top_10 = []
        for c in sorted_lst[:10]:
            val = c.get(val_key or sort_key, 0)
            top_10.append({
                "id": c.get("id", "unknown"),
                "name": c.get("name", "名無しのチョコボ"),
                "breader": c.get("breader", "不明"),
                "val": val * mul
            })
        return top_10

    # 能力値 Top 10抽出用（c0〜c6）
    def extract_top_ability(lst, choco_key):
        # ランク画像に対応するインデックスも算出する。
        # Ver2の比較演算子をそのまま再現するため、単純な100割りは使わない。
        sorted_lst = sorted(lst, key=lambda x: x.get(choco_key, 10), reverse=True)
        top_10 = []
        for c in sorted_lst[:10]:
            val = c.get(choco_key, 10)
            rank_idx = ability_rank_index(val)
            top_10.append({
                "id": c.get("id", "unknown"),
                "name": c.get("name", "名無しのチョコボ"),
                "breader": c.get("breader", "不明"),
                "val": val,
                "rank_idx": rank_idx
            })
        return top_10

    # 各部門の抽出
    rank_win = extract_top(chocobos, "win")
    rank_train = extract_top(chocobos, "train")
    rank_gold = extract_top(chocobos, "gold", mul=100) # 獲得賞金は100倍

    rank_c0 = extract_top_ability(chocobos, "c0") # 筋力
    rank_c1 = extract_top_ability(chocobos, "c1") # スタミナ
    rank_c2 = extract_top_ability(chocobos, "c2") # 粘り
    rank_c3 = extract_top_ability(chocobos, "c3") # 落ち着き
    rank_c4 = extract_top_ability(chocobos, "c4") # 闘争心
    rank_c5 = extract_top_ability(chocobos, "c5") # 賢さ
    rank_c6 = extract_top_ability(chocobos, "c6") # 反射神経

    return {
        "win": rank_win,
        "train": rank_train,
        "gold": rank_gold,
        "c0": rank_c0,
        "c1": rank_c1,
        "c2": rank_c2,
        "c3": rank_c3,
        "c4": rank_c4,
        "c5": rank_c5,
        "c6": rank_c6
    }


def is_current_rank_cache(cache_data):
    """現在のランキング表示形式を満たすキャッシュか確認します。"""
    required_keys = {"win", "train", "gold", "c0", "c1", "c2", "c3", "c4", "c5", "c6"}
    rankings = cache_data.get("rankings") if isinstance(cache_data, dict) else None
    return (
        isinstance(cache_data, dict)
        and cache_data.get("version") == RANK_CACHE_VERSION
        and isinstance(cache_data.get("last_updated"), int)
        and isinstance(cache_data.get("total_chocobos"), int)
        and isinstance(rankings, dict)
        and required_keys.issubset(rankings)
        and all(isinstance(rankings[key], list) for key in required_keys)
    )


def get_rank_cache():
    """キャッシュを取得、または再構築します"""
    cache_path = os.path.join(config.Config['save_dir'], "chocorank_cache.json")
    now = int(time.time())
    cache_data = None
    
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = common.decode_html_entities(json.load(f))
        except (OSError, json.JSONDecodeError) as error:
            sys.stderr.write(f"チョコボランキングキャッシュを読み込めません: {error}\n")
            
    # 24時間キャッシュ (86400秒)
    if (
        not is_current_rank_cache(cache_data)
        or now - cache_data["last_updated"] > 86400
    ):
        common.get_lock("chocorank_cache_build")
        try:
            # 多重更新防止の再チェック
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "r", encoding="utf-8") as f:
                        cache_data = common.decode_html_entities(json.load(f))
                except (OSError, json.JSONDecodeError) as error:
                    sys.stderr.write(f"チョコボランキングキャッシュを再読込できません: {error}\n")
            if (
                not is_current_rank_cache(cache_data)
                or now - cache_data["last_updated"] > 86400
            ):
                chocobos = get_all_chocobos()
                rankings = build_rankings(chocobos)
                cache_data = {
                    "version": RANK_CACHE_VERSION,
                    "last_updated": now,
                    "total_chocobos": len(chocobos),
                    "rankings": rankings
                }
                from sub_def.file_ops import save_data_atomically
                save_data_atomically(cache_data, cache_path, "chocorank_cache")
        finally:
            common.release_lock("chocorank_cache_build")
            
    return cache_data

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")
        
    in_params = common.decode_params()
    mode = in_params.get("mode", "")
    user_id = in_params.get("id", "")
    chara_log = in_params.get("mydata", "")

    # ランキング・重賞履歴はログイン中の本人だけが閲覧できる現行仕様。
    common.require_owner(user_id)

    # 戻るフォーム用のキャラクターデータ
    chara = common.chara_load(user_id) if user_id else None
    if not chara:
        common.show_error("キャラクターデータが見つかりません。ログインし直してください。")

    # アルファベット能力ランク画像
    rank_imgs = [
        "e.gif", "d.gif", "c.gif", "c.gif", "b.gif", "b.gif",
        "a.gif", "a.gif", "s.gif", "s.gif", "ss.gif", "ss.gif",
        "ss.gif", "ss.gif", "ss.gif"
    ]
    
    # 22重賞のレース名リスト (r1〜r22 に対応)
    races_names = [
        "チョコボダービー", "チョコボスタリオン", "チョコボカップ", "レジェンドカップ",
        "CCB賞", "チョコボ桜花賞", "チョコボ皐月賞", "チョコボ記念",
        "チョコボステークス", "キングスカップ", "クイーンカップ", "シルバーカップ",
        "Kイク＆Qエリリン", "チョコリスダービー", "チョコボワールドカップ", "チョコボエンプレス杯",
        "チョコボウル", "ブリーダーズカップ", "ゴールドカップ", "プラチナカップ",
        "チョコボオークス", "チョコボキングス"
    ]
    
    context = {
        "page_background": config.Config["chocobo_farm_background"],
        "mode": mode,
        "chara": chara,
        "chara_log": chara_log,
        "rank_imgs": rank_imgs,
        "races_names": races_names
    }
    
    if mode == "ranking":
        # === チョコボ各種能力Top 10ランキング ===
        cache_data = get_rank_cache()
        update_time_str = common.get_time_str(cache_data["last_updated"])
        
        context.update({
            "rankings": cache_data["rankings"],
            "total_chocobos": cache_data["total_chocobos"],
            "update_time": update_time_str
        })
        common.render_template("chocorank.html", context)
        
    else:
        # === 重賞制覇履歴 ===
        rireki_path = os.path.join(config.Config['save_dir'], "rireki.json")
        rireki_data = []
        if os.path.exists(rireki_path):
            try:
                with open(rireki_path, "r", encoding="utf-8") as f:
                    rireki_data = common.decode_html_entities(json.load(f))
            except (OSError, json.JSONDecodeError) as error:
                sys.stderr.write(f"重賞制覇履歴を読み込めません: {error}\n")
                
        # 履歴データを表示用に整形
        formatted_rireki = []
        for r in rireki_data:
            # r1〜r22 のチェック状況をリスト化
            race_statuses = []
            for i in range(1, 23):
                status = r.get(f"r{i}", 0)
                race_statuses.append("○" if status else "−")
                
            formatted_rireki.append({
                "id": r.get("id", ""),
                "name": r.get("name", "不明"),
                "father": r.get("father", "不明"),
                "mother": r.get("mother", "不明"),
                "breader": r.get("breader", "不明"),
                "races": race_statuses
            })
            
        context.update({
            "rireki": formatted_rireki
        })
        common.render_template("chocorank.html", context)

if __name__ == "__main__":
    main()
