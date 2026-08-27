"""Ver2 / Ver3 比較チェックリストを生成する。"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MONSTER_DATA_DIR = DATA_DIR / "monsters"
CHOCOBO_DATA_DIR = DATA_DIR / "chocobo"
OUTPUT_DIR = ROOT / "docs" / "ver2_comparison"

EQUIPMENT = (
    ("weapon", "武器", "旧版_ver2/item.pl"),
    ("armor", "防具", "旧版_ver2/item.pl"),
    ("accessory", "アクセサリー", "旧版_ver2/item.pl"),
)

STAT_LABELS = {
    "str": "力",
    "int": "知能",
    "mnd": "信仰心",
    "vit": "生命力",
    "dex": "器用さ",
    "agi": "速さ",
    "cha": "魅力",
    "karma": "カルマ",
}

MONSTER_SKILL_LABELS = {
    1: "マイティガード",
    2: "ケアルガ",
    3: "ファイガ",
    4: "ブリザガ",
    5: "サンダガ",
    6: "メテオ",
    7: "グラビガ",
    8: "クエイク",
    9: "アルテマ",
    10: "ショック・ウェーブ・パルサー",
    11: "デジョン",
    12: "ファイア・ブレス",
    13: "ケアルガ / アルテマ",
    14: "お金を盗む",
    15: "ドレイン",
    16: "アポガリプス",
    17: "えりりんの甘いささやき / 祝福のキス",
    18: "メガ・フレア",
    19: "ハァハァ。。。",
    20: "斬・鉄・剣",
    21: "性転換",
    22: "臭い息",
}

V2_MONSTER_MASTERS = {
    "mons_lv1.json": "旧版_ver2/data/normalmons.ini",
    "mons_lv2.json": "旧版_ver2/data/lowmons.ini",
    "mons_lv3.json": "旧版_ver2/data/highmons.ini",
    "mons_lv4.json": "旧版_ver2/data/spmons.ini",
    "mons_isekai.json": "旧版_ver2/data/isekaimons.ini",
    "legend_boss_lv1.json": "旧版_ver2/data/bossmons0.ini",
    "legend_boss_lv2.json": "旧版_ver2/data/bossmons1.ini",
    "legend_boss_lv3.json": "旧版_ver2/data/bossmons2.ini",
    "legend_boss_lv4.json": "旧版_ver2/data/bossmons3.ini",
}

CHOCOBO_STAT_LABELS = {
    "c0": "速度",
    "c1": "スタミナ",
    "c2": "粘り",
    "c3": "落ち着き",
    "c4": "闘争心",
    "c5": "賢さ",
    "c6": "反射神経",
}

ROUTE_DETAILS = {
    "main": ("街のメイン画面", "表示", "旧版_ver2/ffadventure.cgi"),
    "sts": ("自分のステータス", "表示・更新", "旧版_ver2/sts.cgi"),
    "tac_change": ("戦術選択", "表示・更新", "旧版_ver2/tac_change.cgi"),
    "passchange": ("合言葉・パスワード変更", "表示・更新", "旧版_ver2/passchange.cgi"),
    "tensyoku": ("転職", "表示・更新", "旧版_ver2/tensyoku.cgi"),
    "shop": ("宿屋", "状態変更", "旧版_ver2/shop.cgi"),
    "yado": ("宿泊（shopへの互換ルート）", "状態変更", "旧版_ver2/shop.cgi"),
    "shop_weapon": ("武器店", "表示・更新", "旧版_ver2/shop_item.cgi"),
    "shop_armor": ("防具店", "表示・更新", "旧版_ver2/shop_def.cgi"),
    "shop_accessory": ("装飾品店", "表示・更新", "旧版_ver2/shop_acs.cgi"),
    "shop_item": ("武器店（旧URL互換）", "表示・更新", "旧版_ver2/shop_item.cgi"),
    "shop_def": ("防具店（旧URL互換）", "表示・更新", "旧版_ver2/shop_def.cgi"),
    "shop_acs": ("装飾品店（旧URL互換）", "表示・更新", "旧版_ver2/shop_acs.cgi"),
    "bank": ("銀行", "表示・更新", "旧版_ver2/bank.cgi"),
    "souko": ("倉庫", "表示・更新", "旧版_ver2/souko.cgi"),
    "battle": ("人間チャンピオン戦", "状態変更", "旧版_ver2/battle.cgi"),
    "select_battle": ("対人戦の相手選択", "表示・更新", "旧版_ver2/select_battle.cgi"),
    "sentaku": ("対人戦の相手選択（互換ルート）", "表示・更新", "旧版_ver2/select_battle.cgi"),
    "monster": ("通常モンスター修行", "状態変更", "旧版_ver2/monster.cgi"),
    "genei": ("幻影の城（モンスター互換ルート）", "状態変更", "旧版_ver2/monster.cgi"),
    "isekiai": ("異世界（モンスター互換ルート）", "状態変更", "旧版_ver2/monster.cgi"),
    "legend": ("レジェンドプレイス", "表示・状態変更", "旧版_ver2/legend.cgi"),
    "boss": ("レジェンド戦（互換ルート）", "状態変更", "旧版_ver2/legend.cgi"),
    "bbs": ("掲示板投稿", "状態変更", "旧版_ver2/post_message.cgi"),
    "chocofarm": ("チョコボ牧場", "表示", "旧版_ver2/chocofarm.cgi"),
    "morifarm": ("チョコボの森", "表示・更新", "旧版_ver2/morifarm.cgi"),
    "choco": ("チョコボの森（互換ルート）", "表示", "旧版_ver2/morifarm.cgi"),
    "crace": ("チョコボレース", "状態変更", "旧版_ver2/crace.cgi"),
    "ctrain": ("チョコボ訓練", "状態変更", "旧版_ver2/ctrain.cgi"),
    "dendo": ("チョコボ殿堂", "表示・更新", "旧版_ver2/dendo.cgi"),
    "farmrace": ("チョコボ王者戦", "状態変更", "旧版_ver2/farmrace.cgi"),
    "system": ("登録者一覧・画像一覧・他者詳細", "表示", "旧版_ver2/system.cgi"),
    "chara_sts": ("他者詳細（system互換ルート）", "表示", "旧版_ver2/system.cgi"),
    "img_list": ("画像一覧（system互換ルート）", "表示", "旧版_ver2/system.cgi"),
    "ranking": ("登録者一覧（system互換ルート）", "表示", "旧版_ver2/system.cgi"),
    "tenka": ("天下一武道会", "表示・状態変更", "旧版_ver2/tenka.cgi"),
    "rank": ("英雄ランキング", "表示", "旧版_ver2/rank.cgi"),
    "chocorank": ("チョコボランキング", "表示", "旧版_ver2/chocorank.cgi"),
}


def load_json(name: str) -> list[dict[str, Any]]:
    with (DATA_DIR / name).open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"配列ではありません: {name}")
    return [row for row in data if isinstance(row, dict)]


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def job_labels() -> dict[int, str]:
    return {
        job_id: str(job["name"])
        for job_id, job in enumerate(load_json("syoku.json"))
        if "name" in job
    }


def job_text(item: dict[str, Any], labels: dict[int, str]) -> str:
    job_ids = item.get("job_ids", [])
    if not isinstance(job_ids, list):
        return "未設定"
    if not job_ids:
        return "共通・選択不可"
    return ", ".join(f"{job_id}:{labels.get(int(job_id), '不明')}" for job_id in job_ids)


def current_value(kind: str, item: dict[str, Any], labels: dict[int, str]) -> str:
    common = f"価格 {item.get('gold', 0):,}G / 対象職 {job_text(item, labels)}"
    if kind == "weapon":
        return f"ATK {item.get('atk', 0)} / 命中 {item.get('hit_rate', 0)}% / {common}"
    if kind == "armor":
        return f"DEF {item.get('defense', 0)} / 回避 {item.get('evasion_rate', 0)}% / {common}"

    bonus = item.get("bonus", {})
    if not isinstance(bonus, dict):
        bonus = {}
    bonus_text = ", ".join(
        f"{STAT_LABELS[key]} {bonus.get(key, 0):+}"
        for key in STAT_LABELS
        if int(bonus.get(key, 0)) != 0
    ) or "能力補正なし"
    return (
        f"効果ID {item.get('effect_id', 0)} / {bonus_text} / "
        f"命中 {item.get('hit_rate', 0)}% / 回避 {item.get('evasion_rate', 0)}% / "
        f"必殺 {item.get('special_rate', 0)}% / {common}"
    )


def checklist_row(kind: str, item: dict[str, Any], labels: dict[int, str], v2_source: str) -> str:
    item_id = item.get("no", "?")
    name = item.get("name", "名称なし")
    return (
        f"| {kind} {item_id}: {name} | `{v2_source}` の対応定義（ID・名称・数値） | "
        f"{current_value(kind, item, labels)} | 未確認 | 未判定 | 未確認 | "
        "Ver2定義と購入条件・効果を照合後に根拠を記入 |\n"
    )


def stat_text(item: dict[str, Any], prefix: str) -> str:
    values = [
        f"{label} {item.get(prefix + key, 0)}"
        for key, label in STAT_LABELS.items()
    ]
    return " / ".join(values)


def master_requirements(item: dict[str, Any], labels: dict[int, str]) -> str:
    requirements = item.get("job_reqs", [])
    if not isinstance(requirements, list):
        return "未設定"
    matched = [
        f"{job_id}:{labels.get(job_id, '不明')} Lv{level}"
        for job_id, level in enumerate(requirements)
        if int(level) > 0
    ]
    return ", ".join(matched) or "なし"


def tactic_implementation(tactic_id: int) -> str:
    return (
        f"`sub_def/skills.py`: tech_{tactic_id}.hissatu / atowaza、"
        f"wtech_{tactic_id}.whissatu / watowaza"
    )


def write_jobs(labels: dict[int, str]) -> None:
    rows = load_json("syoku.json")
    sections = [
        "# 職業データ比較チェックリスト",
        "",
        "職業IDは `data/syoku.json` の配列位置です。能力条件だけでなく、成長上限と必要なマスター職も照合対象にします。",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for job_id, item in enumerate(rows):
        name = item.get("name", "名称なし")
        current = (
            f"転職能力条件: {stat_text(item, 'req_')} / "
            f"成長上限: {stat_text(item, 'limit_')} / "
            f"必要マスター: {master_requirements(item, labels)} / "
            "`data/syoku.json`・`cgi_py/tensyoku.py`・`sub_def/battle_logic.py`"
        )
        sections.append(
            f"| 職業 {job_id}: {name} | `旧版_ver2/data/syoku.ini` の該当行、"
            f"`旧版_ver2/tensyoku.cgi`、`旧版_ver2/battle.pl` | {current} | "
            "未確認 | 未判定 | 未確認 | 転職条件・成長・熟練度・戦闘補正を照合後に根拠を記入 |"
        )
    (OUTPUT_DIR / "jobs.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def write_skills(labels: dict[int, str]) -> None:
    rows = load_json("tac.json")
    sections = [
        "# 必殺技・戦術比較チェックリスト",
        "",
        "`data/tac.json` の全戦術を列挙します。効果だけでなく、発動率、マスター条件、プレイヤー側・王者側の両実装を確認します。",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in rows:
        tactic_id = int(item.get("no", -1))
        name = item.get("name", "名称なし")
        activation = item.get("activation_denominator")
        activation_text = f"乱数幅 {activation}" if activation is not None else "乱数幅は効果側の既定値・常時効果"
        master_text = "マスター技" if int(item.get("ms", 0)) else "通常技"
        current = (
            f"利用職 {job_text(item, labels)} / {master_text} / {activation_text} / "
            f"説明: {item.get('desc', '')} / {tactic_implementation(tactic_id)}"
        )
        sections.append(
            f"| 戦術 {tactic_id}: {name} | `旧版_ver2/tech/{tactic_id}.pl`、"
            f"`旧版_ver2/wtech/{tactic_id}.pl`、`旧版_ver2/battle.pl` / `wbattle.pl` | "
            f"{current} | 未確認 | 未判定 | 未確認 | 発動率・命中/回避・計算式・回復時点・後発効果を照合後に根拠を記入 |"
        )
    (OUTPUT_DIR / "skills.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def load_monsters() -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(MONSTER_DATA_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"モンスターマスターを読み込めません: {path}") from error
        if not isinstance(data, list):
            raise ValueError(f"モンスターマスターは配列である必要があります: {path}")
        records.extend((path.name, row) for row in data if isinstance(row, dict))
    return records


def write_monster_skills() -> None:
    records = load_monsters()
    by_skill: dict[int, list[tuple[str, dict[str, Any]]]] = {}
    for source, record in records:
        skill_id = as_int(record.get("special_skill_id"))
        if skill_id > 0:
            by_skill.setdefault(skill_id, []).append((source, record))

    sections = [
        "# モンスター特殊技比較チェックリスト",
        "",
        "モンスターが使う特殊技と、その使用モンスターを分けて確認します。"
        "発動率は各モンスターの `special_rate > random.randrange(100)` です。",
        "",
        "## 特殊技一覧",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for skill_id, users in sorted(by_skill.items()):
        rates = [as_int(record.get("special_rate")) for _, record in users]
        sources = ", ".join(sorted({source for source, _ in users}))
        name = MONSTER_SKILL_LABELS.get(skill_id, "名称要確認")
        current = (
            f"使用 {len(users)}体 / special_rate {min(rates)}〜{max(rates)} / "
            f"使用マスター: {sources} / `sub_def/skills.py`: mons_{skill_id}.mons_waza / mons_atowaza"
        )
        sections.append(
            f"| モンスター特殊技 {skill_id}: {name} | `旧版_ver2/mons/{skill_id}.pl`、"
            "`旧版_ver2/mbattle.pl` | "
            f"{current} | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |"
        )

    sections.extend((
        "",
        "## 使用モンスター一覧",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ))
    for source, record in records:
        skill_id = as_int(record.get("special_skill_id"))
        if skill_id <= 0:
            continue
        name = record.get("name", "名称なし")
        v2_source = V2_MONSTER_MASTERS.get(source, "旧版_ver2/data の対応マスター")
        current = (
            f"特殊技 {skill_id}: {MONSTER_SKILL_LABELS.get(skill_id, '名称要確認')} / "
            f"special_rate {as_int(record.get('special_rate'))} / `data/monsters/{source}`"
        )
        sections.append(
            f"| {source}: {name} | `{v2_source}` の対応モンスター・特殊技ID・特殊率 | "
            f"{current} | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |"
        )
    (OUTPUT_DIR / "monster_skills.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def monster_current_value(record: dict[str, Any]) -> str:
    skill_id = as_int(record.get("special_skill_id"))
    weight = record.get("weight")
    weight_text = str(weight) if weight is not None else "1（既定値）"
    return (
        f"経験値 {as_int(record.get('exp_reward'))} / 基礎HP {as_int(record.get('hp_base'))} / "
        f"基礎攻撃 {as_int(record.get('base_damage'))} / 乱数幅 {as_int(record.get('random_range'))} / "
        f"回避 {as_int(record.get('evasion_rate'))} / 基本報酬 {as_int(record.get('gold_reward'))}G / "
        f"特殊技 {skill_id}: {MONSTER_SKILL_LABELS.get(skill_id, 'なし')} / "
        f"特殊率 {as_int(record.get('special_rate'))} / 出現重み {weight_text}"
    )


def write_monsters() -> None:
    sections = [
        "# モンスターデータ比較チェックリスト",
        "",
        "`data/monsters/` の全マスターをファイル別に列挙します。"
        "同名モンスターの重複行は、Ver2の出現重みを再現するための可能性があるため統合せずに確認します。",
        "",
    ]
    total = 0
    for path in sorted(MONSTER_DATA_DIR.glob("*.json")):
        try:
            records = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"モンスターマスターを読み込めません: {path}") from error
        if not isinstance(records, list):
            raise ValueError(f"モンスターマスターは配列である必要があります: {path}")
        records = [record for record in records if isinstance(record, dict)]
        total += len(records)
        v2_source = V2_MONSTER_MASTERS.get(path.name, "旧版_ver2/data の対応マスター")
        sections.extend((
            f"## {path.name}（{len(records)}件）",
            "",
            "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ))
        for index, record in enumerate(records):
            name = record.get("name", "名称なし")
            sections.append(
                f"| {path.name} #{index}: {name} | `{v2_source}` の対応モンスター・全能力値・報酬・特殊技 | "
                f"{monster_current_value(record)} / `data/monsters/{path.name}` | "
                "未確認 | 未判定 | 未確認 | 名前・数値・特殊技・特殊率・出現重みを照合後に根拠を記入 |"
            )
        sections.append("")
    sections.insert(3, f"対象: 9ファイル・{total}件。")
    (OUTPUT_DIR / "monsters.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def load_chocobo_data() -> list[tuple[str, list[dict[str, Any]]]]:
    files: list[tuple[str, list[dict[str, Any]]]] = []
    for path in sorted(CHOCOBO_DATA_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"チョコボマスターを読み込めません: {path}") from error
        if not isinstance(data, list):
            raise ValueError(f"チョコボマスターは配列である必要があります: {path}")
        files.append((path.name, [record for record in data if isinstance(record, dict)]))
    return files


def chocobo_candidate_value(record: dict[str, Any]) -> str:
    return (
        f"価格 {as_int(record.get('price'))}G / 初期出走 {as_int(record.get('run'))} / "
        f"初期勝利 {as_int(record.get('win'))} / 血統 {as_int(record.get('blood'))} / "
        f"技 {as_int(record.get('waza'))} / 父 {record.get('father', '')}（rank {as_int(record.get('fatherrank'))}） / "
        f"母 {record.get('mother', '')}（rank {as_int(record.get('motherrank'))}） / "
        f"e {as_int(record.get('e'))} / ブリーダー {record.get('breader', '')}"
    )


def chocobo_rival_value(record: dict[str, Any]) -> str:
    stats = " / ".join(
        f"{label} {as_int(record.get(key))}"
        for key, label in CHOCOBO_STAT_LABELS.items()
    )
    return (
        f"成長タイプ {as_int(record.get('type'))} / 賞金基準 {as_int(record.get('max'))} / "
        f"{stats} / ブリーダー {record.get('breader', '')}"
    )


def chocobo_v2_source(filename: str) -> str:
    if filename == "chocobofile.json":
        return "旧版_ver2/chocobofile.cgi / choco-farm.pl"
    return "旧版_ver2/crace.cgi / farmrace.cgi の対応ribalデータ"


def write_chocobo_data() -> None:
    files = load_chocobo_data()
    total = sum(len(records) for _, records in files)
    sections = [
        "# チョコボデータ比較チェックリスト",
        "",
        "`data/chocobo/` の全マスターをファイル別に列挙します。"
        "購入・お見合い候補とレース別ライバルを分けず、保存値をすべて比較対象にします。",
        f"対象: {len(files)}ファイル・{total}件。",
        "",
    ]
    for filename, records in files:
        is_candidate_file = filename == "chocobofile.json"
        kind = "購入・お見合い候補" if is_candidate_file else "レースライバル"
        sections.extend((
            f"## {filename}（{kind}・{len(records)}件）",
            "",
            "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ))
        for index, record in enumerate(records):
            name = record.get("name", "名称なし")
            current = chocobo_candidate_value(record) if is_candidate_file else chocobo_rival_value(record)
            check_target = "候補の血統・価格・初期値" if is_candidate_file else "ライバル名・成長型・賞金基準・能力値"
            sections.append(
                f"| {filename} #{index}: {name} | `{chocobo_v2_source(filename)}` の対応データ | "
                f"{current} / `data/chocobo/{filename}` | 未確認 | 未判定 | 未確認 | {check_target}を照合後に根拠を記入 |"
            )
        sections.append("")
    (OUTPUT_DIR / "chocobo_data.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def function_routes() -> dict[str, str]:
    """login.py の FUNCTION_MAP を静的に読み、ルート漏れを検出する。"""
    tree = ast.parse((ROOT / "login.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "FUNCTION_MAP" for target in node.targets):
            continue
        if not isinstance(node.value, ast.Dict):
            raise ValueError("FUNCTION_MAP は辞書である必要があります")
        routes: dict[str, str] = {}
        for key, value in zip(node.value.keys, node.value.values):
            if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                raise ValueError("FUNCTION_MAP のキーが文字列ではありません")
            if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
                raise ValueError("FUNCTION_MAP の値が文字列ではありません")
            routes[key.value] = value.value
        return routes
    raise ValueError("login.py に FUNCTION_MAP がありません")


def mode_values_in_source() -> set[str]:
    """現行コードで `mode` と比較される値を抽出する。"""
    files = [ROOT / "login.py", ROOT / "admin.py", ROOT / "chara_make.py"]
    files.extend(sorted((ROOT / "cgi_py").glob("*.py")))
    values: set[str] = set()

    def strings(node: ast.AST) -> set[str]:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return {node.value}
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            result: set[str] = set()
            for element in node.elts:
                result.update(strings(element))
            return result
        return set()

    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare) or not isinstance(node.left, ast.Name) or node.left.id != "mode":
                continue
            for operator, comparator in zip(node.ops, node.comparators):
                if isinstance(operator, (ast.Eq, ast.NotEq, ast.In, ast.NotIn)):
                    values.update(strings(comparator))
    return values


def mode_values_in_templates() -> set[str]:
    """テンプレートに静的に記述された hidden mode を抽出する。"""
    values: set[str] = set()
    input_pattern = re.compile(
        r"<input\b(?=[^>]*\bname=[\"']mode[\"'])(?=[^>]*\bvalue=[\"']([^\"']+)[\"'])[^>]*>",
        re.IGNORECASE,
    )
    for path in (ROOT / "templates").glob("*.html"):
        values.update(match.group(1) for match in input_pattern.finditer(path.read_text(encoding="utf-8")))
    return values


def documented_mode_values(actions: list[dict[str, str]], routes: dict[str, str]) -> set[str]:
    """台帳の行に記載した mode 値を、互換ルート表記を含めて取り出す。"""
    values = set(routes)
    for action in actions:
        if "mode=" not in action["mode"]:
            continue
        mode_value = action["mode"].split("mode=", 1)[1].split(",", 1)[0]
        values.update(part.strip() for part in mode_value.split("/") if part.strip())
    return values


def action_row(
    category: str,
    name: str,
    mode: str,
    method: str,
    state: str,
    v2_source: str,
    current_source: str,
    checks: str,
) -> dict[str, str]:
    return {
        "category": category,
        "name": name,
        "mode": mode,
        "method": method,
        "state": state,
        "v2_source": v2_source,
        "current_source": current_source,
        "checks": checks,
    }


def command_action_rows() -> list[dict[str, str]]:
    rows = [
        action_row("認証・登録", "トップ／ログイン前画面", "（others.py）", "GET", "表示", "旧版_ver2/others.cgi", "others.py / templates/others.html", "公開範囲、ログイン入力、登録導線"),
        action_row("認証・登録", "新規登録入力", "mode=chara_make", "POST", "表示", "旧版_ver2/others.cgi / chara_make.cgi", "others.py / templates/chara_make.html", "入力項目、初期職、画像選択、CSRF"),
        action_row("認証・登録", "新規登録確認", "mode=make_pre", "POST", "表示", "旧版_ver2/chara_make.cgi", "chara_make.py / templates/chara_make_pre.html", "入力検証、同一IP制限、確認画面"),
        action_row("認証・登録", "新規登録確定", "mode=make_end", "POST", "状態変更", "旧版_ver2/chara_make.cgi", "chara_make.py", "初期能力・初期装備・保存形式・パスワード"),
        action_row("認証・登録", "ログイン", "mode=log_in", "POST", "状態変更", "旧版_ver2/login.cgi", "login.py", "認証方式、セッション、旧ハッシュ移行、日次バックアップ"),
        action_row("認証・登録", "ログアウト", "mode=log_out", "POST/GET", "状態変更", "旧版_ver2/login.cgi", "login.py", "セッション破棄、遷移先"),
        action_row("認証・登録", "合言葉確認", "mode=passset", "POST", "表示", "旧版_ver2/passchange.cgi", "cgi_py/passchange.py", "本人確認条件、画面遷移"),
        action_row("認証・登録", "パスワード変更確定", "mode=passchan", "POST", "状態変更", "旧版_ver2/passchange.cgi", "cgi_py/passchange.py", "旧/新パスワード検証、ハッシュ、セッション更新"),
        action_row("街・プロフィール", "街のメイン画面", "mode=main", "GET/POST", "表示", "旧版_ver2/ffadventure.cgi", "cgi_py/ffadventure.py", "能力表示、王者情報、待機時間、掲示板表示"),
        action_row("街・プロフィール", "レジェンド挑戦を中断して街へ戻る", "mode=main, legend_cancel=1", "POST", "状態変更", "旧版_ver2/ffadventure.cgi", "cgi_py/ffadventure.py", "boss_flagのリセット値、CSRF、途中進行の扱い"),
        action_row("街・プロフィール", "自分のステータスを表示", "mode=sts", "POST", "表示", "旧版_ver2/sts.cgi", "cgi_py/sts.py", "能力・装備補正・職業熟練度・表示値"),
        action_row("街・プロフィール", "画像・発動コメントを変更", "mode=st_buy", "POST", "状態変更", "旧版_ver2/sts.cgi", "cgi_py/sts.py", "画像ID、コメント長・禁止語、保存"),
        action_row("街・プロフィール", "戦術一覧を表示", "mode=tac_change", "POST", "表示", "旧版_ver2/tac_change.cgi", "cgi_py/tac_change.py", "使用可能条件、マスター判定、現在戦術"),
        action_row("街・プロフィール", "戦術を変更", "mode=senjutu_henkou", "POST", "状態変更", "旧版_ver2/tac_change.cgi", "cgi_py/tac_change.py", "戦術ID、職業・熟練度条件、保存"),
        action_row("街・プロフィール", "転職画面を表示", "mode=tensyoku", "POST", "表示", "旧版_ver2/tensyoku.cgi", "cgi_py/tensyoku.py", "候補職、能力条件、マスター条件"),
        action_row("街・プロフィール", "転職を実行", "mode=tensyoku_change", "POST", "状態変更", "旧版_ver2/tensyoku.cgi", "cgi_py/tensyoku.py", "転職条件、現職熟練度、能力上限、戦術"),
        action_row("街・プロフィール", "掲示板へ投稿", "mode=post", "POST", "状態変更", "旧版_ver2/post_message.cgi", "cgi_py/bbs.py", "文字数、保存上限、投稿者、CSRF"),
        action_row("店・資産", "宿泊", "mode=yado", "POST", "状態変更", "旧版_ver2/shop.cgi", "cgi_py/shop.py", "宿代、HP全快、王者HP、boss_flagリセット"),
        action_row("店・資産", "銀行を表示", "mode=bank", "POST", "表示", "旧版_ver2/bank.cgi", "cgi_py/bank.py", "所持金・預金上限、表示単位"),
        action_row("店・資産", "銀行へ預け入れ", "mode=bank_sell", "POST", "状態変更", "旧版_ver2/bank.cgi", "cgi_py/bank.py", "1,000G単位、所持金・預金上限"),
        action_row("店・資産", "銀行から引き出し", "mode=bank_buy", "POST", "状態変更", "旧版_ver2/bank.cgi", "cgi_py/bank.py", "1,000G単位、所持金上限"),
        action_row("店・資産", "倉庫を表示", "mode=souko", "POST", "表示", "旧版_ver2/souko.cgi", "cgi_py/souko.py", "装備中・保管中の区分、表示順"),
    ]

    shops = (
        ("weapon", "武器", "shop_item.cgi"),
        ("armor", "防具", "shop_def.cgi"),
        ("accessory", "装飾品", "shop_acs.cgi"),
    )
    for kind, label, v2_file in shops:
        rows.extend((
            action_row("店・資産", f"{label}店を表示", f"mode=shop_{kind}", "POST", "表示", f"旧版_ver2/{v2_file}", f"cgi_py/shop_{kind}.py", "品揃え、職業制限、価格、所持品表示"),
            action_row("店・資産", f"{label}を購入", "mode=buy", "POST", "状態変更", f"旧版_ver2/{v2_file}", f"cgi_py/shop_{kind}.py", "item_no、価格、職業制限、所持金、保管先"),
            action_row("店・資産", f"{label}を売却", "mode=sell", "POST", "状態変更", f"旧版_ver2/{v2_file}", f"cgi_py/shop_{kind}.py", "売値、装備中の扱い、保管品削除、所持金上限"),
        ))

    for kind, label in (("weapon", "武器"), ("armor", "防具"), ("accessory", "装飾品")):
        rows.extend((
            action_row("店・資産", f"装備中の{label}を倉庫へ外す", f"mode={kind}_remove", "POST", "状態変更", "旧版_ver2/souko.cgi", "cgi_py/souko.py", "初期装備化、保管先、二重登録"),
            action_row("店・資産", f"倉庫の{label}を装備", f"mode={kind}_equip", "POST", "状態変更", "旧版_ver2/souko.cgi", "cgi_py/souko.py", "item_no、職業制限、既存装備の退避"),
            action_row("店・資産", f"倉庫の{label}を削除", f"mode={kind}_delete", "POST", "状態変更", "旧版_ver2/souko.cgi", "cgi_py/souko.py", "item_no、削除対象、復元不能な削除の確認"),
        ))

    rows.extend((
        action_row("戦闘・対戦", "チャンピオンに挑戦", "mode=battle", "POST", "状態変更", "旧版_ver2/battle.cgi / wbattle.pl", "cgi_py/battle.py / sub_def/battle_logic.py", "待機時間、勝敗・引分、経験値・賞金、王者交代"),
        action_row("戦闘・対戦", "対人相手一覧を表示", "mode=log_in", "POST", "表示", "旧版_ver2/select_battle.cgi", "cgi_py/select_battle.py", "対象者抽出、公開範囲、待機時間"),
        action_row("戦闘・対戦", "対人相手を選択", "mode=sentaku", "POST", "表示", "旧版_ver2/select_battle.cgi", "cgi_py/select_battle.py", "相手ID、本人・無効対象の除外"),
        action_row("戦闘・対戦", "選択相手と対戦", "mode=battle", "POST", "状態変更", "旧版_ver2/select_battle.cgi / wbattle.pl", "cgi_py/select_battle.py / sub_def/battle_logic.py", "相手認証、勝敗、経験値・賞金、戦績"),
        action_row("戦闘・対戦", "通常モンスター修行", "mode=monster", "POST", "状態変更", "旧版_ver2/monster.cgi / mbattle.pl", "cgi_py/monster.py / sub_def/battle_logic.py", "出現テーブル、回数制限、勝敗・引分報酬、経験値"),
        action_row("戦闘・対戦", "幻影の城へ挑戦", "mode=genei", "POST", "状態変更", "旧版_ver2/monster.cgi / mbattle.pl", "cgi_py/monster.py / sub_def/battle_logic.py", "出現条件、HP/防御補正、報酬"),
        action_row("戦闘・対戦", "異世界へ挑戦", "mode=isekiai", "POST", "状態変更", "旧版_ver2/monster.cgi / mbattle.pl", "cgi_py/monster.py / sub_def/battle_logic.py", "レベル条件、出現テーブル、特殊報酬"),
        action_row("戦闘・対戦", "レジェンド攻略者一覧を閲覧", "mode=legend, view=ranking", "GET", "表示", "旧版_ver2/legend.cgi", "cgi_py/legend.py", "公開範囲、順位、称号"),
        action_row("戦闘・対戦", "レジェンドの階層へ挑戦", "mode=boss, boss_file=0〜3", "POST", "状態変更", "旧版_ver2/legend.cgi / mbattle.pl", "cgi_py/legend.py / sub_def/battle_logic.py", "進行フラグ、階層順、勝敗・称号・報酬"),
        action_row("戦闘・対戦", "天下一武道会ロビーを表示", "mode=tenka", "POST", "表示", "旧版_ver2/tenka.cgi", "cgi_py/tenka.py", "参加条件、進行状態、対戦相手"),
        action_row("戦闘・対戦", "天下一武道会で対戦", "mode=battle, no=1〜3", "POST", "状態変更", "旧版_ver2/tenka.cgi / wbattle.pl", "cgi_py/tenka.py / sub_def/battle_logic.py", "ラウンド順、引分・敗北、賞金・経験値・制覇履歴"),
        action_row("閲覧", "英雄ランキングを表示", "mode=rank", "GET", "表示", "旧版_ver2/rank.cgi", "cgi_py/rank.py", "部門、勝率の対象条件、キャッシュ"),
        action_row("閲覧", "登録者一覧を表示", "mode=ranking, shtm", "GET", "表示", "旧版_ver2/system.cgi", "cgi_py/system.py", "ページング、公開項目、キャッシュ"),
        action_row("閲覧", "他者の詳細ステータスを表示", "mode=chara_sts, id", "GET", "表示", "旧版_ver2/system.cgi", "cgi_py/system.py", "公開項目、装備・マスター職、ID指定"),
        action_row("閲覧", "キャラクター画像一覧を表示", "mode=img_list", "GET", "表示", "旧版_ver2/system.cgi", "cgi_py/system.py", "画像ID・ファイル対応"),
    ))

    training = (
        ("race0", "バーベルあげ", "速度"), ("race1", "砂浜走り", "スタミナ"),
        ("race2", "スイミング", "粘り"), ("race3", "瞑想", "落ち着き"),
        ("race4", "猛特訓", "闘争心"), ("race5", "お勉強", "賢さ"), ("race6", "坂道ダッシュ", "反射神経"),
    )
    for mode, name, stat in training:
        rows.append(action_row("チョコボ", f"チョコボ訓練: {name}", f"mode={mode}", "POST", "状態変更", "旧版_ver2/ctrain.cgi", "cgi_py/ctrain.py", f"{stat}の増減、寿命、失敗時の副作用、待機時間"))

    rows.extend((
        action_row("チョコボ", "チョコボ牧場を表示", "mode=chocofarm", "POST", "表示", "旧版_ver2/chocofarm.cgi", "cgi_py/chocofarm.py", "所持判定、レース条件、重賞開催条件"),
        action_row("チョコボ", "チョコボの森を表示", "mode=choco / morifarm", "POST", "表示", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "所持判定、候補表示、互換ルート"),
        action_row("チョコボ", "野生チョコボ候補を表示", "mode=choco_shop", "POST", "表示", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "候補抽選、候補数、マスター参照"),
        action_row("チョコボ", "野生チョコボを購入", "mode=choco_buy, item_no", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "候補検証、価格、初期能力、所持制限"),
        action_row("チョコボ", "お見合い相手を表示", "mode=choco_shopb", "POST", "表示", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "性別、引退候補、候補上限"),
        action_row("チョコボ", "お見合い・配合を実行", "mode=choco_buyb, item_no", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "親の引退、血統、能力上限、子の初期値"),
        action_row("チョコボ", "チョコボに名前を付ける", "mode=choco_name", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "名前入力、禁止語、保存"),
        action_row("チョコボ", "チョコボを休ませる", "mode=yadoya", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "寿命・体力の回復、費用、待機時間"),
        action_row("チョコボ", "チョコボを手放す", "mode=choco_sell", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "引退先、売却額、取り消し不可"),
        action_row("チョコボ", "チョコボ殿堂を表示", "mode=list", "POST", "表示", "旧版_ver2/dendo.cgi", "cgi_py/dendo.py / templates/chocofarm.html", "登録済み一覧、トロフィー表示、表示用modeと登録用modeの分離"),
        action_row("チョコボ", "チョコボを殿堂登録", "mode=dendo", "POST", "状態変更", "旧版_ver2/dendo.cgi", "cgi_py/dendo.py", "重賞3勝条件、重複登録、保存値"),
        action_row("チョコボ", "チョコボランキングを表示", "mode=ranking", "POST", "表示", "旧版_ver2/chocorank.cgi", "cgi_py/chocorank.py", "部門、ランキング対象、表示値"),
        action_row("チョコボ", "チョコボ王者戦", "mode=farmrace", "POST", "状態変更", "旧版_ver2/farmrace.cgi", "cgi_py/farmrace.py", "挑戦条件、勝敗、王者更新、待機時間"),
    ))

    regular_races = (
        ("race0", "新馬戦"), ("race1", "500万以下"), ("race2", "900万以下"),
        ("race3", "1600万以下"), ("race4", "オープン特別"), ("race5", "グレードIII"), ("race6", "グレードII"),
    )
    for mode, name in regular_races:
        rows.append(action_row("チョコボ", f"チョコボレース: {name}", f"mode={mode}", "POST", "状態変更", "旧版_ver2/crace.cgi", "cgi_py/crace.py", "勝利数条件、ライバルファイル、寿命、賞金・戦績"))
    for race_id, name in enumerate(("チョコボダービー", "チョコボスタリオン", "チョコボカップ", "ジェイドカップ", "BBA賞", "チョコボ春賞", "チョコボ秋賞", "チョコボキング", "チョコボステークス", "キングスカップ", "クイーンカップ"), start=1):
        rows.append(action_row("チョコボ", f"G1レース: {name}", f"mode=race7, race={race_id}", "POST", "状態変更", "旧版_ver2/crace.cgi", "cgi_py/crace.py", "開催周期・性別、勝利数条件、トロフィー、ライバル"))
    for race_id, name in enumerate(("シルバーカップ", "新潟アドバンス", "チコスダービー", "チョコボードカップ", "チョコボエプソム", "チョコボ王", "ブリーダーズカップ", "ゴールドカップ", "プラチナカップ", "チョコボオークス", "チョコボキングス"), start=12):
        rows.append(action_row("チョコボ", f"G2レース: {name}", f"mode=race8, race={race_id}", "POST", "状態変更", "旧版_ver2/crace.cgi", "cgi_py/crace.py", "開催周期・性別、勝利数条件、トロフィー、ライバル"))
    rows.append(action_row("チョコボ", "殿堂レジェンドレース", "mode=race_dendo", "POST", "状態変更", "旧版_ver2/crace.cgi / denchoco.cgi", "cgi_py/crace.py", "出走条件、殿堂データ、勝敗・報酬"))

    admin_actions = (
        ("管理画面を表示", "kanri_top", "表示", "管理画面認証、一覧範囲"),
        ("管理画面からログアウト", "admin_log_out", "状態変更", "管理セッションの破棄"),
        ("全体メッセージを投稿", "post_all_message", "状態変更", "文字数、保存上限、投稿者"),
        ("マスター一覧を表示", "master_list", "表示", "対象マスター、ID順"),
        ("マスターを編集表示", "master_edit", "表示", "master_type、master_id、新規判定"),
        ("マスターを保存", "master_save", "状態変更", "JSON検証、ID重複、バックアップ"),
        ("マスターを削除", "master_delete", "状態変更", "削除対象、参照整合性、バックアップ"),
        ("プレイヤー所持品を表示", "player_item", "表示", "対象ID、装備・保管品"),
        ("プレイヤー所持品を追加", "player_item_add", "状態変更", "対象ID、アイテム参照、重複"),
        ("バックアップから復元", "backup_restore", "状態変更", "バックアップ名、現在状態退避、復元範囲"),
        ("保護ユーザーを復元", "restore_protected", "状態変更", "保護対象、復元元、上書き"),
        ("全キャラクターデータを表示", "kanri_all", "表示", "一覧範囲、公開情報"),
        ("個別キャラクターデータを表示", "data", "表示", "対象ID、編集項目"),
        ("個別キャラクターデータを保存", "save", "状態変更", "能力値境界、職業・HP・所持金、保存"),
        ("個別キャラクターを削除", "del_chara", "状態変更", "対象ID、関連保存データ、復元可能性"),
        ("未プレイキャラクターを削除", "del_noplay", "状態変更", "対象条件、保護ユーザー、削除範囲"),
    )
    for name, mode, state, checks in admin_actions:
        rows.append(action_row("管理", name, f"mode={mode}", "POST", state, "旧版_ver2/admin.cgi / alldata.cgi", "admin.py / templates/admin.html", checks))
    return rows


def write_commands_actions() -> None:
    routes = function_routes()
    if set(routes) != set(ROUTE_DETAILS):
        missing = sorted(set(routes) - set(ROUTE_DETAILS))
        stale = sorted(set(ROUTE_DETAILS) - set(routes))
        raise ValueError(f"ルート説明の不足または古さがあります: missing={missing}, stale={stale}")

    actions = command_action_rows()
    documented_modes = documented_mode_values(actions, routes)
    undocumented_source = mode_values_in_source() - documented_modes
    undocumented_template = mode_values_in_templates() - documented_modes
    if undocumented_source or undocumented_template:
        raise ValueError(
            "比較台帳に未記載のmodeがあります: "
            f"source={sorted(undocumented_source)}, template={sorted(undocumented_template)}"
        )

    sections = [
        "# コマンド・行動比較チェックリスト",
        "",
        "画面遷移だけのルートと、各ルート内の実行操作を分けて管理します。"
        "比較前に状態変更か表示かを確認し、Ver2との差分を具体的に記録します。",
        "",
        "## ルート一覧（login.py）",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for mode, module in routes.items():
        purpose, state, v2_source = ROUTE_DETAILS[mode]
        sections.append(
            f"| ルート `mode={mode}`: {purpose} | `{v2_source}` | `login.py` → `{module}` / {state} | "
            "未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |"
        )

    sections.extend(("", "## 実行操作一覧", ""))
    categories: list[str] = []
    for action in actions:
        if action["category"] not in categories:
            categories.append(action["category"])
    for category in categories:
        sections.extend((
            f"### {category}",
            "",
            "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ))
        for action in (item for item in actions if item["category"] == category):
            sections.append(
                f"| {action['name']}（`{action['mode']}` / {action['method']} / {action['state']}） | "
                f"`{action['v2_source']}` | `{action['current_source']}` | 未確認 | 未判定 | 未確認 | {action['checks']} |"
            )
        sections.append("")
    sections.insert(4, f"対象: ルート {len(routes)}件、実行操作 {len(actions)}件。")
    (OUTPUT_DIR / "commands_actions.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def comparison_row(name: str, v2_source: str, current_source: str, checks: str) -> str:
    return (
        f"| {name} | `{v2_source}` | `{current_source}` | 未確認 | 未判定 | 未確認 | {checks} |"
    )


def write_static_checklist(filename: str, title: str, introduction: str, sections_data: tuple[tuple[str, tuple[tuple[str, str, str, str], ...]], ...]) -> None:
    sections = [f"# {title}", "", introduction, ""]
    for heading, rows in sections_data:
        sections.extend((
            f"## {heading}",
            "",
            "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ))
        sections.extend(comparison_row(*row) for row in rows)
        sections.append("")
    (OUTPUT_DIR / filename).write_text("\n".join(sections), encoding="utf-8")


def write_battle_logic_checklist() -> None:
    write_static_checklist(
        "battle_logic.md",
        "戦闘計算・結果処理比較チェックリスト",
        "戦闘入口の一覧ではなく、共通シミュレータと各結果処理を比較単位にした台帳です。必殺技の個別効果は skills.md、モンスター特殊技は monster_skills.md と併用します。",
        (
            ("戦闘状態の初期化と攻撃値", (
                ("戦闘モード別の状態初期化", "旧版_ver2/battle.pl:shokika / mbattle.pl:shokika / wbattle.pl:shokika", "sub_def/battle_logic.py:BattleState.__init__", "mode別の初期値、対人・モンスターの状態キー、ターン上限"),
                ("装備・アクセサリーの戦闘用補正コピー", "旧版_ver2/battle.pl:acs_add / wbattle.pl:wacs_add", "sub_def/battle_logic.py:_with_accessory_bonus", "恒久保存値を変更しないこと、8能力値補正、対人側補正"),
                ("モンスターHP・初期HPの乱数", "旧版_ver2/mbattle.pl:mons_read / shokika", "sub_def/battle_logic.py:BattleState.__init__", "hp_base、random_range、最小値、表示用最大HP"),
                ("職業別の基礎ダメージ（全31職）", "旧版_ver2/battle.pl:syokuzero〜syokuthirty", "sub_def/battle_logic.py:get_job_dmg", "各職IDの参照能力値、乱数範囲、武器ATK、カルマの扱い"),
                ("モンスター・対人相手の基礎ダメージ", "旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts", "sub_def/battle_logic.py:BattleSimulator.simulate", "base_damage、random_range、相手職業・装備、幻影の城補正"),
                ("最大ターンと時間切れ", "旧版_ver2/mbattle.pl:winlose / wbattle.pl:winlose", "sub_def/battle_logic.py:BattleState.turn / BattleSimulator.simulate", "最大ターン数、未決着時の引き分け、ログ最終ターン"),
            )),
            ("必殺技・固有効果の発動順", (
                ("選択戦術IDの取得", "旧版_ver2/battle.pl:chara[30] / wbattle.pl:winner[37]", "sub_def/battle_logic.py:get_tactic_id", "未設定値、不正値、現職以外のマスター戦術の使用可否"),
                ("戦術マスター由来の発動率分母", "旧版_ver2/tac.ini / battle.pl:tyosenwaza", "sub_def/battle_logic.py:_load_tactic_activation_denominators / skills.py:skill_check", "説明文の確率と乱数分母、未定義戦術、Ver2との差異"),
                ("プレイヤー必殺率・上限・特殊モード減衰", "旧版_ver2/battle.pl:tyosenwaza", "sub_def/battle_logic.py:BattleSimulator.simulate", "カルマ・職業熟練度・アクセ補正、75/95上限、genei・isekiai・boss補正"),
                ("リミットブレイク", "旧版_ver2/battle.pl:tyosenwaza / wbattle.pl:winwaza", "sub_def/battle_logic.py:BattleSimulator.simulate", "HP10%未満の条件、乱数、プレイヤー・対人相手の双方"),
                ("プレイヤー戦術の必殺技実行", "旧版_ver2/tech/*.pl", "sub_def/skills.py:tech_* .hissatu / run_skill", "全戦術IDの呼出先、発動失敗時、副作用とログ"),
                ("対人相手戦術の必殺技実行", "旧版_ver2/wtech/*.pl", "sub_def/skills.py:wtech_* .whissatu / run_skill", "相手側tactic_id、発動率、プレイヤー側との対称性"),
                ("モンスター特殊技の実行", "旧版_ver2/mons/*.pl", "sub_def/skills.py:mons_* .mons_waza / run_skill", "special_skill_id・special_rate、通常行動との排他、各技効果"),
                ("戦術の後発効果", "旧版_ver2/tech/*.pl:atowaza / wtech/*.pl:watowaza", "sub_def/skills.py:tech_* .atowaza / wtech_* .watowaza", "必殺技後の実行順、対象、累積・上限"),
                ("アクセサリー固有効果", "旧版_ver2/acstech/*.pl / wacstech/*.pl", "sub_def/skills.py:acstech_* / wacstech_*", "effect_id、発動順、対人双方、装備能力補正との重複"),
                ("対人1ターン目の逆転必殺", "旧版_ver2/wbattle.pl:battle_clt", "sub_def/battle_logic.py:BattleSimulator.simulate", "レベル差・装備比較条件、倍率、武器無効化、双方の判定順"),
            )),
            ("ダメージ確定・HP・勝敗", (
                ("クリティカル判定（プレイヤー攻撃）", "旧版_ver2/mbattle.pl:mons_clt / wbattle.pl:battle_clt", "sub_def/battle_logic.py:BattleSimulator.simulate", "HP比率、乱数幅、モンスター戦3倍・対人戦2倍+武器ATK"),
                ("クリティカル判定（敵攻撃）", "旧版_ver2/mbattle.pl:mons_clt / wbattle.pl:battle_clt", "sub_def/battle_logic.py:BattleSimulator.simulate", "モンスター・対人での確率、ダメージ補正、回復技の除外"),
                ("防具DEFによるダメージ減算と最小値", "旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts", "sub_def/battle_logic.py:BattleSimulator.simulate", "モンスター戦0・対人戦1の最小ダメージ、負値・防御不能ログ"),
                ("上級職の被ダメージ軽減", "旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts", "sub_def/battle_logic.py:BattleSimulator.simulate", "職業ID 8〜17の半減、18以上の1/4、双方への適用"),
                ("命中・回避判定", "旧版_ver2/mbattle.pl:mons_kaihi / wbattle.pl:battle_kaihi", "sub_def/battle_logic.py:BattleSimulator.simulate", "dex・agi、武器命中・防具回避・アクセ補正、乱数幅、対人双方"),
                ("先行攻撃による敵行動停止", "旧版_ver2の行動・勝敗処理", "sub_def/battle_logic.py:BattleSimulator.simulate", "敵がこのターンに倒れる場合の敵ダメージ・ログ、対人・モンスター双方"),
                ("ドレイン回復の基準", "旧版_ver2/tech/43.pl ほか", "sub_def/battle_logic.py:BattleSimulator.simulate / skills.py", "防御・回避後の実ダメージ基準、回復比率、0ダメージ時"),
                ("HP・回復・自傷の精算順", "旧版_ver2/mbattle.pl:hp_sum / wbattle.pl:hp_sum", "sub_def/battle_logic.py:BattleSimulator.simulate", "同時精算、最大HP上限、過剰回復、死亡と回復の組合せ"),
                ("ターンログの記録値", "旧版_ver2/mbattle.pl:mons_footer / wbattle.pl:battle_sts", "sub_def/battle_logic.py:BattleSimulator.battle_logs / templates/monster_result.html", "表示HP、ダメージ、回復、勝敗文、HTMLエスケープ"),
                ("勝利・敗北・引き分けの判定", "旧版_ver2/mbattle.pl:winlose / wbattle.pl:winlose", "sub_def/battle_logic.py:BattleSimulator.simulate", "相打ち、判定優先順位、時間切れ、結果コード"),
            )),
            ("戦闘後の報酬・成長・進行", (
                ("通常・幻影・異世界の報酬処理", "旧版_ver2/monster.cgi / mbattle.pl:sentoukeka", "cgi_py/monster.py", "勝利・引き分け・敗北EXP/G、盗み差分、battle_limit、幻影宝箱"),
                ("レジェンドの報酬・階層進行", "旧版_ver2/legend.cgi / mbattle.pl:legend_sentoukeka", "cgi_py/legend.py", "boss_flag、title_id、階層解放、称号、敗北・中断時"),
                ("チャンピオン戦の報酬・王者更新", "旧版_ver2/battle.cgi / wbattle.pl:sentoukeka", "cgi_py/battle.py", "敗北EXP上限、勝利・引き分けEXP、賞金、王者保存、制限回復"),
                ("天下一武道会の報酬・ラウンド進行", "旧版_ver2/tenka.cgi / wbattle.pl:sentoukeka", "cgi_py/tenka.py", "相手順、勝敗・引分、ログ、boss_flag、制限回復"),
                ("対人練習戦の保存有無", "旧版_ver2/select_battle.cgi", "cgi_py/select_battle.py", "戦闘ログのみか、経験値・所持金・戦績・待機時間を更新しないこと"),
                ("経験値加算とレベルアップ", "旧版_ver2/battle.pl:levelup", "sub_def/battle_logic.py:process_levelup", "必要EXP、複数Lv上昇、最大Lv、能力・HP成長、職業上限"),
                ("職業熟練度の正規化とマスター", "旧版_ver2/battle.pl:syoku_regist", "sub_def/battle_logic.py:process_levelup / cgi_py/tensyoku.py", "Lv60上限、既存61以上の正規化、転職時の保存"),
            )),
        ),
    )


def write_progression_checklist() -> None:
    write_static_checklist(
        "ownership_progression.md",
        "所有・進行要素比較チェックリスト",
        "プレイヤー固有・共有の状態が、どこで作成・更新・消去・参照されるかを比較する台帳です。マスターデータの値比較とは分離します。",
        (
            ("キャラクター・戦闘進行", (
                ("キャラクター作成時の初期状態", "旧版_ver2/chara_make.cgi", "chara_make.py", "初期能力、職業、装備、所持金、戦術、battle_limit、boss_flag、チョコボ空値"),
                ("職業熟練度とマスター職", "旧版_ver2/syoku.cgi / tensyoku.cgi", "cgi_py/tensyoku.py / cgi_py/sts.py / sub_def/common.py", "職業別熟練度、Lv60、転職時の退避・復帰、表示"),
                ("装備中の武器・防具・アクセサリー", "旧版_ver2/item/<ID>.cgi", "user_all.json:equipment / cgi_py/shop_*.py / cgi_py/souko.py", "ID・性能スナップショット、職業制限、初期装備、削除時"),
                ("倉庫の武器", "旧版_ver2/souko/item/<ID>.cgi", "user_all.json:souko_weapon / sub_def/common.py:souko_*", "保存形式、件数、装備交換、削除、重複"),
                ("倉庫の防具", "旧版_ver2/souko/def/<ID>.cgi", "user_all.json:souko_armor / sub_def/common.py:souko_*", "保存形式、件数、装備交換、削除、重複"),
                ("倉庫のアクセサリー", "旧版_ver2/souko/acs/<ID>.cgi", "user_all.json:souko_accessory / sub_def/common.py:souko_*", "effect_id・能力補正・説明、装備交換、削除、重複"),
                ("戦績・戦闘回数・勝利数", "旧版_ver2/charalog/<ID>.cgi", "user_all.json:chara / cgi_py/monster.py / battle.py / tenka.py", "battle_count、win_countの更新対象、練習戦除外、ランキング利用"),
                ("修行回数・待機時刻", "旧版_ver2/charalog/<ID>.cgi / mbattle.pl:time_check", "user_all.json:chara.battle_limit,last_time / 各戦闘CGI", "初期値、減算・回復契機、コンテンツ別待機時間"),
                ("レジェンドの進行フラグ・称号", "旧版_ver2/legend.cgi / charalog", "user_all.json:chara.boss_flag,title_id / cgi_py/legend.py", "開始・勝利・敗北・中断時の値、タイトル解放条件"),
                ("人間チャンピオン", "旧版_ver2/datalog/winner.cgi / battle.cgi", "save_data/champion.json / cgi_py/battle.py", "挑戦者の装備・戦術の保存、勝者交代、防衛戦績、初期王者"),
                ("天下一武道会の参加者・対戦履歴", "旧版_ver2/all_tenka.cgi / tenka_log.cgi", "save_data/all_tenka.json,tenka_log.json / cgi_py/tenka.py", "参加者抽出、順序、ログ保持数、制覇履歴"),
            )),
            ("チョコボ所有・レース進行", (
                ("チョコボ所持判定と未所持値", "旧版_ver2/chocolog/<ID>.cgi", "user_all.json:choco / sub_def/common.py:is_choco_owned", "空辞書・欠損・実体データの判定、旧データ互換"),
                ("飼育中チョコボの基本状態", "旧版_ver2/chocolog/<ID>.cgi", "user_all.json:choco / cgi_py/morifarm.py", "名前、性別、血統、画像、能力c0〜c6、寿命、体力、戦績"),
                ("野生チョコボの候補・購入", "旧版_ver2/morifarm.cgi / chocobofile.cgi", "cgi_py/morifarm.py / data/chocobo/chocobofile.json", "候補抽選、価格、候補消費、所持制限、初期値"),
                ("引退・お見合い候補リスト", "旧版_ver2/chocoboms.cgi / chocoboos.cgi", "save_data/chocoboms.json,chocoboos.json / cgi_py/morifarm.py", "性別別保存、候補上限、引退時移動、配合後の削除"),
                ("配合後の子チョコボ", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "父母・血統、能力上限、性別、初期能力、親の扱い"),
                ("訓練・休養による状態変化", "旧版_ver2/ctrain.cgi / morifarm.cgi", "cgi_py/ctrain.py / cgi_py/morifarm.py", "各能力、寿命・体力、失敗、副作用、費用・待機時間"),
                ("通常レースの戦績・クラス進行", "旧版_ver2/crace.cgi", "cgi_py/crace.py / user_all.json:choco", "run、win、gold、class条件、寿命、敗北時の変化"),
                ("G1/G2の個人トロフィー履歴", "旧版_ver2/chocog1/<ID>.cgi", "user_all.json:choco_g1 / cgi_py/crace.py", "r1〜r22、開催日・性別条件、重複勝利、殿堂条件"),
                ("チョコボ殿堂の共有リスト", "旧版_ver2/denchoco.cgi / dendo.cgi", "save_data/denchoco.json / cgi_py/dendo.py", "3重賞条件、同一チョコボの上書き、保存項目、一覧"),
                ("チョコボ王者", "旧版_ver2/chocowinner.cgi / farmrace.cgi", "save_data/chocobo_champion.json / cgi_py/farmrace.py", "挑戦条件、勝者更新、連勝・前王者、初期値"),
            )),
            ("記録・共有状態", (
                ("ログイン履歴", "旧版_ver2/loginlog/<ID>.cgi", "user_all.json:login_log / login.py", "保存件数、日時・IP等の項目、ログイン時更新"),
                ("受信・送信メッセージ", "旧版_ver2/message / sousin", "user_all.json:message / save_data/<ID>/message_sent.json", "保存先分離、件数、既読・削除、変換時の扱い"),
                ("全体メッセージ・掲示板", "旧版_ver2/datalog/message.cgi / post_message.cgi", "save_data/all_message.json / cgi_py/bbs.py / admin.py", "投稿者、保存件数、表示順、管理投稿"),
                ("登録者・ランキング用キャッシュ", "旧版_ver2/alldata.cgi / rank.cgi", "save_data/system_rank_cache.json / cgi_py/system.py / rank.py", "対象プレイヤー、更新時刻、キャッシュ無効化、公開項目"),
            )),
        ),
    )


def write_storage_migration_checklist() -> None:
    write_static_checklist(
        "storage_migration_operations.md",
        "保存・認証・移行・運用比較チェックリスト",
        "現行の安全対策・JSON保存形式はVer2と意図的に異なる可能性があります。差異を見つけた時点で、互換性・安全性・運用上の必要性を分けて判断します。",
        (
            ("入力・表示・認証", (
                ("CGIパラメータの復号・文字列処理", "旧版_ver2/regist.pl / login.cgi", "sub_def/common.py:decode_params", "GET/POSTの優先順位、複数値、文字コード、空値・不正値"),
                ("CGI入口のUTF-8標準入出力", "旧版Ver2 CGIの出力設定", "others.py,login.py,chara_make.py,admin.py:reconfigure", "Windows Apache CP932環境、4入口の維持、UTF-8ヘッダーとの整合"),
                ("HTML出力・リダイレクトのヘッダー", "旧版_ver2/regist.pl:header / footer", "sub_def/utils.py:render_template,redirect", "Content-Type、UTF-8、キャッシュ制御、Location、例外時出力"),
                ("セッションCookieの暗号化・改ざん検証", "旧版_ver2/login.cgi:set_cookie", "sub_def/crypto.py:encrypt_data,decrypt_data,get_session,save_session", "Cookie内容、署名、期限、HttpOnly、旧Cookieとの関係"),
                ("ログイン・ログアウト", "旧版_ver2/login.cgi:log_in", "login.py", "ID・パスワード検証、セッション更新、記憶Cookie、日次バックアップの起点"),
                ("パスワード形式とログイン時移行", "旧版Ver2の保存パスワード", "sub_def/crypto.py:hash_password,verify_password,needs_rehash / login.py", "平文・旧ハッシュ・PBKDF2の受入範囲、成功時再ハッシュ"),
                ("CSRFトークンの生成・検証・再生成", "旧版Ver2のフォーム送信", "sub_def/crypto.py:token_generate,token_regenerate,token_check", "対象POST、トークン寿命、再表示時、エラー時"),
                ("本人操作の認可（IDOR対策）", "旧版Ver2のID・パスワード照合", "sub_def/common.py:require_owner / 各状態変更CGI", "対象操作、Cookieとの照合、ロック前検証、閲覧操作との区別"),
            )),
            ("JSON保存・ロック", (
                ("統合ユーザー保存形式", "旧版_ver2/charalog,item,syoku,souko等の分割ファイル", "save_data/<ID>/user_all.json / sub_def/file_ops.py", "セクション構成、必須・任意キー、旧分割データとの対応"),
                ("ユーザーデータのキー順・旧キー正規化", "旧版Ver2の配列列番号", "sub_def/data_schema.py:order_user_data", "title→title_id、unused30→tactic_id、site/url削除、未知キー保持"),
                ("装備・アクセサリー保存値の正規化", "旧版_ver2/item/<ID>.cgi", "sub_def/data_schema.py:_order_equipment / sub_def/common.py", "武器・防具・アクセ順、bonus8能力、旧アクセキー、説明補完"),
                ("HTMLエンティティの読込正規化", "旧版のHTML保存文字列", "sub_def/file_ops.py:_normalize_loaded_data / sub_def/common.py:decode_html_entities", "再帰対象、二重復号、名前・コメント・ログへの影響"),
                ("単一JSONの原子的書込み", "旧版_ver2/regist.pl:chara_regist ほか", "sub_def/file_ops.py:_write_json_atomically,save_data_atomically", "一時ファイル、fsync、os.replace、例外時の残存一時ファイル"),
                ("read-modify-writeの原子更新", "旧版_ver2/regist.pl:lock / unlock", "sub_def/file_ops.py:update_data_atomically", "読込から保存までの同一ロック、default値、更新関数の例外"),
                ("ユーザー・共有データのロック", "旧版_ver2/regist.pl:lock / unlock", "sub_def/common.py:get_lock,release_lock / sub_def/lock_state.py", "ロック名、再入、タイムアウト、ディレクトリロック、必ず解放すること"),
                ("バックアップ中のスナップショット排他", "旧版には相当処理なし", "sub_def/file_ops.py:backup_snapshot.lock / sub_def/backup.py", "通常保存とバックアップの順序、デッドロック、保存待機"),
                ("部分更新API", "旧版の複数ファイル個別保存", "sub_def/common.py:save_user_sections,souko_regist,choco_regist", "他セクションを消さないこと、読込失敗時、呼出元のロック"),
            )),
            ("バックアップ・管理復元", (
                ("日次バックアップ作成", "旧版_ver2/save_log.cgi", "sub_def/backup.py:create_daily_backup,ensure_daily_backup", "実行契機、対象範囲、同日再実行、失敗時のログイン継続"),
                ("バックアップのマニフェスト・世代削除", "旧版_ver2/save_log.cgi", "sub_def/backup.py:_write_manifest,_prune_daily_backups,list_daily_backups", "件数・容量、形式検証、保持日数、壊れた世代の表示除外"),
                ("管理画面からのバックアップ復元", "旧版Ver2の手動復元運用", "sub_def/backup.py:restore_daily_backup / admin.py:backup_restore", "maintenance_mode必須、パス検証、復元前退避、現在save_dataの置換"),
                ("保護ユーザーの復元", "旧版Ver2の保護データ運用", "admin.py:protected_backup_path,restore_protected_users", "対象ID、JSON妥当性、個別ロック、上書き範囲"),
                ("管理画面によるマスター保存・削除", "旧版_ver2/admin.cgi", "admin.py:validate_master_record,save_master_records", "ID一意性、型・下限、JSON妥当性、アクセサリーキャッシュ無効化"),
            )),
            ("旧版からの移行", (
                ("Ver1→Ver2変換", "旧版_ver1/セーブデータ移行用ファイル/convert_to_ver2.py", "docs/migration_specs.html（履歴資料）", "入力・出力の列対応、原本保持、dry-run、Ver3比較対象外であること"),
                ("Ver2→Ver3ユーザー本体変換", "旧版_ver2/charalog/<ID>.cgi", "旧版_ver2/change_data/convert_all.py / sub_def/data_schema.py", "列番号→charaキー、能力値順、パスワード、戦績、戦術・称号"),
                ("Ver2→Ver3装備・職業・倉庫変換", "旧版_ver2/item,syoku,souko", "旧版_ver2/change_data/convert_all.py", "マスター参照、装備性能、職業熟練度、倉庫件数、旧形式の残存"),
                ("Ver2→Ver3ログ・共有データ変換", "旧版_ver2/loginlog,message,sousin,datalog", "旧版_ver2/change_data/convert_all.py", "message_sentの別保存、champion.json、all_message.json、欠損時"),
                ("Ver2チョコボの移行時初期化", "旧版_ver2のチョコボ保存データ", "旧版_ver2/change_data/convert_all.py / docs/migration_specs.html", "現役チョコボを移さずchoco/choco_g1を空辞書にする意図、既存データとの衝突"),
                ("変換の文字コード・検証用出力", "旧版Ver2のCP932テキスト", "旧版_ver2/change_data/convert_all.py", "CP932読込、文字化け置換、dry-run、検証先出力、現行save_dataを直接上書きしないこと"),
            )),
        ),
    )


def write_index(counts: dict[str, int]) -> None:
    text = f"""# Ver2 / Ver3 比較チェックリスト

