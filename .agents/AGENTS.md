# LearningOS Project Rules

This file contains all project-level rules and context for AI agents working on the **LearningOS MVP** project.

---

## 1. Budget Constraint (STRICT)

- **Maximum Cloud Budget:** ₹200 INR (~$2.40 USD) per month. **No exceptions.**
- **AWS Architecture Strategy:** Must leverage AWS 12-Month Free Tier or Always-Free alternatives.
- **AWS Budget Alert:** Configure AWS Budget alert at ₹150 INR ($1.80 USD) to catch spend before hitting the ceiling.
- **Banned High-Cost Services:**
  - ❌ AWS NAT Gateway (~$32+/month)
  - ❌ AWS Application Load Balancer (~$18-22+/month)
  - ❌ AWS ECS Fargate (beyond free trial compute)
  - ❌ AWS EKS (expensive managed control plane)
- **Approved Free / Zero-Cost Alternatives:**
  - ✅ AWS EC2 `t2.micro` / `t3.micro` (750 hrs/month Free Tier)
  - ✅ Nginx reverse proxy directly on EC2 (replaces paid ALB)
  - ✅ AWS RDS PostgreSQL `db.t3.micro` (750 hrs/month Free Tier)
  - ✅ Free managed PostgreSQL alternatives: Neon, Supabase, Render
  - ✅ Oracle Cloud Always Free tier (4 OCPUs, 24 GB RAM) if AWS free tier expires
  - ✅ Amazon ECR (500MB free storage per month)
  - ✅ GitHub Actions (2,000 min/month free for public repos)

---

## 2. Project Identity

- **Project Name:** LearningOS MVP
- **Jira Project Key:** `LSS`
- **Jira Project Space:** LearningOS MVP
- **GitHub Repo:** `sangameshvakkkar/learningos-app`
- **Local dev port:** Frontend → `http://localhost:5173`, Backend API → `http://localhost:8000`

---

## 3. Tech Stack

### Frontend
- **Framework:** React 18 + TypeScript (Vite)
- **Styling:** Tailwind CSS + vanilla CSS
- **Routing:** react-router-dom v6
- **State / Fetching:** @tanstack/react-query v5
- **Forms:** react-hook-form + zod validation
- **Testing:** Vitest + @testing-library/react + jsdom

### Backend
- **Framework:** FastAPI (Python 3.12)
- **ORM:** SQLAlchemy 2.0 (async-compatible sync sessions)
- **DB Migrations:** Alembic
- **Auth:** JWT via python-jose + passlib[bcrypt]
- **Linting:** Ruff
- **Testing:** pytest + pytest-asyncio + httpx (SQLite in-memory test DB)

### Database
- **Production DB:** PostgreSQL 16
- **Local Dev:** PostgreSQL 16 via Docker (via `docker-compose.yml`)
- **Test DB:** SQLite in-memory (`aiosqlite`) — no Postgres needed for tests

### Infrastructure
- **Local Orchestration:** Docker Compose
- **CI/CD:** GitHub Actions
- **Container Registry:** Amazon ECR (free tier)
- **Deployment Target:** AWS EC2 `t2.micro` / `t3.micro` (Free Tier)
- **Reverse Proxy:** Nginx (running on EC2 — replaces paid ALB)
- **Serving:** Nginx (frontend SPA static files + API proxy)
- **IaC:** Terraform

---

## 4. Architecture Decisions

- **Frontend SPA Routing:** All unmatched nginx requests fall through to `index.html` (`try_files $uri $uri/ /index.html`). Required to support react-router browser history routes on page refresh.
- **Docker Compose Ports:** Frontend nginx listens on port `80` inside container, mapped to `5173` on host (`5173:80`).
- **Auth:** JWT-based local auth only. No external OAuth/OIDC providers for user login.
- **API Filtering:** Empty string query parameters are stripped before sending to backend (backend enforces `min_length=1` on `search` param).
- **CI Structure:** 3-job pipeline — `frontend-validation` → `backend-validation` → `docker-build`. Docker build only runs when both validation jobs pass.
- **No NAT Gateway / ALB** in any cloud deployment. Nginx on EC2 handles all reverse proxy duties.

---

## 5. Repository Structure

