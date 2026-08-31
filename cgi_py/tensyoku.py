#------------------------------------------------------#
#  FFA改 Vips Ver 3.00
#  作成者: ねじりん
#------------------------------------------------------#
#------------------------------------------------------#
#　本スクリプトの著作権はいくにあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改)
#　edit by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#---------------------------------------------------------------#
"""
FFA Python/CGI - 転職システムスクリプト (tensyoku.py)
"""
import os

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
from sub_def.crypto import get_session, token_check

parse_cookie_user = common.parse_cookie_user

def get_syoku_master_list(user_id):
    """
    ユーザーの職業熟練度リストを取得します。
    """
    syoku_data = common.syoku_load(user_id)
    if not syoku_data:
        return [0] * 31
    # 0〜30のキーの熟練度をリストにする
    lst = []
    for i in range(31):
        lst.append(int(syoku_data.get(str(i), 0)))
    return lst

def load_syoku_ini():
    """
    職業マスタデータ(syoku.json)をロードします。
    """
    return common.load_json_list(config.Config["syoku_file"])

def get_job_requirements(target_data):
    """
    転職条件を現在のキャラクターキーに揃えて返します。

    旧版 syoku.ini の条件列は
    str, int, mnd(信仰心), vit, dex(器用さ), agi(速さ), cha(魅力), karma(カルマ)
    の順。
    """
    return {
        "str": target_data.get("req_str", 0),
        "int": target_data.get("req_int", 0),
        "mnd": target_data.get("req_mnd", 0),
        "vit": target_data.get("req_vit", 0),
        "dex": target_data.get("req_dex", 0),
        "agi": target_data.get("req_agi", 0),
        "cha": target_data.get("req_cha", 0),
        "karma": target_data.get("req_karma", 0),
    }

def meets_job_requirements(chara, requirements):
    return all(int(chara.get(key, 0)) >= int(value) for key, value in requirements.items())

def has_job_history(syoku_master, job_id):
    """一度でも就いた職業かを、保存済みの熟練度から判定する。"""
    return 0 <= job_id < len(syoku_master) and syoku_master[job_id] > 0

def meets_job_master_requirements(syoku_master, target_data):
    """未経験職へ転職するための、必要マスター職条件を判定する。"""
    for job_id, required_level in enumerate(target_data["job_reqs"]):
        if job_id < len(syoku_master) and required_level > syoku_master[job_id]:
            return False
    return True

def can_change_to_job(chara, syoku_master, target_job, target_data):
    """経験済み職は前提を免除し、未経験職には従来の前提を適用する。"""
    return has_job_history(syoku_master, target_job) or (
        meets_job_requirements(chara, get_job_requirements(target_data))
        and meets_job_master_requirements(syoku_master, target_data)
    )

