"""
FFA Python/CGI - ディレクトリ作成によるMutex排他ロッククラス (exLock.py)
"""
import os
import time

class exLock:
    def __init__(self, lock_path: str, timeout: int = 15):
        self.lock_path = lock_path
        self.timeout = timeout
        self.locked = False
        
    def lock(self) -> bool:
        """ロック（ディレクトリ作成）を試みます。タイムアウトまで待機します。"""
        start_time = time.time()
        while True:
            try:
                os.mkdir(self.lock_path)
                self.locked = True
                return True
            except FileExistsError:
                # すでにロックが存在する場合は一定時間スリープして再試行
                if time.time() - start_time > self.timeout:
                    # タイムアウト
                    return False
                time.sleep(0.2)
                
    def unlock(self) -> None:
        """ロックを解除（ディレクトリ削除）します。"""
        if self.locked:
            try:
                os.rmdir(self.lock_path)
                self.locked = False
            except FileNotFoundError:
                # 既に解除されている場合は無視
                pass