Ver2から移植したFFA Python版（Ver3）の、データ・コマンド・行動を比較するための作業台帳です。\
ここに記載した「未確認」は差異なしを意味せず、まだ照合していないことを示します。

## 運用ルール

- `Ver2との差異` は、値・条件・処理順・表示・保存形式を具体的に記載する。
- `意図的な仕様か否か` は `意図的` / `不具合` / `要判断` のいずれかを記載し、根拠を備考に残す。
- Ver2に寄せる修正をする前に、現行側で追加された安全対策・バランス調整かを必ず確認する。
- `照合状態` は `未確認` / `確認中` / `一致` / `差異あり` / `対象外` を使う。

## チェック対象一覧

| 区分 | 内容 | 状態 |
| --- | --- | --- |
| 装備データ | [武器・防具・アクセサリー](equipment.md)（武器 {counts['weapon']}件、防具 {counts['armor']}件、アクセサリー {counts['accessory']}件） | 項目作成済み |
| 職業データ | [職業31件](jobs.md)：転職条件、成長上限、必要マスター職 | 項目作成済み |
| 戦術・必殺技データ | [戦術78件](skills.md)：説明、利用職、マスター条件、発動率、効果 | 項目作成済み |
| モンスター特殊技 | [特殊技22種・使用220体](monster_skills.md)：特殊技、特殊率、使用モンスター | 項目作成済み |
| モンスターデータ | [全9ファイル・347件](monsters.md)：出現テーブル、能力値、報酬、ボス・異世界 | 項目作成済み |
| チョコボデータ | [全10ファイル・495件](chocobo_data.md)：候補血統、価格、ライバル、レース能力 | 項目作成済み |
| 戦闘 | [戦闘計算・結果処理](battle_logic.md)：ターン順、必殺技、クリティカル、防御・回避、HP、勝敗、報酬、成長 | 項目作成済み |
| コマンド・画面 | [ルート{len(function_routes())}件・実行操作一覧](commands_actions.md)：移動、店、宿、銀行、転職、ランキング、管理画面 | 項目作成済み |
| 所有・進行要素 | [所有・進行](ownership_progression.md)：職業・装備・倉庫・戦績・王者・レジェンド・チョコボ・共有記録 | 項目作成済み |
| 保存・移行・運用 | [保存・認証・移行・運用](storage_migration_operations.md)：JSON、認証、CSRF、ロック、バックアップ、変換 | 項目作成済み |

