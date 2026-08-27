"""管理者向けのマスターデータ・戦闘仕様ドキュメントを生成する。

正本は config.py、data/*.json、cgi_py/*.py、sub_def/*.py であり、
docs/*.html は確認用の生成物である。ゲーム本体からは読み込まない。
"""

from __future__ import annotations

import argparse
import ast
import html
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402


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
STAT_ORDER = tuple(STAT_LABELS)

DOC_LINKS = (
    ("index.html", "資料一覧"),
    ("equipment_catalog.html", "装備カタログ"),
    ("job_catalog.html", "職業カタログ"),
    ("monster_catalog.html", "モンスターカタログ"),
    ("status_reference.html", "キー・能力値辞典"),
    ("battle_specs.html", "戦闘仕様書"),
    ("skill_specs.html", "必殺技仕様書"),
    ("chocobo_specs.html", "チョコボ仕様書"),
    ("migration_specs.html", "移行・保存形式仕様書"),
    ("operations_specs.html", "管理・運用手順書"),
    ("security_specs.html", "セキュリティ仕様書"),
    ("command_flowcharts.html", "コマンドフローチャート"),
)


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def num(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return esc(value)


def load_json(relative_path: str) -> Any:
    path = ROOT / relative_path
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def shared_css() -> str:
    return """
:root { color-scheme: light; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
* { box-sizing: border-box; }
body { margin: 0; color: #1f2937; background: #f3f6f8; line-height: 1.55; }
main { width: min(1540px, calc(100% - 32px)); margin: 0 auto; padding: 28px 0 60px; }
h1 { margin: 0 0 8px; color: #123b4a; line-height: 1.25; }
h2 { margin: 34px 0 12px; color: #155e75; line-height: 1.3; }
h3 { margin: 24px 0 8px; color: #0f3d4a; }
.lead { margin: 0 0 18px; color: #52616b; }
.doc-nav { display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0 28px; }
.doc-nav a { padding: 7px 10px; color: #075985; background: #e0f2fe; border: 1px solid #bae6fd; border-radius: 6px; text-decoration: none; }
.doc-nav a:hover { background: #bae6fd; }
.note { padding: 12px 14px; color: #475569; background: #fffbeb; border: 1px solid #fde68a; border-radius: 7px; }
.source { color: #64748b; font-size: .9rem; }
.card { margin: 14px 0; padding: 16px; background: #fff; border: 1px solid #cbd5e1; border-radius: 8px; }
.card h3 { margin-top: 0; }
.table-wrap { margin: 12px 0 24px; overflow-x: auto; background: #fff; border: 1px solid #cbd5e1; border-radius: 8px; }
table { width: 100%; border-collapse: collapse; min-width: 720px; }
th, td { padding: 8px 10px; border-top: 1px solid #e2e8f0; text-align: left; vertical-align: top; }
thead th { color: #334155; background: #f8fafc; border-top: 0; white-space: nowrap; font-size: .9rem; }
tbody th { color: #0f3d4a; font-weight: 600; white-space: nowrap; }
code { padding: 1px 4px; color: #0f3d4a; background: #e6f4f1; border-radius: 4px; }
.tag { display: inline-block; margin: 2px 4px 2px 0; padding: 2px 6px; color: #155e75; background: #ecfeff; border: 1px solid #a5f3fc; border-radius: 4px; font-size: .86rem; }
.muted { color: #64748b; }
.small { font-size: .9rem; }
.formula { margin: 8px 0; padding: 10px 12px; color: #334155; background: #f8fafc; border-left: 4px solid #38bdf8; font-family: ui-monospace, SFMono-Regular, Consolas, monospace; white-space: pre-wrap; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 14px; }
@media (max-width: 760px) { main { width: min(100% - 16px, 1540px); padding-top: 18px; } table { min-width: 680px; } }
"""


def page(title: str, lead: str, body: str) -> str:
    nav = "".join(f'<a href="{href}">{esc(label)}</a>' for href, label in DOC_LINKS)
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{shared_css()}</style>
</head>
<body>
<main>
  <h1>{esc(title)}</h1>
  <p class="lead">{esc(lead)}</p>
  <nav class="doc-nav" aria-label="管理者向け資料">{nav}</nav>
  {body}
</main>
</body>
</html>
"""


def table(headers: list[str], rows: list[list[str]], row_headers: bool = False) -> str:
    head = "".join(f"<th>{esc(value)}</th>" for value in headers)
    body_rows = []
    for row in rows:
        cells = []
        for index, value in enumerate(row):
            tag = "th" if row_headers and index == 0 else "td"
            scope = ' scope="row"' if tag == "th" else ""
            cells.append(f"<{tag}{scope}>{value}</{tag}>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body_rows)}</tbody></table></div>'


def tag(text: str) -> str:
    return f'<span class="tag">{esc(text)}</span>'


def skill_methods() -> dict[str, dict[int, set[str]]]:
    """skills.py に定義されたID別の効果メソッドを静的に取得する。"""
    result: dict[str, dict[int, set[str]]] = {
        prefix: {} for prefix in ("tech", "wtech", "mons", "acstech", "wacstech")
    }
    source_path = ROOT / "sub_def" / "skills.py"
    try:
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    except (OSError, SyntaxError):
        return result

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        prefix, separator, raw_id = node.name.rpartition("_")
        if not separator or prefix not in result:
            continue
        try:
            skill_id = int(raw_id)
        except ValueError:
            continue
        result[prefix][skill_id] = {
            method.name for method in node.body if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
    return result


def implementation_status(methods: set[str], expected: str) -> str:
    """呼び出し側が期待するメソッドの実装有無を資料用に表示する。"""
    if expected in methods:
        return tag("実装あり")
    if methods:
        return f'{tag("呼出し不一致")} <code>{esc(" / ".join(sorted(methods)))}</code>'
    return tag("未実装")


def job_catalog() -> str:
    jobs = config.Config["chara_jobs"]
    records = load_json(config.Config["syoku_file"])
    weapons = load_json(config.Config["weapon_file"])
    armors = load_json(config.Config["armor_file"])
    accessories = load_json(config.Config["accessory_file"])
    tactics = load_json(config.Config["tac_file"])

    equipment_counts = {job_id: [0, 0, 0] for job_id in jobs}
    for index, items in enumerate((weapons, armors, accessories)):
        for item in items:
            for job_id in item.get("job_ids", []):
                if job_id in equipment_counts:
                    equipment_counts[job_id][index] += 1

    tactic_counts = {job_id: 0 for job_id in jobs}
    for tactic in tactics:
        for job_id in tactic.get("job_ids", []):
            if job_id in tactic_counts:
                tactic_counts[job_id] += 1

    req_labels = [(key, STAT_LABELS[key]) for key in STAT_ORDER]
    rows = []
    sections = []
    for job_id, job_name in jobs.items():
        data = records[job_id] if job_id < len(records) else {}
        reqs = [f"{label} {num(data.get('req_' + key, 0))}" for key, label in req_labels if data.get('req_' + key, 0)]
        limits = [f"{label} +{num(data.get('limit_' + key, 0))}" for key, label in req_labels if data.get('limit_' + key, 0)]
        mastery = [
            f"{jobs.get(index, '職業' + str(index))} Lv{num(value)}"
            for index, value in enumerate(data.get("job_reqs", []))
            if value
        ]
        equipment = equipment_counts.get(job_id, [0, 0, 0])
        initial = tag("キャラ作成可") if job_id in config.Config["initial_job_ids"] else ""
        rows.append([
            f'<span id="job-{job_id}"></span>{num(job_id)}',
            f"{esc(job_name)} {initial}",
            " / ".join(reqs) if reqs else '<span class="muted">なし</span>',
            " / ".join(limits) if limits else '<span class="muted">上昇なし</span>',
            " / ".join(mastery) if mastery else '<span class="muted">なし</span>',
            f"武器 {equipment[0]} / 防具 {equipment[1]} / アクセ {equipment[2]} / 戦術 {tactic_counts.get(job_id, 0)}",
        ])
        sections.append(f'<a href="#job-{job_id}">{num(job_id)}: {esc(job_name)}</a>')

    body = f"""
<div class="note">職業IDはキャラクター、装備、戦術、職業熟練度から参照される固定値です。既存IDを変更せず、新職業は末尾へ追加してください。<br><span class="source">正本: data/syoku.json / config.py / data/tac.json / data/weapon.json / data/armor.json / data/accessory.json</span></div>
<nav class="doc-nav" aria-label="職業内リンク">{"".join(sections)}</nav>
<h2>項目の意味</h2>
{table(["項目", "意味"], [
    ["req_*", "転職先として選ぶために必要な最低能力値。0は条件なし。"],
    ["limit_*", "レベルアップ時、該当能力が上昇する場合の最大幅。0はレベルアップ上昇なし。"],
    ["job_reqs", "配列位置の職業を、指定レベル以上マスターしている必要がある条件。"],
    ["job_ids", "装備・戦術を購入・装備・使用できる職業IDの配列。空配列は通常の職業別販売対象外。"],
    ["ms", "戦術がマスター職業由来かどうか。1は職業レベル60以上が必要。"],
], row_headers=True)}
<h2>全職業一覧</h2>
{table(["ID", "職業", "転職能力条件", "レベルアップ上昇幅", "熟練度条件", "関連マスター件数"], rows)}
"""
    return page("職業マスター 職業別カタログ", "職業名、転職条件、レベルアップ上昇幅、熟練度条件と関連マスターを確認する管理資料", body)


def monster_catalog() -> str:
    groups = [
        ("通常戦闘・初級", config.Config["monster_lv1_file"], "通常戦闘のmonster0"),
        ("通常戦闘・中級", config.Config["monster_lv2_file"], "通常戦闘のmonster1"),
        ("通常戦闘・上級", config.Config["monster_lv3_file"], "通常戦闘のmonster2"),
        ("通常戦闘・最上級", config.Config["monster_lv4_file"], "通常戦闘のmonster3"),
        ("異世界", config.Config["isekai_file"], "レベル300以上のisekiai"),
        ("レジェンドプレイス・階層1", config.Config["legend_boss_lv1_file"], "boss_file=0"),
        ("レジェンドプレイス・階層2", config.Config["legend_boss_lv2_file"], "boss_file=1"),
        ("レジェンドプレイス・階層3", config.Config["legend_boss_lv3_file"], "boss_file=2"),
        ("レジェンドプレイス・階層4", config.Config["legend_boss_lv4_file"], "boss_file=3"),
    ]
    status_rows = [
        ["name", "モンスター名。ログや結果画面に表示する。"],
        ["exp_reward", "勝利時に得る経験値。通常戦闘の引き分けはこの半分、レジェンドの引き分けもこの半分。"],
        ["random_range", "HP・通常攻撃の乱数幅。0以上 random_range 未満の乱数を加算する。"],
        ["hp_base", "通常戦闘時の基礎HP。HPは hp_base + 乱数。幻影の城は hp_base×2 + 乱数。"],
        ["base_damage", "モンスターの通常攻撃の基礎値。毎ターン random_range の乱数を加算する。"],
        ["evasion_rate", "モンスターの回避率として敵回避判定に使う値。"],
        ["special_skill_id", "sub_def/skills.py の mons_&lt;ID&gt; を呼び出す特殊技ID。0は通常の特殊技なし。"],
        ["special_rate", "モンスター特殊技の発動率。特殊技クラス側で0〜99の乱数と比較する。"],
        ["gold_reward", "勝利時の基本報酬。実際の勝利報酬は基本値に1〜基本値の乱数を加える。"],
        ["weight", "通常戦闘の出現重み。旧版の同一モンスター重複登録を再現する。未指定は1。"],
    ]
    sections = []
    nav = []
    for index, (label, path, condition) in enumerate(groups):
        records = load_json(path)
        anchor = f"group-{index}"
        nav.append(f'<a href="#{anchor}">{esc(label)}</a>')
        rows = []
        for record in records:
            weight = record.get("weight", 1)
            weight_text = num(weight) if "weight" in record else "1 (既定値)"
            rows.append([
                esc(record.get("name", "")),
                num(record.get("exp_reward", 0)),
                num(record.get("random_range", 0)),
                num(record.get("hp_base", 0)),
                num(record.get("base_damage", 0)),
                num(record.get("evasion_rate", 0)),
                num(record.get("special_skill_id", "")),
                num(record.get("special_rate", 0)),
                num(record.get("gold_reward", 0)),
                weight_text,
            ])
        sections.append(f'<section id="{anchor}"><h2>{esc(label)}</h2><p class="source">ファイル: <code>{esc(path)}</code> / 出現条件: {esc(condition)} / {len(records)}件</p>{table(["名前", "経験値", "乱数幅", "基礎HP", "基礎攻撃", "回避", "特殊技ID", "特殊率", "基本報酬", "重み"], rows)}</section>')

    body = f"""
<div class="note">モンスターのキー名は、旧版の短縮キーではなく現行処理の役割に合わせています。特殊技の具体的な処理は <code>sub_def/skills.py</code> の <code>mons_&lt;special_skill_id&gt;</code>、戦闘への適用順は <code>sub_def/battle_logic.py</code> を参照してください。</div>
<h2>データ項目の意味</h2>
{table(["キー", "意味"], status_rows, row_headers=True)}
<h2>出現マスター一覧</h2>
<nav class="doc-nav" aria-label="モンスター分類">{"".join(nav)}</nav>
{"".join(sections)}
"""
    return page("モンスター・ボスマスター一覧", "通常戦闘、異世界、レジェンドプレイスで使われる出現マスターと各キーの意味を確認する管理資料", body)


def status_reference() -> str:
    character_rows = [
        ["id", "ログイン・保存データの識別子"], ["pass", "PBKDF2形式のパスワードハッシュ"],
        ["name", "キャラクター名"], ["img", "config.py の chara_images の画像番号"], ["sex", "性別。0=女、1=男"],
        ["level", "キャラクターレベル"], ["max_hp / hp", "最大HP / 現在HP"],
        *[[key, label] for key, label in STAT_LABELS.items()],
        ["job / job_level", "現在の職業ID / 現職の熟練度レベル"], ["exp", "次のレベルアップ判定に使う保有経験値"],
        ["gold / bank", "所持金 / 銀行預金"], ["weapon_id / armor_id / accessory_id", "装備マスターのNo."],
        ["battle_count / win_count", "戦闘回数 / 勝利数。ランキング・勝率表示に使う"],
        ["battle_limit", "通常戦闘・レジェンドの残り回数。チャンプ戦・天下一後に補充"],
        ["boss_flag", "レジェンド・天下一の進行フラグ。10は挑戦可能状態"],
        ["comment", "戦闘クリティカル表示などに使うキャラクターコメント"], ["host", "最終保存時の接続元"],
        ["last_time", "最後の行動時刻。クールタイム計算に使う"], ["title_id", "レジェンドプレイス攻略称号のID"],
        ["tactic_id", "現在選択中の戦術No."],
    ]
    equipment_rows = [
        ["weapon.atk", "武器攻撃力。職業基礎ダメージへ加算"], ["weapon.hit_rate", "攻撃側の命中補正"],
        ["armor.defense", "被ダメージから減算する防御力"], ["armor.evasion_rate", "防具による回避補正"],
        ["accessory.bonus.*", "力・知能・信仰心・生命力・器用さ・速さ・魅力・カルマへの装備補正"],
        ["accessory.hit_rate", "命中補正"], ["accessory.evasion_rate", "回避補正"],
        ["accessory.special_rate", "必殺技発動率補正"], ["accessory.effect_id", "acstech_&lt;ID&gt; の固有効果"],
    ]
    battle_rows = [
        ["1", "勝利。基本報酬・通常経験値・勝利数を反映"],
        ["2", "引き分け。基礎報酬なし、盗み等の差分のみ反映する戦闘がある"],
        ["0", "敗北。各コマンドの敗北時ペナルティを反映"],
    ]
    body = f"""
<div class="note">このページは保存JSONを直接読むときの辞書です。能力値の並びは旧版の意味順を維持し、内部キーも意味が一致する現行名に統一しています。<br><span class="source">正本: sub_def/data_schema.py / sub_def/battle_logic.py / sub_def/skills.py</span></div>
<h2>キャラクターデータ</h2>
{table(["キー", "意味"], character_rows, row_headers=True)}
<h2>装備データ</h2>
{table(["キー", "意味"], equipment_rows, row_headers=True)}
<h2>戦闘結果値</h2>
{table(["値", "意味"], battle_rows, row_headers=True)}
<h2>能力値の対応順</h2>
{table(["順番", "表示名", "キー"], [[num(index + 1), label, f"<code>{key}</code>"] for index, (key, label) in enumerate(STAT_LABELS.items())])}
"""
    return page("保存キー・能力値リファレンス", "キャラクター、装備、モンスター、戦闘結果で使うキーの意味を確認する管理資料", body)


def battle_specs() -> str:
    c = config.Config
    job_damage_rows = [
        ["0", "str"], ["1, 4, 5", "int"], ["2", "mnd"], ["3", "dex"],
        ["6", "mnd + cha"], ["7, 9, 10, 11, 12, 13, 14, 15, 16", "複数の基本能力値"],
        ["8", "str + vit"], ["17", "int + mnd + cha"], ["18〜21, 28〜30", "8能力値すべて"],
        ["22, 26, 27", "8能力値すべて ×2"], ["23", "str"], ["24", "vit + dex + agi + cha + karma ×2"],
        ["25", "str + int + mnd + vit + dex×5 + agi + cha + karma を2倍"],
    ]
    mode_rows = [
        ["通常戦闘", "monster", "monster0〜3を選択。battle_limit>0、20秒待機", "勝利: gold_reward + 1〜gold_reward、経験値全量 / 引き分け: 経験値半分・盗み差分 / 敗北: 所持金1%・経験値0", "battle_count+1、勝利時win_count+1、battle_limit-1"],
        ["幻影の城", "genei", "battle_count>0、last_timeが5の倍数、レベル帯でモンスター層選択", "通常戦闘と同じ。勝利時1/3で財宝を追加抽選", "通常戦闘と同じ"],
        ["異世界", "isekiai", f"レベル{num(c['isekai_level'])}以上、20秒待機", "通常戦闘と同じ", "通常戦闘と同じ"],
        ["レジェンドプレイス", "boss", "battle_count>0、title_id>=boss_file、battle_limit>0、20秒待機", "勝利: ボス報酬・経験値、boss_flag-1 / 引き分け: 経験値半分・盗み差分 / 敗北: 所持金1%・経験値1", "毎戦battle_count+1、win_countは勝利時、battle_limit-1。勝利継続時のみboss_flagを保持"],
        ["チャンプ戦", "battle", "現チャンプと対戦、20秒待機", "勝利・引き分け: 新チャンプ、相手賞金・盗み差分 / 敗北: 所持金半分、王者防衛", "battle_count+1、勝利時win_count+1、boss_flagを10へ戻し、battle_limitを9999へ補充"],
        ["天下一武道会", "tenka", f"登録メンバー{num(c['tenka_count'])}人、ラウンド順を検証、20秒待機", "勝利: 次ラウンドへ / 引き分け: 所持金半減なし・盗み差分 / 敗北: 所持金半分", "全結果でbattle_count+1・経験値・熟練度保存、battle_limitを9999へ補充"],
        ["練習戦", "select_battle", "対戦相手を指定", "戦闘ログのみ。ステータス、所持金、経験値を保存しない", "保存処理なし"],
    ]
    result_rows = [
        ["1", "勝利", "通常報酬・経験値・勝利数を反映。通常戦闘とレジェンドではbattle_limitを1減算。"],
        ["2", "引き分け", "時間切れまたは相打ち。基礎金額は支給せず、盗みなどの戦闘中差分のみ反映する。"],
        ["0", "敗北", "敗北ペナルティを反映。モンスター戦は所持金1%、レジェンドは所持金1%、対人・天下一は所持金半分。"],
    ]
    turn_rows = [
        ["1", "ターン初期化", "職業と武器から攻撃値を作成。モンスターはbase_damage + 乱数。"],
        ["2", "プレイヤー必殺技", "選択中のtactic_idをtech_&lt;ID&gt;としてhissatu実行。"],
        ["3", "敵必殺技", "対人は相手のwtech、モンスターはmons_<special_skill_id>を実行。"],
        ["4", "後発効果", "戦術のatowaza、アクセサリー固有効果、敵側の同等処理。"],
        ["5", "対人初手判定", "レベル差または武器・防具条件で逆転必殺を判定。"],
        ["6", "クリティカル", "実ダメージがある攻撃だけHP割合によるクリティカル判定。回復技には付かない。"],
        ["7", "防御・回避", "防具DEFを減算し、上級職の防御補正、命中・回避判定を適用。0ダメージ理由もログ出力。"],
        ["8", "HP・回復", "ダメージ、回復、自傷、ドレインを反映してHPを更新。"],
        ["9", "勝敗判定", "敵HP<=0で勝利、プレイヤーHP<=0で敗北、対人双方0で引き分け。最大150ターン。"],
    ]
    body = f"""
<div class="note">このページは現行の <code>sub_def/battle_logic.py</code>、<code>sub_def/skills.py</code>、<code>cgi_py/*.py</code> とConfig値を基準にした処理仕様です。挙動を変更した場合はこの生成スクリプトも更新してください。</div>
<h2>行動制限・共通値</h2>
{table(["項目", "現行値", "意味"], [
    ["対人・レース系クールタイム", f"{num(c['pvp_race_cooldown_seconds'])}秒", "battle / tenka / チョコボレース等の再実行待ち"],
    ["修行・レジェンド系クールタイム", f"{num(c['training_cooldown_seconds'])}秒", "monster / genei / isekiai / legend / チョコボ訓練等の再実行待ち"],
    ["training_battle_limit", num(c['training_battle_limit']), "通常戦闘・レジェンドの残り回数初期値。チャンプ戦・天下一後に補充"],
    ["最大ターン", num(c['max_turns']), "1戦闘のターン上限"],
    ["対人経験値係数", num(c['pvp_base_exp']), "勝利・引き分け時の相手レベルへの乗算値"],
])}
<h2>戦闘入口と結果処理</h2>
{table(["コンテンツ", "mode", "出現・参加条件", "勝利・引き分け・敗北", "保存・進行"], mode_rows)}
<h2>勝敗値の共通定義</h2>
{table(["値", "名称", "処理"], result_rows, row_headers=True)}
<h2>1ターンの処理順</h2>
{table(["順番", "処理", "内容"], turn_rows, row_headers=True)}
<h2>職業別の基礎ダメージ参照</h2>
<p class="small">乱数は各能力値について0以上、能力値未満から抽選し、武器ATKを加算します。正確な職業IDごとの式は <code>sub_def/battle_logic.py:get_job_dmg()</code> が正本です。</p>
{table(["職業ID", "参照する能力値"], job_damage_rows, row_headers=True)}
<h2>必殺技・固有効果の呼び出し規則</h2>
<p class="small">戦術の利用条件、発動率の計算、実装メソッドとマスターの対応は <a href="skill_specs.html">必殺技仕様書</a> にまとめています。</p>
{table(["種類", "呼び出し先", "発動率・補足"], [
    ["戦術", "tactic_id → tech_&lt;ID&gt;", "プレイヤー側。戦術マスターの説明に設定された乱数幅を使う"],
    ["対人相手の戦術", "相手 tactic_id → wtech_&lt;ID&gt;", "相手側の必殺・後発効果として実行"],
    ["モンスター特殊技", "special_skill_id → mons_&lt;ID&gt;", "データのspecial_rateを0〜99乱数と比較"],
    ["装飾品固有効果", "effect_id → acstech_&lt;ID&gt;", "通常攻撃後に実行。相手側はwacstech_&lt;ID&gt;"],
])}
<h2>関連ソース</h2>
<p class="source"><code>cgi_py/monster.py</code> / <code>cgi_py/legend.py</code> / <code>cgi_py/battle.py</code> / <code>cgi_py/tenka.py</code> / <code>cgi_py/select_battle.py</code> / <code>sub_def/battle_logic.py</code> / <code>sub_def/skills.py</code></p>
"""
    return page("FFA 戦闘仕様書", "各戦闘の入口条件、ターン処理、勝利・引き分け・敗北時の報酬と保存状態を確認する管理資料", body)


def skill_specs() -> str:
    """戦術・モンスター技・装飾品効果の運用資料を生成する。"""
    c = config.Config
    tactics = load_json(c["tac_file"])
    accessories = load_json(c["accessory_file"])
    methods = skill_methods()
    jobs = c["chara_jobs"]

    tactic_rows = []
    for tactic in tactics:
        tactic_id = int(tactic["no"])
        job_names = [f"{job_id}: {jobs.get(job_id, '職業' + str(job_id))}" for job_id in tactic.get("job_ids", [])]
        mastery = "現職Lv60以上が必要" if tactic.get("ms", 0) == 1 else "現職で使用可"
        denominator = tactic.get("activation_denominator")
        activation = (
            f"乱数幅 {num(denominator)}"
            if denominator is not None
            else "未指定（効果側の既定判定または常時効果）"
        )
        own_methods = methods["tech"].get(tactic_id, set())
        opponent_methods = methods["wtech"].get(tactic_id, set())
        own_status = (
            f"<code>tech_{tactic_id}.hissatu</code> {implementation_status(own_methods, 'hissatu')}<br>"
            f"<code>tech_{tactic_id}.atowaza</code> {implementation_status(own_methods, 'atowaza')}"
        )
        opponent_status = (
            f"<code>wtech_{tactic_id}.whissatu</code> {implementation_status(opponent_methods, 'whissatu')}<br>"
            f"<code>wtech_{tactic_id}.watowaza</code> {implementation_status(opponent_methods, 'watowaza')}"
        )
        tactic_rows.append([
            num(tactic_id), esc(tactic.get("name", "")),
            " / ".join(job_names) if job_names else "共通・選択不可",
            mastery, activation, esc(tactic.get("desc", "")), own_status, opponent_status,
        ])

    monster_by_skill: dict[int, list[dict[str, Any]]] = {}
    monster_source_names: dict[int, set[str]] = {}
    monster_dir = ROOT / "data" / "monsters"
    for path in sorted(monster_dir.glob("*.json")):
        try:
            records = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(records, list):
            continue
        for record in records:
            if not isinstance(record, dict):
                continue
            try:
                skill_id = int(record.get("special_skill_id", 0))
            except (TypeError, ValueError):
                continue
            if skill_id <= 0:
                continue
            monster_by_skill.setdefault(skill_id, []).append(record)
            monster_source_names.setdefault(skill_id, set()).add(path.name)

    monster_rows = []
    for skill_id, records in sorted(monster_by_skill.items()):
        rates = [int(record.get("special_rate", 0)) for record in records]
        class_methods = methods["mons"].get(skill_id, set())
        monster_rows.append([
            num(skill_id), num(len(records)),
            f"{num(min(rates))}〜{num(max(rates))}",
            " / ".join(sorted(monster_source_names[skill_id])),
            f"<code>mons_{skill_id}.mons_waza</code> {implementation_status(class_methods, 'mons_waza')}<br>"
            f"<code>mons_{skill_id}.mons_atowaza</code> {implementation_status(class_methods, 'mons_atowaza')}",
        ])

    accessories_by_effect: dict[int, list[dict[str, Any]]] = {}
    for accessory in accessories:
        try:
            effect_id = int(accessory.get("effect_id", 0))
        except (TypeError, ValueError):
            continue
        if effect_id > 0:
            accessories_by_effect.setdefault(effect_id, []).append(accessory)

    accessory_rows = []
    for effect_id, records in sorted(accessories_by_effect.items()):
        own_methods = methods["acstech"].get(effect_id, set())
        opponent_methods = methods["wacstech"].get(effect_id, set())
        names = " / ".join(esc(record.get("name", "")) for record in records)
        accessory_rows.append([
            num(effect_id), names,
            f"<code>acstech_{effect_id}.acskouka</code> {implementation_status(own_methods, 'acskouka')}",
            f"<code>wacstech_{effect_id}.wacskouka</code> {implementation_status(opponent_methods, 'wacskouka')}",
        ])

    body = f"""
<div class="note">必殺技は戦術マスターのIDをそのまま <code>sub_def/skills.py</code> のクラス名に使う互換仕様です。IDを振り直さず、戦術の追加・変更時は戦術マスター、プレイヤー側・対人側の実装、資料をまとめて確認してください。</div>
<h2>設定から戦闘までの経路</h2>
{table(["段階", "現行処理", "管理上の確認点"], [
    ["利用可能な戦術", "<code>cgi_py/tac_change.py</code> が現在職の <code>job_ids</code> と <code>ms</code> を検証する。現在の設定では他職も熟練度Lv60以上なら候補へ加える。", "<code>reset_tactics_on_job_change</code>={num(c['reset_tactics_on_job_change'])}。戦術変更のPOSTでも候補にないIDは拒否する。"],
    ["選択の保存", "選択IDを <code>chara.tactic_id</code> へ保存する。0は「普通に戦う」。", "戦術IDは職業IDではない。データ移行・管理編集でも両者を混同しない。"],
    ["プレイヤー側", "各ターンで <code>tech_&lt;tactic_id&gt;.hissatu</code>、通常攻撃後に <code>tech_&lt;tactic_id&gt;.atowaza</code> を実行する。", "クラスまたはメソッドが存在しない場合、<code>run_skill()</code> は何もせず続行する。"],
    ["対人相手側", "各ターンで <code>wtech_&lt;tactic_id&gt;.whissatu</code>、後発で <code>wtech_&lt;tactic_id&gt;.watowaza</code> を実行する。", "下の対応表で実装名を確認する。クラスまたはメソッドが存在しない場合、<code>run_skill()</code> は何もせず続行する。"],
    ["モンスター側", "<code>special_skill_id</code> から <code>mons_&lt;ID&gt;.mons_waza</code> と <code>mons_atowaza</code> を実行する。", "特殊率は各モンスターの <code>special_rate</code> を使う。"],
    ["装飾品", "通常攻撃後に自分側は <code>acstech_&lt;effect_id&gt;.acskouka</code>、対人相手側は <code>wacstech_&lt;effect_id&gt;.wacskouka</code> を実行する。", "<code>effect_id</code> と <code>special_rate</code> は別の役割。前者は固有効果、後者は戦術必殺率への補正。"],
], row_headers=True)}
<h2>戦術必殺技の発動率</h2>
<p class="formula">基本率 = floor(カルマ / 15) + 10 + 現職熟練度Lv
基本率は75で上限 → 装飾品 special_rate を加算 → 95で上限
発動判定 = 率 &gt; random.randrange(乱数幅)
通常は戦術の activation_denominator を乱数幅として使う。</p>
{table(["条件", "補正"], [
    ["発動率ラベルの既定値", "激高=60 / 高=80 / 中=100 / 低=120 / 超低=180 / 激低=200。<code>activation_denominator</code> がある戦術はその値を優先する。"],
    ["幻影の城・異世界", "プレイヤー側の率を3分の1へ切り捨てる。"],
    ["レジェンドプレイス", "プレイヤー側の率を2分の1へ切り捨てる。"],
    ["リミットブレイク", "自HPが最大HPの10%未満かつ4分の2の抽選に通ると、率へ999を加算する。"],
    ["対人相手", "相手のカルマ・現職熟練度・装飾品special_rateから別に計算する。"],
], row_headers=True)}
<p class="note small">乱数幅がDで率が0〜Dの範囲なら、おおよその発動確率は率/Dです。実際には上限・モード減衰・リミットブレイク・効果側の追加抽選があるため、説明文だけから最終ダメージや発動回数を判断しないでください。</p>
<h2>戦術マスターと実装の対応</h2>
<p class="source">正本: <code>{esc(c['tac_file'])}</code> / <code>cgi_py/tac_change.py</code> / <code>sub_def/battle_logic.py</code> / <code>sub_def/skills.py</code></p>
{table(["ID", "戦術名", "利用職", "利用条件", "発動率設定", "説明", "プレイヤー側", "対人相手側"], tactic_rows)}
<h2>モンスター特殊技の使用状況</h2>
<p class="small">各 <code>mons_&lt;ID&gt;</code> はクラス内で <code>special_rate &gt; random.randrange(100)</code> を判定する。表の特殊率は、全モンスターマスターに登録された最小値〜最大値です。</p>
{table(["特殊技ID", "使用モンスター数", "special_rate範囲", "参照マスター", "実装"], monster_rows)}
<h2>装飾品の固有効果</h2>
<p class="source">正本: <code>{esc(c['accessory_file'])}</code> / <code>sub_def/skills.py</code></p>
{table(["effect_id", "該当装飾品", "プレイヤー側", "対人相手側"], accessory_rows)}
<h2>調整時の確認順</h2>
{table(["変更対象", "確認する場所"], [
    ["戦術名・利用職・マスター条件・説明", "<code>data/tac.json</code> の no / job_ids / ms / desc。IDは既存のskillsクラスと対応する。"],
    ["発動率", "<code>activation_denominator</code>、<code>sub_def/battle_logic.py</code> の率計算、装飾品の <code>special_rate</code>。"],
    ["技の効果", "<code>sub_def/skills.py</code> の tech / wtech。必殺と後発効果を分けて確認する。"],
    ["モンスター技", "<code>data/monsters/*.json</code> の special_skill_id / special_rate と <code>mons_&lt;ID&gt;</code>。"],
    ["装飾品固有効果", "<code>data/accessory.json</code> の effect_id と acstech / wacstech。"],
    ["対人の初手逆転必殺", "戦術とは別系統。<code>config.py</code> の counterattack_level_gap / counterattack_damage_multiplier と <code>sub_def/battle_logic.py</code> を確認する。"],
], row_headers=True)}
"""
    return page("FFA 必殺技・特殊効果仕様書", "戦術必殺技、モンスター特殊技、装飾品固有効果の設定・発動率・実装対応を確認する管理資料", body)


def chocobo_specs() -> str:
    c = config.Config
    types = c["chocobo_types"]
    wild_path = c["wild_chocobo_file"]
    wild_records = load_json(wild_path)

    def storage_count(relative_path: str) -> str:
        path = Path(relative_path)
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            return "未作成"
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return "読込不可"
        return f"{len(value):,}件" if isinstance(value, list) else "オブジェクト"

    def data_path(path_value: str) -> str:
        """設定値の絶対パスを、資料内ではプロジェクト相対で表示する。"""
        path = Path(path_value)
        if not path.is_absolute():
            return path.as_posix()
        try:
            return path.resolve().relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return path.as_posix()

    storage_rows = [
        ["現役チョコボ", "save_data/&lt;ユーザーID&gt;/user_all.json の choco", "必要キーが揃った辞書だけを所持状態として扱う。空辞書や欠損データは未所持。"],
        ["重賞個人履歴", "save_data/&lt;ユーザーID&gt;/user_all.json の choco_g1", "r1〜r22の獲得状況。殿堂入り条件と重賞表示に使う。"],
        ["メス引退リスト", "save_data/chocoboms.json", f"オスの配合相手。現行件数 {storage_count('save_data/chocoboms.json')} / 最大 {num(c['chocobo_partner_list_limit'])}件。"],
        ["オス引退リスト", "save_data/chocoboos.json", f"メスの配合相手。現行件数 {storage_count('save_data/chocoboos.json')} / 最大 {num(c['chocobo_partner_list_limit'])}件。"],
        ["殿堂入りリスト", "save_data/denchoco.json", "3つ以上の重賞タイトルを持つチョコボを登録し、殿堂レースの相手にも使う。"],
        ["重賞制覇履歴", "save_data/rireki.json", "全体の重賞制覇履歴。未作成でも重賞処理時に作成される。"],
        ["チョコボチャンプ", data_path(c["chocobo_champion_file"]), "農場王者決定戦の現王者。空の場合は管理者の初期表示データを使う。"],
        ["ランキングキャッシュ", "save_data/chocorank_cache.json", "チョコボランキングの24時間キャッシュ。現役データから再構築される。"],
    ]

    owned_rows = [
        ["id / pass / breader", "所有ユーザーID / パスワードハッシュ / ブリーダー名。通常はユーザーデータから引き継ぐ。"],
        ["name / sex", "チョコボ名 / 性別。sex=0がメス、sex=1がオス。"],
        ["blood", "血統ランク。配合時の子の血統値計算に使う。"],
        ["no / type", "チョコボ画像番号 / 成長タイプID。typeはConfigのchocobo_typesに対応する。"],
        ["life", "体調・寿命値。訓練は200以上、レースは400以上が必要。訓練・レース1回で200消費する。"],
        ["train / run / win", "訓練回数 / 出走回数 / 勝利数。クラス判定、重賞開催周期、ランキングに使う。"],
        ["max / maxmax", "現在の総合能力限界 / 血統などから決まる最終限界値。レース・訓練でmaxが上がる。"],
        ["max0〜max6", "各能力の限界値。現在値が限界を超えないよう訓練後に調整する。"],
        ["c0〜c6", "現在能力。順にスピード、スタミナ、粘り、落ち着き、闘争心、賢さ、反射神経。"],
        ["gold", "チョコボ自身の評価額。画面上の金額はgold×100。レース賞金の一部が蓄積する。"],
        ["father / fblood / mother / mblood", "父名・父方血統値・母名・母方血統値。配合時の親情報として使う。"],
        ["age / love", "画面表示用に残る年齢・なつき度。現行の主要な訓練・レース計算はlifeと能力値を参照する。"],
    ]

    master_rows = [
        ["野生チョコボ購入候補", data_path(wild_path), f"{len(wild_records):,}件", "牧場の購入候補。購入時に現役データへ変換する。"],
    ]
    rival_sections = []
    rival_summary_rows = []
    for race_index, file_name in sorted(c["chocobo_rival_files"].items()):
        relative_path = str(Path(c["chocobo_race_data_dir"]) / file_name).replace("\\", "/")
        records = load_json(relative_path)
        rival_summary_rows.append([
            num(race_index), esc(file_name), f"{len(records):,}件", "通常レースの抽選候補" if race_index <= 6 else ("G1重賞候補" if race_index == 7 else "海外G2候補"),
        ])
        rival_rows = []
        for record in records:
            rival_rows.append([
                num(record.get("no", "")), esc(record.get("name", "")), esc(record.get("breader", "")),
                num(record.get("type", "")), num(record.get("max", "")),
                *[num(record.get(f"c{index}", "")) for index in range(7)],
            ])
        rival_sections.append(
            f'<section id="rival-{race_index}"><h3>{esc(file_name)}（レース番号 {num(race_index)}）</h3>'
            f'<p class="source">ファイル: <code>{esc(relative_path)}</code> / {len(records):,}件</p>'
            f'{table(["No", "名前", "ブリーダー", "成長タイプ", "賞金基準", "速度", "スタミナ", "粘り", "落ち着き", "闘争心", "賢さ", "反射神経"], rival_rows)}</section>'
        )

    wild_rows = []
    for record in wild_records:
        wild_rows.append([
            num(record.get("no", "")), esc(record.get("name", "")), num(record.get("price", "")),
            num(record.get("run", "")), num(record.get("win", "")), num(record.get("blood", "")),
            esc(types.get(record.get("waza"), record.get("waza", ""))), num(record.get("e", "")),
            esc(record.get("father", "")), esc(record.get("mother", "")), esc(record.get("breader", "")),
        ])

    training_rows = [
        ["race0", "バーベルあげ", "瞬発力", "c0", "失敗時にc6が低下"],
        ["race1", "砂浜走り", "持久力", "c1", "失敗時にc5が低下"],
        ["race2", "スイミング", "粘り強さ", "c2", "粘り強さを伸ばす"],
        ["race3", "瞑想", "落ち着き", "c3", "失敗時にc4が低下"],
        ["race4", "猛特訓", "闘争心", "c4", "失敗時にc3が低下"],
        ["race5", "お勉強", "知力", "c5", "失敗時にc1が低下"],
        ["race6", "坂道ダッシュ", "切れ味", "c6", "失敗時にc0が低下"],
    ]
    race_rows = [
        ["race0", "新馬戦", "0勝", "1勝未満", "ribal0"],
        ["race1", "500万以下", "1勝", "5勝未満", "ribal1"],
        ["race2", "900万以下", "5勝", "15勝未満", "ribal2"],
        ["race3", "1600万以下", "15勝", "30勝未満", "ribal3"],
        ["race4", "オープン特別", "30勝", "80勝未満", "ribal4"],
        ["race5", "グレードIII", "50勝", "100勝未満", "ribal5"],
        ["race6", "グレードII", "75勝", "130勝未満", "ribal6"],
        ["race7", "G1重賞", "30勝", "開催枠・性別一致", "ribal7 / choco_g1"],
        ["race8", "海外G2", "30勝", "開催枠・性別一致", "ribal8 / choco_g1"],
        ["race_dendo", "殿堂レジェンドレース", "30勝", "殿堂レースの開催条件", "save_data/denchoco.json"],
    ]
    class_rows = [
        ["0勝", "新馬"], ["1〜4勝", "500万"], ["5〜14勝", "900万"], ["15〜29勝", "1600万"],
        ["30〜49勝", "オープン"], ["50〜74勝", "グレードIV"], ["75〜104勝", "グレードIII"],
        ["105〜139勝", "グレードII"], ["140勝以上", "グレードI"],
    ]

    body = f"""
<div class="note">チョコボ関連の正本は <code>cgi_py/chocofarm.py</code>、<code>cgi_py/morifarm.py</code>、<code>cgi_py/ctrain.py</code>、<code>cgi_py/crace.py</code>、<code>cgi_py/farmrace.py</code>、<code>cgi_py/dendo.py</code>、<code>cgi_py/chocorank.py</code> と Config/data/save_data です。チョコボの能力番号は現行コードの意味に合わせ、c0〜c6はチョコボ専用の能力値として扱います。</div>
<h2>保存先とデータの役割</h2>
{table(["データ", "保存先", "現状", "役割"], storage_rows)}
<h2>現役チョコボのキー</h2>
{table(["キー", "意味"], owned_rows, row_headers=True)}
<h2>牧場での基本処理</h2>
{table(["操作", "処理"], [
    ["購入", "chocobofile.jsonからNoを検証して現役データを作成。初期はメス、life=100、各能力10、train/run/win=0。購入後は名前付けが必要。"],
    ["命名", "名前を保存。禁止ワードと殿堂履歴の重複を確認する。"],
    ["訓練", f"lifeが200以上で実行可能。20ターン、成功率3/4。終了時にlifeを200消費し、訓練回数を1増加。再実行待ちは{num(c['training_cooldown_seconds'])}秒。"],
    ["レース", f"lifeが400以上で実行可能。出走時にlifeを200消費し、出走回数を1増加。再実行待ちは{num(c['pvp_race_cooldown_seconds'])}秒。"],
    ["引退", "評価額をプレイヤーに支払い、性別に応じた引退リストへ登録した後、現役chocoだけを空にする。choco_g1は保持する。"],
    ["お見合い", "オスはchocoboms、メスはchocoboosから候補を抽選。候補が空の場合はchocobofile.jsonへフォールバックせず、相手なしとして扱う。"],
], row_headers=True)}
<h2>訓練メニューと能力</h2>
{table(["mode", "メニュー", "対象", "キー", "失敗時の変動"], training_rows)}
<h2>出走クラスと条件</h2>
{table(["mode", "レース", "勝利数下限", "勝利数上限・追加条件", "参照データ"], race_rows)}
<p class="small">G1は出走回数+訓練回数の40ターン周期、海外G2は60ターン周期で開催枠を判定します。G1/G2勝利時は個人の <code>choco_g1</code>、全体の <code>rireki.json</code>、全体ニュースを更新します。</p>
<h2>勝利数による表示クラス</h2>
{table(["勝利数", "表示クラス"], class_rows)}
<h2>野生チョコボ購入マスター</h2>
<p class="source">ファイル: <code>{esc(wild_path)}</code> / {len(wild_records):,}件。wazaは成長タイプ、eは購入後の画像番号へ変換されます。</p>
{table(["No", "名前", "価格", "出走", "勝利", "血統", "成長タイプ", "画像No", "父", "母", "ブリーダー"], wild_rows)}
<h2>レースライバルマスター</h2>
{table(["レース番号", "ファイル", "件数", "用途"], rival_summary_rows)}
{"".join(rival_sections)}
<h2>チョコボの能力キー</h2>
{table(["キー", "表示名", "レースでの主な役割"], [
    [f"c{index}", label, role] for index, (label, role) in enumerate([
        ("スピード", "序盤・中盤・終盤の移動力"), ("スタミナ", "レース中の消耗に対する余力"),
        ("粘り", "バテた後の粘り、消耗軽減"), ("落ち着き", "積極的な走りや消耗計算"),
        ("闘争心", "ラストスパート判定"), ("賢さ", "走り方と消耗の選択"), ("反射神経", "終盤の加速力"),
    ])
])}
<h2>関連設定</h2>
{table(["設定", "現行値", "意味"], [
    ["choco_images", "番号辞書", "チョコボのnoと画像ファイルを対応付ける。"],
    ["chocobo_types", "番号辞書", "typeと成長タイプ名を対応付ける。"],
    ["chocobo_partner_list_limit", num(c["chocobo_partner_list_limit"]), "引退お見合い候補の最大保持件数。満杯時は既存枠を置換し、無制限には増えない。"],
    ["chocobo_farm_background / chocobo_race_background", "設定値", "牧場画面・レース画面の背景画像。"],
    ["chocobo_race_announcer_image", "設定値", "レース実況欄のアナウンサー画像。キャラクター画像一覧とは別管理。"],
], row_headers=True)}
<h2>関連ソース</h2>
<p class="source"><code>cgi_py/chocofarm.py</code> / <code>cgi_py/morifarm.py</code> / <code>cgi_py/ctrain.py</code> / <code>cgi_py/crace.py</code> / <code>cgi_py/farmrace.py</code> / <code>cgi_py/dendo.py</code> / <code>cgi_py/chocorank.py</code> / <code>sub_def/common.py</code> / <code>data/chocobo/*.json</code></p>
"""
    return page("チョコボ牧場・レース仕様書", "チョコボの保存キー、購入・訓練・レース・配合・引退・殿堂入りと関連マスターを確認する管理資料", body)


def migration_specs() -> str:
    body = f"""
<div class="note">移行スクリプトはゲーム本体の通常処理ではありません。変換元を直接変更せず、別の出力先で検証してから現行 <code>save_data</code> へ配置してください。旧版の配列は列番号自体が仕様なので、キー名を推測して並べ替えないことが重要です。</div>
<h2>変換経路</h2>
{table(["段階", "スクリプト", "入力", "出力"], [
    ["Ver1 → Ver2", "旧版_ver1/セーブデータ移行用ファイル/convert_to_ver2.py", "旧版_ver1のcharalog、charalog2、banklog、datalog、savelog", "Ver2形式のcharalog、item、syoku、souko、datalog、保管用savelog"],
    ["Ver2 → Ver3", "旧版_ver2/change_data/convert_all.py", "旧版_ver2のcharalog、item、syoku、souko、各ログ、datalog", "ユーザー別user_all.json、message_sent.json、champion.json、all_message.json"],
], row_headers=True)}
<h2>Ver1 → Ver2 の対応</h2>
{table(["旧版データ", "Ver2での扱い", "注意点"], [
    ["charalog/&lt;ID&gt;.cgi", "charalog/&lt;ID&gt;.cgi、item/&lt;ID&gt;.cgi、syoku/&lt;ID&gt;.cgiへ分割出力", "キャラクター列は67項目。能力値は旧版の実列順をそのまま維持する。"],
    ["charalog2/&lt;ID&gt;.cgi", "souko/item、souko/def、souko/acsへ変換", "各行の先頭は枠数で、2項目目以降の装備IDを倉庫レコードへ変換する。"],
    ["banklog/&lt;ID&gt;.cgi", "Ver2キャラデータの銀行残高欄へ埋め込み", "独立banklogはVer2では使わない。"],
    ["datalog/winner.cgi", "54項目のVer2チャンプ形式へ変換", "recode.cgiの最高連勝情報も該当欄へ反映する。"],
    ["datalog/recode.cgi", "変換後datalog/recode.cgiへ保存", "チャンプ変換時にも参照する。"],
    ["savelog/&lt;ID&gt;.cgi", "出力先savelogへ保管", "Ver2の通常ゲーム処理では読み込まない復元用スナップショット。"],
], row_headers=True)}
<h2>Ver2 → Ver3 の対応</h2>
{table(["旧版Ver2", "現行Ver3", "内容"], [
    ["charalog/&lt;ID&gt;.cgi", "save_data/&lt;ID&gt;/user_all.json の chara", "旧版列番号から現行キーへ明示的に変換。str,int,mnd,vit,dex,agi,cha,karmaを正しい順で保持する。"],
    ["item/&lt;ID&gt;.cgi", "user_all.json の equipment", "武器、防具、アクセサリーを現行マスターから再構成する。"],
    ["syoku/&lt;ID&gt;.cgi", "user_all.json の syoku", "職業IDごとの熟練度を辞書化する。"],
    ["souko/item・def・acs/&lt;ID&gt;.cgi", "souko_weapon・souko_armor・souko_accessory", "現行マスターの項目名・性能・アクセサリー説明を使って正規化する。"],
    ["loginlog・message・sousin", "login_log・message・message_sent.json", "送信済みメッセージだけはユーザー別の別ファイルへ出力する。"],
    ["datalog/winner.cgi", "save_data/champion.json", "人間チャンプの共有データとして変換する。出力先は--champion-outputで指定可能。"],
    ["datalog/message.cgi", "save_data/all_message.json", "全体ニュースとして変換する。"],
    ["チョコボ関連", "choco={}、choco_g1={}", "Ver2変換では現役チョコボを自動生成せず、未所持で初期化する。"],
], row_headers=True)}
<h2>現行ユーザーデータの構造</h2>
{table(["キー", "役割"], [
    ["chara", "キャラクター本体。現行の正規キー順に並べ替える。"],
    ["equipment", "現在装備中の武器・防具・アクセサリー。"],
    ["syoku", "職業IDをキーにした熟練度辞書。"],
    ["login_log / message", "ログイン履歴 / 受信メッセージ。"],
    ["message_sent.json", "送信済みメッセージ。現行ではuser_all.jsonの外に保存する。"],
    ["souko_weapon / souko_armor / souko_accessory", "倉庫内の装備一覧。"],
    ["choco / choco_g1", "飼育中チョコボ / 個人重賞履歴。未所持時は空辞書。"],
], row_headers=True)}
<h2>現行形式への正規化</h2>
{table(["処理", "内容"], [
    ["キー順整理", "sub_def/data_schema.pyのorder_user_data()が値を変更せず、chara・equipment・bonusなどを定義順に並べる。"],
    ["旧キー除去", "title→title_id、unused30→tactic_idを移行し、旧site/url、旧アクセサリーキーlck/lp/attrib/spare*を出力しない。"],
    ["HTMLエンティティ", "読み込み時にHTMLエンティティを復元する。名前などを二重エスケープしない。"],
    ["アクセサリー", "8能力値をstr,int,mnd,vit,dex,agi,cha,karma、率をhit_rate,evasion_rate,special_rateへ統一する。"],
    ["検証", "変換後に必須キー、装備形式、職業ID、倉庫件数、旧キー残存を検証し、問題があればエラーまたは警告にする。"],
], row_headers=True)}
<h2>実行例と安全な手順</h2>
<p class="formula">python 旧版_ver1/セーブデータ移行用ファイル/convert_to_ver2.py --dry-run
python 旧版_ver2/change_data/convert_all.py --dry-run
python 旧版_ver2/change_data/convert_all.py --output &lt;検証用出力&gt; --shared-output &lt;共有データ出力&gt;</p>
{table(["手順", "実施内容"], [
    ["1", "旧版ディレクトリを読み取り専用の原本として残す。"],
    ["2", "まず--dry-runで件数、警告、マスター不一致、文字化け候補を確認する。"],
    ["3", "本出力ではなく検証用ディレクトリへ書き出し、JSON構文と現行キーを確認する。"],
    ["4", "必要なら--champion-outputでchampion.jsonだけ現行save_dataへ出力する。"],
    ["5", "既存データを上書きする場合は、別途ファイルコピーを取得してから実行する。変換スクリプト自体はバックアップを作成しない。"],
], row_headers=True)}
<h2>関連ファイル</h2>
<p class="source"><code>旧版_ver1/セーブデータ移行用ファイル/README_ver1_to_ver2.md</code> / <code>旧版_ver1/セーブデータ移行用ファイル/convert_to_ver2.py</code> / <code>旧版_ver2/change_data/convert_all.py</code> / <code>sub_def/data_schema.py</code> / <code>sub_def/file_ops.py</code></p>
"""
    return page("セーブデータ移行・保存形式仕様書", "Ver1からVer2、Ver2から現行Ver3への変換経路、キー対応、検証、運用上の注意を確認する管理資料", body)


def operations_specs() -> str:
    c = config.Config
    body = f"""
<div class="note">この資料は現行コードの管理画面と保存処理を基準にしています。通常データはログインを契機に1日1回バックアップされ、最大{num(c['backup_retention_days'])}日分を保持します。保護ユーザー用の固定バックアップ自動作成は別途未実装です。</div>
<h2>管理画面の機能</h2>
{table(["機能", "操作", "保存・削除対象", "備考"], [
    ["登録者一覧", "kanri_all", "save_data/&lt;ID&gt;を一覧表示", "最終行動日時、ホスト、所持金などを確認する。"],
    ["キャラクター編集", "data / save", "user_all.jsonのchara", "名前、レベル、能力、職業、所持金、HP、コメントなどを直接変更する。"],
    ["個別削除", "del_chara", "対象ユーザーのディレクトリ全体", "protected_user_idsのユーザーは削除不可。削除前バックアップは作成しない。"],
    ["放置キャラ一括削除", "del_noplay", "最終行動から一定日数を超えたユーザー", f"{num(c['character_delete_after_days'])}日を基準に管理者が手動実行。自動スケジューラではない。"],
    ["保護ユーザー復元", "restore_protected", "protected_users/&lt;ID&gt;/user_all.json → save_data/&lt;ID&gt;/user_all.json", "復元元が存在し、chara.idが一致する場合だけ復元する。"],
    ["日次バックアップ復元", "backup_restore", "backups/YYYY-MM-DD → save_data", "メンテナンスモード中のみ実行。復元前の現行データはpre_restore_日時へ退避する。"],
    ["全体ニュース投稿", "post_all_message", "save_data/all_message.json", f"管理人名義で投稿し、最大{num(c['all_message_storage_limit'])}件に切り詰める。"],
    ["マスター管理", "master_list / master_save / master_delete", "data/syoku.json等", "職業、戦術、武器、防具、装飾品を検証付きで編集する。"],
    ["倉庫追加", "player_item_add", "対象ユーザーのsouko_*", "現行マスターから装備を作り、倉庫上限を検証する。"],
], row_headers=True)}
<h2>自動削除の実態</h2>
{table(["項目", "現行仕様"], [
    ["判定基準", f"chara.last_timeから{num(c['character_delete_after_days'])}日×24時間×60分×60秒を超えたユーザー。"],
    ["実行契機", "admin.pyの放置キャラ一括削除フォームを管理者がPOST送信したときだけ。cron、タスクスケジューラ、ログイン時の自動実行は確認できない。"],
    ["テストユーザー", "protected_user_idsに含まれるIDは削除対象から除外し、件数も別表示する。"],
    ["削除方法", "対象ユーザーディレクトリをshutil.rmtreeで削除する。個別削除・一括削除とも削除前の自動退避はない。"],
], row_headers=True)}
<h2>バックアップ機能の確認結果</h2>
{table(["対象", "実装状況", "確認内容"], [
    ["通常セーブの定期バックアップ", "実装済み", f"ログイン処理からensure_daily_backup()を呼び、backups/YYYY-MM-DDへ{num(c['backup_retention_days'])}日分を保持する。同日中は二重作成しない。"],
    ["保護ユーザーの自動バックアップ", "未実装", "protected_user_backup_dirの設定と復元処理はあるが、そこへuser_all.jsonをコピーする作成処理はない。"],
    ["保護ユーザーの復元", "実装済み", "admin.pyのrestore_protected。復元元が事前に手動配置されている場合だけ機能する。"],
    ["アトミック保存", "実装済み", "一時JSONへ書き込み、flush/fsync後にos.replaceする。バックアップ作成・復元とbackup_snapshotロックで直列化する。"],
    ["Git履歴", "運用バックアップではない", "過去コミットに保存データが含まれると漏えい・復元リスクになるため、.gitignoreと履歴管理を別途確認する。"],
], row_headers=True)}
<h2>日次バックアップと復元手順</h2>
{table(["手順", "内容"], [
    ["1", "最初のユーザーログイン時にsave_data全体をbackups/YYYY-MM-DDへコピーする。cronや常駐プロセスは使用しない。"],
    ["2", f"{num(c['backup_retention_days'])}日を超えた日付フォルダを自動削除する。"],
    ["3", "管理画面で復元対象日を選び、config.pyのmaintenance_modeを1にしてから復元する。"],
    ["4", "復元前の状態はbackups/pre_restore_YYYYMMDD_HHMMSSへ退避される。"],
    ["5", "保護ユーザー復元を使う場合は、save_data/protected_users/&lt;ID&gt;/user_all.jsonとしてchara.idが一致するファイルを別途手動配置する。"],
    ["6", "バックアップにはパスワードハッシュや個人データが含まれるため、Web公開ディレクトリ外・アクセス制限下で保管する。"],
], row_headers=True)}
<h2>関連設定・ソース</h2>
<p class="source"><code>config.py</code> の character_delete_after_days / protected_user_ids / protected_user_backup_dir / save_dir / backup_dir / backup_retention_days、<code>sub_def/backup.py</code>、<code>admin.py</code>、<code>sub_def/file_ops.py</code></p>
"""
    return page("管理画面・自動削除・バックアップ運用手順書", "管理画面の操作、放置キャラクター削除、テストユーザー保護、現行バックアップ機能の有無と手動運用を確認する資料", body)


def security_specs() -> str:
    c = config.Config
    body = f"""
<div class="note">この資料は現行実装の防御境界を整理したものです。フォームのhidden値、URLパラメータ、Cookieはクライアント側で変更できるため、重要な状態変更はサーバー側で本人確認・CSRF検証・入力検証・排他制御を行う必要があります。</div>
<h2>認証とセッション</h2>
{table(["対象", "実装", "確認ポイント"], [
    ["パスワード保存", "PBKDF2-HMAC-SHA256、ユーザーごとのランダムソルト、100,000回反復", "新形式はpbkdf2$salt$hash。旧固定ソルト・旧平文も検証でき、ログイン成功時に新形式へ再ハッシュする。"],
    ["ログインセッション", "FFAPY_SESSION Cookieに暗号化データを保存", "HMAC-SHA256で改ざん検知し、作成時刻からセッション有効期限を確認する。現行設定は30分。"],
    ["セッション内容", "user_id、password_hash、csrf_token、created_at", "認証時はCookieのIDと保存データのパスワードハッシュを照合する。"],
    ["旧互換Cookie", f"{c['cookie_name']}", "旧形式Cookie入力は暗号化セッションへ変換する互換処理がある。新規処理では旧Cookieを増やさない。"],
    ["ログアウト", "セッションCookieを有効期限切れにする", "destroy_session()がFFAPY_SESSIONを削除する。"],
], row_headers=True)}
<h2>CSRF対策</h2>
{table(["段階", "処理"], [
    ["発行", "token_generate(session)がセッションにランダムトークンを作り、テンプレートへcsrf_tokenとして渡す。"],
    ["送信", "状態変更フォームはhidden name=sでトークンを送信する。"],
    ["検証", "token_check()がフォーム値とセッション値の両方の存在を確認し、hmac.compare_digestで比較する。"],
    ["適用範囲", "ログイン、キャラ作成確定、ゲーム内の主要POST、管理者の保存・削除・ニュース投稿・復元などに適用する。GETの閲覧処理は対象外。"],
    ["失敗時", "不足または不一致ならエラー画面で処理を中断する。"],
], row_headers=True)}
<h2>本人確認・権限</h2>
{table(["境界", "実装"], [
    ["本人操作", "状態変更系のチョコボ、装備購入、倉庫、戦闘などはrequire_owner(user_id)でCookieのuser_idと対象ID、保存済みパスワードハッシュを照合する。"],
    ["ID改ざん対策", "URLやhiddenのidを信用せず、本人セッションとの一致をサーバー側で検証する。"],
    ["管理者", "admin.pyは最初のPOSTで管理者パスワードとCSRFを確認し、以後は暗号化セッションで認証する。"],
    ["入力値", "ID、パスワード、チョコボ名、数値、職業、装備ID、JSONマスターなどを各処理で検証する。"],
    ["表示値", "テンプレートの自動エスケープに加え、装飾HTMLで出す戦闘・レース実況へ保存値を差し込む前にescapeする。"],
], row_headers=True)}
<h2>排他制御と保存</h2>
{table(["対象", "ロック名・方式", "目的"], [
    ["ユーザーデータ", "ユーザーID.lock / os.mkdirベースのディレクトリロック", "同一キャラクターの所持金、装備、戦闘結果、チョコボなどの同時更新を直列化する。"],
    ["新規登録", "character_creation.lock", "確認画面を複数タブから送信した場合も、ID・名前・ホストの再確認と登録を一つの区間で行う。"],
    ["共有データ", "winner、all_message_post、bbs_post、tenka_*、rirekiなど", "チャンプ、ニュース、掲示板、履歴の取りこぼし・上書きを防ぐ。"],
    ["バックアップ", "backup_snapshot / backup_restore", "日次コピー・復元中の保存処理を待たせ、復元操作を一つに直列化する。"],
    ["タイムアウト", "common.get_lockは10秒、file_opsのexLockは15秒が既定", "取得できない場合はTimeoutError。finallyでrelease_lock/unlockする。"],
    ["アトミック保存", "同じディレクトリの一時JSONへ書き、flush/fsync後にos.replace", "書き込み途中のJSONを本体として見せない。"],
], row_headers=True)}
<h2>重要な運用上の注意</h2>
{table(["項目", "現状・対策"], [
    ["秘密鍵の既定値", "FFA_SECRET_KEY未設定時はconfig.pyの既定値を使う。本番では必ず環境変数を設定し、変更時は既存セッションを無効化する運用にする。"],
    ["管理者パスワードの既定値", "FFA_ADMIN_PASSWORD未設定時は既定値を使う。本番では必ず環境変数を設定する。"],
    ["Cookie Secure属性", "現在はHttpOnlyとPathを設定しているが、Secure属性はコメントアウトされている。HTTPS運用時は有効化を検討する。"],
    ["管理者認証情報の受け渡し", "管理者パスワードは最初のPOSTでだけ受け取り、画面遷移・hidden値・URLへは含めない。以後は暗号化セッションで認証する。"],
    ["ファイル公開範囲", "save_data、lock、backups、templates、tools、旧版フォルダには.htaccessを置き、HTTPで取得できないようにする。ApacheでAllowOverrideが無効な場合は同等の設定をVirtualHost側へ追加する。"],
    ["CSRFトークンの扱い", "hidden値は改ざん可能だが、セッション側との一致をサーバーで検証するためhidden値単独を認証情報として扱わない。"],
], row_headers=True)}
<h2>関連ソース</h2>
<p class="source"><code>sub_def/crypto.py</code> / <code>sub_def/common.py</code> / <code>sub_def/exLock.py</code> / <code>sub_def/file_ops.py</code> / <code>sub_def/validation.py</code> / <code>login.py</code> / <code>chara_make.py</code> / <code>admin.py</code></p>
"""
    return page("認証・CSRF・排他ロック・権限チェック セキュリティ仕様書", "現行システムの認証、セッション、CSRF、本人確認、入力検証、排他保存と運用上の注意を確認する資料", body)


def index() -> str:
    cards = [
        ("equipment_catalog.html", "装備マスター 職業別カタログ", "武器・防具・アクセサリーの性能、価格、説明、購入可能職業"),
        ("job_catalog.html", "職業マスター 職業別カタログ", "職業名、転職条件、能力上限、熟練度条件、関連装備・戦術"),
        ("monster_catalog.html", "モンスター・ボスマスター一覧", "通常戦闘、異世界、レジェンドの全モンスターと各キーの意味"),
        ("status_reference.html", "保存キー・能力値リファレンス", "キャラクター・装備・戦闘結果に使うキーの役割"),
        ("battle_specs.html", "FFA 戦闘仕様書", "戦闘入口、出現条件、ターン順、結果分岐、報酬、進行状態"),
        ("skill_specs.html", "FFA 必殺技・特殊効果仕様書", "戦術、モンスター特殊技、装飾品固有効果の発動率と実装対応"),
        ("chocobo_specs.html", "チョコボ牧場・レース仕様書", "チョコボの保存キー、訓練、レース、配合、引退、殿堂入り"),
        ("migration_specs.html", "セーブデータ移行・保存形式仕様書", "Ver1→Ver2→Ver3の変換、キー対応、検証、出力形式"),
        ("operations_specs.html", "管理画面・運用手順書", "管理画面、放置削除、保護ユーザー、バックアップ実装状況"),
        ("security_specs.html", "セキュリティ仕様書", "認証、CSRF、本人確認、排他ロック、アトミック保存"),
        ("command_flowcharts.html", "FFA コマンドフローチャート", "login.pyから各コマンド、保存、画面出力までの呼び出し経路"),
    ]
    cards_html = "".join(f'<article class="card"><h3><a href="{href}">{esc(title)}</a></h3><p>{esc(description)}</p></article>' for href, title, description in cards)
    body = f"""
<div class="note">管理者・開発者向けの現行Ver3仕様資料です。データやコードを変更した場合は、生成スクリプトを実行して資料を更新してください。</div>
<div class="grid">{cards_html}</div>
<h2>生成方法</h2>
<p class="formula">python tools/generate_admin_docs.py
python tools/generate_equipment_catalog.py</p>
<p class="source">装備カタログは <code>tools/generate_equipment_catalog.py</code>、その他の資料は <code>tools/generate_admin_docs.py</code> から生成します。コマンドフローチャートは現行ソースをもとにした手動管理資料です。</p>
"""
    return page("FFA 管理者向けドキュメント", "現行Ver3のマスターデータ、保存キー、戦闘処理、コマンド経路を確認する資料一覧", body)


def write(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "index.html": index(),
        "job_catalog.html": job_catalog(),
        "monster_catalog.html": monster_catalog(),
        "status_reference.html": status_reference(),
        "battle_specs.html": battle_specs(),
        "skill_specs.html": skill_specs(),
        "chocobo_specs.html": chocobo_specs(),
        "migration_specs.html": migration_specs(),
        "operations_specs.html": operations_specs(),
        "security_specs.html": security_specs(),
    }
    for name, content in outputs.items():
        (output_dir / name).write_text(content, encoding="utf-8")
        print(f"管理者資料を生成しました: {output_dir / name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="FFA管理者向けドキュメントを生成します。")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "docs", help="出力先ディレクトリ")
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    write(output_dir)


if __name__ == "__main__":
    main()
