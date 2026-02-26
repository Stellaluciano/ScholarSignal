# ScholarSignal System Design (Text Version)

## High-level flow
1. **Ingestion job** fetches arXiv entries for configured categories.
2. Backend deduplicates papers (arXiv ID + fingerprint hash).
3. Local embedding fallback computes fixed-size vectors.
4. Paper metadata + vectors are stored in Postgres (pgvector).
5. Daily digest job generates stable top-5 recommendations per identity.
6. Frontend (`/today`) reads digest and renders interaction controls.
7. Events are logged (impression, click_abs, click_pdf, download, save, dislike, dwell).
8. Dataset export/import supports manual training/validation cycles.
9. Ranker training artifacts can be produced and loaded for inference fallback routing.

## Services
- `web` (Next.js + NextAuth)
- `backend` (FastAPI)
- `worker` (RQ)
- `scheduler` (RQ scheduler)
- `postgres` (with pgvector)
- `redis`

## Identity modes
- Anonymous users tracked via secure HttpOnly cookie (`scholar_anon_id`).
- OAuth users via NextAuth (GitHub, Google).
- Merge utility supports migrating anonymous history to authenticated user.
