# LearningOS MVP — Jira Epics & User Stories (Project Key: `LSS`)

This document outlines all Epics, Sprints, and User Stories for the Cloud & DevOps learning roadmap of **LearningOS MVP**.

---

## 🚀 Epic 1: LSS-E1 Containerization & CI (Sprint 1)

### 📌 LSS-1: Docker Build Jobs in CI
- **Issue Type:** Story
- **Sprint:** Sprint 1
- **Priority:** High
- **Labels:** `docker`, `ci`
- **Description:** CI should build frontend + backend Docker images on every PR. Build failure blocks merge. Uses `docker/build-push-action` with Buildx.
- **Acceptance Criteria:**
  - CI builds frontend + backend Docker images on every PR
  - Build fails = PR blocked
  - Uses `docker/build-push-action@v6` with Buildx

### 📌 LSS-2: Multi-stage Dockerfile Optimization
- **Issue Type:** Story
- **Sprint:** Sprint 1
- **Priority:** High
- **Labels:** `docker`, `optimization`
- **Description:** Frontend Dockerfile uses multi-stage build (build stage → nginx serve). Backend uses slim Python base. Final frontend image < 50MB.
- **Acceptance Criteria:**
  - Frontend Dockerfile uses multi-stage (build → nginx)
  - Final frontend image < 50MB
  - Backend uses `python:3.12-slim` base

### 📌 LSS-3: Docker Layer Caching in CI
- **Issue Type:** Story
- **Sprint:** Sprint 1
- **Priority:** Medium
- **Labels:** `docker`, `ci`, `caching`
- **Description:** Configure GitHub Actions cache for Docker layers so repeated CI builds reuse cached layers. Target 50%+ build time reduction.
- **Acceptance Criteria:**
  - Repeated CI builds use cached layers
  - Build time reduced by 50%+
  - Uses `type=gha` cache backend

### 📌 LSS-4: Image Versioning Strategy
- **Issue Type:** Story
- **Sprint:** Sprint 1
- **Priority:** Medium
- **Labels:** `docker`, `versioning`
- **Description:** Define and implement image tagging convention. Images tagged with git SHA + latest. Document the tagging strategy.
- **Acceptance Criteria:**
  - Images tagged with git SHA + latest
  - Documented tagging convention in `docs/`
  - No mutable tags besides `latest`

### 📌 LSS-5: Container Security Scanning
- **Issue Type:** Story
- **Sprint:** Sprint 1
- **Priority:** High
- **Labels:** `docker`, `security`
- **Description:** Integrate Trivy container scanning into CI pipeline. Critical/High vulnerabilities block merge. Results visible in PR.
- **Acceptance Criteria:**
  - Trivy scans images in CI
  - Critical/High vulns block merge
  - Scan results visible in PR comments or annotations

### 📌 LSS-6: Backend & Frontend CI Validation
- **Issue Type:** Story
- **Sprint:** Sprint 1
- **Priority:** Medium
- **Labels:** `ci`, `linting`, `testing`
- **Description:** Add Ruff linting and pytest for backend. Add Vitest for frontend. Run tests and linting in CI before Docker build.
- **Acceptance Criteria:**
  - Ruff linting runs in CI
  - Pytest and Vitest test suites run in CI
  - Failure blocks Docker build step

---

## ☁️ Epic 2: LSS-E2 Cloud Infrastructure (AWS) (Sprint 2)

### 📌 LSS-7: AWS Account & IAM Setup
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** Critical
- **Labels:** `aws`, `iam`, `security`
- **Description:** Set up AWS account with proper security: root MFA enabled, IAM admin user created, no root usage for daily work. AWS CLI configured locally.
- **Acceptance Criteria:**
  - AWS account created
  - Root MFA enabled
  - IAM admin user created (no root usage)
  - AWS CLI configured and tested

### 📌 LSS-8: Amazon ECR Repository
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `ecr`, `docker`
- **Description:** Create ECR repositories for frontend and backend images. Configure lifecycle policy to keep last 10 images. Verify manual push/pull.
- **Acceptance Criteria:**
  - ECR repos created for frontend + backend
  - Lifecycle policy: keep last 10 images
  - Can push/pull images manually

### 📌 LSS-9: CI Push to ECR via OIDC
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `ecr`, `ci`, `oidc`
- **Description:** CI pipeline pushes Docker images to ECR on main branch merge. Uses OIDC federation (no static AWS access keys). Tagged with SHA + latest.
- **Acceptance Criteria:**
  - CI pushes images to ECR on main merge
  - Uses OIDC (no static AWS keys)
  - Images tagged with SHA + latest

