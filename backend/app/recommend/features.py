from collections import Counter

import numpy as np


def build_feature_rows(user_positive_papers: list[dict], candidates: list[dict], global_counts: dict[str, int]) -> list[dict]:
    author_aff = Counter(a for p in user_positive_papers for a in p.get("authors", []))
    out: list[dict] = []
    for c in candidates:
        cvec = np.array(c.get("embedding", np.zeros(256)))
        dists = [float(np.linalg.norm(cvec - np.array(p.get("embedding", np.zeros(256))))) for p in user_positive_papers] or [0.0]
        out.append(
            {
                "arxiv_id": c["arxiv_id"],
                "cosine": float(c.get("cosine", 0.0)),
                "recency_days": c.get("recency_days", 0),
                "category_match_count": c.get("category_match_count", 0),
                "author_affinity": sum(author_aff[a] for a in c.get("authors", [])),
                "novelty": min(dists),
                "popularity_proxy": global_counts.get(c["arxiv_id"], 0),
            }
        )
    return out
