#!D:\Python\Python314\python.exe
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
import json

# 共通モジュールと設定モジュールのインポート
try:
    import config
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
except ImportError:
    from . import config
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正



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


def get_protected_user_ids():
    """自動削除・通常の個別削除から保護するユーザーIDを返します。"""
    return set(config.Config.get("protected_user_ids", []))


def protected_backup_path(user_id):
    backup_dir = config.Config.get(
        "protected_user_backup_dir",
        os.path.join(config.Config["save_dir"], "protected_users"),
    )
    return os.path.join(backup_dir, user_id, "user_all.json")


def is_valid_user_file(file_path, user_id):
    """復元元として使える統合ユーザーデータか確認します。"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return isinstance(data, dict) and data.get("chara", {}).get("id") == user_id
    except (OSError, json.JSONDecodeError, AttributeError):
        return False


def restore_protected_users():
    """欠落・破損した保護ユーザーを、固定バックアップから復元します。"""
    restored = []
    unavailable = []

    for user_id in sorted(get_protected_user_ids()):
        source = protected_backup_path(user_id)
        if not is_valid_user_file(source, user_id):
            unavailable.append(user_id)
            continue

        target = os.path.join(config.Config["save_dir"], user_id, "user_all.json")
        if is_valid_user_file(target, user_id):
            continue

        common.get_lock(user_id)
        try:
            if is_valid_user_file(target, user_id):
                continue
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(source, target)
            restored.append(user_id)
        finally:
            common.release_lock(user_id)

    return restored, unavailable

def main():
    # パラメータの取得
    params = common.decode_params()
    mode = params.get("mode", "kanri_top")
    admin_pass = params.get("pass", "").strip()

    # パスワード認証
    if admin_pass != config.Config['admin_password']:
        common.show_error("管理者パスワードが一致しません。")

    # データ改変・削除を伴う操作はCSRFトークン検証を必須とする
    method = os.environ.get("REQUEST_METHOD", "GET").upper()
    if method == "POST" and mode in (
        "save",
        "del_chara",
        "del_noplay",
        "restore_protected",
        "post_all_message",
    ):
        from sub_def.crypto import get_session, token_check
        token_check(params, get_session())

    # 1. 管理画面トップ
    if mode == "kanri_top":
        context = {
            "pass": admin_pass,
            "mode": mode
        }
        common.render_template("admin.html", context)
        return

    # 1.1 管理者による全体ニュース投稿
    elif mode == "post_all_message":
        message = params.get("message", "").strip()
        if not message:
            common.show_error("全体ニュースの本文を入力してください。")
        if len(message) > config.Config["all_message_input_limit"]:
            common.show_error(
                f"全体ニュースは{config.Config['all_message_input_limit']}文字以内で入力してください。"
            )

        common.get_lock("all_message_post")
        try:
            all_messages = common.all_message_load()
            all_messages.insert(
                0,
                {
                    "id": "admin",
                    "name": "管理人",
                    "time": common.get_time_str(),
                    "message": message,
                    "host": "admin",
                },
            )
            common.all_message_regist(
                all_messages[: config.Config["all_message_storage_limit"]]
            )
        finally:
            common.release_lock("all_message_post")

        context = {
            "pass": admin_pass,
            "mode": "kanri_top",
            "message": "全体ニュースを投稿しました。",
        }
        common.render_template("admin.html", context)
        return

    # 1.5 保護ユーザー復元
    elif mode == "restore_protected":
        restored, unavailable = restore_protected_users()
        players = get_all_players()
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))

        message_parts = []
        if restored:
            message_parts.append(f"保護ユーザーを復元しました: {', '.join(restored)}")
        if unavailable:
            message_parts.append(f"復元元が見つかりません: {', '.join(unavailable)}")
        if not message_parts:
            message_parts.append("復元が必要な保護ユーザーはいませんでした。")

        context = {
            "pass": admin_pass,
            "players": players,
            "mode": "kanri_all",
            "message": " / ".join(message_parts),
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
            "chara_syoku": [
                {"id": job_id, "name": job_name}
                for job_id, job_name in config.Config['chara_jobs'].items()
            ]
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
            chara["mnd"] = int(params.get("mnd", chara["mnd"]))
            chara["vit"] = int(params.get("vit", chara["vit"]))
            chara["dex"] = int(params.get("dex", chara["dex"]))
            chara["agi"] = int(params.get("agi", chara["agi"]))
            chara["cha"] = int(params.get("cha", chara["cha"]))
            chara["karma"] = int(params.get("karma", chara["karma"]))
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

        if target_id in get_protected_user_ids():
            players = get_all_players()
            for p in players:
                p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
            context = {
                "pass": admin_pass,
                "players": players,
                "mode": "kanri_all",
                "message": f"保護ユーザー「{target_id}」は削除できません。",
            }
            common.render_template("admin.html", context)
            return
            
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
        limit_seconds = config.Config['character_delete_after_days'] * 24 * 60 * 60
        
        deleted_count = 0
        deleted_names = []
        protected_count = 0
        
        for p in players:
            ltime = now - p.get("last_time", 0)
            if ltime > limit_seconds:
                user_id = p["id"]
                if user_id in get_protected_user_ids():
                    protected_count += 1
                    continue
                user_dir = os.path.join(config.Config['save_dir'], user_id)
                if os.path.exists(user_dir) and os.path.isdir(user_dir):
                    shutil.rmtree(user_dir)
                    deleted_count += 1
                    deleted_names.append(p["name"])
                    
        players = get_all_players()
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
            
        if deleted_count > 0:
            msg = f"放置キャラクターを一括削除しました (削除数: {deleted_count}人: {', '.join(deleted_names)})"
        else:
            msg = "放置キャラクターはいませんでした。"
        if protected_count:
            msg += f" 保護ユーザー {protected_count}人は対象外にしました。"
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
