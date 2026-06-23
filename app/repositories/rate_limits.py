from datetime import UTC, datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.models import ApiRateLimit, Platform


def save_api_rate_limit_state(
    session: Session,
    platform: Platform,
    endpoint: str,
    status_code: int | None,
    retry_after_seconds: int | None = None,
) -> None:
    statement = insert(ApiRateLimit).values(
        platform=platform,
        endpoint=endpoint,
        last_status_code=status_code,
        retry_after_seconds=retry_after_seconds,
        updated_at=datetime.now(UTC),
    )
    statement = statement.on_conflict_do_update(
        constraint="uq_api_rate_limits_identity",
        set_={
            "last_status_code": status_code,
            "retry_after_seconds": retry_after_seconds,
            "updated_at": datetime.now(UTC),
        },
    )
    session.execute(statement)
