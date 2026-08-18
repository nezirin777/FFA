#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""旧版セーブデータを現行の user_all.json へ一括変換する。

旧版の保存形式は配列の列番号が仕様そのものになっているため、列名を
旧キーへ読み替えてから変換する方式は使わない。ここでは旧版の列番号を
現行キーへ直接対応付け、旧キー (lck/lp/attrib/spare*) を出力しない。

通常はこのファイルを直接実行する。入力は ``旧版``、出力はこのファイルと
同じディレクトリの ``users``。現行の保存先へ出す場合は --output を指定する。
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OLD_ROOT = SCRIPT_DIR.parent
DEFAULT_OUTPUT = SCRIPT_DIR / "users"
CURRENT_ROOT = DEFAULT_OLD_ROOT.parent

JOB_COUNT = 31

# 旧版 charalog.cgi の固定列。能力値の対応は旧版の実列順をそのまま記述する。
# 7:力, 8:知能, 9:信仰心, 10:生命力, 11:器用さ, 12:速さ,
# 13:魅力, 20:カルマ
CHARA_COLUMNS = (
    ("id", 0, False),
    ("pass", 1, False),
    ("site", 2, False),
    ("url", 3, False),
    ("name", 4, False),
    ("sex", 5, True),
    ("img", 6, True),
    ("str", 7, True),
    ("int", 8, True),
    ("mnd", 9, True),
    ("vit", 10, True),
    ("dex", 11, True),
    ("agi", 12, True),
    ("cha", 13, True),
    ("job", 14, True),
    ("hp", 15, True),
    ("max_hp", 16, True),
    ("exp", 17, True),
    ("level", 18, True),
    ("gold", 19, True),
    ("karma", 20, True),
    ("battle_count", 21, True),
    ("win_count", 22, True),
    ("comment", 23, False),
    ("weapon_id", 24, True),
    ("battle_limit", 25, True),
    ("host", 26, False),
    ("last_time", 27, True),
    ("boss_flag", 28, True),
    ("armor_id", 29, True),
    ("unused30", 30, True),
    ("accessory_id", 31, True),
    ("title", 32, True),
    ("job_level", 33, True),
)

# 旧版 item.cgi のアクセサリー列。ここも列番号を現行キーへ直接対応付ける。
# 8:力, 9:知能, 10:信仰心, 11:生命力, 12:器用さ, 13:速さ,
# 14:魅力, 15:カルマ, 16:命中率, 17:回避率, 18:奥義発動率。
ACCESSORY_COLUMNS = (
    ("str", 8),
    ("int", 9),
    ("mnd", 10),
    ("vit", 11),
    ("dex", 12),
    ("agi", 13),
    ("cha", 14),
    ("karma", 15),
)

CANONICAL_STATS = ("str", "int", "mnd", "vit", "dex", "agi", "cha", "karma")
CANONICAL_ACCESSORY_RATES = ("hit_rate", "evasion_rate", "special_rate")


def to_int(value: Any) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def read_legacy_text(path: Path) -> str:
    """旧版の主な文字コード(cp932)で読む。空ファイルは空文字列にする。"""
    return path.read_text(encoding="cp932", errors="replace").rstrip("\r\n")


def split_legacy_fields(path: Path) -> list[str]:
    text = read_legacy_text(path)
    if not text:
        return []
    if "<>" in text:
        if text.endswith("<>"):
            text = text[:-2]
        return text.split("<>")
    return text.splitlines()


def zero_accessory() -> dict[str, Any]:
    return {
        "name": "",
        "effect_id": 0,
        "bonus": {key: 0 for key in CANONICAL_STATS},
        "description": "",
        "hit_rate": 0,
        "evasion_rate": 0,
        "special_rate": 0,
    }


