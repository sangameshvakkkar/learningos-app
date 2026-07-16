---
name: kubernetes
description: >
  Kubernetes orchestration skill for LearningOS. Covers pods, deployments, services,
  ingress, ConfigMaps, secrets, Helm charts, HPA, and probes. Activate when working
  on Kubernetes manifests, Helm charts, or container orchestration tasks.
  Reference: docs/academy/skills/07-kubernetes.md
---

# Kubernetes Skill

When working with Kubernetes in LearningOS, follow these instructions.

## When to Use K8s

- 3+ microservices needing orchestration
- Need for self-healing, auto-scaling, rolling updates
- Team has capacity to operate K8s

**Don't use K8s** for 1-3 simple services — ECS Fargate is simpler.

## Core Resources

| Resource | Purpose | LearningOS Use |
|----------|---------|----------------|
| Deployment | Manage pod replicas + rolling updates | Backend service |
| Service | Stable network endpoint | Internal routing |
| Ingress | External HTTP routing | API gateway |
| ConfigMap | Non-sensitive config | CORS origins, log level |
| Secret | Sensitive data | DB URL, JWT secret |
| HPA | Auto-scaling | Scale on CPU/memory |

## Helm Chart Structure

```
helm/learningos/
├── Chart.yaml
├── values.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    └── configmap.yaml
```

## Docker Compose → Kubernetes Mapping

| Compose | Kubernetes |
|---------|-----------|
| `services:` | Deployment + Service |
| `environment:` | ConfigMap / Secret |
| `volumes:` | PersistentVolumeClaim |
| `healthcheck:` | Liveness/readiness probes |
| `depends_on:` | Init containers |

## Health Probes (Required)

```yaml
livenessProbe:            # Restart if unhealthy
  httpGet:
    path: /api/v1/health
    port: 8000
readinessProbe:           # Don't route until ready
  httpGet:
    path: /api/v1/health
    port: 8000
```

## Deep Reference

Read `docs/academy/skills/07-kubernetes.md` for complete guide.
