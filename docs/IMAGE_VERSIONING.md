# Container Image Versioning Strategy

## Overview

Every Docker image built in LearningOS CI is tagged using a two-tag convention:

| Tag | Type | Purpose |
|-----|------|---------|
| `<git-sha>` | Immutable | Exact build traceability. Pinned in deployments. |
| `latest` | Mutable | Always points to the newest build on `main`. |

---

## Why Two Tags?

### The `git-sha` Tag (e.g., `learningos-backend:a1b2c3d`)

- **Immutable** — once pushed, this tag never moves.
- Used in **Kubernetes manifests and ECS task definitions** so a deployment always references an exact, known image.
- Enables **instant rollback**: if a bad deploy goes out, you simply point back to the previous SHA tag.
- Provides a direct link between a running container and the Git commit that produced it.

### The `latest` Tag

- **Mutable** — always overwritten on every push to `main`.
- Used for **local development** (`docker pull learningos-backend:latest`) to quickly get the newest version.
- **Never** used in production deployments — only `sha` tags are used there.

---

## Tag Format

```
<registry>/<image>:<tag>

# Examples:
123456789.dkr.ecr.ap-south-1.amazonaws.com/learningos-backend:a1b2c3d4e5f6
123456789.dkr.ecr.ap-south-1.amazonaws.com/learningos-backend:latest
```

---

## Rules

1. **Production deployments MUST reference sha tags**, never `latest`.
2. **`latest` is for convenience only** — local dev, quick pulls.
3. **No semantic version tags (v1.0.0) until a formal release process is defined.**
4. Tags are applied at build time in GitHub Actions using `${{ github.sha }}`.
5. ECR lifecycle policy keeps only the **last 5 images** to stay within the free 500MB storage tier.

---

## Lifecycle Policy (ECR)

```json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep only the last 5 images",
      "selection": {
        "tagStatus": "any",
        "countType": "imageCountMoreThan",
        "countNumber": 5
      },
      "action": { "type": "expire" }
    }
  ]
}
```

---

## CI/CD Tagging in GitHub Actions

```yaml
tags: |
  ${{ env.ECR_REGISTRY }}/learningos-backend:${{ github.sha }}
  ${{ env.ECR_REGISTRY }}/learningos-backend:latest
```

Both tags are pushed atomically — they point to the same image digest.
