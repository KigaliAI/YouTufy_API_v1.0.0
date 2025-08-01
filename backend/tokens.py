# utils/tokens.py
from itsdangerous import URLSafeTimedSerializer
import os

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
SECURITY_SALT = "reset-password-salt"

def generate_token(email: str) -> str:
    s = URLSafeTimedSerializer(SECRET_KEY)
    return s.dumps(email, salt=SECURITY_SALT)

def verify_token(token: str, max_age: int = 3600) -> str:
    s = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = s.loads(token, salt=SECURITY_SALT, max_age=max_age)
        return email
    except Exception:
        return None

