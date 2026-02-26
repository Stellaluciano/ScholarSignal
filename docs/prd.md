# ScholarSignal PRD Snapshot

## Project
ScholarSignal — Personalized arXiv paper recommendation system.

## MVP Goals
- Daily ingestion of configured arXiv categories.
- 5 personalized recommendations per user per day.
- Supports anonymous cookie identity and OAuth users.
- Captures user feedback events for iterative ranking improvements.
- Self-hosted stack (FastAPI, Next.js, Postgres+pgvector, Redis+RQ).
- Offline fallback embedding path for zero paid API dependency.

## Core Design Constraints
- Store UTC datetimes in database.
- Daily digest schedule semantics based on America/New_York calendar day.
- Recommendation core isolated in `backend/app/recommend/model.py`.
- Manual dataset import/export for train/validation workflows.
- Apache License 2.0 repository-wide.
