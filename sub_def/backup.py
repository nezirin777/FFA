"""日次セーブデータバックアップと復元処理。"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import time
from pathlib import Path
from typing import Any

try:
    import config
except ImportError:
    from .. import config


BACKUP_NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MANIFEST_NAME = "manifest.json"


def _backup_dir() -> Path:
    return Path(config.Config["backup_dir"])


def _save_dir() -> Path:
    return Path(config.Config["save_dir"])


def _today_name() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d")


def _safe_daily_path(name: str) -> Path:
    if not BACKUP_NAME_RE.fullmatch(name):
        raise ValueError("バックアップ名が不正です。")
    path = (_backup_dir() / name).resolve()
    root = _backup_dir().resolve()
    if path.parent != root:
        raise ValueError("バックアップの場所が不正です。")
    return path


def _format_size(size: int) -> str:
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


def _tree_stats(root: Path) -> tuple[int, int]:
    files = 0
    size = 0
    for path in root.rglob("*"):
        if path.is_file() and path.name != MANIFEST_NAME:
            files += 1
            try:
                size += path.stat().st_size
            except OSError:
                pass
    return files, size


def _write_manifest(root: Path, *, kind: str, source_name: str) -> dict[str, Any]:
    files, size = _tree_stats(root)
    manifest = {
        "format": 1,
        "kind": kind,
        "date": source_name,
        "created_at": int(time.time()),
        "files": files,
        "bytes": size,
    }
    (root / MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return manifest


def _read_manifest(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads((path / MANIFEST_NAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or data.get("format") != 1:
        return None
    return data


def _copy_save_data(destination: Path) -> dict[str, Any]:
    source = _save_dir()
    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(f"セーブデータディレクトリがありません: {source}")
    shutil.copytree(source, destination, dirs_exist_ok=True)
    return _write_manifest(destination, kind="daily", source_name=destination.name)


def _prune_daily_backups() -> None:
    root = _backup_dir()
    names = sorted(
        path.name
        for path in root.iterdir()
        if path.is_dir() and BACKUP_NAME_RE.fullmatch(path.name)
    )
    keep = int(config.Config.get("backup_retention_days", 40))
    for name in names[:-max(1, keep)]:
        shutil.rmtree(root / name)


def create_daily_backup(force: bool = False) -> dict[str, Any]:
    """当日分のバックアップを作成し、保持数を超えた古い世代を削除する。"""
    from sub_def import common

    root = _backup_dir()
    root.mkdir(parents=True, exist_ok=True)
    name = _today_name()
    target = _safe_daily_path(name)

    common.get_lock("backup_snapshot")
    try:
        existing = _read_manifest(target) if target.exists() else None
        if existing and not force:
            return {
                "name": name,
                "created": False,
                "files": existing.get("files", 0),
                "bytes": existing.get("bytes", 0),
            }

        temp = root / f".tmp_{name}_{os.getpid()}"
        if temp.exists():
            shutil.rmtree(temp)
        try:
            manifest = _copy_save_data(temp)
            if target.exists():
                shutil.rmtree(target)
            os.replace(temp, target)
        finally:
            if temp.exists():
                shutil.rmtree(temp)

        _prune_daily_backups()
        return {
            "name": name,
            "created": True,
            "files": manifest["files"],
            "bytes": manifest["bytes"],
        }
    finally:
        common.release_lock("backup_snapshot")


def ensure_daily_backup() -> dict[str, Any] | None:
    """ログイン処理から呼ぶ日次バックアップ。失敗してもログインは止めない。"""
    if not config.Config.get("backup_enabled", True):
        return None
    try:
        return create_daily_backup()
    except Exception as error:  # バックアップ障害でゲームへのログインを止めない
        print(f"日次バックアップに失敗しました: {error}", file=__import__("sys").stderr)
        return None


def list_daily_backups() -> list[dict[str, Any]]:
    """管理画面に表示する、検証済みの日次バックアップ一覧を返す。"""
    root = _backup_dir()
    if not root.exists():
        return []

    entries = []
    for path in sorted(root.iterdir(), reverse=True):
        if not path.is_dir() or not BACKUP_NAME_RE.fullmatch(path.name):
            continue
        manifest = _read_manifest(path)
        if not manifest:
            continue
        created_at = int(manifest.get("created_at", 0) or 0)
        entries.append({
            "name": path.name,
            "created_at": created_at,
            "created_at_text": time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(created_at)),
            "files": int(manifest.get("files", 0) or 0),
            "size": _format_size(int(manifest.get("bytes", 0) or 0)),
        })
    return entries


def restore_daily_backup(name: str) -> str:
    """指定した日次バックアップを復元し、復元直前の状態を退避する。"""
    from sub_def import common

    source = _safe_daily_path(name)
    manifest = _read_manifest(source)
    if not manifest:
        raise ValueError("指定されたバックアップが見つからないか、形式が不正です。")
    if not config.Config.get("maintenance_mode"):
        raise RuntimeError("復元前にconfig.pyのmaintenance_modeを1にしてください。")

    root = _backup_dir()
    restore_id = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    emergency = root / f"pre_restore_{restore_id}"
    temp = root / f".restore_{restore_id}_{os.getpid()}"

    common.get_lock("backup_restore")
    common.get_lock("backup_snapshot")
    try:
        if emergency.exists():
            raise RuntimeError("同じ時刻の復元退避先が既に存在します。再試行してください。")
        _copy_save_data(emergency)
        if temp.exists():
            shutil.rmtree(temp)
        shutil.copytree(source, temp, ignore=shutil.ignore_patterns(MANIFEST_NAME))

        current = _save_dir()
        if current.exists():
            shutil.rmtree(current)
        current.parent.mkdir(parents=True, exist_ok=True)
        os.replace(temp, current)
        return emergency.name
    finally:
        if temp.exists():
            shutil.rmtree(temp)
        common.release_lock("backup_snapshot")
        common.release_lock("backup_restore")
