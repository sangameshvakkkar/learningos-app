---
name: aws-cloud
description: >
  AWS cloud skill for LearningOS. Covers ECR, ECS, Fargate, VPC, ALB, RDS, IAM,
  Secrets Manager, S3, and production architecture. Activate when working on any
  AWS deployment, cloud architecture, or service selection task.
  Reference: docs/academy/skills/05-aws-fundamentals.md
---

# AWS Cloud Skill

When working with AWS in LearningOS, follow these instructions.

## Architecture Mapping

Always connect Docker Compose concepts to AWS equivalents:

| Local | AWS | Why |
|-------|-----|-----|
| `postgres` service | Amazon RDS | Managed backups, failover, patching |
| `backend` service | ECS Fargate | Auto-scaling, no server management |
| `frontend` service | S3 + CloudFront | Static files don't need containers |
| Docker network | VPC + private subnets | Network isolation |
| `.env` file | Secrets Manager | Encrypted, rotatable, auditable |
| `docker-compose.yml` | Terraform | Infrastructure as code |
| Port mapping | ALB target groups | Load-balanced routing |

## LearningOS Target Architecture

```
Internet → CloudFront (frontend) → ALB → ECS Fargate (backend) → RDS PostgreSQL
                                                                     ↑
                                          All in private subnets ────┘
```

## IAM Principles

1. **Never use root account** for anything except initial setup
2. **Roles over users** for services — ECS tasks assume IAM roles
3. **Least privilege** — only grant what's needed
4. **OIDC** for CI/CD — GitHub Actions gets temporary credentials, no stored keys

## Cost Awareness

- Use Free Tier eligible resources for learning
- `t3.micro` for EC2, `db.t3.micro` for RDS
- Delete resources when not in use
- Monitor with AWS Cost Explorer

## Security Defaults

- MFA on all human accounts
- Encryption at rest enabled by default
- Private subnets for backend + database
- Security groups: minimum ports, specific source CIDRs

## Deep Reference

Read `docs/academy/skills/05-aws-fundamentals.md` for complete guide.
