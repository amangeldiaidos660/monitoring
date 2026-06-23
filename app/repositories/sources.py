from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.models import Platform, Source, SourceType
from app.seeds.sources import default_tiktok_sources


def seed_tiktok_sources(session: Session) -> int:
    inserted = 0
    for item in default_tiktok_sources():
        now = datetime.now(UTC)
        statement = (
            insert(Source)
            .values(
                source_type=SourceType(item["source_type"]),
                platform=Platform(item["platform"]),
                value=item["value"],
                region_code=item["region_code"],
                priority=100,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            .on_conflict_do_nothing(constraint="uq_sources_identity")
        )
        result = session.execute(statement)
        inserted += result.rowcount or 0
    session.commit()
    return inserted


def list_active_tiktok_sources(session: Session, source_types: list[SourceType], limit: int) -> list[Source]:
    statement = (
        select(Source)
        .where(Source.platform == Platform.TIKTOK)
        .where(Source.is_active.is_(True))
        .where(Source.source_type.in_(source_types))
        .order_by(Source.priority.asc(), Source.created_at.asc())
        .limit(limit)
    )
    return list(session.scalars(statement))
