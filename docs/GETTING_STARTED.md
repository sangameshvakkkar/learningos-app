# Getting Started with LearningOS

Welcome to **LearningOS**! This guide explains what the application is about and how to get it running on your local machine for development and learning.

## What is LearningOS?

LearningOS is a production-quality learning platform designed to teach Cloud and DevOps concepts. It acts as both the **subject of learning** (a real-world codebase you can deploy, monitor, and scale) and the **medium of learning** (it hosts courses about Docker, Kubernetes, CI/CD, and AWS).

### Key Features
- **Course Catalog**: Browse courses categorized by difficulty and topic.
- **Lesson Viewer**: Read through rich, markdown-based lessons.
- **Progress Tracking**: Keep track of your enrollments and completed lessons.
- **Authentication**: JWT-based user registration and login.

### Tech Stack
- **Frontend**: React (Vite), TypeScript, Tailwind CSS, React Query, React Router.
- **Backend**: Python, FastAPI, SQLAlchemy 2, Alembic.
- **Database**: PostgreSQL.
- **Infrastructure**: Docker & Docker Compose (for local development).

---

## Local Development Guide

The easiest way to run the application locally is by using Docker Compose. This ensures you have the exact same environment as production without having to install Node, Python, and PostgreSQL manually on your host machine.

### Prerequisites

You only need two things installed on your machine:
1. [Git](https://git-scm.com/)
2. [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)

### 1. Setup Environment Variables

First, you need to set up the local environment variables. We have provided an example file.

```bash
# In the root of the repository, copy the example environment file
cp .env.example .env
```
*(On Windows PowerShell, use `Copy-Item .env.example .env`)*

The default values in `.env` are already configured to work out-of-the-box with Docker Compose.

### 2. Start the Application

Bring up the entire stack (Database, Backend API, and Frontend) using Docker Compose:

```bash
docker compose up --build
```

**What happens when you run this?**
1. Docker pulls the PostgreSQL database image and starts it.
2. Docker builds the Backend container, installs Python dependencies, runs the database migrations (`alembic upgrade head`), and seeds the database with the default courses.
3. Docker builds the Frontend container, installs NPM dependencies, and starts the Vite development server.

### 3. Access the Application

Once the terminal logs show that the containers are running, you can access the different parts of the application in your browser:

- **Frontend App**: [http://localhost:5173](http://localhost:5173)
- **Backend API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Backend Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

### 4. Stopping the Application

To stop the application, you can simply press `Ctrl+C` in the terminal where Docker Compose is running. 

To stop and completely remove the containers (your database data will persist in the Docker volume), run:

```bash
docker compose down
```

If you ever want to wipe the database clean and start fresh, you can remove the volumes:

```bash
docker compose down -v
```

---

## Development Workflow Without Docker (Optional)

If you prefer to run the applications directly on your host OS (for easier debugging in your IDE), you can do so, provided you have Node.js and Python 3.12+ installed. You still need Docker for the PostgreSQL database.

**1. Start the Database**
```bash
docker compose up -d postgres
```

**2. Start the Backend**
```bash
cd backend
python -m venv .venv

# Activate the virtual environment:
# On Windows: .venv\Scripts\activate
# On Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**3. Start the Frontend**
```bash
cd frontend
npm install
npm run dev
```
