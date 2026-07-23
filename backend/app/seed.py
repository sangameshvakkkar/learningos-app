from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.course import Course
from app.models.lesson import Lesson


COURSES = [
    {
        "title": "Docker Fundamentals",
        "slug": "docker-fundamentals",
        "description": "Master containerization from images and containers to Docker Compose, networking, volumes, and multi-stage builds.",
        "level": "Beginner",
        "duration_minutes": 180,
        "category": "Containers",
        "lessons": [
            {
                "title": "Images & Containers",
                "slug": "images-and-containers",
                "order_index": 0,
                "duration_minutes": 30,
                "content": (
                    "# Images & Containers\n\n"
                    "## What is a Container?\n\n"
                    "A container is a lightweight, standalone, executable package that includes everything needed to run a piece of software: code, runtime, system tools, libraries, and settings.\n\n"
                    "## Images vs Containers\n\n"
                    "- **Image**: A read-only template. Think of it as a blueprint.\n"
                    "- **Container**: A running instance of an image. Think of it as a building built from the blueprint.\n\n"
                    "## Key Commands\n\n"
                    "```bash\n"
                    "# Pull an image\n"
                    "docker pull nginx:alpine\n\n"
                    "# Run a container\n"
                    "docker run -d -p 8080:80 nginx:alpine\n\n"
                    "# List running containers\n"
                    "docker ps\n\n"
                    "# Stop a container\n"
                    "docker stop <container_id>\n"
                    "```\n\n"
                    "## Dockerfile Basics\n\n"
                    "A Dockerfile is a text file with instructions to build an image:\n\n"
                    "```dockerfile\n"
                    "FROM python:3.12-slim\n"
                    "WORKDIR /app\n"
                    "COPY . .\n"
                    "RUN pip install -r requirements.txt\n"
                    "CMD [\"python\", \"main.py\"]\n"
                    "```\n\n"
                    "Each instruction creates a **layer**. Docker caches layers for faster rebuilds.\n"
                ),
            },
            {
                "title": "Docker Compose",
                "slug": "docker-compose",
                "order_index": 1,
                "duration_minutes": 35,
                "content": (
                    "# Docker Compose\n\n"
                    "## Why Compose?\n\n"
                    "Real applications have multiple services: a web server, a database, a cache. Docker Compose lets you define and run multi-container applications with a single YAML file.\n\n"
                    "## docker-compose.yml\n\n"
                    "```yaml\n"
                    "services:\n"
                    "  web:\n"
                    "    build: .\n"
                    "    ports:\n"
                    "      - '8000:8000'\n"
                    "    depends_on:\n"
                    "      db:\n"
                    "        condition: service_healthy\n"
                    "  db:\n"
                    "    image: postgres:16-alpine\n"
                    "    volumes:\n"
                    "      - pgdata:/var/lib/postgresql/data\n"
                    "    healthcheck:\n"
                    "      test: ['CMD-SHELL', 'pg_isready']\n"
                    "volumes:\n"
                    "  pgdata:\n"
                    "```\n\n"
                    "## Key Concepts\n\n"
                    "- **depends_on**: Controls startup order\n"
                    "- **healthcheck**: Ensures a service is actually ready, not just started\n"
                    "- **volumes**: Persist data across container restarts\n"
                ),
            },
            {
                "title": "Networking & Volumes",
                "slug": "networking-and-volumes",
                "order_index": 2,
                "duration_minutes": 40,
                "content": (
                    "# Networking & Volumes\n\n"
                    "## Container Networking\n\n"
                    "Inside Docker Compose, containers communicate using **service names**, not `localhost`.\n\n"
                    "```\n"
                    "backend → postgres:5432  ✅ correct\n"
                    "backend → localhost:5432 ❌ wrong inside containers\n"
                    "```\n\n"
                    "Docker creates an internal DNS that resolves service names to container IPs.\n\n"
                    "## Network Types\n\n"
                    "- **bridge**: Default. Containers on same network can communicate.\n"
                    "- **host**: Container shares host's network stack.\n"
                    "- **none**: No networking.\n\n"
                    "## Volumes\n\n"
                    "Containers are ephemeral — when they stop, data is lost. Volumes persist data.\n\n"
                    "```yaml\n"
                    "volumes:\n"
                    "  pgdata:  # named volume\n"
                    "```\n\n"
                    "**Production thinking**: Databases should never run without volumes.\n"
                ),
            },
            {
                "title": "Multi-stage Builds",
                "slug": "multi-stage-builds",
                "order_index": 3,
                "duration_minutes": 35,
                "content": (
                    "# Multi-stage Builds\n\n"
                    "## The Problem\n\n"
                    "Build tools (compilers, package managers) inflate image size. You need them to build, but not to run.\n\n"
                    "## The Solution\n\n"
                    "Multi-stage builds use multiple `FROM` statements. Each stage starts fresh. You copy only what you need from previous stages.\n\n"
                    "```dockerfile\n"
                    "# Stage 1: Build\n"
                    "FROM node:20-alpine AS builder\n"
                    "WORKDIR /app\n"
                    "COPY package*.json ./\n"
                    "RUN npm ci\n"
                    "COPY . .\n"
                    "RUN npm run build\n\n"
                    "# Stage 2: Serve\n"
                    "FROM nginx:alpine\n"
                    "COPY --from=builder /app/dist /usr/share/nginx/html\n"
                    "```\n\n"
                    "**Result**: Final image is ~25MB instead of ~500MB.\n\n"
                    "## Key Principle\n\n"
                    "Build Once, Deploy Anywhere. The same image runs in dev, staging, and production.\n"
                ),
            },
            {
                "title": "Health Checks & Lifecycle",
                "slug": "health-checks-and-lifecycle",
                "order_index": 4,
                "duration_minutes": 40,
                "content": (
                    "# Health Checks & Lifecycle\n\n"
                    "## Container Lifecycle\n\n"
                    "```\n"
                    "Created → Running → Paused → Stopped → Removed\n"
                    "```\n\n"
                    "## Health Checks\n\n"
                    "A health check tells Docker whether your application inside the container is actually working.\n\n"
                    "```yaml\n"
                    "healthcheck:\n"
                    "  test: ['CMD-SHELL', 'pg_isready -U myuser']\n"
                    "  interval: 5s\n"
                    "  timeout: 5s\n"
                    "  retries: 10\n"
                    "```\n\n"
                    "## Why Health Checks Matter\n\n"
                    "- `depends_on` without health checks only waits for the container to **start**, not be **ready**\n"
                    "- A database container can take 10+ seconds to initialize\n"
                    "- Without health checks, your app crashes because the DB isn't ready\n\n"
                    "## Production Thinking\n\n"
                    "In production (ECS, Kubernetes), health checks determine:\n"
                    "- Whether to route traffic to a container\n"
                    "- Whether to restart a crashed container\n"
                    "- Whether a deployment succeeded or should roll back\n"
                ),
            },
        ],
    },
    {
        "title": "CI/CD Pipelines",
        "slug": "ci-cd-pipelines",
        "description": "Understand continuous integration and continuous delivery. Build GitHub Actions workflows for linting, testing, building, and deploying.",
        "level": "Beginner",
        "duration_minutes": 200,
        "category": "CI/CD",
        "lessons": [
            {
                "title": "Why CI/CD",
                "slug": "why-ci-cd",
                "order_index": 0,
                "duration_minutes": 25,
                "content": (
                    "# Why CI/CD\n\n"
                    "## The Problem Without CI/CD\n\n"
                    "- Developer pushes code → nobody checks it → breaks in production\n"
                    "- \"It works on my machine\" → doesn't work on the server\n"
                    "- Manual deployments → human error, inconsistency\n\n"
                    "## What CI/CD Solves\n\n"
                    "**Continuous Integration (CI)**: Every code change is automatically validated — linted, tested, built.\n\n"
                    "**Continuous Delivery (CD)**: Validated code is automatically deployed to staging/production.\n\n"
                    "## Business Value\n\n"
                    "| Without CI/CD | With CI/CD |\n"
                    "|---|---|\n"
                    "| Bugs found in production | Bugs found in PR |\n"
                    "| Deploy takes hours | Deploy takes minutes |\n"
                    "| Manual, error-prone | Automated, repeatable |\n"
                    "| Fear of deploying | Deploy with confidence |\n"
                ),
            },
            {
                "title": "GitHub Actions Basics",
                "slug": "github-actions-basics",
                "order_index": 1,
                "duration_minutes": 40,
                "content": (
                    "# GitHub Actions Basics\n\n"
                    "## Core Concepts\n\n"
                    "- **Workflow**: A YAML file in `.github/workflows/`\n"
                    "- **Event**: What triggers the workflow (push, PR, schedule)\n"
                    "- **Job**: A set of steps that run on a runner\n"
                    "- **Step**: A single task (run a command, use an action)\n"
                    "- **Runner**: The machine that executes the job\n\n"
                    "## Minimal Workflow\n\n"
                    "```yaml\n"
                    "name: CI\n"
                    "on:\n"
                    "  pull_request:\n"
                    "    branches: [main]\n"
                    "jobs:\n"
                    "  build:\n"
                    "    runs-on: ubuntu-latest\n"
                    "    steps:\n"
                    "      - uses: actions/checkout@v4\n"
                    "      - run: echo 'Hello CI!'\n"
                    "```\n\n"
                    "## Key Actions\n\n"
                    "- `actions/checkout@v4` — Clone your repo\n"
                    "- `actions/setup-node@v4` — Install Node.js\n"
                    "- `actions/setup-python@v5` — Install Python\n"
                ),
            },
            {
                "title": "Linting & Build Jobs",
                "slug": "linting-and-build-jobs",
                "order_index": 2,
                "duration_minutes": 45,
                "content": (
                    "# Linting & Build Jobs\n\n"
                    "## Fail Fast Principle\n\n"
                    "Run the cheapest checks first:\n"
                    "1. **Lint** (~5 seconds) — catch style/type errors\n"
                    "2. **Build** (~2 minutes) — verify compilation\n"
                    "3. **Test** (~5 minutes) — verify behavior\n\n"
                    "If lint fails, skip the build. No point building broken code.\n\n"
                    "## npm ci vs npm install\n\n"
                    "| `npm install` | `npm ci` |\n"
                    "|---|---|\n"
                    "| Updates lock file | Uses lock file exactly |\n"
                    "| Non-deterministic | Deterministic |\n"
                    "| Good for development | Good for CI |\n\n"
                    "**Rule**: Always use `npm ci` in CI pipelines.\n\n"
                    "## Caching\n\n"
                    "```yaml\n"
                    "- uses: actions/setup-node@v4\n"
                    "  with:\n"
                    "    cache: npm\n"
                    "    cache-dependency-path: frontend/package-lock.json\n"
                    "```\n\n"
                    "Caching node_modules saves 30–60 seconds per run.\n"
                ),
            },
            {
                "title": "Docker in CI",
                "slug": "docker-in-ci",
                "order_index": 3,
                "duration_minutes": 45,
                "content": (
                    "# Docker in CI\n\n"
                    "## Why Build Docker Images in CI?\n\n"
                    "**Business problem**: 'We have zero confidence Docker images build successfully before merge.'\n\n"
                    "If the Dockerfile is broken, you find out during deployment — the worst time.\n\n"
                    "## docker/build-push-action\n\n"
                    "```yaml\n"
                    "- uses: docker/setup-buildx-action@v3\n"
                    "- uses: docker/build-push-action@v6\n"
                    "  with:\n"
                    "    context: ./frontend\n"
                    "    push: false          # build only, no push\n"
                    "    tags: myapp:${{ github.sha }}\n"
                    "    cache-from: type=gha\n"
                    "    cache-to: type=gha,mode=max\n"
                    "```\n\n"
                    "## Pipeline Architecture\n\n"
                    "```\n"
                    "validation (lint + build) → docker build → security scan → push\n"
                    "```\n\n"
                    "Docker build depends on validation passing. This is enforced with `needs:`.\n"
                ),
            },
            {
                "title": "Caching & Artifacts",
                "slug": "caching-and-artifacts",
                "order_index": 4,
                "duration_minutes": 45,
                "content": (
                    "# Caching & Artifacts\n\n"
                    "## GitHub Actions Cache\n\n"
                    "Cache dependencies between workflow runs to speed up builds.\n\n"
                    "### Types of Caching\n\n"
                    "1. **Tool cache** (`setup-node`, `setup-python`) — caches installed packages\n"
                    "2. **Docker layer cache** (`type=gha`) — caches Docker build layers\n"
                    "3. **Custom cache** (`actions/cache`) — cache any directory\n\n"
                    "## Artifacts\n\n"
                    "Artifacts are files produced during a workflow that you want to keep:\n\n"
                    "```yaml\n"
                    "- uses: actions/upload-artifact@v4\n"
                    "  with:\n"
                    "    name: build-output\n"
                    "    path: frontend/dist/\n"
                    "```\n\n"
                    "Use cases:\n"
                    "- Build output for deployment\n"
                    "- Test reports\n"
                    "- Security scan results\n\n"
                    "## Cache Invalidation\n\n"
                    "Caches are keyed by a hash (usually of the lock file). When dependencies change, the cache misses and rebuilds.\n"
                ),
            },
        ],
    },
    {
        "title": "Cloud Infrastructure (AWS)",
        "slug": "cloud-infrastructure-aws",
        "description": "Learn core AWS services: VPC networking, IAM security, ECR container registry, ECS container orchestration, and Application Load Balancers.",
        "level": "Intermediate",
        "duration_minutes": 300,
        "category": "Cloud",
        "lessons": [
            {
                "title": "AWS Core Services",
                "slug": "aws-core-services",
                "order_index": 0,
                "duration_minutes": 45,
                "content": (
                    "# AWS Core Services\n\n"
                    "## The AWS Landscape\n\n"
                    "AWS has 200+ services, but you need ~10 to deploy a web application.\n\n"
                    "## Essential Services for LearningOS\n\n"
                    "| Service | Purpose | Analogy |\n"
                    "|---|---|---|\n"
                    "| **VPC** | Private network | Your office building |\n"
                    "| **EC2** | Virtual machines | Computers in the building |\n"
                    "| **ECS** | Container orchestration | A team managing the computers |\n"
                    "| **ECR** | Container registry | A warehouse for Docker images |\n"
                    "| **RDS** | Managed database | A filing cabinet with a guard |\n"
                    "| **ALB** | Load balancer | A receptionist routing visitors |\n"
                    "| **IAM** | Access control | Building security |\n"
                    "| **S3** | Object storage | A storage locker |\n\n"
                    "## Shared Responsibility Model\n\n"
                    "- **AWS manages**: Physical hardware, networking, data centers\n"
                    "- **You manage**: What you deploy, how you configure it, who has access\n"
                ),
            },
            {
                "title": "VPC & Networking",
                "slug": "vpc-and-networking",
                "order_index": 1,
                "duration_minutes": 60,
                "content": (
                    "# VPC & Networking\n\n"
                    "## What is a VPC?\n\n"
                    "A Virtual Private Cloud is your own isolated network in AWS.\n\n"
                    "## Architecture\n\n"
                    "```\n"
                    "VPC (10.0.0.0/16)\n"
                    "├── Public Subnet (10.0.1.0/24)  → ALB, NAT Gateway\n"
                    "├── Public Subnet (10.0.2.0/24)  → ALB (multi-AZ)\n"
                    "├── Private Subnet (10.0.3.0/24) → ECS Tasks, RDS\n"
                    "└── Private Subnet (10.0.4.0/24) → ECS Tasks, RDS (multi-AZ)\n"
                    "```\n\n"
                    "## Key Concepts\n\n"
                    "- **Public subnet**: Has a route to the Internet Gateway\n"
                    "- **Private subnet**: No direct internet access. Uses NAT Gateway for outbound.\n"
                    "- **Security Groups**: Firewall rules (stateful)\n"
                    "- **Route Tables**: Control traffic flow between subnets\n\n"
                    "## Production Rule\n\n"
                    "**Databases always go in private subnets.** No exceptions.\n"
                ),
            },
            {
                "title": "IAM & Security",
                "slug": "iam-and-security",
                "order_index": 2,
                "duration_minutes": 60,
                "content": (
                    "# IAM & Security\n\n"
                    "## IAM = Identity and Access Management\n\n"
                    "Controls **who** can do **what** on **which** resources.\n\n"
                    "## Core Concepts\n\n"
                    "- **User**: A person or service\n"
                    "- **Role**: Temporary permissions (preferred over users)\n"
                    "- **Policy**: JSON document defining permissions\n"
                    "- **Group**: Collection of users with shared policies\n\n"
                    "## Least Privilege Principle\n\n"
                    "```json\n"
                    "{\n"
                    "  \"Effect\": \"Allow\",\n"
                    "  \"Action\": \"ecr:GetAuthorizationToken\",\n"
                    "  \"Resource\": \"*\"\n"
                    "}\n"
                    "```\n\n"
                    "**Never use `*` for Resource in production.** Scope to specific ARNs.\n\n"
                    "## Golden Rules\n\n"
                    "1. Never use root account for daily work\n"
                    "2. Enable MFA on root immediately\n"
                    "3. Use roles, not users, for services\n"
                    "4. Use OIDC for CI/CD (no static access keys)\n"
                ),
            },
            {
                "title": "ECR & ECS",
                "slug": "ecr-and-ecs",
                "order_index": 3,
                "duration_minutes": 70,
                "content": (
                    "# ECR & ECS\n\n"
                    "## Amazon ECR (Elastic Container Registry)\n\n"
                    "A managed Docker image registry — like Docker Hub, but private and integrated with AWS.\n\n"
                    "```bash\n"
                    "# Authenticate Docker with ECR\n"
                    "aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com\n\n"
                    "# Push an image\n"
                    "docker push <account>.dkr.ecr.<region>.amazonaws.com/learningos-frontend:latest\n"
                    "```\n\n"
                    "## Amazon ECS (Elastic Container Service)\n\n"
                    "Runs Docker containers in the cloud.\n\n"
                    "### ECS Concepts\n\n"
                    "- **Cluster**: A logical grouping of tasks\n"
                    "- **Task Definition**: Blueprint for running a container (image, CPU, memory, env vars)\n"
                    "- **Service**: Ensures N copies of a task are always running\n"
                    "- **Fargate**: Serverless compute — no EC2 instances to manage\n\n"
                    "## Fargate vs EC2\n\n"
                    "| Fargate | EC2 |\n"
                    "|---|---|\n"
                    "| No servers to manage | Full control |\n"
                    "| Pay per task | Pay per instance |\n"
                    "| Simpler | Cheaper at scale |\n"
                ),
            },
            {
                "title": "Load Balancers",
                "slug": "load-balancers",
                "order_index": 4,
                "duration_minutes": 65,
                "content": (
                    "# Load Balancers\n\n"
                    "## What is a Load Balancer?\n\n"
                    "Distributes incoming traffic across multiple targets (containers, instances).\n\n"
                    "## Application Load Balancer (ALB)\n\n"
                    "- Works at Layer 7 (HTTP/HTTPS)\n"
                    "- Path-based routing: `/api/*` → backend, `/*` → frontend\n"
                    "- Health checks: removes unhealthy targets\n"
                    "- TLS termination: handles HTTPS for you\n\n"
                    "## Architecture with ECS\n\n"
                    "```\n"
                    "Internet → ALB → Target Group → ECS Tasks\n"
                    "                  ├── /api/*  → Backend Service\n"
                    "                  └── /*      → Frontend Service\n"
                    "```\n\n"
                    "## Health Checks\n\n"
                    "The ALB periodically pings a health check path (e.g., `/api/v1/health`).\n"
                    "If a task fails 3 consecutive checks, ALB stops sending traffic to it and ECS replaces it.\n\n"
                    "This is **self-healing infrastructure**.\n"
                ),
            },
        ],
    },
    {
        "title": "Kubernetes Orchestration",
        "slug": "kubernetes-orchestration",
        "description": "Learn container orchestration with Kubernetes: architecture, Deployments, Services, Ingress, Helm charts, and auto-scaling.",
        "level": "Intermediate",
        "duration_minutes": 350,
        "category": "Orchestration",
        "lessons": [
            {
                "title": "Kubernetes Architecture",
                "slug": "kubernetes-architecture",
                "order_index": 0,
                "duration_minutes": 50,
                "content": (
                    "# Kubernetes Architecture\n\n"
                    "## What is Kubernetes?\n\n"
                    "An open-source container orchestration platform. It automates deployment, scaling, and management of containerized applications.\n\n"
                    "## Architecture\n\n"
                    "```\n"
                    "Control Plane (Master)\n"
                    "├── API Server      → All communication goes through here\n"
                    "├── Scheduler       → Decides which node runs a pod\n"
                    "├── Controller Mgr  → Ensures desired state matches actual state\n"
                    "└── etcd            → Key-value store for cluster state\n\n"
                    "Worker Nodes\n"
                    "├── kubelet         → Agent that runs pods\n"
                    "├── kube-proxy      → Network routing\n"
                    "└── Container Runtime → Actually runs containers (containerd)\n"
                    "```\n\n"
                    "## Key Concepts\n\n"
                    "- **Pod**: Smallest deployable unit. One or more containers.\n"
                    "- **Node**: A machine (virtual or physical) in the cluster.\n"
                    "- **Namespace**: Logical isolation within a cluster.\n"
                    "- **kubectl**: CLI tool to interact with the cluster.\n"
                ),
            },
            {
                "title": "Deployments & Services",
                "slug": "deployments-and-services",
                "order_index": 1,
                "duration_minutes": 60,
                "content": (
                    "# Deployments & Services\n\n"
                    "## Deployments\n\n"
                    "A Deployment manages a set of identical Pods. It handles:\n"
                    "- Rolling updates (zero-downtime)\n"
                    "- Rollbacks\n"
                    "- Scaling (replica count)\n\n"
                    "```yaml\n"
                    "apiVersion: apps/v1\n"
                    "kind: Deployment\n"
                    "metadata:\n"
                    "  name: backend\n"
                    "spec:\n"
                    "  replicas: 3\n"
                    "  selector:\n"
                    "    matchLabels:\n"
                    "      app: backend\n"
                    "  template:\n"
                    "    metadata:\n"
                    "      labels:\n"
                    "        app: backend\n"
                    "    spec:\n"
                    "      containers:\n"
                    "        - name: backend\n"
                    "          image: learningos-backend:latest\n"
                    "          ports:\n"
                    "            - containerPort: 8000\n"
                    "```\n\n"
                    "## Services\n\n"
                    "Services provide stable networking for Pods. Pods come and go; Services give them a stable DNS name.\n\n"
                    "- **ClusterIP**: Internal only (default)\n"
                    "- **NodePort**: Expose on each node's IP\n"
                    "- **LoadBalancer**: Cloud provider load balancer\n"
                ),
            },
            {
                "title": "Ingress & Networking",
                "slug": "ingress-and-networking",
                "order_index": 2,
                "duration_minutes": 55,
                "content": (
                    "# Ingress & Networking\n\n"
                    "## What is Ingress?\n\n"
                    "Ingress manages external HTTP/HTTPS access to services in the cluster.\n\n"
                    "```yaml\n"
                    "apiVersion: networking.k8s.io/v1\n"
                    "kind: Ingress\n"
                    "metadata:\n"
                    "  name: learningos-ingress\n"
                    "spec:\n"
                    "  rules:\n"
                    "    - host: learningos.dev\n"
                    "      http:\n"
                    "        paths:\n"
                    "          - path: /api\n"
                    "            pathType: Prefix\n"
                    "            backend:\n"
                    "              service:\n"
                    "                name: backend\n"
                    "                port:\n"
                    "                  number: 8000\n"
                    "          - path: /\n"
                    "            pathType: Prefix\n"
                    "            backend:\n"
                    "              service:\n"
                    "                name: frontend\n"
                    "                port:\n"
                    "                  number: 80\n"
                    "```\n\n"
                    "## Ingress Controller\n\n"
                    "Ingress resources need an **Ingress Controller** to work (e.g., nginx-ingress, traefik).\n"
                ),
            },
            {
                "title": "Helm Charts",
                "slug": "helm-charts",
                "order_index": 3,
                "duration_minutes": 60,
                "content": (
                    "# Helm Charts\n\n"
                    "## What is Helm?\n\n"
                    "Helm is the package manager for Kubernetes. A **chart** is a collection of K8s manifests with templating.\n\n"
                    "## Chart Structure\n\n"
                    "```\n"
                    "learningos/\n"
                    "├── Chart.yaml        → Chart metadata\n"
                    "├── values.yaml       → Default configuration\n"
                    "├── templates/\n"
                    "│   ├── deployment.yaml\n"
                    "│   ├── service.yaml\n"
                    "│   └── ingress.yaml\n"
                    "```\n\n"
                    "## Key Commands\n\n"
                    "```bash\n"
                    "# Install a release\n"
                    "helm install learningos ./learningos\n\n"
                    "# Upgrade with new values\n"
                    "helm upgrade learningos ./learningos -f prod-values.yaml\n\n"
                    "# Rollback\n"
                    "helm rollback learningos 1\n"
                    "```\n\n"
                    "## Values Templating\n\n"
                    "```yaml\n"
                    "# values.yaml\n"
                    "replicaCount: 3\n"
                    "image:\n"
                    "  repository: learningos-backend\n"
                    "  tag: latest\n"
                    "```\n\n"
                    "Templates reference values: `{{ .Values.replicaCount }}`\n"
                ),
            },
            {
                "title": "Scaling & Self-Healing",
                "slug": "scaling-and-self-healing",
                "order_index": 4,
                "duration_minutes": 65,
                "content": (
                    "# Scaling & Self-Healing\n\n"
                    "## Horizontal Pod Autoscaler (HPA)\n\n"
                    "Automatically scales pods based on metrics:\n\n"
                    "```yaml\n"
                    "apiVersion: autoscaling/v2\n"
                    "kind: HorizontalPodAutoscaler\n"
                    "metadata:\n"
                    "  name: backend-hpa\n"
                    "spec:\n"
                    "  scaleTargetRef:\n"
                    "    apiVersion: apps/v1\n"
                    "    kind: Deployment\n"
                    "    name: backend\n"
                    "  minReplicas: 2\n"
                    "  maxReplicas: 10\n"
                    "  metrics:\n"
                    "    - type: Resource\n"
                    "      resource:\n"
                    "        name: cpu\n"
                    "        target:\n"
                    "          type: Utilization\n"
                    "          averageUtilization: 70\n"
                    "```\n\n"
                    "## Self-Healing\n\n"
                    "- **Liveness probe**: Is the container alive? Restart if not.\n"
                    "- **Readiness probe**: Is it ready to serve traffic? Remove from service if not.\n\n"
                    "```yaml\n"
                    "livenessProbe:\n"
                    "  httpGet:\n"
                    "    path: /api/v1/health\n"
                    "    port: 8000\n"
                    "  initialDelaySeconds: 10\n"
                    "  periodSeconds: 15\n"
                    "```\n\n"
                    "Kubernetes detects failures and replaces pods automatically. This is **self-healing infrastructure**.\n"
                ),
            },
        ],
    },
    {
        "title": "Monitoring & Observability",
        "slug": "monitoring-and-observability",
        "description": "Build visibility into your systems with Prometheus metrics, Grafana dashboards, structured logging, log aggregation, and SRE practices.",
        "level": "Advanced",
        "duration_minutes": 350,
        "category": "Observability",
        "lessons": [
            {
                "title": "Why Observability",
                "slug": "why-observability",
                "order_index": 0,
                "duration_minutes": 40,
                "content": (
                    "# Why Observability\n\n"
                    "## The Three Pillars\n\n"
                    "1. **Metrics**: Numbers over time (request rate, latency, error rate)\n"
                    "2. **Logs**: Discrete events (errors, warnings, audit trails)\n"
                    "3. **Traces**: Request flow across services\n\n"
                    "## Monitoring vs Observability\n\n"
                    "- **Monitoring**: 'Is it up?' — predefined checks\n"
                    "- **Observability**: 'Why is it slow?' — ability to ask arbitrary questions\n\n"
                    "## The Golden Signals (Google SRE)\n\n"
                    "1. **Latency**: How long requests take\n"
                    "2. **Traffic**: How much demand the system handles\n"
                    "3. **Errors**: Rate of failed requests\n"
                    "4. **Saturation**: How 'full' the system is\n\n"
                    "If you can measure these four, you can understand any system.\n"
                ),
            },
            {
                "title": "Prometheus Metrics",
                "slug": "prometheus-metrics",
                "order_index": 1,
                "duration_minutes": 60,
                "content": (
                    "# Prometheus Metrics\n\n"
                    "## What is Prometheus?\n\n"
                    "An open-source monitoring system that **pulls** metrics from targets.\n\n"
                    "## Metric Types\n\n"
                    "- **Counter**: Only goes up (total requests, total errors)\n"
                    "- **Gauge**: Goes up and down (current CPU, active connections)\n"
                    "- **Histogram**: Distribution of values (request latency buckets)\n"
                    "- **Summary**: Similar to histogram, pre-calculated percentiles\n\n"
                    "## Instrumenting FastAPI\n\n"
                    "```python\n"
                    "from prometheus_client import Counter, Histogram\n\n"
                    "REQUEST_COUNT = Counter(\n"
                    "    'http_requests_total',\n"
                    "    'Total HTTP requests',\n"
                    "    ['method', 'path', 'status']\n"
                    ")\n\n"
                    "REQUEST_LATENCY = Histogram(\n"
                    "    'http_request_duration_seconds',\n"
                    "    'HTTP request latency',\n"
                    "    ['method', 'path']\n"
                    ")\n"
                    "```\n\n"
                    "## PromQL Basics\n\n"
                    "```\n"
                    "rate(http_requests_total[5m])  # requests per second\n"
                    "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))  # p95\n"
                    "```\n"
                ),
            },
            {
                "title": "Grafana Dashboards",
                "slug": "grafana-dashboards",
                "order_index": 2,
                "duration_minutes": 55,
                "content": (
                    "# Grafana Dashboards\n\n"
                    "## What is Grafana?\n\n"
                    "A visualization platform that connects to data sources (Prometheus, Loki, CloudWatch) and displays dashboards.\n\n"
                    "## Essential Dashboard Panels\n\n"
                    "1. **Request Rate** — `rate(http_requests_total[5m])`\n"
                    "2. **Error Rate** — errors / total requests\n"
                    "3. **Latency Percentiles** — p50, p95, p99\n"
                    "4. **CPU/Memory** — system resource usage\n\n"
                    "## Dashboard Design Principles\n\n"
                    "- **USE method**: Utilization, Saturation, Errors (for infrastructure)\n"
                    "- **RED method**: Rate, Errors, Duration (for services)\n"
                    "- Put the most important panels at the top\n"
                    "- Use consistent time ranges\n"
                    "- Export dashboards as JSON for version control\n\n"
                    "## Alerting\n\n"
                    "Dashboards are for humans. Alerts are for machines.\n"
                    "Don't rely on someone watching a dashboard — set up alerts.\n"
                ),
            },
            {
                "title": "Log Aggregation",
                "slug": "log-aggregation",
                "order_index": 3,
                "duration_minutes": 50,
                "content": (
                    "# Log Aggregation\n\n"
                    "## The Problem\n\n"
                    "With 10 containers, `docker logs` doesn't scale. You need centralized logging.\n\n"
                    "## Structured Logging\n\n"
                    "```json\n"
                    "{\n"
                    "  \"timestamp\": \"2026-07-23T10:15:30Z\",\n"
                    "  \"level\": \"ERROR\",\n"
                    "  \"correlation_id\": \"abc-123\",\n"
                    "  \"message\": \"Database connection failed\",\n"
                    "  \"service\": \"backend\"\n"
                    "}\n"
                    "```\n\n"
                    "**Structured > Unstructured**. Machines can parse JSON. They can't parse 'Error: something went wrong at line 42'.\n\n"
                    "## Loki\n\n"
                    "A log aggregation system designed for Grafana. Like Prometheus, but for logs.\n\n"
                    "- Indexes labels, not log content (efficient)\n"
                    "- Query with LogQL\n"
                    "- Integrates natively with Grafana\n\n"
                    "## Correlation IDs\n\n"
                    "Assign a unique ID to every incoming request. Pass it through all services. When debugging, filter by correlation ID to see the full request lifecycle.\n"
                ),
            },
            {
                "title": "Alerting & SLOs",
                "slug": "alerting-and-slos",
                "order_index": 4,
                "duration_minutes": 65,
                "content": (
                    "# Alerting & SLOs\n\n"
                    "## SLIs, SLOs, SLAs\n\n"
                    "- **SLI** (Service Level Indicator): A metric (e.g., 'percentage of requests < 500ms')\n"
                    "- **SLO** (Service Level Objective): A target (e.g., '99.5% of requests < 500ms')\n"
                    "- **SLA** (Service Level Agreement): A contract with consequences\n\n"
                    "## Error Budgets\n\n"
                    "If SLO is 99.5%, your error budget is 0.5%.\n"
                    "In a 30-day month: `0.005 × 30 × 24 × 60 = 216 minutes` of downtime allowed.\n\n"
                    "When error budget is exhausted: freeze features, fix reliability.\n\n"
                    "## Alert Design\n\n"
                    "```yaml\n"
                    "# Prometheus alert rule\n"
                    "groups:\n"
                    "  - name: learningos\n"
                    "    rules:\n"
                    "      - alert: HighErrorRate\n"
                    "        expr: rate(http_requests_total{status=~'5..'}[5m]) > 0.05\n"
                    "        for: 5m\n"
                    "        annotations:\n"
                    "          summary: 'Error rate exceeds 5%'\n"
                    "```\n\n"
                    "## Alert Principles\n\n"
                    "- Alert on symptoms, not causes\n"
                    "- Every alert should be actionable\n"
                    "- If nobody acts on an alert, delete it\n"
                ),
            },
        ],
    },
]


def seed_courses() -> None:
    with SessionLocal() as db:
        existing_slugs = set(db.scalars(select(Course.slug)).all())
        for item in COURSES:
            if item["slug"] not in existing_slugs:
                lessons_data = item.pop("lessons", [])
                course = Course(**item)
                db.add(course)
                db.flush()
                for lesson_data in lessons_data:
                    lesson = Lesson(course_id=course.id, **lesson_data)
                    db.add(lesson)
        db.commit()


if __name__ == "__main__":
    seed_courses()