### 📌 LSS-10: VPC & Networking
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `vpc`, `networking`
- **Description:** Create VPC with public and private subnets across 2 AZs. NAT gateway for private subnet egress. Security groups for each service tier.
- **Acceptance Criteria:**
  - VPC with public + private subnets (2 AZs)
  - NAT gateway for private subnet egress
  - Security groups defined for each tier

### 📌 LSS-11: ECS Cluster & Task Definitions
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `ecs`, `fargate`
- **Description:** Create ECS Fargate cluster. Define task definitions for frontend and backend. Environment variables sourced from Secrets Manager.
- **Acceptance Criteria:**
  - ECS Fargate cluster created
  - Task definitions for frontend + backend
  - Env vars from Secrets Manager

### 📌 LSS-12: ECS Services & ALB
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `ecs`, `alb`
- **Description:** Create ECS services for frontend and backend. ALB routes traffic to services. Health checks passing. App accessible via ALB DNS name.
- **Acceptance Criteria:**
  - ECS services running frontend + backend
  - ALB routes traffic correctly
  - Health checks passing
  - App accessible via ALB DNS

### 📌 LSS-13: RDS PostgreSQL
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `rds`, `database`
- **Description:** Provision RDS PostgreSQL instance in private subnet. Backend connects to RDS instead of local postgres. Automated backups enabled.
- **Acceptance Criteria:**
  - RDS instance in private subnet
  - Backend connects to RDS
  - Automated backups enabled
  - Connection string via Secrets Manager

### 📌 LSS-14: First Cloud Deployment (End-to-End)
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** Critical
- **Labels:** `aws`, `deployment`, `pipeline`
- **Description:** Push to main triggers full pipeline: CI builds → ECR push → ECS deploys → app live on ALB. Document the complete pipeline flow.
- **Acceptance Criteria:**
  - Push to main → CI → ECR → ECS → live
  - Full pipeline documented
  - Rollback procedure documented

---

## 🏗️ Epic 3: LSS-E3 Infrastructure as Code (Terraform) (Sprint 3)

### 📌 LSS-15: Terraform Setup & Remote State
- **Issue Type:** Story
- **Sprint:** Sprint 3
- **Priority:** High
- **Labels:** `terraform`, `iac`
- **Description:** Initialize Terraform with AWS provider. Configure S3 backend with DynamoDB state locking. State stored remotely, not locally.
- **Acceptance Criteria:**
  - Terraform initialized with AWS provider
  - S3 backend + DynamoDB lock table
  - State stored remotely
  - `terraform init` succeeds

### 📌 LSS-16: VPC Module (Terraform)
- **Issue Type:** Story
- **Sprint:** Sprint 3
- **Priority:** High
- **Labels:** `terraform`, `vpc`, `networking`
- **Description:** Codify VPC, subnets, route tables, NAT gateway as Terraform module. Should match manually-created infrastructure. `terraform plan` shows no drift.
- **Acceptance Criteria:**
  - VPC module creates all networking resources
  - Matches existing manual infrastructure
  - `terraform plan` shows no drift

### 📌 LSS-17: ECS + ALB Module (Terraform)
- **Issue Type:** Story
- **Sprint:** Sprint 3
- **Priority:** High
- **Labels:** `terraform`, `ecs`, `alb`
- **Description:** Codify ECS cluster, services, task definitions, and ALB as Terraform module. Can destroy and recreate without manual steps.
- **Acceptance Criteria:**
  - ECS + ALB fully managed by Terraform
  - Can destroy and recreate cleanly
  - No manual console steps needed

### 📌 LSS-18: RDS Module (Terraform)
- **Issue Type:** Story
- **Sprint:** Sprint 3
- **Priority:** High
- **Labels:** `terraform`, `rds`, `database`
- **Description:** Codify RDS instance as Terraform module. Credentials stored in Secrets Manager (not in state file). Subnet group in private subnets.
- **Acceptance Criteria:**
  - RDS managed by Terraform
  - Credentials in Secrets Manager
  - `prevent_destroy` lifecycle rule enabled
  - Private subnet placement

