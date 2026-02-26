from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def ny_date(dt: datetime) -> datetime.date:
    return dt.astimezone(ZoneInfo("America/New_York")).date()
