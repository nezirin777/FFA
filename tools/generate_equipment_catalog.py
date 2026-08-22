"""装備マスターから職業別の閲覧用HTMLカタログを生成します。

正本は data/weapon.json などのマスターファイルです。
このHTMLは確認用の生成物であり、ゲーム本体からは読み込みません。
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402


EQUIPMENT_TYPES = (
    ("weapon", "武器", "weapon_file"),
    ("armor", "防具", "armor_file"),
    ("accessory", "アクセサリー", "accessory_file"),
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


def load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"マスターデータは配列である必要があります: {path}")
    return [item for item in data if isinstance(item, dict)]


def escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def number(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return escape(value)


def equipment_details(kind: str, item: dict[str, Any]) -> str:
    if kind == "weapon":
        return " / ".join(
            (
                f"ATK {number(item.get('atk', 0))}",
                f"命中 {number(item.get('hit_rate', 0))}%",
                f"価格 {number(item.get('gold', 0))} G",
            )
        )

    if kind == "armor":
        return " / ".join(
            (
                f"DEF {number(item.get('defense', 0))}",
                f"回避 {number(item.get('evasion_rate', 0))}%",
                f"価格 {number(item.get('gold', 0))} G",
            )
        )

    bonus = item.get("bonus", {})
    bonus_text = [
        f"{STAT_LABELS.get(key, key)} +{number(value)}"
        for key, value in bonus.items()
        if isinstance(value, (int, float)) and value != 0
    ]
    rate_text = [
        f"命中 {number(item.get('hit_rate', 0))}%",
        f"回避 {number(item.get('evasion_rate', 0))}%",
        f"必殺 {number(item.get('special_rate', 0))}%",
    ]
    effects = bonus_text + [value for value in rate_text if not value.endswith(" 0%")]
    if not effects:
        effects.append("補正なし")
    effects.append(f"価格 {number(item.get('gold', 0))} G")
    return " / ".join(effects)


def item_row(kind: str, label: str, item: dict[str, Any]) -> str:
    description = item.get("description", "") if kind == "accessory" else ""
    return """<tr>
  <td>{kind}</td>
  <td>{no}</td>
  <th scope="row">{name}</th>
  <td>{details}</td>
  <td>{description}</td>
</tr>""".format(
        kind=escape(label),
        no=number(item.get("no", "")),
        name=escape(item.get("name", "")),
        details=escape(equipment_details(kind, item)),
        description=escape(description),
    )


def build_groups() -> tuple[dict[int, list[tuple[str, str, dict[str, Any]]]], list[tuple[str, str, dict[str, Any]]]]:
    jobs = config.Config["chara_jobs"]
    groups = {job_id: [] for job_id in jobs}
    special: list[tuple[str, str, dict[str, Any]]] = []

    for kind, label, config_key in EQUIPMENT_TYPES:
        path = ROOT / config.Config[config_key]
        for item in load_json(path):
            job_ids = item.get("job_ids", [])
            if not isinstance(job_ids, list) or not job_ids:
                special.append((kind, label, item))
                continue
            for job_id in job_ids:
                if isinstance(job_id, int) and job_id in groups:
                    groups[job_id].append((kind, label, item))
                else:
                    special.append((kind, f"未定義の職業ID: {job_id}", item))

    for entries in groups.values():
        entries.sort(key=lambda entry: (entry[0], entry[2].get("no", 0)))
    special.sort(key=lambda entry: (entry[0], entry[2].get("no", 0)))
    return groups, special


def render_group(title: str, entries: list[tuple[str, str, dict[str, Any]]], anchor: str) -> str:
    if not entries:
        return ""
    rows = "\n".join(item_row(kind, label, item) for kind, label, item in entries)
    return f"""<section class="job-section" id="{escape(anchor)}">
  <h2>{escape(title)}</h2>
  <table>
    <thead>
      <tr><th>分類</th><th>No.</th><th>装備名</th><th>性能</th><th>説明</th></tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</section>"""


def render_html() -> str:
    groups, special = build_groups()
    jobs = config.Config["chara_jobs"]
    navigation = []
    sections = []
    for job_id, job_name in jobs.items():
        if groups[job_id]:
            anchor = f"job-{job_id}"
            navigation.append(f'<a href="#{anchor}">{escape(job_id)}: {escape(job_name)}</a>')
            sections.append(render_group(f"職業 {job_id}: {job_name}", groups[job_id], anchor))

    if special:
        navigation.append('<a href="#special">初期装備・特殊装備</a>')
        sections.append(render_group("初期装備・特殊装備", special, "special"))

    nav_html = "\n".join(navigation)
    section_html = "\n".join(sections)
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>装備マスター 職業別カタログ</title>
<style>
:root {{ color-scheme: light; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; color: #1f2937; background: #f3f6f8; line-height: 1.5; }}
main {{ width: min(1500px, calc(100% - 32px)); margin: 0 auto; padding: 28px 0 56px; }}
h1 {{ margin: 0 0 8px; color: #123b4a; }}
.note {{ margin: 0 0 20px; color: #52616b; }}
.catalog-nav {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0 28px; }}
.catalog-nav a {{ padding: 7px 10px; color: #075985; background: #e0f2fe; border: 1px solid #bae6fd; border-radius: 6px; text-decoration: none; }}
.job-section {{ margin: 0 0 28px; background: #fff; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden; }}
h2 {{ margin: 0; padding: 12px 16px; color: #fff; background: #155e75; font-size: 1.15rem; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ padding: 9px 10px; border-top: 1px solid #e2e8f0; text-align: left; vertical-align: top; }}
thead th {{ color: #334155; background: #f8fafc; border-top: 0; font-size: .9rem; }}
tbody th {{ color: #0f3d4a; font-weight: 600; }}
td:nth-child(2) {{ width: 70px; white-space: nowrap; }}
td:nth-child(4) {{ min-width: 360px; }}
td:nth-child(5) {{ min-width: 180px; color: #52616b; }}
@media (max-width: 760px) {{
  main {{ width: min(100% - 16px, 1500px); padding-top: 18px; }}
  table {{ display: block; overflow-x: auto; white-space: nowrap; }}
  td:nth-child(4), td:nth-child(5) {{ min-width: 260px; }}
}}
</style>
</head>
<body>
<main>
  <h1>装備マスター 職業別カタログ</h1>
  <p class="note">このページは data/weapon.json / data/armor.json / data/accessory.json から自動生成されます。編集する場合は正本のマスターデータを変更してください。</p>
  <nav class="catalog-nav" aria-label="職業別リンク">{nav_html}</nav>
  {section_html}
</main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="装備マスターの職業別HTMLカタログを生成します。")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "docs" / "equipment_catalog.html",
        help="出力先HTML (既定: docs/equipment_catalog.html)",
    )
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(), encoding="utf-8")
    print(f"装備カタログを生成しました: {output}")


if __name__ == "__main__":
    main()
