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
import os

# 共通モジュールのインポート
try:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    import config
    from sub_def.crypto import get_session, token_check
except ImportError:
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
    from . import config
    from sub_def.crypto import get_session, token_check

# Windows等で標準出力をUTF-8にする設定
def load_job_tactics(job_id, job_level):
    """共通戦術マスターから、特定のジョブで使用可能な戦術を読み込みます。"""
    tactics = []
    for item in common.master_records_for_job(config.Config["tac_file"], job_id):
        # マスター戦術(ms == 1)はジョブレベル60以上でのみ利用可能。
        if item.get("ms", 0) == 0 or (item.get("ms", 0) == 1 and job_level >= 60):
            tactics.append({
                "no": item["no"],
                "name": item["name"],
                "desc": item.get("desc", ""),
                "ms": item.get("ms", 0),
            })
            
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
            
    # 2. マスターした他職業の戦術を追加。Ver2の $master_tac と同じ設定で制御する。
    if config.Config['master_tactics_enabled'] == 1 and syoku:
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
    # IDOR対策: 状態変更は本人のみ許可(ロック取得前にチェック)
    common.require_owner(user_id)
    chara_log = in_params.get("mydata", "")
    mode = in_params.get("mode", "")

    if mode == "senjutu_henkou":
        # === 戦術変更処理 ===
        token_check(in_params, get_session())
        senjutu_no_str = in_params.get("senjutu_no")
        if senjutu_no_str is None:
            common.show_error("変更する戦術を選択してください。")
        try:
            senjutu_no = int(senjutu_no_str)
        except ValueError:
            common.show_error("戦術番号が不正です。")

        # Ver2と同じく、ロックを取得してから最新の職業・熟練度を読み込む。
        # 表示時点の候補で判定・保存すると、転職や戦闘の更新を上書きし得る。
        common.get_lock(user_id)
        try:
            chara = common.chara_load(user_id)
            if not chara:
                common.show_error("キャラクターデータが見つかりません。ログインし直してください。")
            syoku = common.syoku_load(user_id)
            available_tacs = get_available_tactics(chara, syoku)
            selected_tac = next(
                (t for t in available_tacs if t["no"] == senjutu_no), None
            )
            if selected_tac is None:
                common.show_error("選択された戦術は存在しないか、使用する条件を満たしていません。")

            chara["tactic_id"] = senjutu_no
            chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")
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
        chara = common.chara_load(user_id)
        if not chara:
            common.show_error("キャラクターデータが見つかりません。ログインし直してください。")
        syoku = common.syoku_load(user_id)
        available_tacs = get_available_tactics(chara, syoku)

        # 現在の戦術を判定
        now_tac_no = chara.get("tactic_id", 0)
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