def empty_item() -> dict[str, Any]:
    return {
        "weapon": {"name": "素手", "dmg": 0, "effect": 0},
        "armor": {"name": "衣服", "def": 0, "effect": 0},
        "accessory": zero_accessory(),
    }


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return copy.deepcopy(default)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_current_masters(root: Path) -> dict[str, dict[int, dict[str, Any]]]:
    """現行マスターを読み、倉庫用の旧形式差分をここで吸収する。"""
    paths = {
        "item": root / "data" / "item" / "item.json",
        "def": root / "data" / "def" / "def.json",
        "acs": root / "data" / "acs" / "acs.json",
    }
    masters: dict[str, dict[int, dict[str, Any]]] = {key: {} for key in paths}
    for kind, path in paths.items():
        rows = load_json(path, [])
        for row in rows:
            item_id = to_int(row.get("no"))
            if not item_id:
                continue
            if kind == "acs":
                bonus = row.get("bonus", {})
                normalized = {
                    "id": item_id,
                    "name": row.get("name", ""),
                    "gold": to_int(row.get("gold")),
                    "effect_id": to_int(row.get("effect_id")),
                    "bonus": {
                        key: to_int(bonus.get(key)) for key in CANONICAL_STATS
                    },
                    "description": row.get("description", ""),
                    **{
                        key: to_int(row.get(key))
                        for key in CANONICAL_ACCESSORY_RATES
                    },
                }
            else:
                normalized = {
                    "id": item_id,
                    "name": row.get("name", ""),
                    "power": to_int(row.get("power")),
                    "gold": to_int(row.get("gold")),
                    "effect": to_int(row.get("effect", row.get("hit"))),
                }
            masters[kind][item_id] = normalized
    return masters


def load_legacy_accessories(root: Path) -> list[dict[str, Any]]:
    """装備データの説明文補完用。旧版マスターも正しい列順で読む。"""
    path = root / "data" / "acs" / "acs.ini"
    if not path.exists():
        return []
    result = []
    for line in read_legacy_text(path).splitlines():
        cols = line.split("<>")
        if len(cols) < 16:
            continue
        bonus = {
            key: to_int(cols[index])
            for key, index in ACCESSORY_COLUMNS
        }
        result.append({
            "no": to_int(cols[0]),
            "name": cols[1],
            "effect_id": to_int(cols[3]),
            "bonus": bonus,
            "hit_rate": to_int(cols[12]),
            "evasion_rate": to_int(cols[13]),
            "special_rate": to_int(cols[14]),
            "description": cols[15],
        })
    return result


def accessory_description(
    name: str,
    effect_id: int,
    bonus: dict[str, int],
    rates: dict[str, int],
    masters: dict[str, dict[int, dict[str, Any]]],
    legacy_masters: Iterable[dict[str, Any]],
) -> str:
    """旧版 item に説明文がない場合も、名前または能力値から補完する。"""
    for row in masters["acs"].values():
        if row["name"] == name and row.get("description"):
            return row["description"]
    for row in legacy_masters:
        if row["name"] == name and row.get("description"):
            return row["description"]
    for row in masters["acs"].values():
        if row.get("effect_id") != effect_id:
            continue
        if row.get("bonus") == bonus and all(row.get(key, 0) == rates[key] for key in rates):
            return row.get("description", "")
    return ""


def convert_chara(path: Path) -> dict[str, Any]:
    cols = split_legacy_fields(path)
    if len(cols) < len(CHARA_COLUMNS):
        print(
            f"warning: {path.name}: キャラ列が {len(cols)} 個しかありません "
            f"(通常 {len(CHARA_COLUMNS)} 個)",
            file=sys.stderr,
        )
    chara: dict[str, Any] = {}
    for key, index, numeric in CHARA_COLUMNS:
        value = cols[index] if index < len(cols) else ""
        if key in {"site", "url"}:
            continue
        chara[key] = to_int(value) if numeric else value
    chara["bank"] = 0
    return chara


