#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

# 入力
BASE = Path(".")

CHARA_DIR = BASE / "json_chara"
ITEM_DIR = BASE / "json_item"
SYOKU_DIR = BASE / "json_syoku"

SOUKO_ITEM_DIR = BASE / "souko_item"
SOUKO_DEF_DIR = BASE / "souko_def"
SOUKO_ACS_DIR = BASE / "souko_acs"

BANK_DIR = Path("../banklog")

# 出力
OUTPUT_DIR = BASE / "users"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_bank(user_id):
    path = BANK_DIR / f"{user_id}.cgi"

    if not path.exists():
        return 0

    text = path.read_text(encoding="cp932", errors="ignore").strip()

    if text.endswith("<>"):
        text = text[:-2]

    cols = text.split("<>")

    if len(cols) >= 3:
        try:
            return int(cols[2])
        except ValueError:
            return 0

    return 0


def load_json(path, default):
    if not path.exists():
        return default

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_user(user_id, data):

    user_dir = OUTPUT_DIR / user_id
    user_dir.mkdir(exist_ok=True)

    out = user_dir / "user_all.json"

    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# charaを基準にする
for chara_file in CHARA_DIR.glob("*.json"):

    user_id = chara_file.stem

    print(f"convert: {user_id}")

    # キャラクター
    chara_data = load_json(chara_file, {"chara": {}})

    chara = chara_data.get("chara", {})

    # 装備
    item_data = load_json(ITEM_DIR / f"{user_id}.json", {"item": {}})

    item = item_data.get("item", {})

    # 職業
    syoku_data = load_json(SYOKU_DIR / f"{user_id}.json", {"syoku": {}})

    syoku = syoku_data.get("syoku", {})

    # 倉庫
    souko_item = load_json(SOUKO_ITEM_DIR / f"{user_id}.json", [])

    souko_def = load_json(SOUKO_DEF_DIR / f"{user_id}.json", [])

    souko_acs = load_json(SOUKO_ACS_DIR / f"{user_id}.json", [])

    # 銀行
    bank = load_bank(user_id)

    chara["bank"] = bank

    # 最終データ
    user_all = {
        "chara": chara,
        "item": item,
        "syoku": syoku,
        "login_log": [],
        "message": [],
        "souko_item": souko_item,
        "souko_def": souko_def,
        "souko_acs": souko_acs,
        "choco": {},
        "choco_g1": {},
    }

    save_user(user_id, user_all)


print("Done.")