### 📌 LSS-19: Terraform in CI
- **Issue Type:** Story
- **Sprint:** Sprint 3
- **Priority:** High
- **Labels:** `terraform`, `ci`, `iac`
- **Description:** `terraform plan` runs on PRs with output in PR comment. `terraform apply` runs on main merge with manual approval gate.
- **Acceptance Criteria:**
  - `terraform plan` runs on PRs
  - Plan output visible in PR comment
  - `apply` only on main merge (manual approval)
  - No auto-apply without review

---

## ☸️ Epic 4: LSS-E4 Kubernetes (Sprint 4)

### 📌 LSS-20: Local K8s Cluster
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** High
- **Labels:** `kubernetes`, `local`
- **Description:** Set up local Kubernetes cluster using Minikube or Kind. `kubectl` configured and working. Can deploy a test pod successfully.
- **Acceptance Criteria:**
  - Local K8s cluster running
  - `kubectl` configured and connected
  - Test pod deploys and runs successfully

### 📌 LSS-21: LearningOS Deployments & Services
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** High
- **Labels:** `kubernetes`, `deployments`
- **Description:** Deploy frontend, backend, and postgres as Kubernetes Deployments. Create ClusterIP services. App works within the cluster.
- **Acceptance Criteria:**
  - Frontend + backend + postgres as Deployments
  - ClusterIP services for each
  - App functions correctly in cluster

### 📌 LSS-22: Ingress & External Access
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** High
- **Labels:** `kubernetes`, `ingress`, `networking`
- **Description:** Install ingress controller (nginx). Frontend accessible via ingress. Path-based routing sends `/api` to backend.
- **Acceptance Criteria:**
  - Ingress controller installed
  - Frontend accessible via ingress
  - `/api` routes to backend service

### 📌 LSS-23: ConfigMaps & Secrets
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** Medium
- **Labels:** `kubernetes`, `config`, `secrets`
- **Description:** Move all app configuration to ConfigMaps. Sensitive values stored as K8s Secrets. No hardcoded env vars in deployment manifests.
- **Acceptance Criteria:**
  - App config via ConfigMaps
  - Sensitive values via K8s Secrets
  - No hardcoded values in manifests

### 📌 LSS-24: Helm Charts
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** High
- **Labels:** `kubernetes`, `helm`
- **Description:** Package LearningOS as a Helm chart. Configurable via `values.yaml`. Can install, upgrade, and rollback releases.
- **Acceptance Criteria:**
  - Helm chart created for LearningOS
  - Configurable via `values.yaml`
  - `helm install`/`upgrade`/`rollback` tested

### 📌 LSS-25: HPA & Resource Limits
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** Medium
- **Labels:** `kubernetes`, `scaling`, `performance`
- **Description:** Configure Horizontal Pod Autoscaler for backend (CPU-based). Set resource requests and limits. Verify scaling under simulated load.
- **Acceptance Criteria:**
  - HPA on backend (CPU threshold)
  - Resource requests/limits set on all pods
  - Scales up under load

### 📌 LSS-26: Liveness & Readiness Probes
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** Medium
- **Labels:** `kubernetes`, `health`
- **Description:** Configure readiness probes using `/health` endpoint. Liveness probes restart crashed containers. Test failure scenarios.
- **Acceptance Criteria:**
  - Readiness probe on `/api/v1/health`
  - Liveness probe restarts crashed pods
  - Tested: killed process → pod restarts

---

## 📊 Epic 5: LSS-E5 Monitoring & Observability (Sprint 5)

### 📌 LSS-27: Prometheus Server & Scraping
- **Issue Type:** Story
- **Sprint:** Sprint 5
- **Priority:** High
- **Labels:** `monitoring`, `prometheus`
- **Description:** Deploy Prometheus server. Configure scrape targets for backend. Verify metrics queryable via PromQL in Prometheus UI.
- **Acceptance Criteria:**
  - Prometheus deployed (K8s or Docker)
  - Scrapes backend `/metrics` endpoint
  - Metrics queryable in Prometheus UI

### 📌 LSS-28: Grafana Dashboards
- **Issue Type:** Story
- **Sprint:** Sprint 5
- **Priority:** High
- **Labels:** `monitoring`, `grafana`, `dashboards`
- **Description:** Connect Grafana to Prometheus. Build dashboards: request rate, error rate, latency percentiles, system metrics (CPU/memory).
- **Acceptance Criteria:**
  - Grafana connected to Prometheus
  - Dashboard: request rate, error rate, latency p50/p95/p99
  - Dashboard: CPU and memory usage

