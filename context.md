# LearningOS Context

## Project

LearningOS is a Release v0.1 production-quality starter application for a learning workspace. It is intended to be cloned by another engineering team and run locally with Docker Compose or standard local tooling.

## Scope

This release includes:

- React, Vite, TypeScript, Tailwind CSS frontend.
- React Router, Axios, React Query, React Hook Form, and Zod.
- FastAPI backend using Python 3.12, SQLAlchemy 2, Alembic, JWT authentication, and Pydantic v2.
- PostgreSQL database with `users`, `courses`, and `enrollments`.
- Dockerfiles, Docker Compose, environment examples, architecture notes, and release notes.

This release intentionally excludes:

- Kubernetes
- Terraform
- AWS infrastructure
- CI/CD

## Repository Layout

```text
frontend/   React application
backend/    FastAPI application
database/   Reference database schema
docs/       Architecture and release notes
docker/     Reserved for future local Docker assets
```

## Frontend Notes

The frontend uses:

- `src/api` for Axios API clients.
- `src/context` for auth and theme state.
- `src/components` for reusable layout and UI primitives.
- `src/features` for feature-specific components.
- `src/pages` for route-level screens.

Implemented screens:

- Landing page
- Login
- Register
- Dashboard
- Course Catalog
- Profile

## Backend Notes

The backend uses:

- `app/api` for routers and dependencies.
- `app/core` for configuration and security.
- `app/db` for SQLAlchemy engine, session, and metadata.
- `app/models` for database models.
- `app/schemas` for Pydantic API contracts.
- `app/services` for business logic and database access.
- `alembic` for migrations.

Implemented API areas:

- Authentication
- Users
- Courses
- Enrollments
- Health endpoint
- Swagger docs

## Local Run

```bash
cp .env.example .env
docker compose up --build
```

Open:

- Frontend: `http://localhost:5173`
- Swagger: `http://localhost:8000/docs`
- Health: `http://localhost:8000/api/v1/health`

## Engineering Principles

- Keep the codebase clean, small, and production-oriented.
- Prefer existing folder boundaries before adding new abstractions.
- Keep v0.1 focused on local development and starter functionality.
- Add comments only where they clarify non-obvious decisions.
- Do not add cloud infrastructure, Kubernetes, Terraform, or CI/CD unless a future release explicitly asks for it.
