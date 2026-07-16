---
name: security-devsecops
description: >
  Security and DevSecOps skill for LearningOS. Covers IAM, OIDC, container scanning,
  secrets management, network security, policy as code, and shift-left security.
  Activate when working on security configurations, IAM policies, image scanning,
  secrets, or any security-related task.
  Reference: docs/academy/skills/09-security.md
---

# Security & DevSecOps Skill

When working with security in LearningOS, follow these instructions.

## Shift-Left Principle

Security belongs at every stage, not as a final audit:

```
Code → Lint → Test → Build → Scan → Deploy
  ↑      ↑      ↑      ↑      ↑      ↑
  Security checks at EVERY stage
```

## Security Layers (Check All)

1. **Application**: Input validation, auth, CORS, CSRF
2. **Pipeline**: OIDC auth, no static credentials, signed images
3. **Container**: Non-root user, minimal base, CVE scanning
4. **Secrets**: Secrets Manager, never in Git or .env in prod
5. **Network**: VPC, private subnets, security groups
6. **IAM**: Least privilege, roles not users, MFA
7. **Infrastructure**: Encryption at rest + transit

## Non-Negotiable Rules

1. **Never commit secrets to Git** — use Secrets Manager
2. **Never use IAM users for services** — use IAM roles
3. **Never run containers as root** — add `USER` directive
4. **Never use `:latest` tag in production** — pin versions
5. **Never skip CVE scanning** — use Trivy in CI
6. **Never use `*` in IAM policies** — least privilege

## Container Security Checklist

```dockerfile
FROM python:3.12-slim              # ✅ Minimal base
RUN addgroup --system app && \
    adduser --system --ingroup app app  # ✅ Non-root user
COPY --chown=app:app . .           # ✅ Correct ownership
USER app                           # ✅ Run as non-root
```

## OIDC for CI/CD (Preferred over Access Keys)

```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456:role/github-actions
    aws-region: us-east-1
    # No access keys stored!
```

## Deep Reference

Read `docs/academy/skills/09-security.md` for complete guide.
