---
name: container-optimization
description: >
  Container optimization skill for LearningOS. Covers multi-stage builds, layer caching,
  Alpine images, Docker Buildx, image versioning, security scanning, and non-root users.
  Activate when optimizing Dockerfiles, reducing image size, improving build speed,
  or adding security scanning. Reference: docs/academy/skills/04-container-optimization.md
---

# Container Optimization Skill

When optimizing Docker images in LearningOS, follow these instructions.

## Optimization Priorities

1. **Size**: Smaller images = faster pulls, less storage cost, smaller attack surface
2. **Speed**: Layer caching + build order = faster CI and deploys
3. **Security**: Minimal base + non-root + CVE scanning = reduced risk

## Techniques (Apply in Order)

### 1. Multi-Stage Builds

Frontend (already done ✅):
```dockerfile
FROM node:20-alpine AS builder
# ... build ...
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

Backend (to optimize):
```dockerfile
FROM python:3.12-slim AS builder
# ... install deps ...
FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
```

### 2. Layer Cache Order

```dockerfile
COPY requirements.txt .           # Changes rarely
RUN pip install -r requirements.txt  # Cached when deps unchanged
COPY . .                          # Changes on every commit
```

### 3. Alpine / Slim Base Images

Prefer: `python:3.12-slim` or `node:20-alpine`
Avoid: `python:3.12` (full Debian — huge)

### 4. Non-Root User

```dockerfile
RUN addgroup --system app && adduser --system --ingroup app app
USER app
```

### 5. Image Versioning

Tag with git SHA for traceability:
```
learningos-backend:abc123f
learningos-frontend:abc123f
```

Never rely on `:latest` in production.

### 6. Security Scanning

Use Trivy in CI:
```yaml
- uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    exit-code: 1
    severity: CRITICAL,HIGH
```

## Buildx in GitHub Actions

```yaml
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v6
  with:
    context: ./frontend
    push: false
    tags: learningos-frontend:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Deep Reference

Read `docs/academy/skills/04-container-optimization.md` for complete guide.