### 📌 LSS-29: Structured Logging & Loki
- **Issue Type:** Story
- **Sprint:** Sprint 5
- **Priority:** Medium
- **Labels:** `logging`, `loki`, `grafana`
- **Description:** Switch backend to structured JSON logging. Deploy Loki for log aggregation. Grafana queries logs via Loki data source.
- **Acceptance Criteria:**
  - JSON structured log output
  - Loki deployed and receiving logs
  - Grafana queries logs via Loki

### 📌 LSS-30: Alerting Rules
- **Issue Type:** Story
- **Sprint:** Sprint 5
- **Priority:** High
- **Labels:** `monitoring`, `alerting`
- **Description:** Define alert rules: error rate > 5%, p99 latency > 2s, pod restarts > 3. Configure Alertmanager with notification routing.
- **Acceptance Criteria:**
  - Alert on error rate > 5%
  - Alert on p99 latency > 2s
  - Alertmanager routing configured

---

## 🔐 Epic 6: LSS-E6 Security (Sprint 6)

### 📌 LSS-31: IAM Least Privilege Audit
- **Issue Type:** Story
- **Sprint:** Sprint 6
- **Priority:** High
- **Labels:** `security`, `iam`, `aws`
- **Description:** Review all IAM roles and policies. Scope to minimum required permissions. No wildcard (*) in resource fields.
- **Acceptance Criteria:**
  - All IAM roles audited
  - Policies scoped to minimum permissions
  - No `*` in resource fields

### 📌 LSS-32: Secrets Rotation
- **Issue Type:** Story
- **Sprint:** Sprint 6
- **Priority:** Medium
- **Labels:** `security`, `secrets`, `aws`
- **Description:** DB password rotatable via Secrets Manager. JWT secret rotatable without downtime. Rotation procedures documented and tested.
- **Acceptance Criteria:**
  - DB password rotatable via Secrets Manager
  - JWT secret rotation without downtime
  - Tested: rotated secret → app stays healthy

### 📌 LSS-33: Network Policies
- **Issue Type:** Story
- **Sprint:** Sprint 6
- **Priority:** Medium
- **Labels:** `security`, `kubernetes`, `networking`
- **Description:** K8s NetworkPolicies: backend → postgres only, frontend → backend only. Default deny ingress. Tested with blocked traffic verification.
- **Acceptance Criteria:**
  - NetworkPolicies enforced
  - backend → postgres only
  - frontend → backend only
  - Default deny ingress

---

## 🏛️ Epic 7: LSS-E7 Architecture & Capstone (Sprint 7)

### 📌 LSS-34: Production Architecture Diagram
- **Issue Type:** Story
- **Sprint:** Sprint 7
- **Priority:** High
- **Labels:** `architecture`, `documentation`
- **Description:** Full architecture diagram showing all services, networking, data flow. Review against AWS Well-Architected Framework.
- **Acceptance Criteria:**
  - Architecture diagram created
  - Reviewed against Well-Architected Framework
  - Published in `docs/`

### 📌 LSS-35: Cost Optimization Review
- **Issue Type:** Story
- **Sprint:** Sprint 7
- **Priority:** Medium
- **Labels:** `aws`, `cost`, `optimization`
- **Description:** Review AWS Cost Explorer. Apply right-sizing recommendations. Document estimated monthly cost breakdown by service.
- **Acceptance Criteria:**
  - Cost Explorer reviewed
  - Right-sizing applied where needed
  - Monthly cost documented by service

### 📌 LSS-36: Disaster Recovery Design
- **Issue Type:** Story
- **Sprint:** Sprint 7
- **Priority:** High
- **Labels:** `architecture`, `dr`, `backup`
- **Description:** Define RPO and RTO. Document backup strategy. Test DR runbook for database restoration. Verify recovery works end-to-end.
- **Acceptance Criteria:**
  - RPO and RTO defined
  - Backup strategy documented
  - Database restoration tested and verified

### 📌 LSS-37: Load Testing & Capacity Planning
- **Issue Type:** Story
- **Sprint:** Sprint 7
- **Priority:** Medium
- **Labels:** `performance`, `testing`, `capacity`
- **Description:** Load test with k6 (100 concurrent users). Identify bottlenecks. Document scaling plan with specific thresholds.
- **Acceptance Criteria:**
  - k6 load test (100 concurrent users)
  - Bottlenecks identified and documented
  - Scaling plan with thresholds
