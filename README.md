# AI Media Watch

Server-first MVP for continuous social video collection and preparation for analysis.

## Current Scope

Stage 1 infrastructure:

- FastAPI API container.
- Celery worker and Celery Beat scheduler.
- Redis broker/result backend.
- PostgreSQL metadata database.
- MinIO S3-compatible object storage.
- Playwright browser foundation with controlled proxy configuration.
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

The API port is bound to localhost only. Check it from the server:

```bash
curl http://127.0.0.1:8000/health
```

For temporary access from your machine, use an SSH tunnel:

```bash
ssh -L 8000:127.0.0.1:8000 root@SERVER_IP
```

Then open:

```text
http://127.0.0.1:8000/health
```

PostgreSQL, Redis, and MinIO are intentionally not published to the public internet.

## Fast Production Deploy

Production uses a prebuilt GHCR image. The server should not reinstall Python dependencies or rebuild the application image on every deploy.

```bash
docker compose -f docker-compose.prod.yml pull api worker beat
docker compose -f docker-compose.prod.yml up -d --no-build
```

Required GitHub Actions secrets:

- `DO_HOST`: Droplet IP address.
- `DO_USER`: SSH username, usually `root`.
- `DO_SSH_KEY`: private SSH key allowed to access the Droplet.

## Next Implementation Steps

1. Add DB migrations.
2. Implement keyword and account source CRUD.
3. Connect official TikTok and Instagram API clients.
4. Implement authorized browser session support where platform terms allow it.
5. Add real collection tasks and persistence.
6. Add Grafana/Prometheus logging stack after first successful collection run.
