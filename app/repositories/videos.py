from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.collectors.api_collector import ApiVideo
from app.db.models import Platform, RawMetadata, Source, Video, VideoStatus


def save_api_video(session: Session, source: Source, api_video: ApiVideo, collector: str) -> bool:
    existing = session.scalar(select(Video).where(Video.url == api_video.url))
    if existing is None:
        video = Video(
            source_id=source.id,
            platform=Platform.TIKTOK,
            url=api_video.url,
            author=api_video.author,
            caption=api_video.caption,
            posted_at=_parse_tiktok_create_time(api_video.raw.get("create_time")),
            status=VideoStatus.DISCOVERED,
        )
        session.add(video)
        session.flush()
        created = True
    else:
        video = existing
        created = False

    session.add(RawMetadata(video_id=video.id, collector=collector, payload=api_video.raw))
    return created


def _parse_tiktok_create_time(value: object) -> datetime | None:
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(int(value), tz=UTC)
    except (TypeError, ValueError, OSError):
        return None
