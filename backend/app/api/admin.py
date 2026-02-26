from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.db.session import get_db
from app.ingestion.ingest_job import run_ingestion
from app.recommend.datasets import import_parquet_to_db
from app.recommend.model import export_training_data
from app.recommend.trainer import run_nightly_training

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(x_admin_token: str = Header(default="")):
    if x_admin_token != settings.admin_token:
        raise HTTPException(401, "bad token")


@router.post("/ingest/run", dependencies=[Depends(require_admin)])
def ingest(db: Session = Depends(get_db)):
    return {"inserted": run_ingestion(db, settings.arxiv_categories.split(","))}


@router.post("/train/run", dependencies=[Depends(require_admin)])
def train(db: Session = Depends(get_db)):
    return run_nightly_training(db, "/tmp/artifacts")


@router.get("/dataset/export", dependencies=[Depends(require_admin)])
def export_dataset(from_: datetime, to: datetime, db: Session = Depends(get_db)):
    return export_training_data(db, "/tmp/datasets", from_, to)


@router.post("/dataset/import", dependencies=[Depends(require_admin)])
async def import_dataset(table: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = Path("/tmp") / file.filename
    path.write_bytes(await file.read())
    return {"rows": import_parquet_to_db(db, str(path), table)}
