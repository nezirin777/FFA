"""同一プロセス内のファイルロック再入と残存ロック回復を共有管理する。"""

import os
import threading
import time


_state_lock = threading.RLock()
_owners = {}


def current_thread_id():
    return threading.get_ident()


def is_owned(path):
    with _state_lock:
        entry = _owners.get(path)
        return bool(entry and entry[0] == current_thread_id())


def is_owned_by_any_thread(path):
    """現プロセス内のいずれかのスレッドが保持しているかを返す。"""
    with _state_lock:
        return path in _owners


def enter(path):
    with _state_lock:
        thread_id = current_thread_id()
        entry = _owners.get(path)
        if entry and entry[0] == thread_id:
            _owners[path] = (thread_id, entry[1] + 1)
            return True
        if entry:
            return False
        _owners[path] = (thread_id, 1)
        return True


def leave(path):
    with _state_lock:
        thread_id = current_thread_id()
        entry = _owners.get(path)
        if not entry or entry[0] != thread_id:
            return False
        if entry[1] > 1:
            _owners[path] = (thread_id, entry[1] - 1)
            return False
        del _owners[path]
        return True


def remove_stale_lock_dir(path, stale_seconds):
    """期限切れの空ロックディレクトリだけを削除できた場合にTrueを返す。"""
    try:
        stale_seconds = float(stale_seconds)
    except (TypeError, ValueError):
        return False
    if stale_seconds <= 0 or is_owned_by_any_thread(path):
        return False

    try:
        age = time.time() - os.stat(path).st_mtime
        if age < stale_seconds:
            return False
        os.rmdir(path)
        return True
    except (FileNotFoundError, NotADirectoryError, OSError):
        return False
