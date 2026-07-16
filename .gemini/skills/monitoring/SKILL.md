---
name: monitoring
description: >
  Monitoring and observability skill for LearningOS. Covers Prometheus, Grafana,
  Loki, CloudWatch, SLOs/SLIs, alerting, and the four golden signals. Activate
  when working on metrics, dashboards, alerting, or observability tasks.
  Reference: docs/academy/skills/08-monitoring.md
---

# Monitoring & Observability Skill

When working with monitoring in LearningOS, follow these instructions.

## Three Pillars

1. **Metrics** — What is happening? (Prometheus)
2. **Logs** — Why is it happening? (Loki)
3. **Traces** — Where is it happening? (Jaeger/X-Ray)

## Four Golden Signals (Google SRE)

| Signal | Metric | Alert Threshold |
|--------|--------|----------------|
| Latency | Request duration (p50, p95, p99) | p99 > 500ms |
| Traffic | Requests per second | Sudden drop > 50% |
| Errors | 5xx rate | > 1% for 5 minutes |
| Saturation | CPU, memory, connections | > 80% sustained |

Monitor these four and you catch most problems.

## Stack

```
Application → Prometheus (scrape /metrics) → Grafana (visualize)
                                           → Alertmanager (notify)
Containers  → Loki (aggregate logs)        → Grafana (query)
AWS         → CloudWatch (native metrics)  → Grafana (unified)
```

## Alerting Rules

- Alert on **symptoms** not causes ("error rate high" not "CPU high")
- Every alert must be **actionable** — if no action needed, don't alert
- Link runbooks to every alert
- No alert fatigue — too many alerts = all ignored

## SLOs

```
SLI: p99 latency
SLO: 99.9% of requests < 500ms
Error Budget: 0.1% → ~43 minutes/month downtime allowed
```

## Deep Reference

Read `docs/academy/skills/08-monitoring.md` for complete guide.
