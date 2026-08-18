#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""旧版セーブデータを現行の user_all.json へ一括変換する。

旧版の保存形式は配列の列番号が仕様そのものになっているため、列名を
旧キーへ読み替えてから変換する方式は使わない。ここでは旧版の列番号を
現行キーへ直接対応付け、旧キー (lck/lp/attrib/spare*) を出力しない。

通常はこのファイルを直接実行する。入力は ``旧版_ver2``、出力はこのファイルと
同じディレクトリの ``users`` と ``shared``。現行の保存先へ出す場合は
``--output`` と ``--shared-output`` を指定する。
"""

from __future__ import annotations

import argparse
import copy
import html
import json
import sys
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OLD_ROOT = SCRIPT_DIR.parent
DEFAULT_OUTPUT = SCRIPT_DIR / "users"
DEFAULT_SHARED_OUTPUT = SCRIPT_DIR / "shared"
CURRENT_ROOT = DEFAULT_OLD_ROOT.parent

JOB_COUNT = 31
WINNER_FIELD_COUNT = 54

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


def split_legacy_line(line: str) -> list[str]:
    """Ver2の<>区切り1行を分解し、HTMLエンティティを復元する。"""
    line = line.rstrip("\r\n")
    if line.endswith("<>"):
        line = line[:-2]
    if not line:
        return []
    return [html.unescape(value) for value in line.split("<>")]


def split_legacy_fields(path: Path) -> list[str]:
    text = read_legacy_text(path)
    if not text:
        return []
    if "<>" in text:
        return split_legacy_line(text)
    return text.splitlines()


def zero_accessory() -> dict[str, Any]:
    return {
        "name": "なし",
        "effect_id": 0,
        "bonus": {key: 0 for key in CANONICAL_STATS},
        "description": "効果なし",
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
                    "name": html.unescape(str(row.get("name", ""))),
                    "gold": to_int(row.get("gold")),
                    "effect_id": to_int(row.get("effect_id")),
                    "bonus": {
                        key: to_int(bonus.get(key)) for key in CANONICAL_STATS
                    },
                    "description": html.unescape(str(row.get("description", ""))),
                    **{
                        key: to_int(row.get(key))
                        for key in CANONICAL_ACCESSORY_RATES
                    },
                }
            else:
                normalized = {
                    "id": item_id,
                    "name": html.unescape(str(row.get("name", ""))),
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
        cols = split_legacy_line(line)
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
        chara[key] = to_int(value) if numeric else html.unescape(value)
    # Ver2では銀行残高がcharalogの34番目に保存される。Ver1互換の
    # banklogが残っている場合はconvert_user側でそちらを優先する。
    chara["bank"] = to_int(cols[34]) if len(cols) > 34 else 0
    return chara


def convert_item(
    path: Path,
    masters: dict[str, dict[int, dict[str, Any]]],
    legacy_masters: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    cols = split_legacy_fields(path)
    if not cols:
        return empty_item()
    while len(cols) < 20:
        cols.append("")

    bonus = {key: to_int(cols[index]) for key, index in ACCESSORY_COLUMNS}
    rates = {
        "hit_rate": to_int(cols[16]),
        "evasion_rate": to_int(cols[17]),
        "special_rate": to_int(cols[18]),
    }
    name = html.unescape(cols[6]) or "なし"
    effect_id = to_int(cols[7])
    description = html.unescape(cols[19]) or accessory_description(
        name, effect_id, bonus, rates, masters, legacy_masters
    ) or "効果なし"

    return {
        "weapon": {
            "name": html.unescape(cols[0]) or "素手",
            "dmg": to_int(cols[1]),
            "effect": to_int(cols[2]),
        },
        "armor": {
            "name": html.unescape(cols[3]) or "衣服",
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


def convert_login_log(path: Path) -> list[dict[str, Any]]:
    """Ver2 loginlogの各行をVer3のログイン履歴形式へ変換する。"""
    if not path.exists():
        return []
    result = []
    for line in read_legacy_text(path).splitlines():
        cols = split_legacy_line(line)
        if len(cols) < 4:
            continue
        result.append({
            "pass": cols[0],
            "host": cols[1],
            "time": cols[2],
            "failed": to_int(cols[3]),
        })
    return result


def convert_message_log(path: Path) -> list[dict[str, Any]]:
    """受信箱・送信箱・全体告知の共通<>形式をJSON形式へ変換する。"""
    if not path.exists():
        return []
    result = []
    for line in read_legacy_text(path).splitlines():
        cols = split_legacy_line(line)
        if len(cols) < 4:
            continue
        padded = cols + [""] * (5 - len(cols))
        result.append({
            "id": padded[0],
            "name": padded[1],
            "time": padded[2],
            "message": padded[3],
            "host": padded[4],
        })
    return result


def convert_souko_file(path: Path, kind: str) -> list[dict[str, Any]]:
    """Ver2のsouko生データをVer3の倉庫オブジェクトへ変換する。"""
    if not path.exists():
        return []
    result = []
    for line in read_legacy_text(path).splitlines():
        cols = split_legacy_line(line)
        if not cols:
            continue
        if kind in {"item", "def"}:
            cols += [""] * (5 - len(cols))
            item_id = to_int(cols[0])
            if not item_id:
                continue
            if kind == "item":
                result.append({
                    "id": item_id,
                    "name": cols[1],
                    "power": to_int(cols[2]),
                    "gold": to_int(cols[3]),
                    "effect": to_int(cols[4]),
                })
            else:
                result.append({
                    "id": item_id,
                    "name": cols[1],
                    "power": to_int(cols[2]),
                    "gold": to_int(cols[3]),
                    "effect": to_int(cols[4]),
                })
            continue

        # アクセサリー倉庫は、ID・名前・価格・効果IDに続いて、
        # str,int,mnd,vit,dex,agi,cha,karma,命中,必殺,回避,説明文の順。
        cols += [""] * (16 - len(cols))
        item_id = to_int(cols[0])
        if not item_id:
            continue
        result.append({
            "id": item_id,
            "name": cols[1],
            "gold": to_int(cols[2]),
            "effect_id": to_int(cols[3]),
            "bonus": {
                "str": to_int(cols[4]),
                "int": to_int(cols[5]),
                "mnd": to_int(cols[6]),
                "vit": to_int(cols[7]),
                "dex": to_int(cols[8]),
                "agi": to_int(cols[9]),
                "cha": to_int(cols[10]),
                "karma": to_int(cols[11]),
            },
            "hit_rate": to_int(cols[12]),
            "special_rate": to_int(cols[13]),
            "evasion_rate": to_int(cols[14]),
            "description": cols[15] or "効果なし",
        })
    return result


def convert_winner(
    path: Path,
    masters: dict[str, dict[int, dict[str, Any]]],
    legacy_masters: Iterable[dict[str, Any]],
) -> dict[str, Any] | None:
    """Ver2の54項目winner.cgiをVer3のwinner.jsonへ変換する。"""
    if not path.exists():
        return None
    cols = split_legacy_fields(path)
    if len(cols) < WINNER_FIELD_COUNT:
        print(
            f"warning: {path.name}: チャンプ列が {len(cols)} 個しかありません "
            f"(通常 {WINNER_FIELD_COUNT} 個)",
            file=sys.stderr,
        )
    cols += [""] * (WINNER_FIELD_COUNT - len(cols))

    bonus = {
        "str": to_int(cols[28]),
        "int": to_int(cols[29]),
        "mnd": to_int(cols[30]),
        "vit": to_int(cols[31]),
        "dex": to_int(cols[32]),
        "agi": to_int(cols[33]),
        "cha": to_int(cols[53]),
        "karma": to_int(cols[34]),
    }
    rates = {
        "hit_rate": to_int(cols[52]),
        "evasion_rate": to_int(cols[36]),
        "special_rate": to_int(cols[35]),
    }
    accessory_name = cols[27] or "なし"
    accessory_description_text = accessory_description(
        accessory_name,
        to_int(cols[51]),
        bonus,
        rates,
        masters,
        legacy_masters,
    ) or "効果なし"

    return {
        "id": cols[0],
        "name": cols[3],
        "sex": to_int(cols[4]),
        "img": to_int(cols[5]),
        "str": to_int(cols[6]),
        "int": to_int(cols[7]),
        "mnd": to_int(cols[8]),
        "vit": to_int(cols[9]),
        "dex": to_int(cols[10]),
        "agi": to_int(cols[11]),
        "cha": to_int(cols[12]),
        "karma": to_int(cols[13]),
        "job": to_int(cols[14]),
        "hp": to_int(cols[15]),
        "max_hp": to_int(cols[16]),
        "level": to_int(cols[17]),
        "battle_count": to_int(cols[18]),
        "battle_win_count": to_int(cols[19]),
        "comment": cols[20],
        "equipped_item": {
            "weapon": {
                "name": cols[21] or "素手",
                "dmg": to_int(cols[22]),
                "effect": to_int(cols[23]),
            },
            "armor": {
                "name": cols[24] or "衣服",
                "def": to_int(cols[25]),
                "effect": to_int(cols[26]),
            },
            "accessory": {
                "name": accessory_name,
                "effect_id": to_int(cols[51]),
                "bonus": bonus,
                "description": accessory_description_text,
                **rates,
            },
        },
        "unused30": to_int(cols[37]),
        "host": cols[38],
        "job_level": to_int(cols[39]),
        "last_challenger": {
            "id": cols[40],
            "name": cols[41],
        },
        "win_count": to_int(cols[44]),
        "max_win_count": to_int(cols[45]),
        "max_win_id": cols[46],
        "max_win_name": cols[49],
        "gold": to_int(cols[50]),
    }


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
    souko_paths = {
        kind: old_root / "souko" / kind / f"{user_id}.cgi"
        for kind in ("item", "def", "acs")
    }

    chara = convert_chara(chara_path)
    item = convert_item(item_path, masters, legacy_masters) if item_path.exists() else empty_item()
    # Ver2の銀行残高はキャラデータ内にある。Ver1互換のbanklogが残る
    # 場合だけ、旧ファイルの値を優先して読み込む。
    if bank_path.exists():
        chara["bank"] = load_bank(bank_path)

    lines = ["0", "0", "0"]
    if charalog2_path.exists():
        lines = read_legacy_text(charalog2_path).splitlines()
        while len(lines) < 3:
            lines.append("0")

    warehouse = {}
    for index, kind in enumerate(("item", "def", "acs")):
        if souko_paths[kind].exists():
            warehouse[kind] = convert_souko_file(souko_paths[kind], kind)
        else:
            # 旧変換途中のデータにはcharalog2が残る場合があるため、
            # その形式も引き続き受け付ける。
            warehouse[kind] = convert_warehouse_lines(
                lines[index], kind, masters, charalog2_path
            )

    user = {
        "chara": chara,
        "item": item,
        "syoku": convert_syoku(syoku_path),
        "login_log": convert_login_log(old_root / "loginlog" / f"{user_id}.cgi"),
        "message": convert_message_log(old_root / "message" / f"{user_id}.cgi"),
        "souko_item": warehouse["item"],
        "souko_def": warehouse["def"],
        "souko_acs": warehouse["acs"],
        "choco": {},
        "choco_g1": {},
        # main()でuser_all.jsonとは別のmessage_sent.jsonへ保存する。
        "_message_sent": convert_message_log(
            old_root / "sousin" / f"{user_id}.cgi"
        ),
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
        help="Ver2データのルート (既定: このファイルの親ディレクトリ)",
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
        "--shared-output",
        type=Path,
        default=DEFAULT_SHARED_OUTPUT,
        help="winner.json・all_message.jsonの出力先 (既定: change_data/shared)",
    )
    parser.add_argument(
        "--winner-output",
        type=Path,
        default=None,
        help="winner.jsonだけ別の場所へ出力する (省略時はshared-output内)",
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
    shared_output = args.shared_output.resolve()
    winner_output = (
        args.winner_output.resolve()
        if args.winner_output
        else shared_output / "winner.json"
    )
    masters = load_current_masters(args.current_root.resolve())
    legacy_masters = load_legacy_accessories(old_root)
    chara_dir = old_root / "charalog"
    if not chara_dir.exists():
        print(f"エラー: charalog が見つかりません: {chara_dir}", file=sys.stderr)
        return 1

    converted = 0
    for chara_path in sorted(chara_dir.glob("*.cgi")):
        user = convert_user(chara_path, old_root, masters, legacy_masters)
        message_sent = user.pop("_message_sent", [])
        converted += 1
        if not args.dry_run:
            user_dir = output / chara_path.stem
            user_dir.mkdir(parents=True, exist_ok=True)
            with (user_dir / "user_all.json").open("w", encoding="utf-8") as handle:
                json.dump(user, handle, ensure_ascii=False, indent=2)
            # Ver3の送信済み箱はuser_all.jsonではなく、ユーザー別の
            # message_sent.jsonとして管理される。
            if message_sent:
                with (user_dir / "message_sent.json").open("w", encoding="utf-8") as handle:
                    json.dump(message_sent, handle, ensure_ascii=False, indent=2)
        print(f"変換: {chara_path.stem}")

    winner = convert_winner(old_root / "datalog" / "winner.cgi", masters, legacy_masters)
    all_message = convert_message_log(old_root / "datalog" / "message.cgi")
    if not args.dry_run:
        shared_output.mkdir(parents=True, exist_ok=True)
        if winner is not None:
            winner_output.parent.mkdir(parents=True, exist_ok=True)
            with winner_output.open("w", encoding="utf-8") as handle:
                json.dump(winner, handle, ensure_ascii=False, indent=2)
        with (shared_output / "all_message.json").open("w", encoding="utf-8") as handle:
            json.dump(all_message, handle, ensure_ascii=False, indent=2)

    mode = "検証完了" if args.dry_run else "出力完了"
    print(f"{mode}: ユーザー{converted}件、チャンプ={'あり' if winner else 'なし'}、全体メッセージ={len(all_message)}件")
    if not args.dry_run:
        print(f"ユーザーデータ出力先: {output}")
        print(f"共有データ出力先: {shared_output}")
        if winner is not None:
            print(f"チャンプデータ出力先: {winner_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
