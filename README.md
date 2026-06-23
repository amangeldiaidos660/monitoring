# AI Media Watch

Server-first MVP for continuous social video collection and preparation for analysis.

## Current Scope

Stage 1 infrastructure:

- FastAPI API container.
- Celery worker and Celery Beat scheduler.
- Redis broker/result backend.
- PostgreSQL metadata database.
- MinIO S3-compatible object storage.
- Playwright browser foundation with proxy rotation configuration.
- Official API collector skeletons for TikTok Research API and Instagram Graph API.

Local installation is not required for the intended workflow. Commit this project to GitHub, then deploy it to a DigitalOcean Droplet with Docker Compose.

## Services

- `api`: FastAPI service.
- `worker`: Celery background worker.
- `beat`: periodic Celery scheduler.
- `postgres`: metadata storage.
- `redis`: queue broker.
- `minio`: object storage for future video/audio/frame assets.

## Server Run

On the server:

```bash
cp .env.example .env
docker compose up -d --build
```

Health check:

```text
GET http://SERVER_IP:8000/health
```

## Next Implementation Steps

1. Add DB migrations.
2. Implement keyword and account source CRUD.
3. Connect official TikTok and Instagram API clients.
4. Implement Playwright session storage and login flow.
5. Add real collection tasks and persistence.
6. Add Grafana/Prometheus logging stack after first successful collection run.

