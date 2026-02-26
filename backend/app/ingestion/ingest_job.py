from sqlalchemy import select

from app.db.models import Paper
from app.ingestion.arxiv_client import fetch_arxiv
from app.ingestion.embed_job import embed_text
from app.utils.hashing import fingerprint_paper


def run_ingestion(db, categories: list[str]) -> int:
    rows = fetch_arxiv(categories)
    count = 0
    for r in rows:
        existing = db.execute(select(Paper).where(Paper.arxiv_id == r["arxiv_id"])).scalar_one_or_none()
        if existing:
            continue
        p = Paper(
            **r,
            fingerprint_sha256=fingerprint_paper(r["title"], r["authors"]),
            embedding=embed_text(f"{r['title']}\n{r['abstract']}"),
        )
        db.add(p)
        count += 1
    db.commit()
    return count
