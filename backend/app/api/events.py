import time
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.anon import ensure_anon_cookie
from app.db.models import AnonymousUser
from app.db.models import Event, EventType
from app.db.session import get_db

router = APIRouter(prefix="/events", tags=["events"])
RATE = defaultdict(list)


class EventIn(BaseModel):
    arxiv_id: str
    event_type: EventType
    source: str
    rank_position: int | None = None
    dwell_ms: int | None = None


@router.post("")
def create_event(payload: EventIn, request: Request, response: Response, db: Session = Depends(get_db)):
    now = time.time()
    key = payload.arxiv_id
    RATE[key] = [t for t in RATE[key] if now - t < 60]
    if len(RATE[key]) > 120:
        raise HTTPException(429, "rate limited")
    RATE[key].append(now)
    anon_id = ensure_anon_cookie(request, response)
    if not db.get(AnonymousUser, anon_id):
        db.add(AnonymousUser(anon_id=anon_id))
    e = Event(
        arxiv_id=payload.arxiv_id,
        event_type=payload.event_type,
        source=payload.source,
        rank_position=payload.rank_position,
        dwell_ms=payload.dwell_ms,
        anon_id=anon_id,
        occurred_at=datetime.now(timezone.utc),
    )
    db.add(e)
    db.commit()
    return {"ok": True}
