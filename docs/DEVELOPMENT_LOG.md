# LearningOS — Development Log

> **Purpose**: Append-only record of major development changes, feature additions, and architectural decisions.
> **Rule**: Never delete entries. Append new sections at the bottom.
> **Jira scope**: Cloud & DevOps tasks only (`LSS` project). Dev work lives here.

---

## Format

Each entry follows this template:

```
## [YYYY-MM-DD] — <Title>

**Type**: Feature | Fix | Refactor | Architecture | Infrastructure
**Area**: Frontend | Backend | Database | Infra | Docs

### What changed
<brief description>

### Why
<business or technical reason>

### Files touched
- path/to/file

### Notes
<anything non-obvious — decisions made, things to revisit>
```

---

## [2026-07-23] — v0.1 Initial Release

**Type**: Feature  
**Area**: Full Stack

### What changed
First production-quality release of LearningOS. Full-stack learning platform with authentication, course catalog, enrollments, and progress tracking.

### Why
Baseline application to learn Cloud & DevOps by building and operating a real system. Application intentionally complete so all future work is infrastructure/platform work, not feature development.

### Stack
- **Frontend**: React + Vite + TypeScript + Tailwind CSS + React Router + Axios + React Query + React Hook Form + Zod
- **Backend**: FastAPI + Python 3.12 + SQLAlchemy 2 + Alembic + Pydantic v2 + JWT auth
- **Database**: PostgreSQL (via Docker Compose locally)
- **Infrastructure**: Docker, Docker Compose, multi-stage Dockerfiles, `.env.example`

### Features
**Frontend screens**: Landing, Login, Register, Dashboard, Course Catalog, Profile, Sidebar, Navbar, Dark Mode  
**Backend APIs**: Auth, Users, Courses, Enrollments, Health endpoint, Swagger UI  
**Database tables**: `users`, `courses`, `enrollments`

### Files touched
- `frontend/` — full React application
- `backend/` — full FastAPI application
- `database/` — reference schema
- `docker-compose.yml` — 3-service stack (postgres, backend, frontend)
- `backend/Dockerfile` — multi-stage Python image
- `frontend/Dockerfile` — multi-stage Node → nginx image
- `.env.example` — environment variable template
- `docs/ARCHITECTURE.md` — architecture overview
- `docs/GETTING_STARTED.md` — local dev guide

### Notes
- App seeded with course data via `backend/app/seed.py`
- Local run: `docker compose up --build` → frontend on :5173, backend on :8000
- Alembic manages all schema migrations
- `SECRET_KEY` must be changed in production

---

<!-- APPEND NEW ENTRIES BELOW THIS LINE -->
