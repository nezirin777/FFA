#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(".")

WEAPON_INI = BASE / "data/item/item.ini"
DEF_INI = BASE / "data/def/def.ini"
ACS_INI = BASE / "data/acs/acs.ini"

CHARALOG2 = BASE / "charalog2"

OUT_ITEM = BASE / "souko_item"
OUT_DEF = BASE / "souko_def"
OUT_ACS = BASE / "souko_acs"

OUT_ITEM.mkdir(exist_ok=True)
OUT_DEF.mkdir(exist_ok=True)
OUT_ACS.mkdir(exist_ok=True)


def load_weapon():
    table = {}

    with open(WEAPON_INI, encoding="cp932") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            c = line.split("<>")
            if len(c) < 5:
                continue

            table[c[0].zfill(4)] = {
                "id": int(c[0]),
                "name": c[1],
                "power": int(c[2]),
                "gold": int(c[3]),
                "effect": int(c[4]),
            }

    return table


def load_def():
    table = {}

    with open(DEF_INI, encoding="cp932") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            c = line.split("<>")
            if len(c) < 5:
                continue

            table[c[0].zfill(4)] = {
                "id": int(c[0]),
                "name": c[1],
                "def": int(c[2]),
                "gold": int(c[3]),
                "effect": int(c[4]),
            }

    return table


def load_acs():
    table = {}

    with open(ACS_INI, encoding="cp932") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            c = line.split("<>")
            if len(c) < 16:
                continue

            table[c[0].zfill(4)] = {
                "id": int(c[0]),
                "name": c[1],
                "gold": int(c[2]),
                "effect_id": int(c[3]),
                "bonus": {
                    "str": int(c[4]),
                    "int": int(c[5]),
                    "dex": int(c[6]),
                    "vit": int(c[7]),
                    "agi": int(c[8]),
                    "mnd": int(c[9]),
                    "lck": int(c[10]),
                    "lp": int(c[11]),
                },
                "attrib": int(c[12]),
                "spare1": int(c[13]),
                "spare2": int(c[14]),
                "spare3": 0,
            }

    return table


WEAPON = load_weapon()
DEF = load_def()
ACS = load_acs()


def convert(ids, master):
    result = []

    for x in ids[1:]:
        x = x.strip()

        if x == "" or x == "0000":
            continue

        if x in master:
            result.append(master[x])

    return result


for file in CHARALOG2.glob("*.cgi"):

    lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()

    while len(lines) < 3:
        lines.append("0")

    weapon_ids = lines[0].split(",")
    def_ids = lines[1].split(",")
    acs_ids = lines[2].split(",")

    json.dump(
        convert(weapon_ids, WEAPON),
        open(OUT_ITEM / (file.stem + ".json"), "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2,
    )

    json.dump(
        convert(def_ids, DEF),
        open(OUT_DEF / (file.stem + ".json"), "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2,
    )

    json.dump(
        convert(acs_ids, ACS),
        open(OUT_ACS / (file.stem + ".json"), "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2,
    )

print("Done.")
