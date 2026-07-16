# Skill 09: Security & DevSecOps

> Security is not a phase — it's a property of every layer

## Status: ⬜ Sprint 11

## Why DevSecOps?

**Business Problem**: "We passed the code review. We passed the tests. We deployed to production. Then we got breached because the Docker image had a known CVE from 2023."

DevSecOps solves: security as an afterthought, vulnerable dependencies, leaked secrets, over-privileged access.

## The Shift-Left Principle

```
Traditional:     Code → Build → Test → Deploy → Security Audit
                                                 ^^^^^^^^^^^^
                                                 Too late, too expensive

DevSecOps:       Security → Code → Build → Test → Deploy
                 ^^^^^^^^
                 Security from the start, automated everywhere
```

## Security Layers

```
┌─────────────────────────────────────────┐
│ Layer 7: Application Security           │
│   Input validation, auth, CORS, CSRF    │
├─────────────────────────────────────────┤
│ Layer 6: CI/CD Pipeline Security        │
│   OIDC, no static creds, signed images  │
├─────────────────────────────────────────┤
│ Layer 5: Container Security             │
│   Non-root, minimal base, CVE scanning  │
├─────────────────────────────────────────┤
│ Layer 4: Secrets Management             │
│   Secrets Manager, no .env in prod      │
├─────────────────────────────────────────┤
│ Layer 3: Network Security               │
│   VPC, private subnets, security groups │
├─────────────────────────────────────────┤
│ Layer 2: IAM & Access Control           │
│   Least privilege, roles, no root       │
├─────────────────────────────────────────┤
│ Layer 1: Infrastructure Security        │
│   Encryption at rest, in transit, KMS   │
└─────────────────────────────────────────┘
```

## IAM Deep Dive

### Principle of Least Privilege

```json
// ❌ Over-privileged (never do this)
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}

// ✅ Least privilege
{
  "Effect": "Allow",
  "Action": [
    "ecr:GetDownloadUrlForLayer",
    "ecr:BatchGetImage"
  ],
  "Resource": "arn:aws:ecr:us-east-1:123456:repository/learningos-*"
}
```

### Roles vs Users

```
IAM User   → A person with long-lived credentials (access keys)
IAM Role   → An identity assumed temporarily by a service

Rule: Services should NEVER use IAM users.
      ECS tasks, Lambda, GitHub Actions → always use roles.
```

## OIDC for CI/CD

**Problem**: GitHub Actions needs AWS access to push images to ECR.

```
❌ Store AWS access keys as GitHub Secrets
   → Long-lived credentials
   → Can be leaked
   → Hard to rotate

✅ Use OIDC (OpenID Connect)
   → GitHub proves its identity to AWS
   → AWS grants temporary credentials
   → No stored secrets
   → Credentials expire automatically
```

```yaml
# GitHub Actions with OIDC
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/github-actions
    aws-region: us-east-1
    # No access keys! OIDC handles authentication
```

## Container Security

### Image Scanning

```yaml
# Trivy in CI pipeline
- name: Scan Docker Image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: learningos-backend:${{ github.sha }}
    exit-code: 1                    # Fail pipeline on HIGH/CRITICAL
    severity: CRITICAL,HIGH
    format: table
```

### Dockerfile Security

```dockerfile
# ✅ Security best practices
FROM python:3.12-slim                  # Minimal base image
RUN addgroup --system app && \
    adduser --system --ingroup app app  # Non-root user
WORKDIR /app
COPY --chown=app:app . .              # Owned by non-root
USER app                               # Run as non-root
```

### Supply Chain Security

```
Signed Images     → Verify image integrity (cosign, Notary)
SBOM              → Software Bill of Materials (know what's inside)
Base Image Policy → Only allow approved base images
Pin Digests       → Use sha256 digest, not mutable tags
```

## Secrets Management

```
❌ .env files in production
❌ Secrets in Docker images
❌ Secrets in Git history
❌ Secrets in environment variables (visible in `ps`)

✅ AWS Secrets Manager
✅ HashiCorp Vault
✅ Kubernetes Secrets (with encryption at rest)
✅ OIDC for service-to-service auth
```

## Network Security

```
Public Subnet:  ALB (receives internet traffic)
Private Subnet: Backend, Database (no direct internet access)
Security Group: Firewall rules per service

Backend SG:     Allow port 8000 from ALB SG only
Database SG:    Allow port 5432 from Backend SG only
ALB SG:         Allow port 443 from 0.0.0.0/0 (internet)
```

**Result**: Even if backend is compromised, attacker can't reach database directly from the internet.

## Policy as Code

### OPA (Open Policy Agent)

```rego
# Deny containers running as root
deny[msg] {
  input.spec.containers[_].securityContext.runAsUser == 0
  msg := "Containers must not run as root"
}

# Deny images without approved registry
deny[msg] {
  image := input.spec.containers[_].image
  not startswith(image, "123456789.dkr.ecr.us-east-1.amazonaws.com/")
  msg := sprintf("Image %v is not from approved registry", [image])
}
```

### Kyverno (Kubernetes-native)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-non-root
spec:
  rules:
    - name: check-non-root
      match:
        resources:
          kinds: [Pod]
      validate:
        message: "Running as root is not allowed"
        pattern:
          spec:
            containers:
              - securityContext:
                  runAsNonRoot: true
```

## Security Checklist for LearningOS

### Already Done

- [x] JWT authentication
- [x] Password hashing (bcrypt)
- [x] CORS configuration
- [x] `.dockerignore` excludes secrets

### Sprint 6 (Current)

- [ ] Container image scanning in CI (Trivy)
- [ ] Non-root user in Dockerfiles

### Sprint 7

- [ ] OIDC for GitHub Actions → AWS
- [ ] Secrets Manager for database credentials
- [ ] Private subnets for backend + database

### Sprint 11

- [ ] Full IAM policy review
- [ ] Network policy enforcement
- [ ] Policy as Code
- [ ] Secrets rotation
- [ ] SBOM generation

## Key Takeaway

Security isn't a checkbox at the end — it's embedded in every layer. The cost of fixing a vulnerability increases 100x from development to production. **Shift left: find it early, fix it cheap.**
