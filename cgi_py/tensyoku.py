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

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
import os
import json

# 共通モジュールと設定モジュールのインポート
import config
from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正

def parse_cookie_user(cookie_str):
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

def save_syoku_master_list(user_id, master_list):
    """
    ユーザーの職業熟練度リストを保存します。
    """
    syoku_data = {str(i): master_list[i] for i in range(31)}
    common.syoku_regist(user_id, syoku_data)

def load_syoku_ini():
    """
    職業マスタデータ(syoku.json)をロードします。
    """
    path = os.path.join(common.BASE_DIR, config.Config['syoku_file'])
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

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
            syoku_target_str = params.get("syoku", "").strip()
            if syoku_target_str == "no" or not syoku_target_str:
                common.release_lock(user_id)
                common.show_error("転職先の職業を選択してください。")
                
            try:
                target_syoku = int(syoku_target_str)
                if target_syoku < 0 or target_syoku >= len(config.Config['chara_jobs']):
                    common.release_lock(user_id)
                    common.show_error("指定された職業は存在しません。")
            except ValueError:
                common.release_lock(user_id)
                common.show_error("指定された職業は存在しません。")
                
            # 転職前の現在の職業の熟練度を保存する
            # chara["job_level"] (インデックス33) には現在の職業の熟練度が入っています
            current_job = chara["job"]
            syoku_master[current_job] = chara["job_level"]
            save_syoku_master_list(user_id, syoku_master)
            
            # 転職先職業の必要条件チェック
            target_data = syoku_ini[target_syoku]
            a = target_data["req_str"]
            b = target_data["req_int"]
            c = target_data["req_mnd"]
            d = target_data["req_vit"]
            e = target_data["req_dex"]
            f = target_data["req_agi"]
            g = target_data["req_lck"]
            h = target_data["req_level"]
            
            # 特性値の条件確認
            if not (chara["str"] >= a and chara["int"] >= b and chara["mnd"] >= c and 
                    chara["vit"] >= d and chara["dex"] >= e and chara["agi"] >= f and 
                    chara["lck"] >= g and chara["level"] >= h):
                common.release_lock(user_id)
                common.show_error("まだ転職条件（能力値・レベル）を満たしていません。")
                
            # 熟練度要件の確認
            syoku_require = target_data["job_reqs"]
            for idx, req_val in enumerate(syoku_require):
                if idx < len(syoku_master) and req_val > syoku_master[idx]:
                    common.release_lock(user_id)
                    common.show_error(f"まだ転職条件（他の職業の熟練度要求）を満たしていません。")
                    
            # 転職実行
            chara["job"] = target_syoku
            if config.Config['master_tac_limit']:
                chara["unused30"] = 0 # 転職後の戦術（タクティクス）をクリア
                
            # 転職先職業の熟練度レベルをロードして設定
            chara["job_level"] = syoku_master[target_syoku]
            if chara["job_level"] <= 0:
                chara["job_level"] = 1
                
            # 転職先職業の熟練度が20未満の場合、現在のステータスが約10%減少する
            msg_penalty = ""
            if chara["job_level"] < 20:
                chara["str"] = int(chara["str"]) - int(chara["str"] / 10)
                chara["int"] = int(chara["int"]) - int(chara["int"] / 10)
                chara["mnd"] = int(chara["mnd"]) - int(chara["mnd"] / 10)
                chara["vit"] = int(chara["vit"]) - int(chara["vit"] / 10)
                chara["dex"] = int(chara["dex"]) - int(chara["dex"] / 10)
                chara["agi"] = int(chara["agi"]) - int(chara["agi"] / 10)
                chara["lck"] = int(chara["lck"]) - int(chara["lck"] / 10)
                
                # カルマ（LP）の減少 (力/5を引く)
                chara["lp"] = int(chara["lp"]) - int(chara["str"] / 5)
                
                # 最低限界値の保証
                if chara["str"] < 9: chara["str"] = 9
                if chara["int"] < 8: chara["int"] = 8
                if chara["mnd"] < 8: chara["mnd"] = 8
                if chara["vit"] < 9: chara["vit"] = 9
                if chara["dex"] < 9: chara["dex"] = 9
                if chara["agi"] < 8: chara["agi"] = 8
                if chara["lck"] < 8: chara["lck"] = 8
                if chara["lp"] < 1: chara["lp"] = 1
                
                msg_penalty = "※転職先の熟練度が低いため、能力値が10%減少しました。"
                
            # キャラクター情報保存
            common.chara_regist(user_id, chara)
            
            context = {
                "chara": chara,
                "user_id": user_id,
                "msg_penalty": msg_penalty,
                "job_name": config.Config['chara_jobs'][target_syoku]
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
                    
                a = target_data["req_str"]
                b = target_data["req_int"]
                c = target_data["req_mnd"]
                d = target_data["req_vit"]
                e = target_data["req_dex"]
                f = target_data["req_agi"]
                g = target_data["req_lck"]
                h = target_data["req_level"]
                
                # 条件チェック
                if (chara["str"] >= a and chara["int"] >= b and chara["mnd"] >= c and 
                    chara["vit"] >= d and chara["dex"] >= e and chara["agi"] >= f and 
                    chara["lck"] >= g and chara["level"] >= h):
                    
                    # 熟練度要件のチェック
                    syoku_require = target_data["job_reqs"]
                    req_ok = True
                    for idx, req_val in enumerate(syoku_require):
                        if idx < len(syoku_master) and req_val > syoku_master[idx]:
                            req_ok = False
                            break
                            
                    if req_ok:
                        job_info = {
                            "id": i,
                            "name": config.Config['chara_jobs'][i],
                            "master_level": syoku_master[i]
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
