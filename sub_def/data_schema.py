"""保存JSONのキー順を統一するためのデータ構造ヘルパー。"""

from typing import Any


# キャラクターJSONは、意味のまとまりごとに並べる。
# 値は変更せず、未定義の追加キーは最後へ残す。
CHARA_KEY_ORDER = (
    "id",
    "pass",
    "name",
    "img",
    "sex",
    "level",
    "max_hp",
    "hp",
    "str",
    "int",
    "mnd",
    "vit",
    "dex",
    "agi",
    "cha",
    "karma",
    "job",
    "job_level",
    "exp",
    "gold",
    "bank",
    "weapon_id",
    "armor_id",
    "accessory_id",
    "battle_count",
    "win_count",
    "battle_limit",
    "boss_flag",
    "comment",
    "host",
    "last_time",
    "title_id",
    "tactic_id",
)

USER_DATA_KEY_ORDER = (
    "chara",
    "equipment",
    "item",  # 旧形式の装備データ。現行データに残っている場合も順序だけ整える。
    "syoku",
    "login_log",
    "souko_weapon",
    "souko_armor",
    "souko_accessory",
    "souko_item",
    "souko_def",
    "souko_acs",
    "choco",
    "choco_g1",
)

EQUIPMENT_KEY_ORDER = ("weapon", "armor", "accessory")
ACCESSORY_KEY_ORDER = (
    "name",
    "effect_id",
    "bonus",
    "hit_rate",
    "evasion_rate",
    "special_rate",
    "description",
)
BONUS_KEY_ORDER = ("str", "int", "mnd", "vit", "dex", "agi", "cha", "karma")


def _ordered_dict(data: dict[str, Any], key_order: tuple[str, ...]) -> dict[str, Any]:
    ordered = {key: data[key] for key in key_order if key in data}
    ordered.update({key: value for key, value in data.items() if key not in ordered})
    return ordered


def _order_equipment(data: dict[str, Any]) -> dict[str, Any]:
    ordered = _ordered_dict(data, EQUIPMENT_KEY_ORDER)
    for item_key, item_data in list(ordered.items()):
        if not isinstance(item_data, dict):
            continue
        if item_key == "accessory":
            item_data = _ordered_dict(item_data, ACCESSORY_KEY_ORDER)
            bonus = item_data.get("bonus")
            if isinstance(bonus, dict):
                item_data["bonus"] = _ordered_dict(bonus, BONUS_KEY_ORDER)
        ordered[item_key] = item_data
    return ordered


def order_user_data(data: dict[str, Any]) -> dict[str, Any]:
    """user_all.jsonを値を変えずに読みやすいキー順へ並べ替える。"""
    if not isinstance(data, dict):
        return data

    ordered = _ordered_dict(data, USER_DATA_KEY_ORDER)
    # 私信機能は廃止済み。旧変換データを含めて以後の保存で残さない。
    ordered.pop("message", None)
    ordered.pop("message_sent", None)
    chara = ordered.get("chara")
    if isinstance(chara, dict):
        # 旧キーが残るデータを読み込んだ場合も、現行名へ一度だけ移行する。
        for old_key, new_key in (("title", "title_id"), ("unused30", "tactic_id")):
            if old_key in chara:
                if new_key not in chara:
                    chara[new_key] = chara[old_key]
                chara.pop(old_key, None)
        chara = _ordered_dict(chara, CHARA_KEY_ORDER)
        # 旧版のサイト名・URLは現行キャラクター仕様では使用しない。
        chara.pop("site", None)
        chara.pop("url", None)
        ordered["chara"] = chara

    for item_key in ("equipment", "item"):
        item_data = ordered.get(item_key)
        if isinstance(item_data, dict):
            ordered[item_key] = _order_equipment(item_data)

    return ordered
