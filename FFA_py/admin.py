#!D:\Python\Python314\python.exe
# -*- coding: utf-8 -*-
#------------------------------------------------------#
#  FFA改 Vips Ver 3.00
#  作成者: ねじりん
#------------------------------------------------------#
#------------------------------------------------------#
#　本スクリプトの著作権は下記の2人にあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改) 管理モードスクリプト
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
# FF BATTLE de i
#　programed by jun-k
#　http://www5b.biglobe.ne.jp/~jun-kei/
#　jun-kei@vanilla.freemail.ne.jp
#------------------------------------------------------#
#------------------------------------------------------#
# 本スクリプトの作成者はいくですが、スクリプトの著作権はCUMROさん
# にあります、必要な著作権表示を消去して使用することはできません
# 本スクリプトに関してのお問い合わせはいくまでお願いします。
# CUMROには絶対にしないで下さい。
#------------------------------------------------------#
"""
FFA Python/CGI - 管理者ツールスクリプト (admin.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')
import os
import time
import shutil

# 共通モジュールと設定モジュールのインポート
try:
    import config
    import common
except ImportError:
    from . import config
    from . import common



def get_all_players():
    """全プレイヤーのデータを取得します"""
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
    # パラメータの取得
    params = common.decode_params()
    mode = params.get("mode", "kanri_top")
    admin_pass = params.get("pass", "").strip()

    # パスワード認証
    if admin_pass != config.Config['admin_password']:
        common.show_error("管理者パスワードが一致しません。")

    # 1. 管理画面トップ
    if mode == "kanri_top":
        context = {
            "pass": admin_pass,
            "mode": mode
        }
        common.render_template("admin.html", context)
        return

    # 2. 全キャラクター表示
    elif mode == "kanri_all":
        players = get_all_players()
        # 最終行動時間順にソート (新しい順)
        players.sort(key=lambda x: x.get("last_time", 0), reverse=True)
        
        # 時刻表示文字列を付与
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
            
        context = {
            "pass": admin_pass,
            "players": players,
            "mode": mode
        }
        common.render_template("admin.html", context)
        return

    # 3. キャラクターデータ個別編集画面
    elif mode == "data":
        target_id = params.get("target_id", "").strip()
        if not target_id:
            common.show_error("対象キャラクターIDが指定されていません。")
            
        chara = common.chara_load(target_id)
        if not chara:
            common.show_error("指定されたキャラクターデータが見つかりません。")
            
        context = {
            "pass": admin_pass,
            "chara": chara,
            "mode": mode,
            "chara_syoku": config.Config['chara_jobs']
        }
        common.render_template("admin.html", context)
        return

    # 4. 個別データ保存処理
    elif mode == "save":
        target_id = params.get("target_id", "").strip()
        if not target_id:
            common.show_error("対象IDが不足しています。")
            
        common.get_lock(target_id)
        try:
            chara = common.chara_load(target_id)
            if not chara:
                common.show_error("データが見つかりません。")
                
            # パラメータの書き換え
            chara["name"] = params.get("name", chara["name"]).strip()
            chara["level"] = int(params.get("level", chara["level"]))
            chara["gold"] = int(params.get("gold", chara["gold"]))
            chara["hp"] = int(params.get("hp", chara["hp"]))
            chara["max_hp"] = int(params.get("max_hp", chara["max_hp"]))
            chara["str"] = int(params.get("str", chara["str"]))
            chara["int"] = int(params.get("int", chara["int"]))
            chara["dex"] = int(params.get("dex", chara["dex"]))
            chara["vit"] = int(params.get("vit", chara["vit"]))
            chara["agi"] = int(params.get("agi", chara["agi"]))
            chara["mnd"] = int(params.get("mnd", chara["mnd"]))
            chara["lck"] = int(params.get("lck", chara["lck"]))
            chara["lp"] = int(params.get("lp", chara["lp"]))
            chara["job"] = int(params.get("job", chara["job"]))
            chara["job_level"] = int(params.get("job_level", chara["job_level"]))
            chara["comment"] = params.get("comment", chara["comment"]).strip()
            
            # 保存
            common.chara_regist(target_id, chara)
        finally:
            common.release_lock(target_id)
            
        players = get_all_players()
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
        context = {
            "pass": admin_pass,
            "players": players,
            "mode": "kanri_all",
            "message": f"キャラクター「{chara['name']}」のデータを更新しました。"
        }
        common.render_template("admin.html", context)
        return

    # 5. 個別キャラクター削除
    elif mode == "del_chara":
        target_id = params.get("target_id", "").strip()
        if not target_id:
            common.show_error("対象IDが不足しています。")
            
        user_dir = os.path.join(config.Config['save_dir'], target_id)
        if os.path.exists(user_dir) and os.path.isdir(user_dir):
            shutil.rmtree(user_dir)
            
        players = get_all_players()
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
        context = {
            "pass": admin_pass,
            "players": players,
            "mode": "kanri_all",
            "message": f"キャラクターID「{target_id}」を削除しました。"
        }
        common.render_template("admin.html", context)
        return

    # 6. 長期間未ログインキャラクター一括削除
    elif mode == "del_noplay":
        players = get_all_players()
        now = int(time.time())
        limit_seconds = config.Config['delete_limit_days'] * 24 * 60 * 60
        
        deleted_count = 0
        deleted_names = []
        
        for p in players:
            ltime = now - p.get("last_time", 0)
            if ltime > limit_seconds:
                user_id = p["id"]
                user_dir = os.path.join(config.Config['save_dir'], user_id)
                if os.path.exists(user_dir) and os.path.isdir(user_dir):
                    shutil.rmtree(user_dir)
                    deleted_count += 1
                    deleted_names.append(p["name"])
                    
        players = get_all_players()
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
            
        msg = f"放置キャラクターを一括削除しました (削除数: {deleted_count}人: {', '.join(deleted_names)})" if deleted_count > 0 else "放置キャラクターはいませんでした。"
        context = {
            "pass": admin_pass,
            "players": players,
            "mode": "kanri_all",
            "message": msg
        }
        common.render_template("admin.html", context)
        return

    else:
        common.show_error("無効な管理モードです。")

if __name__ == "__main__":
    main()
