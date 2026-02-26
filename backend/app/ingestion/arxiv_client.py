from datetime import datetime, timezone
from typing import Any

import feedparser
import httpx


def fetch_arxiv(categories: list[str], max_results: int = 50) -> list[dict[str, Any]]:
    query = " OR ".join(f"cat:{c}" for c in categories)
    url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    text = httpx.get(url, timeout=20).text
    feed = feedparser.parse(text)
    out = []
    for e in feed.entries:
        arxiv_id = e.id.split("/abs/")[-1]
        out.append(
            {
                "arxiv_id": arxiv_id,
                "title": e.title,
                "abstract": e.summary,
                "authors": [a.name for a in e.authors],
                "categories": [t["term"] for t in e.tags],
                "published_at": datetime.fromisoformat(e.published.replace("Z", "+00:00")).astimezone(timezone.utc),
                "updated_at": datetime.fromisoformat(e.updated.replace("Z", "+00:00")).astimezone(timezone.utc),
                "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            }
        )
    return out
