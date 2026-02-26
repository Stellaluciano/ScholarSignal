# ScholarSignal

ScholarSignal is a fully open-source, self-hosted web app that recommends **5 arXiv papers per user per day** and improves over time from user feedback (views, clicks, PDF opens, downloads, saves, dislikes, dwell). Daily digest scheduling is based on **America/New_York** calendar dates while all DB times are stored in UTC.

## Features
- FastAPI backend with PostgreSQL + pgvector.
- Next.js frontend with NextAuth (GitHub/Google) + anonymous secure cookie mode.
- arXiv ingestion and local embedding fallback (HashingVectorizer) with no paid API requirement.
- Daily digest persistence and impression logging.
- Export/import training datasets in parquet.
- Recommendation algorithm isolated in `backend/app/recommend/model.py`.
- Redis + RQ worker and scheduler queues.

## Repo Structure
Matches requested structure with backend, web, docs, and scripts directories.

## Quick Start
```bash
cp .env.example .env
docker compose up --build
```

Open:
- Web: http://localhost:3000
- API: http://localhost:8000/api/v1/health

## Auth Model
- Anonymous mode: backend sets `scholar_anon_id` cookie (`HttpOnly`, `Secure`, `SameSite=Lax`, `Path=/`, 365 days).
- Logged in mode: NextAuth JWT strategy with GitHub and Google providers.
- Merge endpoint logic available in `backend/app/auth/merge.py` for `anon_id -> user_id` history reconciliation.

## Single Domain Deployment
Use Next.js rewrites in `web/next.config.js` to proxy `/api/*` to backend internal service. This gives one-domain UX behind a reverse proxy / ingress.

## China-Mainland-friendly Setup
- Configure Docker registry mirrors in daemon config.
- Set proxy env vars before build if required:
```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
export NO_PROXY=localhost,127.0.0.1,postgres,redis,backend,web
```
- For Python/pip mirrors set `PIP_INDEX_URL`; for npm set `npm config set registry`.


## Documentation Artifacts
- `docs/prd.md` contains a text PRD snapshot.
- `docs/system_design.md` contains a text architecture summary.
- Binary image assets are intentionally avoided in this repository.

## Manual Ops
- Trigger ingestion: `POST /api/v1/admin/ingest/run` with `X-Admin-Token`.
- Trigger training: `POST /api/v1/admin/train/run`.
- Export datasets: `GET /api/v1/admin/dataset/export`.
- Import dataset parquet: `POST /api/v1/admin/dataset/import`.

## License
This repository is licensed under **Apache License 2.0**. See `LICENSE` and `NOTICE`.
