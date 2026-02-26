from datetime import datetime, timezone

from sqlalchemy import select

from app.db.models import DailyDigest, Event, EventType, Paper
from app.recommend.model import UserContext, recommend_topk
from app.utils.time import ny_date


def generate_digest_for_identity(db, *, user_id=None, anon_id=None, categories=None):
    papers = db.execute(select(Paper)).scalars().all()
    events = db.execute(select(Event).where((Event.user_id == user_id) if user_id else (Event.anon_id == anon_id))).scalars().all()
    payload_papers = [
        {"arxiv_id": p.arxiv_id, "categories": p.categories, "published_at": p.published_at.replace(tzinfo=timezone.utc), "embedding": p.embedding}
        for p in papers
    ]
    payload_events = [{"arxiv_id": e.arxiv_id, "event_type": e.event_type.value, "dwell_ms": e.dwell_ms} for e in events]
    picks = recommend_topk(UserContext(categories=categories or [], seen_set=set()), payload_papers, payload_events, k=5)
    digest = DailyDigest(user_id=user_id, anon_id=anon_id, digest_date=ny_date(datetime.now(timezone.utc)), arxiv_ids=picks)
    db.add(digest)
    for i, aid in enumerate(picks, start=1):
        db.add(Event(user_id=user_id, anon_id=anon_id, arxiv_id=aid, event_type=EventType.impression, rank_position=i, source="daily_digest"))
    db.commit()
    return digest
