# Runna

Runna is a running assistant platform with:

- FastAPI backend
- PostgreSQL/PostGIS database
- Flutter mobile app
- route generation
- social feed and chat
- accident detection and emergency alerts

## Current status

This repository is scaffolded for Phase 1 from `plan.md`.

Included today:

- backend application skeleton
- Docker setup for backend and PostgreSQL/PostGIS
- environment templates
- Alembic migration scaffolding
- mobile placeholder structure

## Quick start

1. Copy `.env.example` to `.env`.
2. Start infrastructure:

```powershell
docker compose up --build
```

3. Open the API docs:

`http://localhost:8000/docs`

## Notes

- Flutter SDK is not installed in this environment yet, so the mobile app is scaffolded as a placeholder and should be initialized with `flutter create mobile` later.
- OSRM is not enabled in Docker yet; it will be added when route generation is implemented.

