# LearningOS

LearningOS Release v0.1 is a production-quality starter application for a learning workspace.

## Stack

- Frontend: React, Vite, TypeScript, Tailwind CSS, React Router, Axios, React Query, React Hook Form, Zod
- Backend: FastAPI, Python 3.12, SQLAlchemy 2, Alembic, JWT authentication, Pydantic v2
- Database: PostgreSQL
- Local infrastructure: Docker Compose

## Repository Layout

```text
frontend/   React application
backend/    FastAPI application
database/   Reference database schema
docs/       Architecture and release notes
docker/     Reserved for future local Docker assets
```

## Run Locally With Docker

```bash
cp .env.example .env
docker compose up --build
```

Open:

- Frontend: http://localhost:5173
- API health: http://localhost:8000/api/v1/health
- Swagger: http://localhost:8000/docs

The backend runs Alembic migrations and seeds the initial course catalog when the container starts.

## Run Without Docker

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## v0.1 Features

- Landing page
- Login and registration
- JWT-protected dashboard
- Course catalog and enrollment
- Profile page
- Sidebar and navbar
- Dark mode
- Health endpoint and Swagger
- PostgreSQL tables for users, courses, and enrollments

## Scope

This release intentionally does not include Kubernetes, Terraform, AWS, or CI/CD.
