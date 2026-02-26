from datetime import datetime, timedelta, timezone

from app.recommend.model import export_training_data, train_ranker


def run_nightly_training(db_session, out_dir: str) -> dict:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=30)
    paths = export_training_data(db_session, out_dir, start, end)
    return train_ranker(paths["train"], paths["valid"], out_dir)
