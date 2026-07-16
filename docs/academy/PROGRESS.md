# Progress Tracker

> Current status of the LearningOS Academy journey

## Current Sprint: Sprint 6 — Docker Build Pipeline

**Started**: June 26, 2026  
**Current Date**: July 13, 2026  
**Active Story**: LOS-33 — Docker Build Pipeline

---

## Sprint History

### Sprint 1 — Project Kickoff ✅

- [x] Define project vision and goals
- [x] Set up fictional company structure
- [x] Define roles (CTO, Scrum Master, DevOps, etc.)
- [x] Establish learning-by-building approach

**Key Lesson**: Real engineering organizations have structure. Simulate it.

---

### Sprint 2 — Application Planning ✅

- [x] Design Jira project (Epics → Stories → Sub-tasks)
- [x] Define sprint planning process
- [x] Establish story points, priorities, labels
- [x] Define acceptance criteria, DoD, DoR

**Key Lesson**: Every task represents work a real team would perform.

---

### Sprint 3 — Repository Setup ✅

- [x] Create GitHub repository
- [x] Set up Confluence space
- [x] Define branching strategy
- [x] Establish repository structure

**Key Lesson**: Repository is the single source of truth.

---

### Sprint 4 — Docker Platform ✅

- [x] Docker architecture fundamentals
- [x] Images vs Containers
- [x] Docker Compose
- [x] Container networking (service names, not localhost)
- [x] Volumes and persistent storage
- [x] Health checks
- [x] Container lifecycle
- [x] Build context and layer caching
- [x] Production architecture thinking (private subnets for databases)

**Key Lesson**: `localhost` is wrong inside containers. Service names resolve via Docker DNS.

---

### Sprint 5 — GitHub Actions CI ✅ (mostly)

- [x] CI/CD fundamentals and business value
- [x] GitHub Actions: events, workflows, jobs, steps
- [x] Hosted vs self-hosted runners
- [x] `actions/checkout@v4`
- [x] `actions/setup-node`
- [x] `npm ci` (deterministic builds)
- [x] ESLint integration
- [x] Build validation
- [x] Secrets and variables
- [x] Pipeline architecture
- [x] Debugging real pipeline failures
- [x] Fixed missing `package-lock.json` (root cause analysis)
- [ ] Caching (will cover in Sprint 6)
- [ ] Artifacts (will cover in Sprint 6)
- [ ] Matrix builds (planned for later)

**Key Lesson**: When pipeline fails, fix the repo — don't work around it. `npm ci` > `npm install`.

---

### Sprint 6 — Docker Build Pipeline 🔄 IN PROGRESS

- [ ] Add Docker build jobs to CI
- [ ] Multi-stage Dockerfile optimization
- [ ] Docker layer caching in GitHub Actions
- [ ] Image versioning strategy
- [ ] Security scanning (Trivy or similar)
- [ ] Backend CI validation (lint/test)
- [ ] Pipeline architecture: validation → build → scan

**Current Story**: LOS-33 — Pipeline should build frontend and backend Docker images on every PR.

**Business Problem**: "We have zero confidence Docker images build successfully before merge."

---

### Sprint 7 — ECR + ECS Deployment ⬜

- [ ] Amazon ECR (container registry)
- [ ] Push images from CI
- [ ] ECS task definitions
- [ ] ECS service + cluster
- [ ] Application Load Balancer
- [ ] IAM roles for ECS
- [ ] AWS Secrets Manager integration
- [ ] First cloud deployment

---

### Sprint 8 — Terraform (IaC) ⬜

- [ ] Why Infrastructure as Code
- [ ] Terraform basics: providers, resources, state
- [ ] Remote state (S3 + DynamoDB)
- [ ] Modules and composition
- [ ] Terraform for VPC, ECS, ALB, RDS
- [ ] `terraform plan` in CI

---

### Sprint 9 — Kubernetes ⬜

- [ ] Kubernetes architecture
- [ ] Deployments, Services, Ingress
- [ ] ConfigMaps and Secrets
- [ ] Helm charts
- [ ] Horizontal Pod Autoscaling
- [ ] Liveness and readiness probes
- [ ] Migrate LearningOS from ECS to K8s

---

### Sprint 10 — Monitoring & Observability ⬜

- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Loki for log aggregation
- [ ] CloudWatch integration
- [ ] Alerting rules
- [ ] SLOs and SLIs
- [ ] Application instrumentation

---

### Sprint 11 — Security ⬜

- [ ] IAM deep dive
- [ ] OIDC for CI/CD (no static credentials)
- [ ] Container image scanning
- [ ] DevSecOps pipeline
- [ ] Policy as Code (OPA/Kyverno)
- [ ] Network policies
- [ ] Secrets rotation

---

### Sprint 12 — Cloud Architect Capstone ⬜

- [ ] Production-ready LearningOS on AWS
- [ ] End-to-end architecture review
- [ ] Cost optimization
- [ ] Disaster recovery design
- [ ] Architecture diagram
- [ ] Presentation to simulated stakeholders

---

## Mindset Evolution

| Phase | Thinking Style | Example |
|-------|---------------|---------|
| Sprint 1–3 | "What command?" | "How do I create a Dockerfile?" |
| Sprint 4–5 | "Why this way?" | "Why `npm ci` not `npm install`?" |
| Sprint 6+ | "What's the architecture?" | "Should Docker build be a separate pipeline job?" |
| Sprint 9+ | "What are the tradeoffs?" | "ECS vs K8s for our scale?" |
| Sprint 12 | "How do we operate this?" | "What's our SLO and blast radius?" |
