import json
from pathlib import Path

import pandas as pd


def export_parquet(train_rows: list[dict], valid_rows: list[dict], papers: list[dict], out_dir: str) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    t, v, p = out / "train.parquet", out / "valid.parquet", out / "papers.parquet"
    pd.DataFrame(train_rows).to_parquet(t, index=False)
    pd.DataFrame(valid_rows).to_parquet(v, index=False)
    pd.DataFrame(papers).to_parquet(p, index=False)
    schema = out / "schema.json"
    schema.write_text(json.dumps({"train": [*pd.DataFrame(train_rows).columns]}), encoding="utf-8")
    return {"train": str(t), "valid": str(v), "papers": str(p), "schema": str(schema)}


def import_parquet_to_db(db_session, parquet_path: str, table: str) -> int:
    df = pd.read_parquet(parquet_path)
    df.to_sql(table, db_session.bind, if_exists="append", index=False)
    return len(df)
