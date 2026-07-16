# Skill 03: GitHub Actions

> GitHub's native CI/CD platform — workflows that run on every push, PR, or schedule

## Status: ✅ Learned (Sprint 5)

## Architecture

```
Event (push, PR, schedule, manual)
  └── Workflow (.github/workflows/*.yml)
        └── Job (runs on a runner)
              └── Step (single action or command)
```

## Core Concepts

### Events (Triggers)

```yaml
on:
  push:
    branches: [main]           # Runs on push to main
  pull_request:
    branches: [main]           # Runs on PR targeting main
  schedule:
    - cron: '0 6 * * 1'        # Every Monday at 6 AM UTC
  workflow_dispatch:            # Manual trigger button
```

### Workflows

A YAML file in `.github/workflows/`. One repo can have many workflows.

```yaml
name: CI Pipeline
on:
  pull_request:
    branches: [main]
```

### Jobs

Jobs run **in parallel by default**. Use `needs:` for dependencies.

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest     # GitHub-hosted runner
    steps: [...]

  build:
    runs-on: ubuntu-latest
    needs: lint                 # Waits for lint to finish
    steps: [...]
```

### Steps

```yaml
steps:
  - name: Checkout code                    # Action (reusable)
    uses: actions/checkout@v4

  - name: Setup Node                       # Action with config
    uses: actions/setup-node@v4
    with:
      node-version: 20

  - name: Install dependencies             # Shell command
    run: npm ci
    working-directory: frontend
```

### Runners

| Type | Description | Use Case |
|------|------------|----------|
| `ubuntu-latest` | GitHub-hosted Linux | Most CI jobs |
| `windows-latest` | GitHub-hosted Windows | Windows-specific builds |
| Self-hosted | Your own machine | Custom hardware, GPU, private network |

## Secrets and Variables

```yaml
# Secrets: encrypted, never logged
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}

# Variables: non-sensitive configuration
env:
  NODE_ENV: ${{ vars.NODE_ENV }}
```

- Secrets are set in GitHub → Settings → Secrets and Variables
- Never hardcode secrets in workflow files
- GitHub automatically redacts secrets from logs

## Marketplace Actions

Reusable actions created by the community:

| Action | Purpose |
|--------|---------|
| `actions/checkout@v4` | Clone repository |
| `actions/setup-node@v4` | Install Node.js |
| `actions/setup-python@v5` | Install Python |
| `actions/cache@v4` | Cache dependencies |
| `docker/setup-buildx-action@v3` | Docker Buildx |
| `docker/build-push-action@v6` | Build/push Docker images |
| `docker/login-action@v3` | Login to container registries |

## Caching (Sprint 6)

Speed up pipelines by caching dependencies:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

Cache invalidates when `package-lock.json` changes. Otherwise, reuses cached `node_modules`.

## Artifacts (Sprint 6)

Save files between jobs or for download:

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: frontend/dist/

# In another job:
- uses: actions/download-artifact@v4
  with:
    name: build-output
```

## Matrix Builds (Future)

Run same job across multiple configurations:

```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
    os: [ubuntu-latest, windows-latest]
```

Generates 6 parallel jobs (3 versions × 2 OS).

## Debugging Workflow Failures

1. **Read the logs** — GitHub Actions shows step-by-step output
2. **Check the failing step** — Red X marks the exact failure
3. **Look for the error message** — Usually in the last 10-20 lines
4. **Reproduce locally** — Run the same commands on your machine
5. **Check environment differences** — Runner OS, Node version, etc.

## LearningOS Current Workflow

```yaml
# .github/workflows/ci.yml
name: LearningOS CI
on:
  pull_request:
    branches: [main]
jobs:
  frontend-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
        working-directory: frontend
      - run: npm run build
        working-directory: frontend
      - run: npm run lint
        working-directory: frontend
```

### What's Missing (Sprint 6 work)

- [ ] Backend validation job
- [ ] Docker build jobs
- [ ] Caching for faster runs
- [ ] Step ordering (lint before build — fail fast)
- [ ] Job dependencies (`needs:`)

## Key Takeaway

GitHub Actions is infrastructure as code for your CI/CD pipeline. The YAML is version-controlled, reviewable, and auditable — just like application code.
