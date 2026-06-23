from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.collection.collect_keywords")
def collect_keywords() -> dict[str, str]:
    return {"status": "scheduled", "task": "collect_keywords"}


@celery_app.task(name="app.tasks.collection.monitor_accounts")
def monitor_accounts() -> dict[str, str]:
    return {"status": "scheduled", "task": "monitor_accounts"}

