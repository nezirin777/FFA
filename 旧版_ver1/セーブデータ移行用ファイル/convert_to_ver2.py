#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FFA Emiliar Ver1のセーブデータをVer2形式へ変換するスクリプト。

旧版の移行用CGIはキャラ・装備・職業・倉庫の一部だけを変換する構成
でした。このスクリプトでは、Ver1のデータを一度の実行でまとめて変換
します。

  charalog                 -> Ver2 charalog + 銀行残高
  charalog2                -> Ver2 souko/{item,def,acs}
  banklog                  -> charalog[34]
  datalog/winner.cgi       -> Ver2 datalog/winner.cgi
  datalog/recode.cgi       -> Ver2 datalog/recode.cgi + 王者データ
  savelog                  -> 出力先savelog（保管用）

入出力の生データは、旧版CGIが使用するShift-JIS/CP932で扱います。
変換元を上書きしないよう、初期状態では別の出力先へ保存します。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable


CP932 = "cp932"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = SCRIPT_DIR.parent
DEFAULT_OUTPUT = DEFAULT_SOURCE / "converted_ver2"

CHARA_FIELD_COUNT = 67
SYOKU_MASTER_COUNT = 31
WINNER_FIELD_COUNT = 54

DEFAULT_WEAPON = "\u7d20\u624b"      # 素手
DEFAULT_ARMOR = "\u666e\u6bb5\u7740"  # 普段着
DEFAULT_ACCESSORY = "\u306a\u3057"   # なし


