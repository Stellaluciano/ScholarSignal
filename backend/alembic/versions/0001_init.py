"""init"""

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.create_table("users", sa.Column("id", sa.UUID(), primary_key=True), sa.Column("provider", sa.String(32), nullable=False), sa.Column("provider_sub", sa.String(255), nullable=False, unique=True), sa.Column("email", sa.String(255)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("anonymous_users", sa.Column("anon_id", sa.UUID(), primary_key=True), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("papers", sa.Column("arxiv_id", sa.String(), primary_key=True), sa.Column("title", sa.Text(), nullable=False), sa.Column("abstract", sa.Text(), nullable=False), sa.Column("authors", sa.JSON(), nullable=False), sa.Column("categories", sa.JSON(), nullable=False), sa.Column("published_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.Column("abs_url", sa.Text(), nullable=False), sa.Column("pdf_url", sa.Text(), nullable=False), sa.Column("fingerprint_sha256", sa.String(64), nullable=False), sa.Column("embedding", Vector(256)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_papers_fingerprint_sha256", "papers", ["fingerprint_sha256"])
    op.create_table("events", sa.Column("id", sa.UUID(), primary_key=True), sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id")), sa.Column("anon_id", sa.UUID(), sa.ForeignKey("anonymous_users.anon_id")), sa.Column("arxiv_id", sa.String(), sa.ForeignKey("papers.arxiv_id"), nullable=False), sa.Column("event_type", sa.String(32), nullable=False), sa.Column("rank_position", sa.Integer()), sa.Column("source", sa.String(50), nullable=False), sa.Column("dwell_ms", sa.Integer()), sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("daily_digests", sa.Column("id", sa.UUID(), primary_key=True), sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id")), sa.Column("anon_id", sa.UUID(), sa.ForeignKey("anonymous_users.anon_id")), sa.Column("digest_date", sa.Date(), nullable=False), sa.Column("arxiv_ids", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("user_id", "digest_date"), sa.UniqueConstraint("anon_id", "digest_date"))
    op.create_table("model_artifacts", sa.Column("id", sa.UUID(), primary_key=True), sa.Column("version", sa.String(100), nullable=False, unique=True), sa.Column("kind", sa.String(50), nullable=False), sa.Column("path", sa.Text(), nullable=False), sa.Column("metrics", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("preferences", sa.Column("id", sa.UUID(), primary_key=True), sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id")), sa.Column("anon_id", sa.UUID(), sa.ForeignKey("anonymous_users.anon_id")), sa.Column("categories", sa.JSON(), nullable=False), sa.Column("keywords", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))


def downgrade():
    for t in ["preferences", "model_artifacts", "daily_digests", "events", "papers", "anonymous_users", "users"]:
        op.drop_table(t)
