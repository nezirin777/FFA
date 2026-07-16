"""
FFA Python/CGI セキュリティ・暗号化モジュール (sub_def/crypto.py)
"""
import base64
import hashlib
import hmac
import json
import time
import os
import sys
from http import cookies
from typing import Any

try:
    import config
except ImportError:
    from .. import config
Config = config.Config

# セッション秘密鍵
SECRET_KEY: bytes = Config.get("secret_key", "FFA_SECRET_KEY_DEFAULT_1234567890").encode("utf-8")

def _derive_key(salt: bytes) -> bytes:
    """PBKDF2 を用いて秘密鍵とソルトから暗号用キーを導出します (タイミング攻撃・辞書攻撃対策)"""
    return hashlib.pbkdf2_hmac("sha256", SECRET_KEY, salt, 1000, 32)

def encrypt_data(data: dict[str, Any]) -> str:
    """データを暗号化し、HMAC-SHA256署名付きBase64文字列で返します (Encrypt-then-MAC)"""
    json_bytes = json.dumps(data).encode("utf-8")
    
    # 毎リクエストでランダムなノンス(ソルト)を生成
    salt = os.urandom(16)
    key = _derive_key(salt)
    
    # 擬似乱数ストリーム(XOR)による暗号化
    encrypted = bytearray(len(json_bytes))
    for i in range(len(json_bytes)):
        block_idx = i // 32
        block_offset = i % 32
        block_key = hashlib.sha256(key + salt + block_idx.to_bytes(4, "big")).digest()
        encrypted[i] = json_bytes[i] ^ block_key[block_offset]
        
    payload = salt + bytes(encrypted)
    signature = hmac.new(SECRET_KEY, payload, hashlib.sha256).digest()
    
    final_payload = signature + salt + bytes(encrypted)
    return base64.urlsafe_b64encode(final_payload).decode("utf-8")

def decrypt_data(cookie_val: str) -> dict[str, Any] | None:
    """暗号化されたクッキー値の署名を検証し、復号します。改ざん検知時は None を返します。"""
    try:
        raw_data = base64.urlsafe_b64decode(cookie_val.encode("utf-8"))
        if len(raw_data) < 32 + 16:
            return None
            
        signature = raw_data[:32]
        salt = raw_data[32:48]
        encrypted = raw_data[48:]
        
        # 署名の定時間検証 (タイミング攻撃の防御)
        payload = salt + encrypted
        expected_signature = hmac.new(SECRET_KEY, payload, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected_signature):
            return None
            
        key = _derive_key(salt)
        decrypted = bytearray(len(encrypted))
        for i in range(len(encrypted)):
            block_idx = i // 32
            block_offset = i % 32
            block_key = hashlib.sha256(key + salt + block_idx.to_bytes(4, "big")).digest()
            decrypted[i] = encrypted[i] ^ block_key[block_offset]
            
        return json.loads(bytes(decrypted).decode("utf-8"))
    except Exception:
        return None

# === セッション管理 ===
SESSION_COOKIE_NAME = "FFAPY_SESSION"

def get_session() -> dict[str, Any]:
    """暗号化されたクッキーから現在のセッションデータを読み込みます。"""
    cookie_str = os.environ.get("HTTP_COOKIE", "")
    cookie = cookies.SimpleCookie()
    cookie.load(cookie_str)
    
    if SESSION_COOKIE_NAME in cookie:
        session_val = cookie[SESSION_COOKIE_NAME].value
        decrypted = decrypt_data(session_val)
        if decrypted:
            # 有効期限チェック (Configのsession_expiryを参照)
            created_at = decrypted.get("created_at", 0)
            expiry = Config.get("session_expiry", 1800)
            if time.time() - created_at < expiry:
                return decrypted
    return {}

