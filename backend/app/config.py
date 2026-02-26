# Copyright 2026 ScholarSignal Contributors
# Licensed under the Apache License, Version 2.0.
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    admin_token: str = Field(default="change-me", alias="ADMIN_TOKEN")
    arxiv_categories: str = Field(default="cs.AI,cs.CL,cs.LG", alias="ARXIV_CATEGORIES")
    digest_tz: str = Field(default="America/New_York", alias="DIGEST_TZ")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")

    class Config:
        env_file = ".env"


settings = Settings()
