---
name: debugging
description: >
  Debugging and troubleshooting skill for LearningOS. Covers systematic debugging
  methodology, the debugging ladder, log reading, root cause analysis, and common
  failure patterns. Activate when any error occurs, a pipeline fails, a container
  won't start, or any troubleshooting is needed.
  Reference: docs/academy/references/debugging-playbook.md
---

# Debugging & Troubleshooting Skill

When debugging issues in LearningOS, follow this systematic approach.

## The Debugging Ladder

Always follow this order. Never skip steps:

```
1. READ the error message — word by word, not skimming
2. CHECK the logs — container logs, CI logs, system logs
3. REPRODUCE — can you make it fail consistently?
4. ISOLATE — what changed? what's different?
5. SEARCH — Google the EXACT error message, not a summary
6. FIX THE ROOT CAUSE — not a workaround
```

## Fix the Source, Not the Symptom

```
❌ Pipeline fails on npm ci → switch to npm install
✅ Pipeline fails on npm ci → fix missing package-lock.json

❌ Docker build fails → add --force flag
✅ Docker build fails → fix the Dockerfile instruction

❌ Container can't connect → hardcode IP address
✅ Container can't connect → use service name in Docker DNS
```

**Principle**: If the fix involves a workaround, you haven't found the root cause.

## Common Failure Patterns

### Docker

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "Connection refused" between containers | Using `localhost` | Use service name |
| Build context too large | Missing `.dockerignore` | Add `.dockerignore` |
| "COPY failed: file not found" | Wrong build context | Check `docker-compose.yml` build path |
| Container exits immediately | CMD fails | Check `docker logs <container>` |
| DB connection fails on startup | No `depends_on` health check | Add `condition: service_healthy` |

### CI/CD

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `npm ci` fails | Missing/outdated `package-lock.json` | Run `npm install` locally, commit lock file |
| "Permission denied" | Wrong working directory | Add `working-directory:` |
| Secret is empty | Not configured in repo settings | Add in GitHub → Settings → Secrets |
| Action not found | Wrong action version | Check marketplace for correct `@v` tag |

### Python/Backend

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Import error | Missing dependency | Add to `requirements.txt` |
| DB migration fails | Schema mismatch | `alembic upgrade head` |
| bcrypt error | Password too long | Truncate or hash before bcrypt |

## How to Report Issues (Learner Practice)

Never say: "It doesn't work"

Always say:
```
I see: [exact error message]
When I: [exact action taken]
I tried: [what you attempted]
I think: [your hypothesis]
```

This is how production engineers communicate in incident channels.

## Root Cause Analysis Template

After fixing any issue:

```
What happened: [description]
Root cause: [why it happened]
Fix: [what we changed]
Prevention: [how to prevent recurrence]
Lesson: [what pattern to remember]
```
