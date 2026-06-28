# LearningOS Architecture

LearningOS v0.1 uses a small clean architecture split by runtime.

## Frontend

The React application lives in `frontend/`.

- `src/api`: Axios clients for backend resources.
- `src/context`: authentication and theme state.
- `src/components`: reusable layout and UI primitives.
- `src/features`: feature-specific components.
- `src/pages`: route-level screens.

## Backend

The FastAPI application lives in `backend/`.

- `app/api`: routers and request dependencies.
- `app/core`: configuration and security primitives.
- `app/db`: SQLAlchemy engine, session, and metadata.
- `app/models`: database models.
- `app/schemas`: Pydantic API contracts.
- `app/services`: business logic and database operations.
- `alembic`: database migrations.

## Database

PostgreSQL stores users, courses, and enrollments. Alembic is the source of truth for schema changes.
