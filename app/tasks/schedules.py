from celery.schedules import crontab

from app.config import settings


def beat_schedule() -> dict:
    return {
        "collect-keywords": {
            "task": "app.tasks.collection.collect_keywords",
            "schedule": crontab(minute=f"*/{settings.collect_keywords_interval_minutes}"),
        },
        "monitor-accounts": {
            "task": "app.tasks.collection.monitor_accounts",
            "schedule": crontab(minute=f"*/{settings.monitor_accounts_interval_minutes}"),
        },
    }