class Converter:
    def __init__(self, source: Path, output: Path, dry_run: bool, overwrite: bool):
        self.source = source
        self.output = output
        self.dry_run = dry_run
        self.overwrite = overwrite
        self.warnings: list[str] = []
        self.stats = {
            "characters": 0,
            "savelogs": 0,
            "warehouses": 0,
            "winner": 0,
            "recode": 0,
            "warnings": 0,
        }
        self.weapons: dict[str, list[str]] = {}
        self.armors: dict[str, list[str]] = {}
        self.accessories: dict[str, list[str]] = {}
        self.banks: dict[str, str] = {}

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    @staticmethod
    def normalize_id(value: str) -> str:
        value = value.strip()
        if not value:
            return ""
        try:
            return f"{int(value):04d}"
        except ValueError:
            return value

    @staticmethod
    def legacy_truthy(value: str) -> bool:
        # Perlの条件判定に合わせ、空文字と文字列"0"は未習得として扱う。
        return value.strip() not in ("", "0")

    @staticmethod
    def decode_text(value: str) -> str:
        # 旧版CGIは値をHTMLとして出力するため、HTMLエンティティはそのまま
        # 残す。ここでデコードするとCP932にない文字へ変わり、名前が"?"
        # に置き換わる場合がある。
        return value

    @classmethod
    def read_first_line(cls, path: Path) -> str:
        raw = path.read_bytes().splitlines()
        if not raw:
            return ""
        return raw[0].decode(CP932, errors="replace").rstrip("\r\n")

    @classmethod
    def split_record(cls, line: str) -> list[str]:
        fields = line.rstrip("\r\n").split("<>")
        if fields and fields[-1] == "":
            fields.pop()
        return [cls.decode_text(field) for field in fields]

    @staticmethod
    def pad(fields: list[str], count: int) -> list[str]:
        return fields + [""] * max(0, count - len(fields))

    @staticmethod
    def record_text(fields: Iterable[object]) -> str:
        return "<>".join(str(field) for field in fields) + "<>\n"

    def write_text(self, path: Path, text: str, encoding: str = CP932) -> None:
        if self.dry_run:
            return
        if path.exists() and not self.overwrite:
            raise FileExistsError(
                f"出力ファイルが既に存在します: {path}（上書きする場合は--overwriteを指定してください）"
            )
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding=encoding, errors="replace", newline="") as handle:
            handle.write(text)

    def write_record(self, path: Path, fields: Iterable[object]) -> None:
        self.write_text(path, self.record_text(fields))

    def list_records(self, directory: Path) -> list[Path]:
        if not directory.exists():
            self.warn(f"ディレクトリがありません: {directory}")
            return []
        return sorted(
            path
            for path in directory.iterdir()
            if path.is_file() and path.suffix.lower() == ".cgi"
        )

    def load_master(self, path: Path) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        if not path.exists():
            self.warn(f"マスターファイルがありません: {path}")
            return result
        for line_number, raw in enumerate(path.read_bytes().splitlines(), start=1):
            line = raw.decode(CP932, errors="replace")
            fields = self.split_record(line)
            if not fields or not fields[0]:
                continue
            key = self.normalize_id(fields[0])
            if key in result:
                self.warn(f"マスターデータのIDが重複しています {key}: {path}:{line_number}")
            result[key] = fields[1:]
        return result

    def load_masters(self) -> None:
        # 装備のIDだけを保存するVer1データから、Ver2が必要とする
        # 装備名・性能・効果値を各マスターファイルで復元する。
        data = self.source / "data"
        self.weapons = self.load_master(data / "item" / "item.ini")
        self.armors = self.load_master(data / "def" / "def.ini")
        self.accessories = self.load_master(data / "acs" / "acs.ini")

    def load_banks(self) -> None:
        # Ver2ではbanklogを別管理しないため、後でキャラデータ34番目へ
        # 埋め込めるよう、先にIDごとの残高を読み込んでおく。
        for path in self.list_records(self.source / "banklog"):
            fields = self.pad(self.split_record(self.read_first_line(path)), 3)
            account_id = fields[0] or path.stem
            bank = fields[2] or "0"
            self.banks[account_id] = bank

    def lookup(self, table: dict[str, list[str]], item_id: str, kind: str) -> list[str] | None:
        key = self.normalize_id(item_id)
        if not key:
            return None
        row = table.get(key)
        if row is None:
            self.warn(f"{kind}のID {item_id!r}がマスターにありません。未装備として変換します")
        return row

    def weapon_item(self, item_id: str) -> list[str]:
        row = self.lookup(self.weapons, item_id, "武器")
        if row is None:
            return [DEFAULT_WEAPON, "0", "0"]
        row = self.pad(row, 4)
        return [row[0], row[1], row[3]]

    def armor_item(self, item_id: str) -> list[str]:
        row = self.lookup(self.armors, item_id, "防具")
        if row is None:
            return [DEFAULT_ARMOR, "0", "0"]
        row = self.pad(row, 4)
        return [row[0], row[1], row[3]]

    def accessory_item(self, item_id: str) -> list[str]:
        row = self.lookup(self.accessories, item_id, "アクセサリー")
        if row is None:
            return [DEFAULT_ACCESSORY, "0"] + ["0"] * 11 + ["-"]
        row = self.pad(row, 15)
        # アクセサリーマスターは「名前、価格、効果ID、能力値補正、命中率、
        # 必殺率、回避率、説明文」の順。itemファイルには価格を保存しない。
        return [row[0], row[2]] + row[3:15]

    def equipment_file(self, chara: list[str]) -> list[str]:
        # キャラデータには装備IDしかないため、Ver2のitemファイル用に
        # 武器3項目、防具3項目、アクセサリー14項目へ展開する。
        chara = self.pad(chara, 36)
        return (
            self.weapon_item(chara[24])
            + self.armor_item(chara[29])
            + self.accessory_item(chara[31])
        )

    def warehouse_record(self, kind: str, item_id: str) -> list[str]:
        # 倉庫は装備IDだけでなく、売却価格や性能も1行に保持する。
        key = self.normalize_id(item_id)
        if kind == "item":
            row = self.lookup(self.weapons, item_id, "倉庫の武器")
            if row is None:
                return ["0", DEFAULT_WEAPON, "0", "0", "0"]
            row = self.pad(row, 4)
            return [key, row[0], row[1], row[2], row[3]]
        if kind == "def":
            row = self.lookup(self.armors, item_id, "倉庫の防具")
            if row is None:
                return ["0", DEFAULT_ARMOR, "0", "0", "0"]
            row = self.pad(row, 4)
            return [key, row[0], row[1], row[2], row[3]]
        row = self.lookup(self.accessories, item_id, "倉庫のアクセサリー")
        if row is None:
            return ["0", DEFAULT_ACCESSORY, "0", "0"] + ["0"] * 11 + ["-"]
        row = self.pad(row, 15)
        return [key, row[0], row[1], row[2]] + row[3:15]

    def normalized_chara(self, fields: list[str], account_id: str) -> list[str]:
        # Ver1の職業熟練度など後半項目はVer2では別ファイル管理となる。
        # その領域を空欄に戻し、34番目だけ銀行残高として設定する。
        fields = self.pad(fields, 34)
        if fields[0] and fields[0] != account_id:
            self.warn(
                f"キャラファイル名と内部IDが一致しません: {account_id!r} と {fields[0]!r}"
            )
        output = fields[:34]
        output.append(self.banks.get(account_id, "0"))
        output.extend([""] * (CHARA_FIELD_COUNT - len(output)))
        return output[:CHARA_FIELD_COUNT]

    def syoku_record(self, fields: list[str]) -> list[str]:
        # Ver1の熟練度は値の有無だけを持つため、移行時は習得済みを60へ
        # 揃え、未習得を0としてVer2のsyokuファイルを作成する。
        fields = self.pad(fields, 34 + SYOKU_MASTER_COUNT)
        return [
            "60" if self.legacy_truthy(fields[34 + index]) else "0"
            for index in range(SYOKU_MASTER_COUNT)
        ]

    def convert_characters(self) -> None:
        # キャラ本体・現在の装備・職業熟練度をID単位で同時に変換する。
        for path in self.list_records(self.source / "charalog"):
            account_id = path.stem
            old_fields = self.split_record(self.read_first_line(path))
            chara = self.normalized_chara(old_fields, account_id)
            self.write_record(self.output / "charalog" / path.name, chara)
            self.write_record(self.output / "item" / path.name, self.equipment_file(old_fields))
            self.write_record(self.output / "syoku" / path.name, self.syoku_record(old_fields))
            self.stats["characters"] += 1

    def convert_warehouses(self) -> None:
        # charalog2の各行は、先頭が枠数で、その後ろに装備IDが並ぶCSV。
        # 先頭値を除外してVer2の倉庫レコードへ変換する。
        for path in self.list_records(self.source / "charalog2"):
            lines = path.read_text(encoding=CP932, errors="replace").splitlines()
            kinds = ("item", "def", "acs")
            for index, kind in enumerate(kinds):
                source_line = lines[index] if index < len(lines) else ""
                records = []
                fields = source_line.split(",") if source_line else []
                for item_id in fields[1:]:
                    item_id = item_id.strip()
                    if item_id and item_id != "0000":
                        records.append(self.warehouse_record(kind, item_id))
                destination = self.output / "souko" / kind / path.name
                if self.dry_run:
                    continue
                if destination.exists() and not self.overwrite:
                    raise FileExistsError(
                        f"出力ファイルが既に存在します: {destination}（上書きする場合は--overwriteを指定してください）"
                    )
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("w", encoding=CP932, errors="replace", newline="") as handle:
                    for record in records:
                        handle.write(self.record_text(record))
            self.stats["warehouses"] += 1

    def convert_savelogs(self) -> None:
        # Ver2にはsave_data/load_gameがないため、実行データには使わないが
        # 旧版の復元用スナップショットを保管用として残す。
        for path in self.list_records(self.source / "savelog"):
            account_id = path.stem
            old_fields = self.split_record(self.read_first_line(path))
            self.write_record(
                self.output / "savelog" / path.name,
                self.normalized_chara(old_fields, account_id),
            )
            self.stats["savelogs"] += 1

    def recode_fields(self) -> list[str]:
        path = self.source / "datalog" / "recode.cgi"
        if not path.exists():
            self.warn(f"最高連勝記録ファイルがありません: {path}")
            return ["0", "", "", ""]
        fields = self.pad(self.split_record(self.read_first_line(path)), 4)
        return fields[:4]

    def convert_winner(self) -> None:
        source = self.source / "datalog" / "winner.cgi"
        if not source.exists():
            self.warn(f"チャンプデータがありません: {source}")
            return
        old = self.pad(self.split_record(self.read_first_line(source)), 71)
        recode = self.recode_fields()
        weapon = self.weapon_item(old[24])
        armor = self.armor_item(old[33])
        accessory = self.accessory_item(old[35])

        # Ver2のwinner.cgiはキャラデータそのものではなく、戦闘用の54項目
        # スナップショット。能力値の順序を暗黙の添字計算に任せないよう、
        # ここで旧項目から新項目への対応を明示する。
        winner = [""] * WINNER_FIELD_COUNT
        winner[0] = old[0]
        winner[1] = old[2]
        winner[2] = old[3]
        winner[3] = old[4]
        winner[4] = old[5]
        winner[5] = old[6]
        winner[6:13] = old[7:14]
        winner[13] = old[20]
        winner[14] = old[14]
        winner[15] = old[15]
        winner[16] = old[16]
        winner[17] = old[18]
        winner[18] = old[21]
        winner[19] = old[22]
        winner[20] = old[23]
        winner[21:24] = weapon
        winner[24:27] = armor
        winner[27] = accessory[0]
        winner[28:34] = accessory[2:8]
        winner[34] = accessory[9]
        winner[35] = accessory[11]
        winner[36] = accessory[12]
        winner[37] = old[34]  # 武器側の奥義・特殊技ID
        winner[38] = old[26]
        winner[39] = old[37]
        winner[40] = ""       # Ver1のチャンプ記録には挑戦者IDがない
        winner[41] = old[31]
        winner[42] = old[29]
        winner[43] = old[30]
        winner[44] = old[28]
        winner[45] = recode[0]
        winner[46] = recode[2]
        winner[47] = recode[3]
        winner[48] = recode[3]  # recode.cgiにはサイト/URL相当の値が1つだけある
        winner[49] = recode[1]
        winner[50] = old[19]
        winner[51] = accessory[1]
        winner[52] = accessory[10]
        winner[53] = accessory[8]  # 魅力補正はVer2でも別項目として保持する

        self.write_record(self.output / "datalog" / "winner.cgi", winner)
        self.stats["winner"] = 1

        recode_path = self.source / "datalog" / "recode.cgi"
        if recode_path.exists():
            self.write_record(self.output / "datalog" / "recode.cgi", recode)
            self.stats["recode"] = 1

    def write_readme(self) -> None:
        text = """# Ver1からVer2への変換結果

このディレクトリには、FFA Emiliar Ver2用に変換した生データが入ります。

- `banklog`は`charalog`の34番目へ埋め込んでいます。Ver2には独立した
  banklogはありません。
- `savelog`は保管用として残しています。Ver2では旧版の`save_data`と
  `load_game`が廃止されているため、通常のゲーム処理では読み込みません。
- `datalog/winner.cgi`はVer2の54項目形式へ変換しています。
- `datalog/recode.cgi`は保存し、最高連勝記録をチャンプデータにも反映しています。

変換した生データは、旧版CGIに合わせてShift-JIS/CP932で保存しています。
"""
        self.write_text(self.output / "README.md", text, encoding="utf-8")

    def run(self) -> int:
        if not self.source.exists():
            raise FileNotFoundError(f"変換元ディレクトリが存在しません: {self.source}")
        if self.output.resolve() == self.source.resolve():
            raise ValueError("変換元と同じディレクトリへは出力できません")
        if self.output.exists() and not self.dry_run and not self.overwrite:
            raise FileExistsError(
                f"出力先ディレクトリが既に存在します: {self.output}（上書きする場合は--overwriteを指定してください）"
            )

        self.load_masters()
        self.load_banks()
        self.convert_characters()
        self.convert_warehouses()
        self.convert_savelogs()
        self.convert_winner()
        self.write_readme()
        self.stats["warnings"] = len(self.warnings)
        return 0

    def summary(self) -> dict[str, object]:
        return {
            "source": str(self.source),
            "output": str(self.output),
            "dry_run": self.dry_run,
            **self.stats,
            "warning_messages": self.warnings,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="FFA Emiliar Ver1の生データをVer2形式へ変換します。"
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Ver1のルートディレクトリ（初期値: スクリプトの親ディレクトリ）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="変換結果の出力先（初期値: converted_ver2）",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="出力先に同名ファイルがある場合に上書きする",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ファイルを書き込まず、形式確認と件数集計だけ行う",
    )
    parser.add_argument(
        "--json-summary",
        action="store_true",
        help="結果概要をJSON形式で表示する",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    converter = Converter(
        source=args.source.resolve(),
        output=args.output.resolve(),
        dry_run=args.dry_run,
        overwrite=args.overwrite,
    )
    try:
        result = converter.run()
    except (FileNotFoundError, FileExistsError, ValueError) as error:
        print(f"エラー: {error}", file=sys.stderr)
        return 1

    if args.json_summary:
        print(json.dumps(converter.summary(), ensure_ascii=False, indent=2))
    else:
        print(
            "変換完了: キャラ={characters}, 保存ログ={savelogs}, "
            "倉庫={warehouses}, チャンプ={winner}, 連勝記録={recode}, "
            "警告={warnings}".format(**converter.stats)
        )
        if converter.warnings:
            for warning in converter.warnings:
                print(f"警告: {warning}", file=sys.stderr)
        if not args.dry_run:
            print(f"出力先: {converter.output}")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