def main():
    if config.Config['maintenance_mode']:
        common.show_error("現在メンテナンス中です。しばらくお待ちください。")

    params = common.decode_params()
    mode = params.get("mode", "").strip()
    user_id = params.get("id", "").strip()
    
    # ユーザー認証
    cookie_str = common.get_cookie(config.Config['cookie_name'])
    c_id, c_pass = parse_cookie_user(cookie_str)
    
    if not user_id:
        if c_id:
            user_id = c_id
        else:
            common.show_error("ログイン情報がありません。再度ログインしてください。")
            
    # ロック取得
    common.get_lock(user_id)
    try:
        chara = common.chara_load(user_id)
        if not chara:
            common.release_lock(user_id)
            common.show_error("キャラクター情報が見つかりません。")
            
        # パスワードチェック
        if c_id != user_id or c_pass != chara["pass"]:
            common.release_lock(user_id)
            common.show_error("ログインパスワードが一致しません。")
            
        syoku_master = get_syoku_master_list(user_id)
        syoku_ini = load_syoku_ini()
        
        # 1. 転職実行処理 (tensyoku_change)
        if mode == "tensyoku_change":
            token_check(params, get_session())
            syoku_target_str = params.get("syoku", "").strip()
            if syoku_target_str == "no" or not syoku_target_str:
                common.release_lock(user_id)
                common.show_error("転職先の職業を選択してください。")
                
            try:
                target_syoku = int(syoku_target_str)
                if target_syoku not in config.Config['chara_jobs']:
                    common.release_lock(user_id)
                    common.show_error("指定された職業は存在しません。")
            except ValueError:
                common.release_lock(user_id)
                common.show_error("指定された職業は存在しません。")
                
            # 現在職を退避する前の職歴で、再転職かどうかを確定する。
            is_return_job = has_job_history(syoku_master, target_syoku)

            # 転職前の現在の職業の熟練度を保存する
            # chara["job_level"] (インデックス33) には現在の職業の熟練度が入っています
            current_job = chara["job"]
            syoku_master[current_job] = chara["job_level"]
            
            # 転職先職業の必要条件チェック
            target_data = syoku_ini[target_syoku]
            if not is_return_job:
                requirements = get_job_requirements(target_data)

                # 未経験職だけは、従来どおり能力値・カルマの前提を確認する。
                if not meets_job_requirements(chara, requirements):
                    common.release_lock(user_id)
                    common.show_error("まだ転職条件（能力値・カルマ）を満たしていません。")

                # 未経験職だけは、必要マスター職も確認する。
                if not meets_job_master_requirements(syoku_master, target_data):
                    common.release_lock(user_id)
                    common.show_error("まだ転職条件（他の職業の熟練度要求）を満たしていません。")
                    
            # 転職実行
            chara["job"] = target_syoku
            if config.Config['reset_tactics_on_job_change']:
                chara["tactic_id"] = 0 # 転職後の戦術（タクティクス）をクリア
                
            # 転職先職業の熟練度レベルをロードして設定
            chara["job_level"] = syoku_master[target_syoku]
            if chara["job_level"] <= 0:
                chara["job_level"] = 1
                
            # 転職先職業の熟練度が20未満の場合、現在のステータスが約10%減少する
            msg_penalty = ""
            if chara["job_level"] < 20:
                chara["str"] = int(chara["str"]) - int(chara["str"] / 10)
                chara["int"] = int(chara["int"]) - int(chara["int"] / 10)
                chara["agi"] = int(chara["agi"]) - int(chara["agi"] / 10)
                chara["vit"] = int(chara["vit"]) - int(chara["vit"] / 10)
                chara["mnd"] = int(chara["mnd"]) - int(chara["mnd"] / 10)
                chara["dex"] = int(chara["dex"]) - int(chara["dex"] / 10)
                chara["cha"] = int(chara["cha"]) - int(chara["cha"] / 10)
                
                # カルマの減少 (力/5を引く)
                chara["karma"] = int(chara["karma"]) - int(chara["str"] / 5)
                
                # 最低限界値の保証
                if chara["str"] < 9: chara["str"] = 9
                if chara["int"] < 8: chara["int"] = 8
                if chara["vit"] < 9: chara["vit"] = 9
                if chara["mnd"] < 8: chara["mnd"] = 8
                if chara["dex"] < 9: chara["dex"] = 9
                if chara["agi"] < 8: chara["agi"] = 8
                if chara["cha"] < 8: chara["cha"] = 8
                if chara["karma"] < 1: chara["karma"] = 1
                
                msg_penalty = "※転職先の熟練度が低いため、能力値が10%減少しました。"
                
            # 職業熟練度とキャラクター情報を同じ更新で保存する。
            syoku_data = {str(index): syoku_master[index] for index in range(31)}
            chara["host"] = os.environ.get("REMOTE_ADDR", "127.0.0.1")
            common.save_user_sections(user_id, chara=chara, syoku=syoku_data)
            
            context = {
                "chara": chara,
                "user_id": user_id,
                "msg_penalty": msg_penalty,
                "job_name": config.Config['chara_jobs'].get(target_syoku, "不明な職業")
            }
            common.render_template("tensyoku_result.html", context)
            
        # 2. 転職画面初期表示
        else:
            # 転職できる職業の一覧を算出
            available_jobs = []
            available_unmastered_jobs = []
            
            for i, target_data in enumerate(syoku_ini):
                if i == chara["job"]:
                    continue # 現在の職業は除外
                    
                if can_change_to_job(chara, syoku_master, i, target_data):
                    job_info = {
                        "id": i,
                        "name": config.Config['chara_jobs'].get(i, "不明な職業"),
                        "master_level": syoku_master[i],
                        "is_return_job": has_job_history(syoku_master, i),
                    }
                    available_jobs.append(job_info)
                    if syoku_master[i] < 60:
                        available_unmastered_jobs.append(job_info)
                            
            context = {
                "chara": chara,
                "user_id": user_id,
                "available_jobs": available_jobs,
                "available_unmastered_jobs": available_unmastered_jobs
            }
            common.render_template("tensyoku.html", context)
            
    finally:
        common.release_lock(user_id)

if __name__ == "__main__":
    main()