def convert_item(
    path: Path,
    masters: dict[str, dict[int, dict[str, Any]]],
    legacy_masters: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    cols = split_legacy_fields(path)
    while len(cols) < 20:
        cols.append("")

    bonus = {key: to_int(cols[index]) for key, index in ACCESSORY_COLUMNS}
    rates = {
        "hit_rate": to_int(cols[16]),
        "evasion_rate": to_int(cols[17]),
        "special_rate": to_int(cols[18]),
    }
    name = cols[6]
    effect_id = to_int(cols[7])
    description = cols[19] or accessory_description(
        name, effect_id, bonus, rates, masters, legacy_masters
    )

    return {
        "weapon": {
            "name": cols[0],
            "dmg": to_int(cols[1]),
            "effect": to_int(cols[2]),
        },
        "armor": {
            "name": cols[3],
            "def": to_int(cols[4]),
            "effect": to_int(cols[5]),
        },
        "accessory": {
            "name": name,
            "effect_id": effect_id,
            "bonus": bonus,
            "description": description,
            **rates,
        },
    }


def item_id_key(value: str) -> int:
    value = value.strip()
    if not value or value == "0000":
        return 0
    return to_int(value)


def convert_syoku(path: Path) -> dict[str, int]:
    cols = split_legacy_fields(path) if path.exists() else []
    return {str(index): to_int(cols[index]) if index < len(cols) else 0 for index in range(JOB_COUNT)}


def load_bank(path: Path) -> int:
    if not path.exists():
        return 0
    cols = split_legacy_fields(path)
    return to_int(cols[2]) if len(cols) > 2 else 0


def validate_user(user: dict[str, Any], source: Path) -> None:
    chara = user["chara"]
    missing = [key for key in CANONICAL_STATS if key not in chara]
    forbidden = [key for key in ("lck", "lp", "site", "url") if key in chara]
    if missing or forbidden:
        raise ValueError(f"{source}: キャラ能力値キーが不正です missing={missing} forbidden={forbidden}")

    accessory = user["item"]["accessory"]
    if set(accessory["bonus"]) != set(CANONICAL_STATS):
        raise ValueError(f"{source}: アクセサリーボーナスのキーが不正です")
    forbidden = [key for key in ("lck", "lp", "attrib", "spare1", "spare2", "spare3") if key in accessory]
    if forbidden:
        raise ValueError(f"{source}: 旧アクセサリーキーが残っています {forbidden}")
    for key in CANONICAL_ACCESSORY_RATES:
        if key not in accessory:
            raise ValueError(f"{source}: {key} がありません")


def convert_user(
    chara_path: Path,
    old_root: Path,
    masters: dict[str, dict[int, dict[str, Any]]],
    legacy_masters: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    user_id = chara_path.stem
    item_path = old_root / "item" / f"{user_id}.cgi"
    syoku_path = old_root / "syoku" / f"{user_id}.cgi"
    charalog2_path = old_root / "charalog2" / f"{user_id}.cgi"
    bank_path = old_root / "banklog" / f"{user_id}.cgi"

    chara = convert_chara(chara_path)
    item = convert_item(item_path, masters, legacy_masters) if item_path.exists() else empty_item()
    chara["bank"] = load_bank(bank_path)
    lines = ["0", "0", "0"]
    if charalog2_path.exists():
        lines = read_legacy_text(charalog2_path).splitlines()
        while len(lines) < 3:
            lines.append("0")

    user = {
        "chara": chara,
        "item": item,
        "syoku": convert_syoku(syoku_path),
        "login_log": [],
        "message": [],
        "souko_item": convert_warehouse_lines(lines[0], "item", masters, charalog2_path),
        "souko_def": convert_warehouse_lines(lines[1], "def", masters, charalog2_path),
        "souko_acs": convert_warehouse_lines(lines[2], "acs", masters, charalog2_path),
        "choco": {},
        "choco_g1": {},
    }
    validate_user(user, chara_path)
    return user


def convert_warehouse_lines(
    line: str,
    kind: str,
    masters: dict[str, dict[int, dict[str, Any]]],
    source: Path,
) -> list[dict[str, Any]]:
    result = []
    ids = line.split(",")
    for raw_id in ids[1:]:
        item_id = item_id_key(raw_id)
        if not item_id:
            continue
        master = masters[kind].get(item_id)
        if master is None:
            print(
                f"warning: {source.name}: {kind} マスター {raw_id.strip()} が見つかりません",
                file=sys.stderr,
            )
            continue
        result.append(copy.deepcopy(master))
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--old-root",
        type=Path,
        default=DEFAULT_OLD_ROOT,
        help="旧版データのルート (既定: このファイルの親の親)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="user_all.json の出力先 (既定: change_data/users)",
    )
    parser.add_argument(
        "--current-root",
        type=Path,
        default=CURRENT_ROOT,
        help="現行マスター(data/*/*.json)のルート (既定: リポジトリルート)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="変換件数と検証だけ行い、ファイルを書き込まない",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    old_root = args.old_root.resolve()
    output = args.output.resolve()
    masters = load_current_masters(args.current_root.resolve())
    legacy_masters = load_legacy_accessories(old_root)
    chara_dir = old_root / "charalog"
    if not chara_dir.exists():
        print(f"error: charalog が見つかりません: {chara_dir}", file=sys.stderr)
        return 1

    converted = 0
    for chara_path in sorted(chara_dir.glob("*.cgi")):
        user = convert_user(chara_path, old_root, masters, legacy_masters)
        converted += 1
        if not args.dry_run:
            user_dir = output / chara_path.stem
            user_dir.mkdir(parents=True, exist_ok=True)
            with (user_dir / "user_all.json").open("w", encoding="utf-8") as handle:
                json.dump(user, handle, ensure_ascii=False, indent=2)
        print(f"convert: {chara_path.stem}")

    mode = "検証完了" if args.dry_run else "出力完了"
    print(f"{mode}: {converted} users")
    if not args.dry_run:
        print(f"output: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
