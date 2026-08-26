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
import os
import time
import shutil
import json
import hmac

# 共通モジュールと設定モジュールのインポート
try:
    import config
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正
except ImportError:
    from . import config
    from sub_def import common  # common.pyのsub_defへの移動に伴うインポート修正


MASTER_DEFINITIONS = {
    "syoku": {
        "label": "職業",
        "config_key": "syoku_file",
        "id_mode": "index",
        "can_delete": False,
    },
    "tac": {
        "label": "必殺技・戦術",
        "config_key": "tac_file",
        "id_mode": "no",
        "can_delete": True,
    },
    "weapon": {
        "label": "武器",
        "config_key": "weapon_file",
        "id_mode": "no",
        "can_delete": True,
    },
    "armor": {
        "label": "防具",
        "config_key": "armor_file",
        "id_mode": "no",
        "can_delete": True,
    },
    "accessory": {
        "label": "装飾品",
        "config_key": "accessory_file",
        "id_mode": "no",
        "can_delete": True,
    },
}

STAT_KEYS = ("str", "int", "mnd", "vit", "dex", "agi", "cha", "karma")


def get_master_definition(master_type):
    definition = MASTER_DEFINITIONS.get(master_type)
    if not definition:
        common.show_error("指定されたマスターデータが見つかりません。")
    return definition


def get_master_path(master_type):
    definition = get_master_definition(master_type)
    configured_path = config.Config[definition["config_key"]]
    if os.path.isabs(configured_path):
        return configured_path
    return os.path.join(config.BASE_DIR, configured_path)


def load_master_records(master_type):
    from sub_def.file_ops import load_data_with_lock

    records = load_data_with_lock(
        get_master_path(master_type), f"admin_master_{master_type}"
    )
    if not isinstance(records, list):
        common.show_error("マスターデータの形式が不正です。")
    return records


def master_record_id(master_type, record, index):
    definition = get_master_definition(master_type)
    return index if definition["id_mode"] == "index" else record.get("no", "")


def _require_int(record, key, minimum=0):
    value = record.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{key} は {minimum} 以上の整数で指定してください。")


def validate_master_record(master_type, record, existing_ids, selected_id=None):
    """管理画面から入力された1レコードを、現行JSONの契約に照らして検証する。"""
    if not isinstance(record, dict):
        raise ValueError("レコードはJSONオブジェクトで指定してください。")
    if not str(record.get("name", "")).strip():
        raise ValueError("name は必須です。")

    if master_type == "syoku":
        for key in (
            *(f"req_{stat}" for stat in STAT_KEYS),
            *(f"limit_{stat}" for stat in STAT_KEYS),
        ):
            _require_int(record, key)
        job_reqs = record.get("job_reqs")
        if (
            not isinstance(job_reqs, list)
            or len(job_reqs) != len(config.Config["chara_jobs"])
            or any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in job_reqs)
        ):
            raise ValueError("job_reqs は職業数分の整数配列で指定してください。")
        return

    _require_int(record, "no")
    if record["no"] in existing_ids and record["no"] != selected_id:
        raise ValueError(f"no={record['no']} は既に使用されています。")

    job_ids = record.get("job_ids")
    valid_job_ids = set(config.Config["chara_jobs"])
    if (
        not isinstance(job_ids, list)
        or len(job_ids) != len(set(job_ids))
        or any(isinstance(job_id, bool) or job_id not in valid_job_ids for job_id in job_ids)
    ):
        raise ValueError("job_ids は重複のない有効な職業ID配列で指定してください。")

    if master_type == "tac":
        _require_int(record, "ms")
        if "activation_denominator" in record:
            _require_int(record, "activation_denominator", 1)
        return

    _require_int(record, "gold")
    if master_type == "weapon":
        _require_int(record, "atk")
        _require_int(record, "hit_rate", -999999999999)
    elif master_type == "armor":
        _require_int(record, "defense")
        _require_int(record, "evasion_rate", -999999999999)
    elif master_type == "accessory":
        _require_int(record, "effect_id")
        bonus = record.get("bonus")
        if not isinstance(bonus, dict) or set(bonus) != set(STAT_KEYS):
            raise ValueError("bonus は8能力値キーを持つオブジェクトで指定してください。")
        for key in STAT_KEYS:
            _require_int(bonus, key)
        for key in ("hit_rate", "evasion_rate", "special_rate"):
            _require_int(record, key, -999999999999)


def save_master_records(master_type, records):
    from sub_def.file_ops import save_data_atomically

    save_data_atomically(
        records,
        get_master_path(master_type),
        f"admin_master_{master_type}",
    )
    if master_type == "accessory":
        # 同一プロセス内で共通モジュールが持つ説明文キャッシュも更新する。
        common._acs_master_cache = None


