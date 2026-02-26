from datetime import datetime, timezone

import numpy as np

from app.recommend import model


def test_profile_weights():
    emb = {"a": np.ones(256, dtype=np.float32), "b": np.ones(256, dtype=np.float32) * 2}
    events = [
        {"arxiv_id": "a", "event_type": "save"},
        {"arxiv_id": "b", "event_type": "dislike"},
    ]
    p = model.build_user_profile(events, emb)
    assert p.shape[0] == 256


def test_mmr_diversify():
    emb = {"a": np.ones(256), "b": np.ones(256) * 0.9, "c": np.eye(1, 256, 0).flatten()}
    out = model.diversify_mmr([("a", 1.0), ("b", 0.99), ("c", 0.5)], emb, k=2)
    assert len(out) == 2


def test_export_schema(tmp_path):
    class Dummy:
        def execute(self, *_a, **_k):
            class R:
                def mappings(self):
                    return self

                def all(self):
                    return [{"arxiv_id": "a", "event_type": "save", "occurred_at": datetime.now(timezone.utc)}]

            return R()

    out = model.export_training_data(Dummy(), str(tmp_path), datetime.now(timezone.utc), datetime.now(timezone.utc))
    assert "schema" in out


def test_model_isolated_imports():
    txt = open("app/recommend/model.py", encoding="utf-8").read()
    assert "fastapi" not in txt.lower()
    assert "sqlalchemy" not in txt.lower()
