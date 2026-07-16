---
name: ci-cd-pipelines
description: >
  CI/CD pipeline skill for LearningOS. Covers GitHub Actions workflows, pipeline
  architecture, quality gates, fail-fast ordering, caching, artifacts, and secrets.
  Activate when working on .github/workflows/, pipeline design, or any CI/CD task.
  Reference: docs/academy/skills/02-ci-cd.md and docs/academy/skills/03-github-actions.md
---

# CI/CD Pipeline Skill

When working with CI/CD in LearningOS, follow these instructions.

## Pipeline Design Principles

1. **Fail Fast**: Cheapest checks first. Lint (5s) → Test (30s) → Build (2m) → Docker Build (3m) → Scan (1m).
2. **Separation of Concerns**: Validation ≠ Packaging ≠ Deployment. Use separate jobs.
3. **Build Once, Deploy Many**: Same artifact across all environments. Tag with git SHA.
4. **Deterministic Builds**: `npm ci` not `npm install`. `pip install -r requirements.txt` with pinned versions.
5. **Quality Gates**: Every stage must pass before next. Use `needs:` in GitHub Actions.

## GitHub Actions Patterns

### Job Structure

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  build:
    needs: lint          # Only runs if lint passes
    runs-on: ubuntu-latest
    steps: [...]

  docker:
    needs: [lint, build] # Runs after both pass
    runs-on: ubuntu-latest
    steps: [...]
```

### Required Actions

| Action | Purpose |
|--------|---------|
| `actions/checkout@v4` | Clone repo |
| `actions/setup-node@v4` | Install Node.js |
| `actions/setup-python@v5` | Install Python |
| `actions/cache@v4` | Cache dependencies |
| `docker/setup-buildx-action@v3` | Docker Buildx |
| `docker/build-push-action@v6` | Build/push images |

### Secrets Management

- Never hardcode secrets in YAML
- Use `${{ secrets.NAME }}` for sensitive values
- Use `${{ vars.NAME }}` for non-sensitive config
- GitHub auto-redacts secrets from logs

## LearningOS Pipeline Architecture

```
PR to main
  ├── frontend-validation (lint → build)
  ├── backend-validation (lint → test)
  └── docker-build (needs: validation jobs)
       ├── frontend image
       └── backend image
```

## Validation Checklist

Before merging any pipeline change:

1. Workflow YAML passes `yamllint` or GitHub's syntax checker
2. Pipeline triggers on correct events (`pull_request` to `main`)
3. Jobs use `needs:` for correct ordering
4. Secrets are configured in repo settings
5. Pipeline actually runs successfully on a test PR

## Common Mistakes

- Running `npm install` instead of `npm ci` → non-deterministic
- No `working-directory` for monorepo → commands run in wrong folder
- Missing `needs:` → jobs run in parallel when they should be sequential
- Docker build without caching → slow CI runs
- Not failing pipeline on lint/test errors → broken code merges

## Deep Reference

Read `docs/academy/skills/02-ci-cd.md` and `docs/academy/skills/03-github-actions.md` for complete guides.
