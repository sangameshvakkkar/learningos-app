# LearningOS MVP — Jira Epics & User Stories (Project Key: `LSS`)

> ⚠️ **COST CONSTRAINT RULE**: Maximum cloud spending must NOT exceed **₹200 INR/month (~$2.40 USD)**.
> All cloud architectures in this backlog strictly use **AWS 12-Month Free Tier** (EC2 `t2.micro`/`t3.micro`, RDS Free Tier) and **zero-cost alternatives** (Nginx on EC2 instead of paid ALB, avoiding NAT Gateway charges).

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

## ☁️ Epic 2: LSS-E2 Zero-Cost Cloud Infrastructure (AWS Free Tier) (Sprint 2)

### 📌 LSS-7: AWS Account & Free-Tier Security Setup
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** Critical
- **Labels:** `aws`, `iam`, `security`, `cost-control`
- **Description:** Set up AWS account with Root MFA, IAM Admin user, AWS Budget Alerts set at ₹150 INR ($1.80 USD) to prevent unexpected charges.
- **Acceptance Criteria:**
  - AWS account created & Root MFA enabled
  - IAM admin user created (no root usage)
  - AWS Budget alert set at ₹150 INR ($1.80 USD)
  - AWS CLI configured locally

### 📌 LSS-8: Amazon ECR Repository (Free Tier)
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `ecr`, `docker`
- **Description:** Create ECR repositories for frontend and backend images. Configure lifecycle policy to keep last 5 images to stay under 500MB free storage tier.
- **Acceptance Criteria:**
  - ECR repos created for frontend + backend
  - Lifecycle policy: keep last 5 images (under 500MB free limit)
  - Can push/pull images manually

### 📌 LSS-9: CI Push to ECR via OIDC
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `ecr`, `ci`, `oidc`
- **Description:** CI pipeline pushes Docker images to ECR on main branch merge using free OIDC federation (no static AWS keys).
- **Acceptance Criteria:**
  - CI pushes images to ECR on main merge
  - Uses OIDC (no static AWS keys)
  - Images tagged with SHA + latest

### 📌 LSS-10: Zero-Cost VPC & Security Groups
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `vpc`, `networking`, `zero-cost`
- **Description:** Create standard VPC with Internet Gateway. Avoid NAT Gateway ($32/mo fee!). Use public subnets with tight Security Groups.
- **Acceptance Criteria:**
  - VPC with Internet Gateway (100% Free)
  - NO NAT Gateway created
  - Security Groups restricting HTTP/HTTPS and SSH access

### 📌 LSS-11: Free-Tier EC2 Deployment (t2.micro / t3.micro)
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `ec2`, `docker-compose`, `zero-cost`
- **Description:** Provision AWS Free Tier EC2 instance (`t2.micro`/`t3.micro` — 750 hrs/mo free). Run frontend + backend using Docker Compose and Nginx reverse proxy (avoiding $20/mo ALB fee).
- **Acceptance Criteria:**
  - EC2 `t2.micro` or `t3.micro` instance running (Free Tier)
  - Docker & Docker Compose installed
  - App accessible via EC2 Elastic IP / Public IP
  - Zero ALB/NAT gateway charges incurred

### 📌 LSS-12: Database Setup (RDS Free Tier or Managed Free Postgres)
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** High
- **Labels:** `aws`, `rds`, `database`, `free-tier`
- **Description:** Provision RDS PostgreSQL `db.t3.micro` (750 hrs free tier) or integrate free managed database (Neon / Supabase).
- **Acceptance Criteria:**
  - PostgreSQL database running on AWS RDS Free Tier or Neon/Supabase free tier
  - Backend connects securely via SSL/TLS
  - Zero monthly cost ($0.00 / ₹0)

### 📌 LSS-13: End-to-End Zero-Cost Cloud Deployment Pipeline
- **Issue Type:** Story
- **Sprint:** Sprint 2
- **Priority:** Critical
- **Labels:** `aws`, `deployment`, `pipeline`, `zero-cost`
- **Description:** Automated CI/CD pipeline deploys code changes to EC2 Free Tier automatically upon push to `main`.
- **Acceptance Criteria:**
  - Push to main → CI build → ECR push → EC2 deployment update
  - Complete zero-cost deployment verified ($0 / ₹0 billed)
  - Rollback procedure documented

---

## 🏗️ Epic 3: LSS-E3 Infrastructure as Code (Terraform) (Sprint 3)

### 📌 LSS-14: Terraform Setup & Remote State (Free S3 Backend)
- **Issue Type:** Story
- **Sprint:** Sprint 3
- **Priority:** High
- **Labels:** `terraform`, `iac`
- **Description:** Initialize Terraform with S3 backend + DynamoDB state locking (within AWS Free Tier limits).
- **Acceptance Criteria:**
  - S3 backend + DynamoDB lock table
  - State stored remotely without cost

### 📌 LSS-15: EC2 & VPC Module (Terraform)
- **Issue Type:** Story
- **Sprint:** Sprint 3
- **Priority:** High
- **Labels:** `terraform`, `ec2`, `zero-cost`
- **Description:** Codify zero-cost VPC, Security Groups, and Free-Tier EC2 instance as Terraform modules.
- **Acceptance Criteria:**
  - Terraform code manages VPC & EC2 instance
  - `terraform plan` shows zero paid components (no ALB, no NAT GW)

### 📌 LSS-16: Terraform in CI
- **Issue Type:** Story
- **Sprint:** Sprint 3
- **Priority:** High
- **Labels:** `terraform`, `ci`, `iac`
- **Description:** `terraform plan` runs on PRs with output in PR comment. `terraform apply` runs on main merge with manual approval gate.
- **Acceptance Criteria:**
  - `terraform plan` runs on PRs
  - Plan output visible in PR comment
  - `apply` only on main merge (manual approval)

---

## ☸️ Epic 4: LSS-E4 Kubernetes (Local & Free Tier) (Sprint 4)

### 📌 LSS-17: Local K8s Cluster (Minikube / k3s)
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** High
- **Labels:** `kubernetes`, `local`
- **Description:** Set up local Kubernetes cluster using Minikube / k3s on developer machine (100% free, zero cloud cost).
- **Acceptance Criteria:**
  - Local K8s cluster running
  - `kubectl` configured and connected
  - App deployed and tested locally

### 📌 LSS-18: LearningOS Deployments & Services
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** High
- **Labels:** `kubernetes`, `deployments`
- **Description:** Deploy frontend, backend, and postgres as Kubernetes Deployments. Create ClusterIP services.
- **Acceptance Criteria:**
  - Frontend + backend + postgres as Deployments
  - ClusterIP services for each
  - App functions correctly in cluster

### 📌 LSS-19: Ingress, ConfigMaps & Helm Charts
- **Issue Type:** Story
- **Sprint:** Sprint 4
- **Priority:** High
- **Labels:** `kubernetes`, `helm`, `ingress`
- **Description:** Package app with Helm, Nginx Ingress Controller, ConfigMaps, and Secrets.
- **Acceptance Criteria:**
  - Helm chart created and installable
  - Ingress controller routes traffic locally
