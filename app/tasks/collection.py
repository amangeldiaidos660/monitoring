from datetime import UTC, datetime
import asyncio

from app.collectors.tiktok_research import TikTokResearchApiError, TikTokResearchCollector
from app.db.models import CollectionRun, CollectionRunStatus, Platform, Source, SourceType
from app.db.session import SessionLocal
from app.repositories.rate_limits import save_api_rate_limit_state
from app.repositories.sources import list_active_tiktok_sources
from app.repositories.videos import save_api_video
from app.tasks.celery_app import celery_app

DEFAULT_SOURCE_LIMIT = 20


@celery_app.task(name="app.tasks.collection.collect_keywords")
def collect_keywords(limit: int = DEFAULT_SOURCE_LIMIT) -> dict[str, int | str]:
    return _collect_sources([SourceType.KEYWORD, SourceType.HASHTAG], limit)


@celery_app.task(name="app.tasks.collection.monitor_accounts")
def monitor_accounts(limit: int = DEFAULT_SOURCE_LIMIT) -> dict[str, int | str]:
    return _collect_sources([SourceType.ACCOUNT], limit)


def _collect_sources(source_types: list[SourceType], limit: int) -> dict[str, int | str]:
    collector = TikTokResearchCollector()
    processed = 0
    discovered = 0
    failed = 0

    with SessionLocal() as session:
        sources = list_active_tiktok_sources(session, source_types=source_types, limit=limit)
        for source in sources:
            processed += 1
            try:
                discovered += asyncio.run(_collect_one_source(session, collector, source))
            except TikTokResearchApiError as error:
                save_api_rate_limit_state(
                    session,
                    platform=Platform.TIKTOK,
                    endpoint="/v2/research/video/query/",
                    status_code=error.status_code,
                    retry_after_seconds=error.retry_after_seconds,
                )
                session.commit()
                failed += 1
            except Exception:
                failed += 1

    return {
        "status": "completed",
        "processed_sources": processed,
        "new_videos": discovered,
        "failed_sources": failed,
    }


async def _collect_one_source(session, collector: TikTokResearchCollector, source: Source) -> int:
    run = CollectionRun(
        source_id=source.id,
        platform=Platform.TIKTOK,
        source_type=source.source_type,
        query_value=source.value,
        status=CollectionRunStatus.STARTED,
    )
    session.add(run)
    session.commit()

    try:
        if source.source_type == SourceType.KEYWORD:
            videos = await collector.collect_keyword(source.value)
        elif source.source_type == SourceType.HASHTAG:
            videos = await collector.collect_hashtag(source.value)
        elif source.source_type == SourceType.ACCOUNT:
            videos = await collector.collect_account(source.value)
        else:
            videos = []

        new_count = 0
        for video in videos:
            if save_api_video(session, source, video, collector="tiktok_research"):
                new_count += 1
        run.status = CollectionRunStatus.COMPLETED
        run.items_found = len(videos)
        run.finished_at = datetime.now(UTC)
        session.commit()
        return new_count
    except Exception as error:
        run.status = CollectionRunStatus.FAILED
        run.error = f"{type(error).__name__}: {error}"
        run.finished_at = datetime.now(UTC)
        session.commit()
        raise
