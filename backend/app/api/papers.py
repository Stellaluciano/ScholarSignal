from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.db.models import Paper
from app.db.session import get_db

router = APIRouter(prefix="/papers", tags=["papers"])


@router.get("")
def list_papers(query: str = "", category: str = "", from_: datetime | None = Query(default=None, alias="from"), to: datetime | None = None, limit: int = 20, db: Session = Depends(get_db)):
    conds = []
    if query:
        conds.append(Paper.title.ilike(f"%{query}%"))
    if category:
        conds.append(Paper.categories.cast(str).ilike(f"%{category}%"))
    if from_:
        conds.append(Paper.published_at >= from_)
    if to:
        conds.append(Paper.published_at <= to)
    q = select(Paper)
    if conds:
        q = q.where(and_(*conds))
    return db.execute(q.limit(limit)).scalars().all()


@router.get("/{arxiv_id}")
def get_paper(arxiv_id: str, db: Session = Depends(get_db)):
    return db.get(Paper, arxiv_id)
