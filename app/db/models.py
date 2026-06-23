from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class SourceType(StrEnum):
    KEYWORD = "keyword"
    HASHTAG = "hashtag"
    ACCOUNT = "account"


class Platform(StrEnum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    OTHER = "other"


class VideoStatus(StrEnum):
    DISCOVERED = "discovered"
    QUEUED = "queued"
    DOWNLOADED = "downloaded"
    FAILED = "failed"


class CollectionRunStatus(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid4().hex)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    platform: Mapped[Platform] = mapped_column(Enum(Platform), nullable=False)
    value: Mapped[str] = mapped_column(String(512), nullable=False)
    region_code: Mapped[str] = mapped_column(String(8), nullable=False, default="KZ")
    language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    videos: Mapped[list["Video"]] = relationship(back_populates="source")

    __table_args__ = (UniqueConstraint("source_type", "platform", "value", name="uq_sources_identity"),)


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid4().hex)
    source_id: Mapped[str | None] = mapped_column(ForeignKey("sources.id"), nullable=True)
    platform: Mapped[Platform] = mapped_column(Enum(Platform), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    caption: Mapped[str | None] = mapped_column(Text, nullable=True)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    status: Mapped[VideoStatus] = mapped_column(Enum(VideoStatus), nullable=False, default=VideoStatus.DISCOVERED)

    source: Mapped[Source | None] = relationship(back_populates="videos")
    raw_metadata: Mapped[list["RawMetadata"]] = relationship(back_populates="video")


class RawMetadata(Base):
    __tablename__ = "raw_metadata"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid4().hex)
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.id"), nullable=False)
    collector: Mapped[str] = mapped_column(String(128), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    video: Mapped[Video] = relationship(back_populates="raw_metadata")


class ApiRateLimit(Base):
    __tablename__ = "api_rate_limits"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid4().hex)
    platform: Mapped[Platform] = mapped_column(Enum(Platform), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    remaining: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reset_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    retry_after_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    __table_args__ = (UniqueConstraint("platform", "endpoint", name="uq_api_rate_limits_identity"),)


class CollectionRun(Base):
    __tablename__ = "collection_runs"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid4().hex)
    source_id: Mapped[str | None] = mapped_column(ForeignKey("sources.id"), nullable=True)
    platform: Mapped[Platform] = mapped_column(Enum(Platform), nullable=False)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    query_value: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[CollectionRunStatus] = mapped_column(
        Enum(CollectionRunStatus),
        nullable=False,
        default=CollectionRunStatus.STARTED,
    )
    items_found: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
