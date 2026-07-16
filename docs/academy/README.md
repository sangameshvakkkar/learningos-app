# LearningOS Academy

> A project-driven mentorship: Cloud Engineer → DevOps Engineer → Cloud Architect

## What Is This?

LearningOS Academy is a structured learning program that teaches Cloud and DevOps engineering by building and operating a real application — LearningOS itself. Instead of isolated tutorials, every concept is tied to a business problem, a Jira story, and a hands-on implementation.

## Philosophy

```
"Solve business problems first; choose tools second."
```

- **Project-first**: Technology emerges as solutions to real engineering problems
- **Production mindset**: Every decision considers reliability, security, and scale
- **Fail-forward**: Every failure is a learning opportunity, not a setback
- **Platform thinking**: Build systems that enable other engineers

## Academy Structure

```text
docs/academy/
├── README.md                  ← You are here
├── PROGRESS.md                ← Current status and sprint tracker
├── MENTORSHIP_GUIDE.md        ← How this mentorship works
│
├── skills/                    ← Technology skill guides
│   ├── 01-docker.md
│   ├── 02-ci-cd.md
│   ├── 03-github-actions.md
│   ├── 04-container-optimization.md
│   ├── 05-aws-fundamentals.md
│   ├── 06-terraform.md
│   ├── 07-kubernetes.md
│   ├── 08-monitoring.md
│   └── 09-security.md
│
├── sprints/                   ← Sprint-by-sprint execution plans
│   ├── sprint-06-docker-build-pipeline.md
│   ├── sprint-07-ecr-ecs-deployment.md
│   ├── sprint-08-terraform-iac.md
│   ├── sprint-09-kubernetes.md
│   ├── sprint-10-monitoring.md
│   ├── sprint-11-security.md
│   └── sprint-12-capstone.md
│
└── references/                ← Architecture decisions and patterns
    ├── pipeline-architecture.md
    ├── aws-architecture.md
    └── debugging-playbook.md
```

## Quick Start

1. Read [MENTORSHIP_GUIDE.md](./MENTORSHIP_GUIDE.md) — understand how this program works
2. Check [PROGRESS.md](./PROGRESS.md) — see where you are
3. Open current sprint in `sprints/` — follow the instructions
4. Reference `skills/` — when you need deeper understanding of a technology

## Learning Path Overview

| Sprint | Focus | Key Skills | Business Problem |
|--------|-------|------------|-----------------|
| 1–3 | ✅ Foundation | Agile, Git, Repo Structure | "How do real teams organize?" |
| 4 | ✅ Containers | Docker, Compose, Networking | "How do we run locally without 'works on my machine'?" |
| 5 | ✅ CI Pipeline | GitHub Actions, Linting, Builds | "How do we catch bugs before merge?" |
| **6** | **🔄 Current** | **Docker in CI, Multi-stage, Caching** | **"How do we know Docker images build before merge?"** |
| 7 | ⬜ Cloud Deploy | ECR, ECS, ALB, IAM | "How do we deploy to production?" |
| 8 | ⬜ IaC | Terraform, State, Modules | "How do we make infrastructure reproducible?" |
| 9 | ⬜ Orchestration | Kubernetes, Helm, Ingress | "How do we scale and self-heal?" |
| 10 | ⬜ Observability | Prometheus, Grafana, CloudWatch | "How do we know when things break?" |
| 11 | ⬜ Security | IAM, OIDC, DevSecOps, Scanning | "How do we prevent breaches?" |
| 12 | ⬜ Capstone | Full production architecture | "Can we run LearningOS like a real company?" |

## Mindset Principles

These principles guide every decision in the academy:

1. **Why before How** — Understand the problem before picking a tool
2. **Reproducibility over Convenience** — `npm ci` not `npm install`, IaC not ClickOps
3. **Fail Fast** — Catch errors early in the pipeline, not in production
4. **Build Once, Deploy Many** — Same artifact across environments
5. **Separation of Concerns** — Validation ≠ Packaging ≠ Deployment
6. **Least Privilege** — Minimum permissions, maximum security
7. **Observable by Default** — If you can't measure it, you can't manage it
8. **Automate Standards** — Use CI/CD to enforce what humans forget
