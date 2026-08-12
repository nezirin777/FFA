"""同一プロセス内のファイルロック再入を共有管理する。"""

import threading


_state_lock = threading.RLock()
_owners = {}


def current_thread_id():
    return threading.get_ident()


def is_owned(path):
    with _state_lock:
        entry = _owners.get(path)
        return bool(entry and entry[0] == current_thread_id())


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
