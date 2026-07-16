# Skill 01: Docker

> Containerization — packaging applications so they run the same everywhere

## Status: ✅ Learned (Sprint 4)

## Why Docker Exists

**Business Problem**: "It works on my machine" — the most expensive sentence in software engineering.

Docker solves: environment consistency, dependency isolation, reproducible deployments.

## Core Concepts

### Images vs Containers

```
Image    = Blueprint (read-only, versioned, shareable)
Container = Running instance of an image (ephemeral, writable layer)
```

An image is like a class. A container is like an object. You can create many containers from one image.

### Dockerfile

A Dockerfile is a recipe for building an image:

```dockerfile
FROM node:20-alpine          # Base image (start from here)
WORKDIR /app                 # Set working directory
COPY package.json ./         # Copy dependency manifest
RUN npm ci                   # Install dependencies
COPY . .                     # Copy application code
RUN npm run build            # Build the application
CMD ["node", "server.js"]    # Default command when container starts
```

### Build Context

Everything in the directory you run `docker build` from is the "build context" — it gets sent to the Docker daemon. Use `.dockerignore` to exclude files (like `node_modules`).

### Layer Caching

Each instruction creates a layer. Docker caches layers. **Order matters**:

```dockerfile
# ✅ Good: Dependencies change less often than code
COPY package.json package-lock.json ./
RUN npm ci
COPY . .

# ❌ Bad: Every code change invalidates the npm ci cache
COPY . .
RUN npm ci
```

**Rule**: Copy things that change least first.

### Multi-Stage Builds

Use multiple `FROM` statements to keep final images small:

```dockerfile
# Stage 1: Build (large image with build tools)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (tiny image with only output)
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

**Why?** Build tools (npm, gcc, etc.) don't belong in production. Multi-stage cuts image size by 10-50x.

## Docker Compose

Compose runs multiple containers as a single application:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data    # Persistent!
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s

  backend:
    build: ./backend
    depends_on:
      postgres:
        condition: service_healthy               # Wait for DB
    environment:
      DATABASE_URL: postgresql://...@postgres:5432/...
      #                                  ^^^^^^^^
      #                           Service name, NOT localhost!

volumes:
  postgres_data:    # Named volume survives container restarts
```

## Critical Concepts

### Networking

- Containers in the same Compose network communicate via **service names**
- `localhost` inside a container means *that container*, not the host
- `postgres:5432` works because Docker DNS resolves service names

### Volumes

- **Named volumes**: Persist data across container restarts (databases)
- **Bind mounts**: Map host directory into container (development)
- Backend/frontend don't need persistent storage — they're stateless

### Health Checks

- Compose `depends_on` with `condition: service_healthy` ensures startup order
- Without health checks, backend might start before database is ready

## Production Thinking

| Local (Compose) | Production (AWS) |
|-----------------|------------------|
| All on one machine | Services on separate machines |
| `postgres` service | Amazon RDS (managed) |
| Docker network | VPC + private subnets |
| Port mapping `-p` | Load balancer |
| `.env` file | AWS Secrets Manager |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `localhost` between containers | Use service names |
| `npm install` in Dockerfile | Use `npm ci` (deterministic) |
| No `.dockerignore` | Exclude `node_modules`, `.git`, etc. |
| Single-stage for frontend | Multi-stage: builder → nginx |
| No health checks on database | Add `pg_isready` health check |
| Storing data in container filesystem | Use named volumes |

## Commands Reference

```bash
docker build -t myapp .              # Build image
docker run -p 8080:80 myapp          # Run container
docker compose up --build            # Start all services
docker compose down -v               # Stop and remove volumes
docker compose logs backend          # View service logs
docker ps                            # List running containers
docker exec -it <id> sh              # Shell into container
docker images                        # List local images
```

## LearningOS Application

- Frontend: Multi-stage (builder → nginx) ✅
- Backend: Single-stage (to be improved in Sprint 6)
- PostgreSQL: Uses named volume for persistence ✅
- Networking: Service name resolution ✅
- Health checks: PostgreSQL `pg_isready` ✅
