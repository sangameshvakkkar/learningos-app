---
name: terraform-iac
description: >
  Terraform Infrastructure as Code skill for LearningOS. Covers HCL, providers,
  resources, state management, modules, remote backend, and CI integration.
  Activate when working on Terraform files, infrastructure provisioning, or IaC tasks.
  Reference: docs/academy/skills/06-terraform.md
---

# Terraform IaC Skill

When working with Terraform in LearningOS, follow these instructions.

## Core Workflow

```
terraform init    → Download providers
terraform plan    → Preview changes (ALWAYS review)
terraform apply   → Execute changes
terraform destroy → Tear down (careful!)
```

**Golden Rule**: Never `apply` without reading the `plan`.

## Project Structure

```
terraform/
├── environments/
│   ├── dev/        → Dev-specific config
│   └── prod/       → Prod-specific config
├── modules/
│   ├── vpc/
│   ├── ecs/
│   ├── rds/
│   └── alb/
└── README.md
```

## State Management

- Remote state in S3 + DynamoDB locking
- Never commit `terraform.tfstate` to Git
- State file contains secrets — treat as sensitive
- One state file per environment

## Best Practices

1. **Variables** for everything that differs between environments
2. **Modules** for reusable infrastructure components
3. **Outputs** to expose values for other modules/tools
4. **`sensitive = true`** on variables containing secrets
5. **`lifecycle { prevent_destroy = true }`** on critical resources (RDS)
6. **Plan in CI** on PRs — `terraform plan` as PR comment
7. **Apply on merge** — only after human review

## Common Mistakes

- State in Git → use S3 backend
- Hardcoded values → use variables
- One giant `main.tf` → use modules
- No locking → use DynamoDB
- `destroy` without thinking → use `prevent_destroy`

## Deep Reference

Read `docs/academy/skills/06-terraform.md` for complete guide.
