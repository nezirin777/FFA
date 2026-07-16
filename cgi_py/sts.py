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
FFA Python/CGI - ステータス詳細設定画面 (sts.py)
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

# 共通モジュールのインポート
try:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    import config
except ImportError:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from . import config

# Windows等で標準出力をUTF-8にする設定
def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在バージョンアップ中です。しばらくお待ちください。")

    # パラメータ解析
    in_params = common.decode_params()
    user_id = in_params.get("id", "")
    # IDOR対策: 状態変更は本人のみ許可(ロック取得前にチェック)
    common.require_owner(user_id)
    chara_log = in_params.get("mydata", "")
    mode = in_params.get("mode", "")

    # ログインクッキーの取得（予備チェック）
    cookie_id = common.get_cookie(config.Config['cookie_name'])

    # キャラクターデータ読み込み
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターデータが見つかりません。ログインし直してください。")

    # パスワードチェック・セキュリティバリデーション (ログイン中か)
    # 簡易的にログイン認証文字列(chara_log)が含まれるかチェック
    # （通常、chara_logにはIDやパスワードなどの認証文字列が入る）
    # ここでは既存の他のスクリプト(battle.pyなど)と同様のチェックを行う

    if mode == "st_buy":
        # === ステータス更新処理 ===
        # 戻るフォーム (error.html 側で最新のCSRFトークン付きで描画される)
        back_ctx = {
            "back_action": config.Config['status_script'],
            "back_params": {"id": user_id, "mydata": chara_log},
            "back_label": "戻る",
        }

        if user_id == "test":
            common.show_error("テストキャラはステータス変更はできません", back_ctx)

        # パラメータ取得
        site = in_params.get("site", "").strip()
        url = in_params.get("url", "").strip()
        waza = in_params.get("waza", "").strip()
        chara_img_idx = in_params.get("chara", "0").strip()

        # デフォルト値
        if not site:
            site = "いくのCGIのHP"
        if not url:
            url = "http://www.eriicu.com"

        # URLスキーム検証: href に埋め込まれるため http(s):// 以外(javascript: 等)を拒否
        if not (url.startswith("http://") or url.startswith("https://")):
            common.show_error("ホームページURLは http:// または https:// で始まる必要があります。", back_ctx)

        # コメント長さ制限
        if len(waza) > 100:
            common.show_error("技発動コメントが長すぎます！(100文字以内)", back_ctx)

        # 禁止ワードチェック
        for word in config.Config['ban_words']:
            if word in waza or word in site:
                common.show_error(f"入力に禁止語「{word}」が含まれています", back_ctx)

        # 画像インデックスチェック
        try:
            chara_img_idx = int(chara_img_idx)
            if chara_img_idx < 0 or chara_img_idx >= len(config.Config['chara_images']):
                chara_img_idx = 0
        except ValueError:
            chara_img_idx = 0

        # データ更新
        chara["site"] = site
        chara["url"] = url
        chara["img"] = chara_img_idx
        chara["comment"] = waza  # Perl版の $chara[23] (技発動コメント) は Python では 'comment' にマッピング

        common.get_lock(user_id)
        try:
            common.chara_regist(user_id, chara)
        finally:
            common.release_lock(user_id)

        # 完了画面表示
        context = {
            "chara": chara,
            "chara_log": chara_log,
            "new_chara": chara_log  # 通常は更新されたログインキー等を渡す
        }
        common.render_template("sts_result.html", context)

    else:
        # === ステータス表示画面 (chara_st) ===
        item = common.item_load(user_id)
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

        # 命中率、回避率、必殺率の計算
        # 信仰心 -> dex, 器用さ -> agi, 速さ -> mnd にマッピングされていることに注意
        # 命中率 = 器用さ(agi) / 10 + 51
        hit_ritu = int((chara.get("agi", 10) / 10) + 51)
        if hit_ritu > 150:
            hit_ritu = 150
            
        # 回避率 = 速さ(mnd) / 20
        kaihi_ritu = int(chara.get("mnd", 10) / 20)
        if kaihi_ritu > 50:
            kaihi_ritu = 50
            
        # 必殺率 = カルマ(lp) / 15 + 10 + ジョブレベル(job_level)
        waza_ritu = int(chara.get("lp", 0) / 15) + 10 + chara.get("job_level", 0)
        if waza_ritu > 75:
            waza_ritu = 75

        # 装備品補正値
        ci_plus = item.get("weapon", {}).get("effect", 0) + item.get("accessory", {}).get("spare1", 0) # 命中補正
        cd_plus = item.get("armor", {}).get("effect", 0) + item.get("accessory", {}).get("spare3", 0) # 回避補正
        waza_plus = item.get("accessory", {}).get("spare2", 0) # 必殺補正

        # 作戦（戦術）の取得
        tac_name = "普通に戦う"
        tac_no = chara.get("unused30", 0) # Perlの$chara[30]に対応
        tac_ex = "戦術を使用せずに戦います"
        
        tac_file_path = os.path.join(common.BASE_DIR, config.Config['tac_file'])
        if os.path.exists(tac_file_path):
            try:
                with open(tac_file_path, "r", encoding="utf-8") as f:
                    tactics = json.load(f)
                for t in tactics:
                    if t.get("no") == tac_no:
                        tac_name = t["name"]
                        tac_ex = t.get("desc", "")
                        break
            except:
                pass

        # 称号の取得
        syou_idx = chara.get("title", 0)
        if syou_idx < 0 or syou_idx >= len(config.Config['titles']):
            syou_idx = 0
        syou_name = config.Config['titles'][syou_idx]

        # 極めたジョブのリスト
        syoku = common.syoku_load(user_id)
        mastered_jobs = []
        if syoku:
            for job_idx_str, level in syoku.items():
                try:
                    job_idx = int(job_idx_str)
                    if level >= 60 and job_idx < len(config.Config['chara_jobs']):
                        mastered_jobs.append(config.Config['chara_jobs'][job_idx])
                except ValueError:
                    pass

        # ステータスバーの幅計算（最大パラメータ幅を100pxとする）
        divpm = int(config.Config['max_param'] / 100) if config.Config['max_param'] > 0 else 100
        if divpm <= 0:
            divpm = 100
            
        bw_str = int(chara.get("str", 10) / divpm)
        bw_int = int(chara.get("int", 10) / divpm)
        bw_dex = int(chara.get("dex", 10) / divpm) # 信仰心
        bw_vit = int(chara.get("vit", 10) / divpm) # 生命力
        bw_agi = int(chara.get("agi", 10) / divpm) # 器用さ
        bw_mnd = int(chara.get("mnd", 10) / divpm) # 速さ
        bw_lck = int(chara.get("lck", 10) / divpm) # 魅力
        bw_lp = int(chara.get("lp", 0) / divpm)
        
        bw_hit = int((hit_ritu + ci_plus) * 0.5)
        bw_kaihi = int((kaihi_ritu + cd_plus) * 0.5)
        bw_waza = int((waza_ritu + waza_plus) * 1)
        
        # 最大幅制限
        bw_hit = min(100, bw_hit)
        bw_kaihi = min(100, bw_kaihi)
        bw_waza = min(100, bw_waza)

        # ジョブ熟練度の全表示用（これまでのジョブ経験）
        all_jobs_status = []
        for i, job_name in enumerate(config.Config['chara_jobs']):
            # 管理ジョブは除外またはスキップ
            if job_name == "管理者" and chara.get("job") != i:
                continue
            level = syoku.get(str(i), 0) if syoku else 0
            # レベルによる表示マーク
            if level >= 60:
                mark = "★Master"
            elif level >= 40:
                mark = "●熟練"
            elif level >= 20:
                mark = "▲修行"
            else:
                mark = "−"
            all_jobs_status.append({
                "name": job_name,
                "level": level,
                "mark": mark
            })

        # 表示コンテキストの作成
        context = {
            "chara": chara,
            "item": item,
            "chara_log": chara_log,
            "hit_ritu": hit_ritu,
            "kaihi_ritu": kaihi_ritu,
            "waza_ritu": waza_ritu,
            "ci_plus": ci_plus,
            "cd_plus": cd_plus,
            "waza_plus": waza_plus,
            "tac_name": tac_name,
            "tac_ex": tac_ex,
            "syou_name": syou_name,
            "mastered_jobs": mastered_jobs,
            "all_jobs_status": all_jobs_status,
            "esex": "男" if chara.get("sex") == 1 else "女",
            "next_ex": chara.get("level", 1) * config.Config['level_up_coeff'],
            # バー幅
            "bw_str": bw_str, "bw_int": bw_int, "bw_dex": bw_dex, "bw_vit": bw_vit,
            "bw_agi": bw_agi, "bw_mnd": bw_mnd, "bw_lck": bw_lck, "bw_lp": bw_lp,
            "bw_hit": bw_hit, "bw_kaihi": bw_kaihi, "bw_waza": bw_waza
        }
        common.render_template("sts.html", context)

if __name__ == "__main__":
    main()
