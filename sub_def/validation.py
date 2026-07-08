"""
FFA Python/CGI 防衛的入力値バリデーション（ファイル名保護・予約語・文字コード検証） (sub_def/validation.py)
"""
import re
from typing import Any

# Windows/Linux 予約語セット (ファイル名使用不可)
_RESERVED_FILENAMES: frozenset[str] = frozenset({
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
})

def validate_username(username: str) -> str | None:
    """
    ユーザー名を検証します。
    問題がある場合はエラーメッセージ、正常な場合は None を返します。
    """
    if not username:
        return "ユーザー名を入力してください。"
        
    if len(username) < 2 or len(username) > 16:
        return "ユーザー名は2文字以上16文字以内で入力してください。"
        
    # ファイル名として利用される可能性があるため予約語チェック
    base_name = username.upper().split(".")[0]
    if base_name in _RESERVED_FILENAMES:
        return "使用できない文字列がユーザー名に含まれています。"
        
    # ディレクトリトラバーサル、制御文字、不正なパス記号の検知
    if re.search(r"[\x00-\x1f\x7f-\x9f\\/:*?\"<>|]", username):
        return "ファイルシステムに影響を与える記号（/、\\、:、* 等）や制御文字は使用できません。"
        
    # Shift-JIS 互換性の検証 (レガシー環境の文字化け防止)
    try:
        username.encode("cp932")
    except UnicodeEncodeError:
        return "Shift-JIS (cp932) に変換できない文字（絵文字や一部の特殊漢字など）は使用できません。"
        
    return None

def validate_password(password: str) -> str | None:
    """パスワードの長さを検証します。"""
    if not password:
        return "パスワードを入力してください。"
    if len(password) < 4 or len(password) > 20:
        return "パスワードは4文字以上20文字以内で入力してください。"
    return None

def check_sjis_compatibility(text: str) -> bool:
    """テキストが Shift-JIS (cp932) に安全にエンコードできるか確認します。"""
    try:
        text.encode("cp932")
        return True
    except UnicodeEncodeError:
        return False
