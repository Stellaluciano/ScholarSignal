from sqlalchemy import update
from sqlalchemy.orm import Session

from app.db.models import DailyDigest, Event, Preference


def merge_user_history(db: Session, anon_id, user_id) -> None:
    for model in (Event, DailyDigest, Preference):
        db.execute(update(model).where(model.anon_id == anon_id).values(user_id=user_id, anon_id=None))
    db.commit()
