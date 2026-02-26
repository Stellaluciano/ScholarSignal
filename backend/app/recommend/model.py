"""Dependency-light recommendation core for ScholarSignal."""
from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


WEIGHTS = {
    "save": 3.0,
    "download_pdf": 2.0,
    "click_pdf": 1.5,
    "click_abs": 1.0,
    "dwell": 1.0,
    "dislike": -3.0,
}


@dataclass
class UserContext:
    categories: list[str]
    seen_set: set[str]


def _cos(a: np.ndarray, b: np.ndarray) -> float:
    den = np.linalg.norm(a) * np.linalg.norm(b)
    if den == 0:
        return 0.0
    return float(np.dot(a, b) / den)


def build_user_profile(events: list[dict], paper_embeddings: dict[str, np.ndarray]) -> np.ndarray:
    vecs: list[np.ndarray] = []
    ws: list[float] = []
    for ev in events:
        aid = ev["arxiv_id"]
        if aid not in paper_embeddings:
            continue
        w = WEIGHTS.get(ev["event_type"], 0.0)
        if ev["event_type"] == "dwell" and ev.get("dwell_ms", 0) < 20_000:
            w = 0.0
        if w == 0:
            continue
        vecs.append(paper_embeddings[aid])
        ws.append(w)
    if not vecs:
        return np.zeros(256, dtype=np.float32)
    arr = np.vstack(vecs)
    profile = np.average(arr, axis=0, weights=np.array(ws, dtype=np.float32))
    return profile.astype(np.float32)


def generate_candidates(user_pref: dict, recent_papers: list[dict], seen_set: set[str]) -> list[str]:
    cats = set(user_pref.get("categories", []))
    first = [p["arxiv_id"] for p in recent_papers if p["arxiv_id"] not in seen_set and (not cats or cats.intersection(set(p.get("categories", []))))]
    if first:
        return first
    return [p["arxiv_id"] for p in recent_papers if p["arxiv_id"] not in seen_set]


def score_candidates(profile_vec: np.ndarray, candidates: list[str], paper_embeddings: dict[str, np.ndarray], meta: dict[str, dict]) -> list[tuple[str, float]]:
    now = datetime.now(timezone.utc)
    out: list[tuple[str, float]] = []
    for aid in candidates:
        emb = paper_embeddings.get(aid)
        if emb is None:
            continue
        sim = _cos(profile_vec, emb)
        days = max((now - meta[aid]["published_at"]).days, 0)
        recency_boost = 1.0 / (1.0 + days)
        seen_penalty = 0.3 if meta[aid].get("seen_recently") else 0.0
        out.append((aid, sim + 0.2 * recency_boost - seen_penalty))
    return sorted(out, key=lambda x: x[1], reverse=True)


def diversify_mmr(scored: list[tuple[str, float]], paper_embeddings: dict[str, np.ndarray], k: int = 5, lambda_: float = 0.7) -> list[str]:
    if not scored:
        return []
    selected: list[str] = [scored[0][0]]
    rem = scored[1:]
    while rem and len(selected) < k:
        best = None
        best_score = -1e9
        for aid, rel in rem:
            max_sim = max(_cos(paper_embeddings[aid], paper_embeddings[s]) for s in selected)
            mmr = lambda_ * rel - (1 - lambda_) * max_sim
            if mmr > best_score:
                best = aid
                best_score = mmr
        selected.append(best)
        rem = [x for x in rem if x[0] != best]
    return selected


def recommend_topk(user_context: UserContext, papers: list[dict], events: list[dict], k: int = 5) -> list[str]:
    embeddings = {p["arxiv_id"]: p["embedding"] for p in papers if p.get("embedding") is not None}
    meta = {p["arxiv_id"]: {"published_at": p["published_at"], "seen_recently": p["arxiv_id"] in user_context.seen_set} for p in papers}
    profile = build_user_profile(events, embeddings)
    candidates = generate_candidates({"categories": user_context.categories}, papers, set())
    scored = score_candidates(profile, candidates, embeddings, meta)
    return diversify_mmr(scored, embeddings, k=k)


def export_training_data(db_session, out_dir: str, start_date: datetime, end_date: datetime) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = db_session.execute("SELECT arxiv_id, event_type, occurred_at FROM events WHERE occurred_at >= :s AND occurred_at < :e", {"s": start_date, "e": end_date}).mappings().all()
    df = pd.DataFrame(rows)
    train = out / "train.parquet"
    valid = out / "valid.parquet"
    if df.empty:
        df = pd.DataFrame(columns=["arxiv_id", "event_type", "occurred_at"])
    split = int(len(df) * 0.8)
    df.iloc[:split].to_parquet(train, index=False)
    df.iloc[split:].to_parquet(valid, index=False)
    schema = out / "schema.json"
    schema.write_text(json.dumps({"columns": list(df.columns)}), encoding="utf-8")
    return {"train": str(train), "valid": str(valid), "schema": str(schema)}


def train_ranker(train_path: str, valid_path: str, artifacts_dir: str) -> dict:
    train_df = pd.read_parquet(train_path)
    valid_df = pd.read_parquet(valid_path)
    artifact = {"train_rows": len(train_df), "valid_rows": len(valid_df), "version": datetime.now(timezone.utc).strftime("v1-%Y%m%d%H%M")}
    out = Path(artifacts_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{artifact['version']}.pkl"
    with path.open("wb") as f:
        pickle.dump(artifact, f)
    artifact["path"] = str(path)
    artifact["metrics"] = {"auc": 0.5}
    return artifact


def load_artifact(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)


def predict_ranker(model, features: np.ndarray) -> np.ndarray:
    return np.zeros(features.shape[0], dtype=np.float32)
