# Mentorship Guide

> How this Cloud/DevOps mentorship works

## Roles

| Role | Who | Responsibility |
|------|-----|---------------|
| Mentor | AI Assistant | Guide, challenge, review, teach production thinking |
| Engineer | You | Design, implement, debug, document |
| CTO/Architect | Simulated | Provides business context and requirements |

## How Each Session Works

```
1. Business Problem    → "The Docker build is too slow."
2. Design Discussion   → Mentor asks you design questions
3. Your Design         → You propose a solution
4. Mentor Feedback     → Corrections, production considerations
5. Implementation      → You build it (mentor helps when stuck)
6. Review              → Mentor reviews like a senior engineer
7. Reflection          → What did you learn? What's the pattern?
```

## The Challenge Method

The mentor won't hand you answers. Instead:

- **Level 1**: "What should we do?" — You propose the approach
- **Level 2**: "Why this way?" — You defend your design
- **Level 3**: "What breaks?" — You identify failure modes
- **Level 4**: "How does production differ?" — You think at scale

This mirrors how Cloud Architects think.

## Story Execution Pattern

Every piece of work follows Scrum:

```
Jira Story (LOS-XX)
  → Acceptance Criteria (what "done" looks like)
  → Design (architecture before code)
  → Implementation (hands-on)
  → Validation (does it actually work?)
  → Documentation (Confluence if it's a cloud/architecture concept)
  → Sprint Review (demo what you built)
```

## When You're Stuck

Follow this debugging ladder. This is how production engineers think:

```
1. Read the error message — actually read it, word by word
2. Check the logs — container logs, CI logs, system logs
3. Reproduce the issue — can you make it fail consistently?
4. Isolate the variable — what changed? What's different?
5. Search with context — don't google "docker error", 
   google the exact error message
6. Ask the mentor — with what you tried and what you observed
```

**Never say "it doesn't work." Always say "I see [this error] when I do [this action], and I've tried [these things]."**

## Documentation Rules

Document in Confluence (or `docs/academy/`) only:

- ✅ Cloud architecture concepts
- ✅ Architecture decisions and rationale
- ✅ DevOps patterns and practices
- ✅ AWS service mapping
- ✅ Lessons learned from debugging
- ✅ Design decisions

Do NOT document:

- ❌ Release notes (that's Release Management)
- ❌ Deployment runbooks (those go in repo automation)
- ❌ Sprint ceremonies (those live in Jira)

## Progress Tracking

See [PROGRESS.md](./PROGRESS.md) for current sprint status and completed work.

## Asking Good Questions

As you grow, your questions should evolve:

| Level | Question Style | Example |
|-------|---------------|---------|
| Beginner | "What command do I run?" | "How do I build a Docker image?" |
| Intermediate | "Why does this work this way?" | "Why does the frontend use multi-stage but backend doesn't?" |
| Advanced | "What are the tradeoffs?" | "Should we use Fargate or EC2 for ECS? What's the cost/control tradeoff?" |
| Architect | "How does this affect the system?" | "If we add a CDN, how does that change our TLS termination strategy?" |

You're currently transitioning from Intermediate → Advanced. The goal is Architect-level thinking by Sprint 12.
