# Skill 07: Kubernetes

> Container orchestration at scale — self-healing, auto-scaling, declarative infrastructure

## Status: ⬜ Sprint 9

## Why Kubernetes?

**Business Problem**: "We have 20 microservices running on ECS. Managing task definitions, scaling policies, and service discovery individually is becoming painful. We need a platform."

Kubernetes solves: container orchestration, service discovery, scaling, self-healing, rolling deployments, configuration management.

## When NOT to Use Kubernetes

If you have:
- 1-3 services → ECS Fargate is simpler
- Serverless workloads → Lambda is cheaper
- No team to operate K8s → Managed services win

**K8s is a platform for building platforms.** Don't add complexity without need.

## Architecture

```
┌─────────────────────────────────────────┐
│              Kubernetes Cluster          │
│                                         │
│  Control Plane                          │
│  ├── API Server (kubectl talks here)    │
│  ├── Scheduler (places pods on nodes)   │
│  ├── Controller Manager (desired state) │
│  └── etcd (cluster state database)      │
│                                         │
│  Worker Nodes                           │
│  ├── Node 1                             │
│  │   ├── Pod (container group)          │
│  │   ├── Pod                            │
│  │   └── kubelet (node agent)           │
│  ├── Node 2                             │
│  │   ├── Pod                            │
│  │   └── Pod                            │
│  └── Node 3                             │
│       └── Pod                           │
└─────────────────────────────────────────┘
```

## Core Resources

### Pod

Smallest deployable unit. Usually one container per pod.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: learningos-backend
spec:
  containers:
    - name: backend
      image: 123456789.dkr.ecr.us-east-1.amazonaws.com/learningos-backend:abc123
      ports:
        - containerPort: 8000
```

### Deployment

Manages pods with desired state, rolling updates, rollbacks.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learningos-backend
spec:
  replicas: 3                    # Always keep 3 pods running
  selector:
    matchLabels:
      app: learningos-backend
  template:
    metadata:
      labels:
        app: learningos-backend
    spec:
      containers:
        - name: backend
          image: learningos-backend:v1.2.3
          ports:
            - containerPort: 8000
          livenessProbe:           # Restart if unhealthy
            httpGet:
              path: /api/v1/health
              port: 8000
          readinessProbe:          # Don't route traffic until ready
            httpGet:
              path: /api/v1/health
              port: 8000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
```

### Service

Stable network endpoint for a set of pods.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: learningos-backend
spec:
  selector:
    app: learningos-backend
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP               # Internal only
```

### Ingress

External HTTP routing (like ALB).

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: learningos
spec:
  rules:
    - host: api.learningos.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: learningos-backend
                port:
                  number: 80
```

### ConfigMap & Secret

```yaml
# Non-sensitive configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: learningos-config
data:
  CORS_ORIGINS: "https://learningos.com"
  LOG_LEVEL: "info"

# Sensitive data (base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: learningos-secrets
type: Opaque
data:
  DATABASE_URL: cG9zdGdyZXNxbDovLy4uLg==    # base64
```

### HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: learningos-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70     # Scale up when CPU > 70%
```

## Helm

Package manager for Kubernetes. Bundles YAML into reusable charts.

```text
helm/learningos/
├── Chart.yaml
├── values.yaml           # Default configuration
├── values-prod.yaml      # Production overrides
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    └── configmap.yaml
```

```bash
helm install learningos ./helm/learningos -f values-prod.yaml
helm upgrade learningos ./helm/learningos -f values-prod.yaml
helm rollback learningos 1      # Rollback to revision 1
```

## Mapping: Docker Compose → Kubernetes

| Docker Compose | Kubernetes |
|---------------|-----------|
| `services:` | Deployment + Service |
| `ports:` | Service `targetPort` |
| `environment:` | ConfigMap / Secret |
| `volumes:` | PersistentVolumeClaim |
| `depends_on:` | Init containers / readiness probes |
| `healthcheck:` | Liveness / readiness probes |
| `docker-compose.yml` | Helm chart |
| `docker compose up` | `helm install` |

## Managed Kubernetes Options

| Service | Provider | Notes |
|---------|----------|-------|
| **EKS** | AWS | Most enterprise adoption |
| **GKE** | Google | Best K8s experience |
| **AKS** | Azure | Tight Azure integration |

For LearningOS Sprint 9, we'll use **EKS** (to stay in AWS ecosystem).

## Prerequisites for Sprint 9

- [ ] Complete Sprint 7 & 8 (ECS + Terraform first)
- [ ] Understand Deployments, Services, Ingress concepts
- [ ] Install `kubectl` and `helm`
- [ ] Understand why K8s exists (not just how)

## Key Takeaway

Kubernetes is a **declarative system**. You tell it *what* you want (3 replicas, healthy, accessible on port 80), and it figures out *how* to make that happen. If a pod dies, K8s replaces it. If traffic increases, K8s scales. Your job shifts from managing servers to defining desired state.