def master_list_context(master_type, message=None):
    definition = get_master_definition(master_type)
    records = load_master_records(master_type)
    rows = [
        {
            "id": master_record_id(master_type, record, index),
            "name": record.get("name", "(名称なし)"),
            "record": record,
        }
        for index, record in enumerate(records)
    ]
    return {
        "mode": "master_list",
        "master_type": master_type,
        "master_label": definition["label"],
        "master_rows": rows,
        "can_delete": definition["can_delete"],
        "message": message,
    }


def master_edit_context(master_type, master_id=None, is_new=False):
    definition = get_master_definition(master_type)
    records = load_master_records(master_type)
    if is_new:
        if master_type == "syoku":
            record = {
                "name": "新規職業",
                **{f"req_{stat}": 0 for stat in STAT_KEYS},
                **{f"limit_{stat}": 0 for stat in STAT_KEYS},
                "job_reqs": [0] * len(config.Config["chara_jobs"]),
            }
        elif master_type == "tac":
            record = {
                "no": max((item.get("no", -1) for item in records), default=-1) + 1,
                "name": "新規戦術",
                "desc": "",
                "activation_denominator": 100,
                "ms": 0,
                "job_ids": [],
            }
        elif master_type == "weapon":
            record = {
                "no": max((item.get("no", 999) for item in records), default=999) + 1,
                "name": "新規武器",
                "atk": 0,
                "gold": 0,
                "hit_rate": 0,
                "job_ids": [],
            }
        elif master_type == "armor":
            record = {
                "no": max((item.get("no", 1999) for item in records), default=1999) + 1,
                "name": "新規防具",
                "defense": 0,
                "gold": 0,
                "evasion_rate": 0,
                "job_ids": [],
            }
        else:
            record = {
                "no": max((item.get("no", 0) for item in records), default=0) + 1,
                "name": "新規装飾品",
                "gold": 0,
                "effect_id": 0,
                "bonus": {stat: 0 for stat in STAT_KEYS},
                "description": "",
                "hit_rate": 0,
                "evasion_rate": 0,
                "special_rate": 0,
                "job_ids": [],
            }
        selected_id = ""
    else:
        try:
            selected_id = int(master_id)
        except (TypeError, ValueError):
            common.show_error("マスターデータのIDが不正です。")
        record = next(
            (
                item
                for index, item in enumerate(records)
                if master_record_id(master_type, item, index) == selected_id
            ),
            None,
        )
        if record is None:
            common.show_error("指定されたマスターデータが見つかりません。")
        record = json.loads(json.dumps(record, ensure_ascii=False))

    return {
        "mode": "master_edit",
        "master_type": master_type,
        "master_label": definition["label"],
        "master_id": selected_id,
        "is_new": is_new,
        "record_json": json.dumps(record, ensure_ascii=False, indent=2),
    }


def player_item_context(target_id, message=None):
    chara = common.chara_load(target_id)
    if not chara:
        common.show_error("指定されたキャラクターが見つかりません。")

    options = []
    item_type_labels = {"weapon": "武器", "armor": "防具", "accessory": "装飾品"}
    for item_type in ("weapon", "armor", "accessory"):
        for record in load_master_records(item_type):
            options.append(
                {
                    "value": f"{item_type}:{record.get('no')}",
                    "label": f"{record.get('no')} - {record.get('name', '(名称なし)')}",
                    "type": item_type_labels[item_type],
                }
            )

    return {
        "mode": "player_item",
        "target_id": target_id,
        "target_name": chara.get("name", target_id),
        "item_options": options,
        "warehouse_counts": {
            "weapon": len(common.souko_load(target_id, "weapon")),
            "armor": len(common.souko_load(target_id, "armor")),
            "accessory": len(common.souko_load(target_id, "accessory")),
        },
        "message": message,
    }


