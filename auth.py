import hmac
import hashlib
import base64
import json
import time
from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, status
from backend.database import get_db

SECRET_KEY = "mediverse_super_secret_jwt_key_2026"

def create_access_token(data: dict, expires_in: int = 86400 * 7) -> str:
    """Create a self-contained signed HMAC-SHA256 token"""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    payload["exp"] = int(time.time()) + expires_in

    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"{header_b64}.{payload_b64}.{sig_b64}"

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify HMAC token and check expiration"""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts

        message = f"{header_b64}.{payload_b64}"
        expected_sig = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(sig_b64 + "=" * (-len(sig_b64) % 4))

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload_json = base64.urlsafe_b64decode(payload_b64 + "=" * (-len(payload_b64) % 4)).decode()
        payload = json.loads(payload_json)

        if payload.get("exp", 0) < time.time():
            return None # Expired

        return payload
    except Exception:
        return None

def get_current_user_from_token(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

    token = authorization.replace("Bearer ", "").strip()
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("user_id")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, role, name, phone FROM users WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()

    if not user_row:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = dict(user_row)
    profile = None

    if user["role"] == "patient":
        cursor.execute("SELECT * FROM patients WHERE user_id = ?", (user["id"],))
        p_row = cursor.fetchone()
        if p_row:
            profile = dict(p_row)
    elif user["role"] == "doctor":
        cursor.execute("SELECT * FROM doctors WHERE user_id = ?", (user["id"],))
        d_row = cursor.fetchone()
        if d_row:
            profile = dict(d_row)

    conn.close()
    return {"user": user, "profile": profile}
