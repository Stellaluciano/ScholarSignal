from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Preference
from app.db.session import get_db

router = APIRouter(prefix="/preferences", tags=["preferences"])


class PrefIn(BaseModel):
    categories: list[str] = []
    keywords: list[str] = []


@router.get("")
def get_pref(db: Session = Depends(get_db)):
    return db.execute(select(Preference).limit(1)).scalar_one_or_none()


@router.put("")
def put_pref(payload: PrefIn, db: Session = Depends(get_db)):
    p = db.execute(select(Preference).limit(1)).scalar_one_or_none() or Preference()
    p.categories = payload.categories
    p.keywords = payload.keywords
    p.updated_at = datetime.now(timezone.utc)
    db.add(p)
    db.commit()
    return p
