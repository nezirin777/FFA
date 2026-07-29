#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

INPUT_DIR = Path("charalog")
OUTPUT_DIR = Path("json")
OUTPUT_DIR.mkdir(exist_ok=True)

FIELDS = [
    "id",
    "pass",
    "site",
    "url",
    "name",
    "sex",
    "img",
    "str",
    "int",
    "dex",
    "vit",
    "agi",
    "mnd",
    "lck",
    "job",
    "hp",
    "max_hp",
    "exp",
    "level",
    "gold",
    "lp",
    "unused21",
    "unused22",
    "comment",
    "weapon_id",
    "battle_limit",
    "host",
    "last_time",
    "boss_flag",
    "armor_id",
    "unused30",
    "accessory_id",
    "title",
    "job_level",
]

INT_FIELDS = {
    "sex",
    "img",
    "str",
    "int",
    "dex",
    "vit",
    "agi",
    "mnd",
    "lck",
    "job",
    "hp",
    "max_hp",
    "exp",
    "level",
    "gold",
    "lp",
    "unused21",
    "unused22",
    "weapon_id",
    "battle_limit",
    "last_time",
    "boss_flag",
    "armor_id",
    "unused30",
    "accessory_id",
    "title",
    "job_level",
}


def to_int(v):
    try:
        return int(v)
    except:
        return 0


for path in INPUT_DIR.glob("*.cgi"):
    text = path.read_text(encoding="shift_jis", errors="ignore").rstrip()

    # 末尾の <> を除去
    if text.endswith("<>"):
        text = text[:-2]

    cols = text.split("<>")

    chara = {}

    for i, key in enumerate(FIELDS):
        value = cols[i] if i < len(cols) else ""

        if key in INT_FIELDS:
            chara[key] = to_int(value)
        else:
            chara[key] = value

    # bank は別ファイル管理なので仮で0
    chara["bank"] = 0

    out = {"chara": chara}

    out_path = OUTPUT_DIR / (path.stem + ".json")
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

print("Done.")
