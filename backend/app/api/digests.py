import uuid

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.anon import ensure_anon_cookie
from app.db.models import AnonymousUser, DailyDigest
from app.db.session import get_db
from app.recommend.digest import generate_digest_for_identity
from app.utils.time import ny_date, utcnow

router = APIRouter(prefix="/digests", tags=["digests"])


@router.get("/today")
def today(request: Request, response: Response, db: Session = Depends(get_db)):
    anon_id = ensure_anon_cookie(request, response)
    if not db.get(AnonymousUser, anon_id):
        db.add(AnonymousUser(anon_id=anon_id))
        db.commit()
    today_date = ny_date(utcnow())
    d = db.execute(select(DailyDigest).where(DailyDigest.anon_id == anon_id, DailyDigest.digest_date == today_date)).scalar_one_or_none()
    if not d:
        d = generate_digest_for_identity(db, anon_id=anon_id)
    return d


@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    anon_id = ensure_anon_cookie(request, response)
    d = generate_digest_for_identity(db, anon_id=uuid.UUID(str(anon_id)))
    return d
