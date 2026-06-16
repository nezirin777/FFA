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
FFA Python/CGI - 作戦（戦術）変更画面 (tac_change.py)
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
def load_job_tactics(job_id, job_level):
    """特定のジョブで使用可能な戦術を読み込みます"""
    tactics = []
    tac_path = os.path.join(common.BASE_DIR, config.Config['tac_folder'], f"tac{job_id}.json")
    
    if os.path.exists(tac_path):
        try:
            with open(tac_path, "r", encoding="utf-8") as f:
                items = json.load(f)
            for item in items:
                # マスター戦術(ms == 1)の場合はジョブレベルが60以上である必要がある
                if item.get("ms", 0) == 0 or (item.get("ms", 0) == 1 and job_level >= 60):
                    tactics.append({
                        "no": item["no"],
                        "name": item["name"],
                        "desc": item.get("desc", ""),
                        "ms": item.get("ms", 0)
                    })
        except Exception:
            pass
            
    return tactics

def get_available_tactics(chara, syoku):
    """現在のキャラクターが使用可能なすべての戦術を取得します"""
    available_tacs = []
    
    # 0. デフォルト戦術（普通に戦う）
    available_tacs.append({
        "no": 0,
        "name": "普通に戦う",
        "desc": "戦術を使用せずに戦います",
        "ms": 0
    })
    
    current_job = chara.get("job", 0)
    current_job_lv = chara.get("job_level", 0)
    
    # 1. 現在の職業の戦術を追加
    current_tacs = load_job_tactics(current_job, current_job_lv)
    for t in current_tacs:
        if t["no"] != 0:
            available_tacs.append(t)
            
    # 2. マスターした他職業の戦術を追加 (config.Config['master_tac_limit'] == 1 の場合)
    if config.Config['master_tac_limit'] == 1 and syoku:
        for job_idx_str, level in syoku.items():
            try:
                job_idx = int(job_idx_str)
                # ジョブレベルが60以上で、かつ現在の職業とは異なる場合、その職業の戦術も使える
                if level >= 60 and job_idx != current_job:
                    other_tacs = load_job_tactics(job_idx, level)
                    for t in other_tacs:
                        if t["no"] != 0 and not any(x["no"] == t["no"] for x in available_tacs):
                            available_tacs.append(t)
            except ValueError:
                pass
                
    return available_tacs

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在バージョンアップ中です。しばらくお待ちください。")

    # パラメータ解析
    in_params = common.decode_params()
    user_id = in_params.get("id", "")
    chara_log = in_params.get("mydata", "")
    mode = in_params.get("mode", "")

    # キャラクターデータのロード
    chara = common.chara_load(user_id)
    if not chara:
        common.show_error("キャラクターデータが見つかりません。ログインし直してください。")

    # 職業熟練度データのロード
    syoku = common.syoku_load(user_id)
    
    # 使用可能な全戦術を取得
    available_tacs = get_available_tactics(chara, syoku)

    if mode == "senjutu_henkou":
        # === 戦術変更処理 ===
        senjutu_no_str = in_params.get("senjutu_no", "0")
        try:
            senjutu_no = int(senjutu_no_str)
        except ValueError:
            senjutu_no = 0

        # 選択された戦術が本当に使用可能か照合
        selected_tac = None
        for t in available_tacs:
            if t["no"] == senjutu_no:
                selected_tac = t
                break

        if selected_tac is None:
            common.show_error("選択された戦術は存在しないか、使用する条件を満たしていません。")

        # 変更保存
        chara["unused30"] = senjutu_no # Perlの$chara[30]に対応
        
        common.get_lock(user_id)
        try:
            common.chara_regist(user_id, chara)
        finally:
            common.release_lock(user_id)

        # 結果画面表示
        context = {
            "chara": chara,
            "chara_log": chara_log,
            "new_chara": chara_log,
            "selected_tac_name": selected_tac["name"]
        }
        common.render_template("tac_result.html", context)

    else:
        # === 戦術選択画面表示 (senjutu) ===
        # 現在の戦術を判定
        now_tac_no = chara.get("unused30", 0)
        now_tac_name = "普通に戦う"
        now_tac_desc = "戦術を使用せずに戦います"
        
        for t in available_tacs:
            if t["no"] == now_tac_no:
                now_tac_name = t["name"]
                now_tac_desc = t["desc"]
                break

        context = {
            "chara": chara,
            "chara_log": chara_log,
            "available_tacs": available_tacs,
            "now_tac_no": now_tac_no,
            "now_tac_name": now_tac_name,
            "now_tac_desc": now_tac_desc
        }
        common.render_template("tac_change.html", context)

if __name__ == "__main__":
    main()
