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
FFA Python/CGI - 英雄ランキング表示スクリプト (rank.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
import os
import time

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正

def get_all_players():
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

def build_rankings(players):
    """全プレイヤーから各部門のTop 10を作成します"""
    
    def extract_top(lst, sort_key, val_key=None):
        # 指定キーでソートして上位10名を取得
        sorted_lst = sorted(lst, key=lambda x: x.get(sort_key, 0), reverse=True)
        top_10 = []
        for p in sorted_lst[:10]:
            val = p.get(val_key or sort_key, 0)
            top_10.append({
                "id": p["id"],
                "name": p["name"],
                "site": p.get("site", "無名"),
                "url": p.get("url", "http://"),
                "val": val
            })
        return top_10

    # 1. レベル
    rank_level = extract_top(players, "level")
    # 2. HP (max_hp)
    rank_hp = extract_top(players, "max_hp")
    # 3. 力 (str)
    rank_str = extract_top(players, "str")
    # 4. 知能 (int)
    rank_int = extract_top(players, "int")
    
    # 5. 信仰心
    # Perlの$chara[9]に対応。Python側でインデックス9は'dex'にマッピングされています。
    # よって、信仰心部門は 'dex' キーでソートします。
    rank_mnd = extract_top(players, "dex")
    
    # 6. 生命力 (vit)
    rank_vit = extract_top(players, "vit")
    
    # 7. 器用さ
    # Perlの$chara[11]に対応。Python側でインデックス11は'agi'にマッピングされています。
    # よって、器用さ部門は 'agi' キーでソートします。
    rank_dex = extract_top(players, "agi")
    
    # 8. 速さ
    # Perlの$chara[12]に対応。Python側でインデックス12は'mnd'にマッピングされています。
    # よって、速さ部門は 'mnd' キーでソートします。
    rank_agi = extract_top(players, "mnd")
    
    # 9. 魅力 (lck)
    rank_lck = extract_top(players, "lck")
    # 10. カルマ (lp)
    rank_lp = extract_top(players, "lp")
    
    # 11. 勝率
    # 総対人戦数が1000（Perlの1000戦以上）または100戦以上？ 
    # 登録者が少ないテスト環境等を考慮し、対人戦数が10回以上の人を対象にします（Perlは1000戦以上）
    # ここでは1000戦以上を基本としつつ、少なければ10戦以上に緩和するなどの処理も可能ですが、
    # 基本の1000戦でフィルタリングします。
    win_players = []
    for p in players:
        total_battles = p.get("unused21", 0)
        wins = p.get("unused22", 0)
        if total_battles >= 1000:
            ratio = round((wins / total_battles) * 100, 2)
            win_players.append({
                "id": p["id"],
                "name": p["name"],
                "site": p.get("site", "無名"),
                "url": p.get("url", "http://"),
                "val": ratio,
                "total_battles": total_battles
            })
    win_players.sort(key=lambda x: x["val"], reverse=True)
    rank_win_ratio = win_players[:10]

    return {
        "level": rank_level,
        "hp": rank_hp,
        "str": rank_str,
        "int": rank_int,
        "mnd": rank_mnd,
        "vit": rank_vit,
        "dex": rank_dex,
        "agi": rank_agi,
        "lck": rank_lck,
        "lp": rank_lp,
        "win_ratio": rank_win_ratio
    }

def get_rank_cache():
    cache_path = os.path.join(config.Config['save_dir'], "rank_cache.json")
    now = int(time.time())
    
    # キャッシュを読み込む
    cache_data = None
    if os.path.exists(cache_path):
        try:
            import json
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
        except:
            pass
            
    # キャッシュが無効（24時間経過）または存在しない場合は再構築
    # 24時間 = 86400秒
    if not cache_data or now - cache_data.get("last_updated", 0) > 86400:
        common.get_lock("rank_cache")
        try:
            # ロック取得後に再チェック（他プロセスが更新した可能性があるため）
            if os.path.exists(cache_path):
                try:
                    import json
                    with open(cache_path, "r", encoding="utf-8") as f:
                        cache_data = json.load(f)
                except:
                    pass
            
            if not cache_data or now - cache_data.get("last_updated", 0) > 86400:
                players = get_all_players()
                rankings = build_rankings(players)
                cache_data = {
                    "last_updated": now,
                    "total_players": len(players),
                    "rankings": rankings
                }
                import json
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(cache_data, f, ensure_ascii=False, indent=2)
        finally:
            common.release_lock("rank_cache")
            
    return cache_data

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    cache_data = get_rank_cache()
    
    # フォーマット日付
    update_time_str = common.get_time_str(cache_data["last_updated"])
    
    context = {
        "rankings": cache_data["rankings"],
        "total_players": cache_data["total_players"],
        "update_time": update_time_str
    }
    common.render_template("rank.html", context)

if __name__ == "__main__":
    main()
