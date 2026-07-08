"""
FFA Python/CGI アトミックファイルI/O・Mutex排他制御モジュール (sub_def/file_ops.py)
"""
import os
import json
import tempfile
import sys
from typing import Any

# パス解決のための親ディレクトリ参照
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from . import exLock

try:
    import config
except ImportError:
    from .. import config
Config = config.Config

def save_data_atomically(data: Any, file_path: str, lock_name: str) -> None:
    """データをアトミックに保存します (一時ファイル生成 -> fsync -> os.replace と Mutexロックの適用)"""
    lock_dir = Config.get("lock_dir", "./lock")
    os.makedirs(lock_dir, exist_ok=True)
    
    # exLock による排他制御 (二重書き込み、読み書き競合の完全防御)
    lock = exLock.exLock(os.path.join(lock_dir, f"{lock_name}.lock"))
    if not lock.lock():
        raise TimeoutError(f"排他ロックの取得に失敗しました: {lock_name}")
        
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    
    temp_file_path = None
    try:
        # 同一ディレクトリ内に安全な一時ファイルを作成 (Windows/Linux対応)
        # delete=False にすることで、クローズ後もファイルを維持し rename に備える
        with tempfile.NamedTemporaryFile(
            mode="w", dir=dir_path, prefix=".tmp_", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(data, temp_file, ensure_ascii=False, indent=2)
            temp_file.flush()
            # OS キャッシュをストレージに強制フラッシュし破損を防ぐ
            os.fsync(temp_file.fileno())
            temp_file_path = temp_file.name
            
        # アトミックな置換 (os.replace はアトミック性が保証される)
        os.replace(temp_file_path, file_path)
    except Exception as e:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise e
    finally:
        lock.unlock()

def load_data_with_lock(file_path: str, lock_name: str) -> Any:
    """Mutexロックを獲得した状態で安全にデータをロードします。ファイルが存在しない場合は None を返します。"""
    lock_dir = Config.get("lock_dir", "./lock")
    os.makedirs(lock_dir, exist_ok=True)
    
    lock = exLock.exLock(os.path.join(lock_dir, f"{lock_name}.lock"))
    if not lock.lock():
        raise TimeoutError(f"排他ロックの取得に失敗しました: {lock_name}")
        
    try:
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    finally:
        lock.unlock()

# === ユーザー個別の一元化データのロード・セーブ ===
def _user_path(user_id: str) -> str:
    save_dir = Config.get("save_dir", "./save_data")
    return os.path.join(save_dir, user_id)

def load_user_all(user_id: str) -> dict[str, Any] | None:
    """統合されたユーザーデータをロードします。"""
    user_dir = _user_path(user_id)
    file_path = os.path.join(user_dir, "user_all.json")
    # ユーザー名単位の排他ロックを掛けて安全にロード
    return load_data_with_lock(file_path, f"user_{user_id}")

def save_user_all(user_id: str, data: dict[str, Any]) -> None:
    """統合されたユーザーデータをアトミックに保存します。"""
    user_dir = _user_path(user_id)
    file_path = os.path.join(user_dir, "user_all.json")
    # ユーザー名単位の排他ロックを掛けて安全にアトミック保存
    save_data_atomically(data, file_path, f"user_{user_id}")
