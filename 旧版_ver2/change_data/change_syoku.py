#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

INPUT_DIR = Path("../syoku")
OUTPUT_DIR = Path("json_syoku")
OUTPUT_DIR.mkdir(exist_ok=True)

MAX_JOB = 31


def to_int(v):
    v = v.strip()
    if v == "":
        return 0
    try:
        return int(v)
    except ValueError:
        return 0


for path in INPUT_DIR.glob("*.cgi"):
    text = path.read_text(encoding="shift_jis", errors="ignore").rstrip()

    # 末尾の <> を除去
    if text.endswith("<>"):
        text = text[:-2]

    cols = text.split("<>")

    syoku = {}

    for i in range(MAX_JOB):
        if i < len(cols):
            syoku[str(i)] = to_int(cols[i])
        else:
            syoku[str(i)] = 0

    out = {"syoku": syoku}

    out_path = OUTPUT_DIR / (path.stem + ".json")
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

print("Done.")