## 共通の記入列

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 例: 武器 1001: アイアンソード | 旧版の定義ファイル・該当ID | Ver3のJSON・参照コード | 数値や条件を具体的に記載 | 意図的 / 不具合 / 要判断 | 未確認など | コミット、仕様書、確認日 |
"""
    (OUTPUT_DIR / "README.md").write_text(text, encoding="utf-8")


def write_equipment(labels: dict[int, str]) -> None:
    sections = [
        "# 装備データ比較チェックリスト",
        "",
        "Ver3の装備マスターを全件列挙した初期台帳です。Ver2の `item.pl` と照合して記入します。",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for kind, label, v2_source in EQUIPMENT:
        rows = load_json(f"{kind}.json")
        sections.extend(("", f"## {label}（{len(rows)}件）", ""))
        sections.extend(checklist_row(kind, item, labels, v2_source) for item in rows)
    (OUTPUT_DIR / "equipment.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    labels = job_labels()
    counts = {kind: len(load_json(f"{kind}.json")) for kind, _, _ in EQUIPMENT}
    write_index(counts)
    write_equipment(labels)
    write_jobs(labels)
    write_skills(labels)
    write_monster_skills()
    write_monsters()
    write_chocobo_data()
    write_commands_actions()
    write_battle_logic_checklist()
    write_progression_checklist()
    write_storage_migration_checklist()


if __name__ == "__main__":
    main()
