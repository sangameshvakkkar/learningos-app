# LearningOS Future Prompt

You are the Application Team for LearningOS.

Continue developing the LearningOS repository as a production-quality application while preserving the existing architecture.

## Project

LearningOS is a learning workspace starter application.

Current release: v0.1

## Tech Stack

Frontend:

- React
- Vite
- TypeScript
- Tailwind CSS
- React Router
- Axios
- React Query
- React Hook Form
- Zod

Backend:

- FastAPI
- Python 3.12
- SQLAlchemy 2
- Alembic
- PostgreSQL
- JWT Authentication
- Pydantic v2

Database:

- PostgreSQL

## Current Architecture

```text
frontend/
backend/
database/
docs/
docker/
```

## Existing Features

Frontend:

- Landing Page
- Login
- Register
- Dashboard
- Course Catalog
- Profile
- Sidebar
- Navbar
- Dark Mode

Backend:

- Authentication
- Users
- Courses
- Enrollments
- Health Endpoint
- Swagger

Database:

- `users`
- `courses`
- `enrollments`

Infrastructure:

- Dockerfile for frontend
- Dockerfile for backend
- `docker-compose.yml`
- `.env.example`
- README

## Development Instructions

Before changing code:

1. Read `context.md`, `README.md`, and `docs/ARCHITECTURE.md`.
2. Inspect the existing folder structure and follow current patterns.
3. Keep changes scoped to the requested feature or fix.

When implementing:

1. Use clean architecture boundaries already present in the repo.
2. Add backend behavior through models, schemas, services, and routers as appropriate.
3. Add frontend behavior through API clients, feature components, pages, and shared UI components as appropriate.
4. Update Alembic migrations for database schema changes.
5. Update docs and `.env.example` when configuration or run steps change.

Validation checklist:

```bash
cd frontend
npm install
npm run build
npm run lint
```

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m compileall app
```

```bash
docker compose config
```

## Constraints

Do not implement unless explicitly requested:

- Kubernetes
- Terraform
- AWS infrastructure
- CI/CD

Keep Release v0.1 starter-friendly and locally runnable.
