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
FFA Python/CGI - システム詳細設定・登録者一覧 (system.py)
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
try:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    import config
except ImportError:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from . import config

# Windows等で標準出力をUTF-8にする設定
def get_all_players():
    """全プレイヤーのデータをロードします"""
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

def build_rankings_cache():
    """全プレイヤーをレベル順にソートし、必要な項目をキャッシュします"""
    cache_path = os.path.join(config.Config['save_dir'], "system_rank_cache.json")
    now = int(time.time())
    
    players = get_all_players()
    # レベル降順でソート
    sorted_players = sorted(players, key=lambda x: x.get("level", 1), reverse=True)
    
    cache_data = {
        "last_updated": now,
        "total_players": len(sorted_players),
        "players": sorted_players
    }
    
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
    return cache_data

def get_rankings_cache():
    """ランキングキャッシュを取得、または再構築します"""
    cache_path = os.path.join(config.Config['save_dir'], "system_rank_cache.json")
    now = int(time.time())
    cache_data = None
    
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
        except:
            pass
            
    # 24時間キャッシュ
    if not cache_data or now - cache_data.get("last_updated", 0) > 86400:
        common.get_lock("system_rank_cache")
        try:
            # 二重更新チェック
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "r", encoding="utf-8") as f:
                        cache_data = json.load(f)
                except:
                    pass
            if not cache_data or now - cache_data.get("last_updated", 0) > 86400:
                cache_data = build_rankings_cache()
        finally:
            common.release_lock("system_rank_cache")
            
    return cache_data

