#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

INPUT_DIR = Path("../item")
OUTPUT_DIR = Path("json_item")
OUTPUT_DIR.mkdir(exist_ok=True)


def to_int(v):
    try:
        return int(v)
    except:
        return 0


for path in INPUT_DIR.glob("*.cgi"):
    text = path.read_text(encoding="shift_jis", errors="ignore").rstrip()

    if text.endswith("<>"):
        text = text[:-2]

    cols = text.split("<>")

    while len(cols) < 21:
        cols.append("")

    out = {
        "item": {
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
                "name": cols[6],
                "effect_id": to_int(cols[7]),
                "bonus": {
                    "str": to_int(cols[8]),
                    "int": to_int(cols[9]),
                    "dex": to_int(cols[10]),
                    "vit": to_int(cols[11]),
                    "agi": to_int(cols[12]),
                    "mnd": to_int(cols[13]),
                    "lck": to_int(cols[14]),
                    "lp": to_int(cols[15]),
                },
                "attrib": to_int(cols[16]),
                "spare1": to_int(cols[17]),
                "spare2": to_int(cols[18]),
                "description": cols[19],
            },
        }
    }

    out_path = OUTPUT_DIR / (path.stem + ".json")
    out_path.write_text(
        json.dumps(out, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

print("Done.")
