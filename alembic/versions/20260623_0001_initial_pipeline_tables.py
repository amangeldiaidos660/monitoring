"""initial pipeline tables

Revision ID: 20260623_0001
Revises:
Create Date: 2026-06-23
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260623_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

platform_enum = sa.Enum("TIKTOK", "INSTAGRAM", "YOUTUBE", "OTHER", name="platform")
source_type_enum = sa.Enum("KEYWORD", "HASHTAG", "ACCOUNT", name="sourcetype")
video_status_enum = sa.Enum("DISCOVERED", "QUEUED", "DOWNLOADED", "FAILED", name="videostatus")
collection_run_status_enum = sa.Enum("STARTED", "COMPLETED", "FAILED", name="collectionrunstatus")


def upgrade() -> None:
    platform_enum.create(op.get_bind(), checkfirst=True)
    source_type_enum.create(op.get_bind(), checkfirst=True)
    video_status_enum.create(op.get_bind(), checkfirst=True)
    collection_run_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "sources",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("source_type", source_type_enum, nullable=False),
        sa.Column("platform", platform_enum, nullable=False),
        sa.Column("value", sa.String(length=512), nullable=False),
        sa.Column("region_code", sa.String(length=8), nullable=False),
        sa.Column("language", sa.String(length=16), nullable=True),
        sa.Column("category", sa.String(length=64), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_type", "platform", "value", name="uq_sources_identity"),
    )
    op.create_table(
        "videos",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("source_id", sa.String(length=32), nullable=True),
        sa.Column("platform", platform_enum, nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("discovered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", video_status_enum, nullable=False),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    op.create_table(
        "raw_metadata",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("video_id", sa.String(length=32), nullable=False),
        sa.Column("collector", sa.String(length=128), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["video_id"], ["videos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "api_rate_limits",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("platform", platform_enum, nullable=False),
        sa.Column("endpoint", sa.String(length=255), nullable=False),
        sa.Column("remaining", sa.Integer(), nullable=True),
        sa.Column("reset_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("retry_after_seconds", sa.Integer(), nullable=True),
        sa.Column("last_status_code", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("platform", "endpoint", name="uq_api_rate_limits_identity"),
    )
    op.create_table(
        "collection_runs",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("source_id", sa.String(length=32), nullable=True),
        sa.Column("platform", platform_enum, nullable=False),
        sa.Column("source_type", source_type_enum, nullable=False),
        sa.Column("query_value", sa.String(length=512), nullable=False),
        sa.Column("status", collection_run_status_enum, nullable=False),
        sa.Column("items_found", sa.Integer(), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("collection_runs")
    op.drop_table("api_rate_limits")
    op.drop_table("raw_metadata")
    op.drop_table("videos")
    op.drop_table("sources")
    collection_run_status_enum.drop(op.get_bind(), checkfirst=True)
    video_status_enum.drop(op.get_bind(), checkfirst=True)
    source_type_enum.drop(op.get_bind(), checkfirst=True)
    platform_enum.drop(op.get_bind(), checkfirst=True)
