import uuid
from datetime import timedelta

from fastapi import Request, Response

COOKIE_NAME = "scholar_anon_id"


def ensure_anon_cookie(request: Request, response: Response) -> uuid.UUID:
    raw = request.cookies.get(COOKIE_NAME)
    try:
        anon_id = uuid.UUID(raw) if raw else uuid.uuid4()
    except (ValueError, TypeError):
        anon_id = uuid.uuid4()
    response.set_cookie(
        key=COOKIE_NAME,
        value=str(anon_id),
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=int(timedelta(days=365).total_seconds()),
    )
    return anon_id