def warehouse_entry_from_master(item_type, record):
    """マスターを現行倉庫の保存形式へ変換する。"""
    if item_type == "weapon":
        return {
            "id": record["no"],
            "name": record["name"],
            "atk": record["atk"],
            "gold": record.get("gold", 0),
            "hit_rate": record.get("hit_rate", 0),
        }
    if item_type == "armor":
        return {
            "id": record["no"],
            "name": record["name"],
            "defense": record["defense"],
            "gold": record.get("gold", 0),
            "evasion_rate": record.get("evasion_rate", 0),
        }
    return {
        "id": record["no"],
        "name": record["name"],
        "gold": record.get("gold", 0),
        "effect_id": record.get("effect_id", 0),
        "bonus": record.get("bonus", {stat: 0 for stat in STAT_KEYS}),
        "hit_rate": record.get("hit_rate", 0),
        "evasion_rate": record.get("evasion_rate", 0),
        "special_rate": record.get("special_rate", 0),
        "description": record.get("description", ""),
    }



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
    method = os.environ.get("REQUEST_METHOD", "GET").upper()
    from sub_def.crypto import get_session, save_session, token_check
    from sub_def.utils import redirect

    session = get_session()
    if mode == "admin_log_out":
        session.pop("is_admin", None)
        redirect("others.py", extra_headers=[save_session(session)])

    # 管理画面のパスワードは認証時のPOSTでのみ受け取り、以後は暗号化セッションで判定する。
    if not session.get("is_admin"):
        if method != "POST":
            common.show_error("管理者認証が必要です。トップページからログインしてください。")
        token_check(params, session)
        admin_pass = params.get("pass", "")
        if not hmac.compare_digest(admin_pass, config.Config["admin_password"]):
            common.show_error("管理者パスワードが一致しません。")
        session["is_admin"] = True
        redirect("admin.py?mode=kanri_top", extra_headers=[save_session(session)])

    # データ改変・削除を伴う操作はCSRFトークン検証を必須とする
    if method == "POST" and mode in (
        "save",
        "del_chara",
        "del_noplay",
        "restore_protected",
        "backup_restore",
        "post_all_message",
        "master_save",
        "master_delete",
        "player_item_add",
    ):
        token_check(params, session)

    # 1. 管理画面トップ
    if mode == "kanri_top":
        from sub_def.backup import list_daily_backups
        context = {
            "mode": mode,
            "backup_entries": list_daily_backups(),
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
            "mode": "kanri_top",
            "message": "全体ニュースを投稿しました。",
        }
        common.render_template("admin.html", context)
        return

    # 1.2 マスターデータ一覧
    elif mode == "master_list":
        master_type = params.get("master_type", "")
        context = master_list_context(master_type)
        common.render_template("admin.html", context)
        return

    # 1.3 マスターデータ編集画面
    elif mode == "master_edit":
        master_type = params.get("master_type", "")
        context = master_edit_context(
            master_type,
            params.get("master_id"),
            params.get("new") == "1",
        )
        common.render_template("admin.html", context)
        return

    # 1.4 マスターデータ保存
    elif mode == "master_save":
        master_type = params.get("master_type", "")
        definition = get_master_definition(master_type)
        records = load_master_records(master_type)
        is_new = params.get("is_new") == "1"
        selected_id = None
        if not is_new:
            try:
                selected_id = int(params.get("master_id", ""))
            except (TypeError, ValueError):
                common.show_error("マスターデータのIDが不正です。")

        try:
            record = json.loads(params.get("record_json", ""))
            existing_ids = {
                master_record_id(master_type, item, index)
                for index, item in enumerate(records)
            }
            validate_master_record(
                master_type,
                record,
                existing_ids,
                selected_id,
            )
            if is_new:
                records.append(record)
            else:
                target_index = next(
                    (
                        index
                        for index, item in enumerate(records)
                        if master_record_id(master_type, item, index) == selected_id
                    ),
                    None,
                )
                if target_index is None:
                    raise ValueError("編集対象のマスターデータが見つかりません。")
                records[target_index] = record
            save_master_records(master_type, records)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            context = master_edit_context(master_type, selected_id, is_new)
            context["record_json"] = params.get("record_json", "")
            context["message"] = f"保存できません: {error}"
            common.render_template("admin.html", context)
            return

        context = master_list_context(
            master_type,
            f"{definition['label']}マスターを保存しました。",
        )
        common.render_template("admin.html", context)
        return

    # 1.5 マスターデータ削除
    elif mode == "master_delete":
        master_type = params.get("master_type", "")
        definition = get_master_definition(master_type)
        if not definition["can_delete"]:
            common.show_error("このマスターはID順を維持するため削除できません。")
        try:
            selected_id = int(params.get("master_id", ""))
        except (TypeError, ValueError):
            common.show_error("マスターデータのIDが不正です。")

        records = load_master_records(master_type)
        target_index = next(
            (
                index
                for index, item in enumerate(records)
                if master_record_id(master_type, item, index) == selected_id
            ),
            None,
        )
        if target_index is None:
            common.show_error("削除対象のマスターデータが見つかりません。")
        records.pop(target_index)
        save_master_records(master_type, records)
        context = master_list_context(
            master_type,
            f"{definition['label']} No.{selected_id} を削除しました。",
        )
        common.render_template("admin.html", context)
        return

    # 1.6 プレイヤー倉庫への装備追加
    elif mode == "player_item":
        target_id = params.get("target_id", "").strip()
        context = player_item_context(target_id)
        common.render_template("admin.html", context)
        return

    elif mode == "player_item_add":
        target_id = params.get("target_id", "").strip()
        item_ref = params.get("item_ref", "")
        item_type, separator, item_no_text = item_ref.partition(":")
        if not separator or item_type not in ("weapon", "armor", "accessory"):
            common.show_error("追加する装備が指定されていません。")
        try:
            item_no = int(item_no_text)
        except (TypeError, ValueError):
            common.show_error("追加する装備IDが不正です。")

        records = load_master_records(item_type)
        record = next((item for item in records if item.get("no") == item_no), None)
        if record is None:
            common.show_error("指定された装備がマスターに存在しません。")

        limit_key = {
            "weapon": "max_weapons",
            "armor": "max_armors",
            "accessory": "max_accessories",
        }[item_type]
        common.get_lock(target_id)
        try:
            data = common.load_user_all(target_id)
            if not data or not data.get("chara"):
                common.show_error("指定されたキャラクターが見つかりません。")
            warehouse_key = f"souko_{item_type}"
            warehouse = data.get(warehouse_key, [])
            if len(warehouse) >= config.Config[limit_key]:
                raise ValueError(f"{item_type}倉庫がいっぱいです。")
            warehouse.append(warehouse_entry_from_master(item_type, record))
            data[warehouse_key] = warehouse
            common.save_user_unified(target_id, data)
        except ValueError as error:
            context = player_item_context(target_id, f"追加できません: {error}")
            common.render_template("admin.html", context)
            return
        finally:
            common.release_lock(target_id)

        context = player_item_context(
            target_id,
            f"{record['name']}を{item_type}倉庫へ追加しました。",
        )
        common.render_template("admin.html", context)
        return

    # 1.5 日次バックアップ復元
    elif mode == "backup_restore":
        from sub_def.backup import list_daily_backups, restore_daily_backup

        backup_name = params.get("backup_name", "").strip()
        try:
            emergency_name = restore_daily_backup(backup_name)
        except (ValueError, RuntimeError, OSError) as error:
            common.show_error(f"バックアップを復元できません: {error}")

        context = {
            "mode": "kanri_top",
            "backup_entries": list_daily_backups(),
            "message": (
                f"{backup_name}のバックアップを復元しました。"
                f"復元前の状態はbackups/{emergency_name}へ退避しています。"
            ),
        }
        common.render_template("admin.html", context)
        return

    # 1.6 保護ユーザー復元
    elif mode == "restore_protected":
        restored, unavailable = restore_protected_users()
        players = common.get_all_players()
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
            "players": players,
            "mode": "kanri_all",
            "message": " / ".join(message_parts),
        }
        common.render_template("admin.html", context)
        return

    # 2. 全キャラクター表示
    elif mode == "kanri_all":
        players = common.get_all_players()
        # 最終行動時間順にソート (新しい順)
        players.sort(key=lambda x: x.get("last_time", 0), reverse=True)
        
        # 時刻表示文字列を付与
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
            
        context = {
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
            
        players = common.get_all_players()
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
        context = {
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
            players = common.get_all_players()
            for p in players:
                p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
            context = {
                "players": players,
                "mode": "kanri_all",
                "message": f"保護ユーザー「{target_id}」は削除できません。",
            }
            common.render_template("admin.html", context)
            return
            
        user_dir = os.path.join(config.Config['save_dir'], target_id)
        if os.path.exists(user_dir) and os.path.isdir(user_dir):
            shutil.rmtree(user_dir)
            
        players = common.get_all_players()
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
        context = {
            "players": players,
            "mode": "kanri_all",
            "message": f"キャラクターID「{target_id}」を削除しました。"
        }
        common.render_template("admin.html", context)
        return

    # 6. 長期間未ログインキャラクター一括削除
    elif mode == "del_noplay":
        players = common.get_all_players()
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
                    
        players = common.get_all_players()
        for p in players:
            p["last_time_str"] = common.get_time_str(p.get("last_time", 0))
            
        if deleted_count > 0:
            msg = f"放置キャラクターを一括削除しました (削除数: {deleted_count}人: {', '.join(deleted_names)})"
        else:
            msg = "放置キャラクターはいませんでした。"
        if protected_count:
            msg += f" 保護ユーザー {protected_count}人は対象外にしました。"
        context = {
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
