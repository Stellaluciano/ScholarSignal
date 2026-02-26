from jose import jwt

from app.config import settings


def verify_nextauth_jwt(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
