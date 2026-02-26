# Copyright 2026 ScholarSignal Contributors
# Licensed under the Apache License, Version 2.0.
from fastapi import FastAPI

from app.api import admin, digests, events, health, papers, preferences

app = FastAPI(title="ScholarSignal")
app.include_router(health.router, prefix="/api/v1")
app.include_router(papers.router, prefix="/api/v1")
app.include_router(digests.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
app.include_router(preferences.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
