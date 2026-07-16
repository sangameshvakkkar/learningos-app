# Skill 05: AWS Fundamentals

> Cloud computing with Amazon Web Services — the infrastructure behind production

## Status: ⬜ Sprint 7–8

## Why AWS?

**Business Problem**: "Our app runs on Docker Compose on a laptop. How do we serve 10,000 users?"

AWS provides: scalable compute, managed databases, global networking, security, and 200+ services.

## Core Concepts

### Regions and Availability Zones

```
AWS Region (e.g., us-east-1)
  ├── Availability Zone (us-east-1a) ← separate data center
  ├── Availability Zone (us-east-1b) ← separate data center
  └── Availability Zone (us-east-1c) ← separate data center
```

- **Region**: Geographic area (e.g., Mumbai, Virginia, Frankfurt)
- **AZ**: Isolated data center within a region
- **Multi-AZ**: Deploy across AZs for high availability

### The Shared Responsibility Model

```
AWS manages:     Physical security, hardware, hypervisor, network
You manage:      OS patching, app code, IAM, encryption, firewall rules
```

## Services You'll Use (LearningOS)

### Compute

| Service | What | When to Use |
|---------|------|-------------|
| **ECS** | Container orchestration | Running Docker containers (Sprint 7) |
| **Fargate** | Serverless containers | No server management needed |
| **EC2** | Virtual machines | Full control over OS |
| **Lambda** | Serverless functions | Event-driven, short tasks |

### Networking

| Service | What | When to Use |
|---------|------|-------------|
| **VPC** | Virtual private network | Isolate your infrastructure |
| **Subnets** | Network segments | Public (ALB) vs private (DB, app) |
| **ALB** | Application Load Balancer | Route traffic to containers |
| **Route 53** | DNS | Custom domains |
| **CloudFront** | CDN | Serve frontend globally |

### Storage & Database

| Service | What | When to Use |
|---------|------|-------------|
| **RDS** | Managed PostgreSQL/MySQL | Production database |
| **S3** | Object storage | Static files, backups, Terraform state |
| **ElastiCache** | Managed Redis | Session caching |

### Security

| Service | What | When to Use |
|---------|------|-------------|
| **IAM** | Identity & Access Management | Control who can do what |
| **Secrets Manager** | Secret storage | Database passwords, API keys |
| **KMS** | Key Management | Encryption keys |
| **Security Groups** | Firewall rules | Control network access |

### Container Registry

| Service | What | When to Use |
|---------|------|-------------|
| **ECR** | Container image registry | Store Docker images (Sprint 7) |

## LearningOS Production Architecture (Target)

```
                Internet
                   │
            ┌──────┴──────┐
            │  CloudFront  │ ← CDN for frontend
            │   (S3 origin)│
            └──────┬──────┘
                   │
            ┌──────┴──────┐
            │     ALB      │ ← Application Load Balancer
            │  (public)    │
            └──────┬──────┘
                   │
         ┌─────────┴─────────┐
         │   Private Subnet   │
         │                    │
         │  ┌──────────────┐  │
         │  │  ECS Fargate  │  │ ← Backend containers
         │  │  (backend)    │  │
         │  └──────┬───────┘  │
         │         │          │
         │  ┌──────┴───────┐  │
         │  │   RDS         │  │ ← Managed PostgreSQL
         │  │  (postgres)   │  │
         │  └──────────────┘  │
         └────────────────────┘
```

### Mapping: Docker Compose → AWS

| Docker Compose | AWS Equivalent | Why |
|---------------|---------------|-----|
| `postgres` service | Amazon RDS | Managed backups, failover, patching |
| `backend` service | ECS Fargate task | Auto-scaling, health checks |
| `frontend` service | S3 + CloudFront | Static files don't need a container |
| Docker network | VPC + subnets | Network isolation |
| `.env` file | Secrets Manager | Encrypted, rotatable |
| `docker-compose.yml` | Terraform | Infrastructure as code |
| `-p 8000:8000` | ALB target group | Load-balanced routing |

## IAM Fundamentals

```
User        → A person (you)
Role        → An identity assumed by services (ECS task, Lambda)
Policy      → A JSON document defining permissions
Group       → A collection of users with shared policies

Principle of Least Privilege:
  Give exactly the permissions needed, nothing more.
```

## Cost Awareness

| Resource | Cost Model | Tip |
|----------|-----------|-----|
| EC2/Fargate | Per hour/second | Right-size instances |
| RDS | Per hour + storage | Use `db.t3.micro` for learning |
| ALB | Per hour + LCU | One ALB can serve many services |
| S3 | Per GB stored + requests | Cheap for static assets |
| Data transfer | Per GB out | Biggest surprise cost |
| ECR | Per GB stored | Clean old images |

**Free Tier**: 12 months of limited free usage. Use `t2.micro` / `t3.micro`.

## Prerequisites for Sprint 7

- [ ] AWS account created
- [ ] MFA enabled on root account
- [ ] IAM user created (don't use root)
- [ ] AWS CLI installed and configured
- [ ] Understand VPC, subnet, security group basics
- [ ] Understand IAM roles vs users

## Key Takeaway

AWS is a toolbox, not a solution. Understanding **when** and **why** to use each service matters more than knowing every API call. Start with the business problem, then pick the right service.