def save_session(session_data: dict[str, Any]) -> str:
    """セッションデータを暗号化し、Set-Cookieヘッダー用の文字列を返します。"""
    session_data["created_at"] = time.time()
    encrypted_val = encrypt_data(session_data)
    
    cookie = cookies.SimpleCookie()
    cookie[SESSION_COOKIE_NAME] = encrypted_val
    cookie[SESSION_COOKIE_NAME]["path"] = "/"
    cookie[SESSION_COOKIE_NAME]["httponly"] = True
    # HTTP環境でも動くよう、Secure属性は必要に応じて設定（ローカル開発に配慮）
    # cookie[SESSION_COOKIE_NAME]["secure"] = True 
    return cookie.output()

def destroy_session() -> str:
    """セッションを破棄するための Set-Cookie ヘッダー用文字列を返します。"""
    cookie = cookies.SimpleCookie()
    cookie[SESSION_COOKIE_NAME] = ""
    cookie[SESSION_COOKIE_NAME]["path"] = "/"
    cookie[SESSION_COOKIE_NAME]["httponly"] = True
    cookie[SESSION_COOKIE_NAME]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
    return cookie.output()

# === CSRF対策 ===
def token_generate(session: dict[str, Any]) -> str:
    """セッション内に CSRF トークンを生成して保存し、トークン文字列を返します。"""
    if "csrf_token" not in session:
        session["csrf_token"] = base64.b64encode(os.urandom(24)).decode("utf-8")
    return session["csrf_token"]

def token_regenerate(session: dict[str, Any]) -> str:
    """セッション内の CSRF トークンを強制的に再生成して保存し、新しいトークン文字列を返します。"""
    session["csrf_token"] = base64.b64encode(os.urandom(24)).decode("utf-8")
    return session["csrf_token"]

def token_check(FORM: dict[str, Any], session: dict[str, Any]) -> None:
    """CSRFトークンを検証します。不正な場合は不正アクセスとして停止します。"""
    token_in_form = FORM.get("s")
    token_in_session = session.get("csrf_token")
    
    if not token_in_session or not token_in_form:
        from .utils import show_error
        show_error("CSRFトークンが不足しています。再試行してください。")
        
    if not hmac.compare_digest(token_in_form, token_in_session):
        from .utils import show_error
        show_error("不正なリクエスト（CSRF）を検知しました。操作を中断します。")

# === パスワードハッシュ ===
_PBKDF2_ITER = 100000  # 新形式の反復回数

def _hash_with_salt(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITER, 32)

def hash_password(password: str) -> str:
    """ユーザー毎のランダムソルトで PBKDF2-SHA256 ハッシュを生成します（新形式: pbkdf2$salt$hash）。
    ソルトが各ユーザーで異なるため、同一パスワードでもハッシュが一致しません（レインボーテーブル対策）。
    """
    salt = os.urandom(16)
    h = _hash_with_salt(password, salt)
    return "pbkdf2$" + base64.b64encode(salt).decode("utf-8") + "$" + base64.b64encode(h).decode("utf-8")

def _hash_legacy(password: str) -> str:
    """旧形式（全ユーザー共通の固定ソルト）ハッシュ。既存パスワードの検証にのみ使用。"""
    salt = base64.b64encode(SECRET_KEY[:16]).decode("utf-8")
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 2000, 32)
    return base64.b64encode(hashed).decode("utf-8")

def verify_password(password: str, stored: str) -> bool:
    """パスワードを検証します。新形式(salted)・旧形式(固定ソルト)・平文(旧レガシー)のいずれにも対応。"""
    if not stored:
        return False
    if stored.startswith("pbkdf2$"):
        try:
            _, salt_b64, hash_b64 = stored.split("$", 2)
            salt = base64.b64decode(salt_b64)
            expected = base64.b64decode(hash_b64)
            return hmac.compare_digest(_hash_with_salt(password, salt), expected)
        except Exception:
            return False
    # 旧固定ソルト形式
    if hmac.compare_digest(_hash_legacy(password), stored):
        return True
    # さらに古い平文形式
    return hmac.compare_digest(password, stored)

def needs_rehash(stored: str) -> bool:
    """新形式(pbkdf2$...)でなければ True。ログイン成功時に新形式へ移行する判定に使う。"""
    return not (stored or "").startswith("pbkdf2$")