```
learningos-app/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # FastAPI routers (auth, courses, lessons, users, health)
│   │   ├── db/               # SQLAlchemy engine, session, base
│   │   ├── models/           # ORM models (User, Course, Lesson, LessonProgress, Enrollment)
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── seed.py           # DB seeding (5 courses with lessons)
│   │   └── main.py           # FastAPI app entry point
│   ├── alembic/              # DB migrations
│   ├── tests/                # pytest tests (conftest.py, test_auth.py, test_courses.py)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/              # Axios API clients (courses, auth)
│   │   ├── components/       # Shared UI components (Button, Input, Skeleton, Toast, etc.)
│   │   ├── context/          # React context (AuthContext, ThemeContext)
│   │   ├── features/courses/ # CourseDetailPage, LessonViewerPage, CourseCard
│   │   ├── pages/            # CatalogPage, DashboardPage, LandingPage, LoginPage, etc.
│   │   ├── router.tsx        # React Router config
│   │   └── setupTests.ts     # Vitest test setup
│   ├── nginx.conf            # Custom nginx config for SPA routing
│   ├── Dockerfile            # Multi-stage: node build → nginx serve
│   └── package.json
├── docs/
│   ├── JIRA_BACKLOG.md       # All LSS epics & stories (7 Epics, 37 Stories)
│   ├── GETTING_STARTED.md    # Local setup guide
│   ├── ARCHITECTURE.md       # System architecture overview
│   └── DEVELOPMENT_LOG.md    # Development decisions log
├── .github/workflows/
│   └── ci.yml                # GitHub Actions CI pipeline
├── docker-compose.yml        # Local dev orchestration
└── .agents/AGENTS.md         # This file — project rules for AI agents
```

---

## 6. CI/CD Pipeline Rules

- **Lint → Test → Build → Docker** — strictly sequential.
- Frontend must pass `npm run lint` and `npm run test -- --run` before build.
- Backend must pass `ruff check`, `compileall`, and `pytest` before Docker build.
- Docker build job (`docker-build`) is gated on both validation jobs passing.
- Images tagged with `${{ github.sha }}` (immutable) AND `latest` (mutable).
- Docker layer caching uses `type=gha` GitHub Actions cache backend.
- No image push to ECR yet — push coming in Sprint 2 (LSS-8 / LSS-9) via OIDC.

---

## 7. Jira Backlog Summary (LSS key)

| Epic | Topic | Sprint | Stories |
|------|-------|--------|---------|
| LSS-E1 | Containerization & CI | Sprint 1 | LSS-1 to LSS-6 |
| LSS-E2 | Cloud Infrastructure (AWS Free Tier) | Sprint 2 | LSS-7 to LSS-13 |
| LSS-E3 | Infrastructure as Code (Terraform) | Sprint 3 | LSS-14 to LSS-16 |
| LSS-E4 | Kubernetes (Local + Free Tier) | Sprint 4 | LSS-17 to LSS-19 |
| LSS-E5 | Monitoring & Observability | Sprint 5 | LSS-20 to LSS-23 |
| LSS-E6 | Security | Sprint 6 | LSS-24 to LSS-26 |
| LSS-E7 | Architecture & Capstone | Sprint 7 | LSS-27 to LSS-30 |

Full backlog details: `docs/JIRA_BACKLOG.md`

---

## 8. Completed Work (Track A — App Gap-Fill)

All baseline application features are DONE before DevOps track starts:
- ✅ Backend models: `Lesson`, `LessonProgress`, `Enrollment`
- ✅ Alembic migrations applied and seeding works
- ✅ API endpoints: courses, lessons, enrollments, lesson progress
- ✅ Frontend pages: CatalogPage (search/filter), DashboardPage, CourseDetailPage, LessonViewerPage
- ✅ Toast notifications, ErrorBoundary, Axios 401 interceptors
- ✅ Unit tests: backend (pytest + SQLite in-memory), frontend (Vitest + JSDOM)
- ✅ CI pipeline: lint + test + docker-build
- ✅ SPA nginx routing fix (`try_files $uri /index.html`)
- ✅ Empty-string query param strip fix (API filtering)
- ✅ `docs/GETTING_STARTED.md` local setup guide

---

## 9. Current Sprint Status (Sprint 1 — LSS-E1)

| Story | Status |
|-------|--------|
| LSS-1: Docker Build Jobs in CI | ✅ Done |
| LSS-2: Multi-stage Dockerfile Optimization | ✅ Done |
| LSS-3: Docker Layer Caching in CI | ✅ Done |
| LSS-4: Image Versioning Strategy | ✅ Done |
| LSS-5: Container Security Scanning (Trivy) | ✅ Done |
| LSS-6: Backend & Frontend CI Validation | ✅ Done |

---

## 10. AWS Guidance & Rules

- Prefer the AWS MCP Server for AWS interactions — it provides sandboxed execution, observability, and audit logging. If unavailable, use the AWS CLI directly.
- Before starting a task, check whether a relevant AWS skill is available. Load the skill with `retrieve_skill` and prefer its guidance over general knowledge.
- When uncertain about specific AWS details (API parameters, permissions, limits, error codes), verify against documentation rather than guessing. State uncertainty explicitly if you cannot confirm.
- When creating infrastructure, prefer infrastructure-as-code (Terraform / CloudFormation) over direct CLI commands.
- When working with infrastructure, follow AWS Well-Architected Framework principles while maintaining the strict ₹200 INR/month budget constraint.

