# Skill 08: Monitoring & Observability

> If you can't measure it, you can't manage it

## Status: ⬜ Sprint 10

## Why Monitoring?

**Business Problem**: "Production went down at 3 AM. We found out when a customer tweeted about it. It took 2 hours to figure out which service was broken."

Monitoring solves: silent failures, unknown performance issues, capacity planning, incident response.

## The Three Pillars of Observability

```
Observability
├── Metrics    → "What is happening?" (numbers over time)
├── Logs       → "Why is it happening?" (event details)
└── Traces     → "Where is it happening?" (request flow across services)
```

### Metrics

Numerical measurements over time.

```
cpu_usage{service="backend"} = 73%
http_requests_total{method="GET", status="200"} = 15234
request_duration_seconds{percentile="p99"} = 0.45
```

**Tools**: Prometheus, CloudWatch, Datadog

### Logs

Structured event records.

```json
{
  "timestamp": "2026-07-13T10:30:00Z",
  "level": "ERROR",
  "service": "backend",
  "message": "Database connection failed",
  "error": "connection refused",
  "trace_id": "abc123"
}
```

**Tools**: Loki, CloudWatch Logs, ELK Stack

### Traces

Follow a single request across multiple services.

```
User → ALB → Backend → Database
       2ms    45ms      120ms
                          └── Slow query: SELECT * FROM enrollments
```

**Tools**: Jaeger, AWS X-Ray, OpenTelemetry

## Prometheus + Grafana Stack

```
                    ┌─────────┐
                    │ Grafana  │ ← Dashboards & visualization
                    └────┬────┘
                         │ queries
                    ┌────┴────┐
                    │Prometheus│ ← Time-series database
                    └────┬────┘
                         │ scrapes /metrics
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Backend    Frontend    PostgreSQL
         :8000/      (nginx)    (exporter)
         metrics
```

### Application Instrumentation

```python
# FastAPI with Prometheus metrics
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)
```

## SLOs, SLIs, and SLAs

| Term | Meaning | Example |
|------|---------|---------|
| **SLI** (Indicator) | What you measure | Request latency, error rate |
| **SLO** (Objective) | Your target | "99.9% of requests < 500ms" |
| **SLA** (Agreement) | Business promise | "99.9% uptime or we refund" |

```
SLI: p99 latency = 450ms
SLO: p99 latency < 500ms  → ✅ Meeting objective
SLA: 99.9% availability   → Breach = financial penalty
```

### Error Budgets

```
SLO = 99.9% availability
Error Budget = 0.1% downtime = ~43 minutes/month

Used 15 minutes this month → 28 minutes remaining
→ Safe to deploy new features

Used 40 minutes this month → 3 minutes remaining
→ STOP deploying, focus on reliability
```

## Alerting

```yaml
# Prometheus alerting rule
groups:
  - name: learningos
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High 5xx error rate on {{ $labels.service }}"
```

### Alert Design Principles

- **Alert on symptoms, not causes** → "Error rate > 5%" not "CPU > 80%"
- **Actionable alerts only** → If nobody needs to act, don't alert
- **No alert fatigue** → Too many alerts = all alerts ignored
- **Runbook links** → Every alert should link to remediation steps

## CloudWatch (AWS Native)

```
CloudWatch
├── Metrics      → ECS CPU, memory, request count
├── Logs         → Container stdout/stderr
├── Alarms       → Trigger on threshold breach
├── Dashboards   → Visualization
└── Log Insights → Query language for logs
```

Good for AWS-native services. Prometheus+Grafana better for custom metrics and portability.

## LearningOS Monitoring (Sprint 10)

```text
monitoring/
├── docker-compose.monitoring.yml
├── prometheus/
│   ├── prometheus.yml           # Scrape configuration
│   └── alerts.yml               # Alerting rules
├── grafana/
│   ├── dashboards/
│   │   ├── backend.json         # Backend dashboard
│   │   └── infrastructure.json  # System dashboard
│   └── provisioning/
│       └── datasources.yml      # Auto-configure Prometheus
└── loki/
    └── loki-config.yml          # Log aggregation config
```

## The Four Golden Signals (Google SRE)

| Signal | Question | Metric |
|--------|---------|--------|
| **Latency** | How fast? | Request duration (p50, p95, p99) |
| **Traffic** | How much? | Requests per second |
| **Errors** | How broken? | Error rate (5xx / total) |
| **Saturation** | How full? | CPU, memory, disk, connections |

If you monitor these four things, you catch most problems.

## Prerequisites for Sprint 10

- [ ] Complete Sprint 7-9 (app running on cloud)
- [ ] Understand HTTP status codes (2xx, 4xx, 5xx)
- [ ] Basic understanding of time-series data
- [ ] Health endpoint already built (`/api/v1/health` ✅)

## Key Takeaway

Monitoring isn't optional — it's the difference between "we detected and fixed the issue in 5 minutes" and "we found out from Twitter after 2 hours." **Build observability into the platform from day one, not as an afterthought.**