def calculate_stats(chara, item):
    """キャラクターの命中・回避・必殺などの表示用ステータスを計算します"""
    # 命中・回避・必殺
    hit_ritu = int((chara.get("agi", 10) / 10) + 51)
    if hit_ritu > 150:
        hit_ritu = 150
        
    kaihi_ritu = int(chara.get("mnd", 10) / 20)
    if kaihi_ritu > 50:
        kaihi_ritu = 50
        
    waza_ritu = int(chara.get("lp", 0) / 15) + 10 + chara.get("job_level", 0)
    if waza_ritu > 75:
        waza_ritu = 75

    ci_plus = item.get("weapon", {}).get("effect", 0) + item.get("accessory", {}).get("spare1", 0)
    cd_plus = item.get("armor", {}).get("effect", 0) + item.get("accessory", {}).get("spare3", 0)
    waza_plus = item.get("accessory", {}).get("spare2", 0)

    # 削除までの残り日数算出 (最終更新時間 + limit日数 - 現在時刻)
    now = int(time.time())
    limit_sec = config.Config['delete_limit_days'] * 24 * 60 * 60
    delete_time = chara.get("last_time", now) + limit_sec
    left_days = max(0, int((delete_time - now) / (24 * 60 * 60)))

    # 勝率
    battle_count = chara.get("unused21", 0)
    win_count = chara.get("unused22", 0)
    win_ratio = int((win_count / battle_count) * 100) if battle_count > 0 else 0

    # パラメータバー幅計算 (最大パラメータ幅 100px とする)
    divpm = int(config.Config['max_param'] / 100) if config.Config['max_param'] > 0 else 100
    if divpm <= 0:
        divpm = 100
        
    bw_str = int(chara.get("str", 10) / divpm)
    bw_int = int(chara.get("int", 10) / divpm)
    bw_dex = int(chara.get("dex", 10) / divpm)
    bw_vit = int(chara.get("vit", 10) / divpm)
    bw_agi = int(chara.get("agi", 10) / divpm)
    bw_mnd = int(chara.get("mnd", 10) / divpm)
    bw_lck = int(chara.get("lck", 10) / divpm)
    bw_lp = int(chara.get("lp", 0) / divpm)
    
    bw_hit = int((hit_ritu + ci_plus) * 0.5)
    bw_kaihi = int((kaihi_ritu + cd_plus) * 0.5)
    bw_waza = int((waza_ritu + waza_plus) * 1)

    return {
        "hit_ritu": hit_ritu, "kaihi_ritu": kaihi_ritu, "waza_ritu": waza_ritu,
        "ci_plus": ci_plus, "cd_plus": cd_plus, "waza_plus": waza_plus,
        "left_days": left_days, "win_ratio": win_ratio,
        "bw_str": bw_str, "bw_int": bw_int, "bw_dex": bw_dex, "bw_vit": bw_vit,
        "bw_agi": bw_agi, "bw_mnd": bw_mnd, "bw_lck": bw_lck, "bw_lp": bw_lp,
        "bw_hit": bw_hit, "bw_kaihi": bw_kaihi, "bw_waza": bw_waza
    }

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在バージョンアップ中です。しばらくお待ちください。")
        
    in_params = common.decode_params()
    mode = in_params.get("mode", "")

    if mode == "chara_sts":
        # === 他人の詳細ステータス閲覧 ===
        target_id = in_params.get("id", "")
        target_chara = common.chara_load(target_id)
        if not target_chara:
            common.show_error("指定されたキャラクターデータが見つかりません。")

        target_item = common.item_load(target_id)
        if not target_item:
            target_item = {
                "weapon": {"name": "素手", "dmg": 0, "effect": 0},
                "armor": {"name": "衣服", "def": 0, "effect": 0},
                "accessory": {
                    "name": "なし", "effect_id": 0,
                    "bonus": {"str": 0, "int": 0, "dex": 0, "vit": 0, "agi": 0, "mnd": 0, "lck": 0, "lp": 0},
                    "attrib": 0, "spare1": 0, "spare2": 0, "spare3": 0
                }
            }

        # ステータス詳細計算
        stats = calculate_stats(target_chara, target_item)

        # 称号名
        syou_idx = target_chara.get("title", 0)
        syou_name = config.Config['titles'][syou_idx] if 0 <= syou_idx < len(config.Config['titles']) else config.Config['titles'][0]

        # 極めたジョブのリスト
        syoku = common.syoku_load(target_id)
        mastered_jobs = []
        if syoku:
            for job_idx_str, level in syoku.items():
                try:
                    job_idx = int(job_idx_str)
                    if level >= 60 and job_idx < len(config.Config['chara_jobs']):
                        mastered_jobs.append(config.Config['chara_jobs'][job_idx])
                except ValueError:
                    pass

        context = {
            "chara": target_chara,
            "item": target_item,
            "syou_name": syou_name,
            "mastered_jobs": mastered_jobs,
            "esex": "男" if target_chara.get("sex") == 1 else "女",
            "next_ex": target_chara.get("level", 1) * config.Config['level_up_coeff'],
            **stats
        }
        common.render_template("system_chara_sts.html", context)

    elif mode == "img_list":
        # === 画像インデックス一覧表示 ===
        context = {
            "chara_img": config.Config['chara_images']
        }
        common.render_template("system_img_list.html", context)

    else:
        # === 登録者一覧ランキング (ranking_no_html) ===
        try:
            shtm = common.to_int(in_params.get("shtm", "0"), 0)
        except ValueError:
            shtm = 0
            
        cache_data = get_rankings_cache()
        all_players = cache_data["players"]
        total_players = cache_data["total_players"]
        update_time_str = common.get_time_str(cache_data["last_updated"])
        
        # 1ページ20件
        items_per_page = 20
        ifr = shtm * items_per_page
        ito = min(total_players, ifr + items_per_page)
        
        page_players = all_players[ifr:ito]
        
        # 各プレイヤーの表示用ステータスを事前計算して結合
        formatted_players = []
        for idx, p in enumerate(page_players):
            p_id = p["id"]
            p_item = common.item_load(p_id) or {
                "weapon": {"name": "素手", "dmg": 0, "effect": 0},
                "armor": {"name": "衣服", "def": 0, "effect": 0},
                "accessory": {
                    "name": "なし", "effect_id": 0,
                    "bonus": {"str": 0, "int": 0, "dex": 0, "vit": 0, "agi": 0, "mnd": 0, "lck": 0, "lp": 0},
                    "attrib": 0, "spare1": 0, "spare2": 0, "spare3": 0
                }
            }
            stats = calculate_stats(p, p_item)
            formatted_players.append({
                "chara": p,
                "rank_num": ifr + idx + 1,
                "job_name": config.Config['chara_jobs'][p.get("job", 0)],
                **stats
            })

        # ページングリンク情報
        total_pages = (total_players + items_per_page - 1) // items_per_page
        pages_links = []
        for i in range(total_pages):
            p_start = i * items_per_page + 1
            p_end = min(total_players, (i + 1) * items_per_page)
            pages_links.append({
                "page": i,
                "label": f"{p_start}位〜{p_end}位"
            })

        context = {
            "players": formatted_players,
            "total_players": total_players,
            "ifr": ifr + 1,
            "ito": ito,
            "shtm": shtm,
            "total_pages": total_pages,
            "pages_links": pages_links,
            "update_time": update_time_str,
            "chara_img": config.Config['chara_images']
        }
        common.render_template("system_ranking.html", context)

if __name__ == "__main__":
    main()
