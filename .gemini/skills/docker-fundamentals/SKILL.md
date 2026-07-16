---
name: docker-fundamentals
description: >
  Docker containerization skill for LearningOS. Covers images, containers, Compose,
  networking, volumes, health checks, multi-stage builds, and production architecture.
  Activate when working on Dockerfiles, docker-compose.yml, container builds, or
  any containerization task. Reference: docs/academy/skills/01-docker.md
---

# Docker Fundamentals Skill

When working with Docker in LearningOS, follow these instructions.

## Key Principles

1. **Multi-stage builds** for frontend (builder → nginx). Backend may not need multi-stage since Python doesn't compile to static files.
2. **Layer caching order**: Copy dependency manifests first (`package.json`, `requirements.txt`), install, THEN copy source code.
3. **`npm ci` not `npm install`** in Dockerfiles — deterministic, reproducible builds.
4. **Service names for networking** — containers communicate via Docker DNS (e.g., `postgres:5432`), never `localhost`.
5. **Named volumes** for persistent data (PostgreSQL). Stateless services (backend, frontend) need no volumes.
6. **Health checks** on database services — use `pg_isready` so `depends_on` with `condition: service_healthy` works.
7. **`.dockerignore`** must exclude `node_modules`, `.git`, `__pycache__`, `.env`.

## Production Mapping

Always mention production equivalents when teaching:

| Local (Compose) | Production (AWS) |
|-----------------|------------------|
| `postgres` service | Amazon RDS |
| Docker network | VPC + private subnets |
| Port mapping | ALB target group |
| `.env` file | AWS Secrets Manager |

## Validation Checklist

Before any Docker change is complete:

```bash
docker compose config              # Validate compose syntax
docker compose build               # Build all images
docker compose up -d               # Start services
docker compose ps                  # Verify all healthy
docker compose logs <service>      # Check for errors
```

## Common Mistakes to Watch For

- Using `localhost` between containers → use service names
- Missing `.dockerignore` → bloated build context
- Single-stage frontend build → use multi-stage with nginx
- No health check on postgres → backend may start before DB ready
- `COPY . .` before dependency install → cache invalidation on every code change

## Deep Reference

Read `docs/academy/skills/01-docker.md` for complete Docker guide.
