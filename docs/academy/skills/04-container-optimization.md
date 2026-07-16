# Skill 04: Container Optimization

> Making Docker images smaller, faster, and more secure

## Status: 🔄 Sprint 6 (Current)

## Why Optimize?

| Metric | Unoptimized | Optimized | Impact |
|--------|------------|-----------|--------|
| Image size | 1.2 GB | 25 MB | Faster pulls, less storage cost |
| Build time | 8 min | 45 sec | Faster CI, faster deploys |
| Attack surface | Large | Minimal | Fewer CVEs, less risk |
| Layer count | 15 | 6 | Faster transfers |

## Techniques

### 1. Multi-Stage Builds

**Problem**: Build tools (npm, gcc, pip) don't belong in production.

```dockerfile
# Stage 1: Build (large image, has build tools)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build
# Image so far: ~400MB

# Stage 2: Production (tiny, only serves files)
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
# Final image: ~25MB
```

**Result**: Production image has no Node.js, no npm, no source code. Just nginx + static files.

### 2. Layer Caching

Docker caches each layer. When a layer changes, all subsequent layers rebuild.

```dockerfile
# ✅ Optimal order (dependencies change rarely, code changes often)
COPY package.json package-lock.json ./    # Layer 1: cached most of the time
RUN npm ci                                 # Layer 2: cached when deps unchanged
COPY . .                                   # Layer 3: changes on every commit
RUN npm run build                          # Layer 4: rebuilds due to Layer 3

# ❌ Bad order
COPY . .                                   # Everything changes → nothing cached
RUN npm ci                                 # Rebuilds every time
RUN npm run build
```

### 3. Alpine Base Images

```dockerfile
FROM node:20           # ~350MB
FROM node:20-slim      # ~200MB
FROM node:20-alpine    # ~130MB
```

Alpine uses musl libc instead of glibc. Smaller, but occasionally has compatibility issues.

### 4. `.dockerignore`

Exclude files from build context:

```
node_modules
.git
*.md
.env
.vscode
dist
__pycache__
.pytest_cache
```

**Why?** Sending 500MB of `node_modules` to Docker daemon wastes time and may leak secrets.

### 5. Minimize Layers

```dockerfile
# ❌ Multiple RUN = multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# ✅ Single RUN = one layer, with cleanup
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

### 6. Non-Root User

```dockerfile
# Don't run as root in production
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

Running as root inside a container = running as root on the host (in many configurations). **Security risk.**

### 7. Docker Buildx

Docker Buildx is the next-generation builder with advanced features:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t myapp .
```

Features:
- Multi-platform builds (amd64 + arm64)
- Better caching (remote cache, GitHub Actions cache)
- BuildKit backend (parallelized builds)
- Build secrets (don't leak credentials in layers)

### 8. GitHub Actions Cache for Docker

```yaml
- uses: docker/build-push-action@v6
  with:
    context: ./frontend
    push: false
    tags: learningos-frontend:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

Uses GitHub Actions cache backend — layers cached across CI runs.

## Backend Optimization (Sprint 6 Task)

Current backend Dockerfile is single-stage:

```dockerfile
FROM python:3.12-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

**Questions to consider**:
- Does the backend benefit from multi-stage like frontend?
- Python apps don't compile to static files — what's the equivalent optimization?
- Should we separate `alembic upgrade head` from the runtime CMD?

## Image Versioning

```bash
# ❌ Using :latest
docker build -t myapp:latest .    # Which version is this? Who knows!

# ✅ Using git SHA
docker build -t myapp:abc123f .   # Traceable to exact commit

# ✅ Using semantic version + SHA
docker build -t myapp:v1.2.3-abc123f .   # Best of both worlds
```

**Rule**: Every image should be traceable to a specific commit.

## Security Scanning

```bash
# Trivy — scan image for CVEs
trivy image myapp:latest

# In CI:
- uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    exit-code: 1                    # Fail pipeline on vulnerabilities
    severity: CRITICAL,HIGH
```

## LearningOS Sprint 6 Targets

- [ ] Optimize frontend Dockerfile (already multi-stage ✅)
- [ ] Optimize backend Dockerfile (add multi-stage or slim)
- [ ] Add Docker builds to CI pipeline
- [ ] Implement layer caching with `cache-from: type=gha`
- [ ] Add image versioning with `${{ github.sha }}`
- [ ] Add Trivy security scan

## Key Takeaway

Container optimization is about three things: **size** (cost), **speed** (developer experience), and **security** (attack surface). All three improve with the same techniques.
