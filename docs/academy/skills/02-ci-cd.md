# Skill 02: CI/CD

> Continuous Integration and Continuous Delivery — automating quality and deployment

## Status: ✅ Learned (Sprint 5)

## Why CI/CD Exists

**Business Problem**: "We deployed on Friday and everything broke. Nobody knows which change caused it."

CI/CD solves: manual testing gaps, integration failures, deployment fear, slow feedback loops.

## Definitions

### Continuous Integration (CI)

Every code change is automatically:
1. Built
2. Tested
3. Validated

Against the main branch. **Every. Single. Change.**

### Continuous Delivery (CD)

Every validated change is **ready to deploy** at the push of a button.

### Continuous Deployment

Every validated change is **automatically deployed** to production. No human approval needed.

```
CI ──────────────► CD ──────────────► Continuous Deployment
"Does it build?"   "Can we deploy?"   "It's already deployed."
```

Most teams start with CI + CD. Continuous Deployment requires high test confidence.

## Pipeline Architecture

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Lint    │───▶│  Test    │───▶│  Build   │───▶│  Deploy  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
   Fail Fast       Quality        Artifact        Release
   (seconds)       Gate           Creation
```

### Key Principles

#### Fail Fast

Put the cheapest, fastest checks first:

```
Lint (5s) → Unit Tests (30s) → Build (2m) → Integration Tests (5m) → Deploy (3m)
```

If linting fails, why waste time building? Every stage is a **quality gate**.

#### Build Once, Deploy Many

```
❌ Wrong: Build for staging, then build again for production
✅ Right: Build once → deploy to staging → promote same artifact to production
```

Same artifact, different configuration. This guarantees what you tested is what you deploy.

#### Deterministic Builds

```bash
npm ci          # ✅ Uses lock file exactly — reproducible
npm install     # ❌ May update dependencies — non-deterministic
pip freeze      # ✅ Pin exact versions
pip install     # ⚠️  May resolve differently tomorrow
```

## Quality Gates

A quality gate is a check that must pass before the pipeline continues:

| Gate | Purpose | Tool |
|------|---------|------|
| Linting | Code style and errors | ESLint, Ruff, Flake8 |
| Unit tests | Logic correctness | Jest, Pytest |
| Build | Compilation succeeds | `npm run build`, `docker build` |
| Security scan | Known vulnerabilities | Trivy, Snyk |
| Coverage | Enough tests | Istanbul, Coverage.py |

## Pipeline vs Workflow

```
Pipeline = The entire automated process from code to production
Workflow = A specific automation file (e.g., .github/workflows/ci.yml)
Job      = A unit of work within a workflow (e.g., "lint", "build")
Step     = A single command within a job
```

## Business Value

| Without CI/CD | With CI/CD |
|--------------|-----------|
| "Did anyone test this?" | Every PR is automatically validated |
| Deploy takes hours | Deploy takes minutes |
| Bugs found in production | Bugs found before merge |
| Fear of deploying | Confidence in every release |
| Manual repetitive work | Automated, consistent process |

## LearningOS Pipeline

Current state:
```
PR to main → frontend-validation (checkout → npm ci → build → lint)
```

Sprint 6 target:
```
PR to main
  ├── frontend-validation (lint → build)
  ├── backend-validation (lint → test)
  └── docker-build (build frontend image, build backend image)
```

Sprint 7+ target:
```
PR to main → validate → build → scan → push to ECR → deploy to ECS
```

## Key Takeaway

CI/CD is not a tool — it's a **practice**. GitHub Actions, Jenkins, GitLab CI are implementations. The principle is: *automate everything that humans do inconsistently.*
