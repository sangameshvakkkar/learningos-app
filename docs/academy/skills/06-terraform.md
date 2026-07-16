# Skill 06: Terraform

> Infrastructure as Code — reproducible, version-controlled cloud infrastructure

## Status: ⬜ Sprint 8

## Why Terraform?

**Business Problem**: "I clicked 47 buttons in the AWS Console to set up the environment. Now I need to create the same setup for staging. And I don't remember what I clicked."

Terraform solves: manual infrastructure setup (ClickOps), environment drift, undocumented changes, unreproducible infrastructure.

## Core Concepts

### Infrastructure as Code (IaC)

```
ClickOps (bad)              IaC (good)
──────────────              ──────────
Click in AWS Console        Write .tf files
Screenshot the settings     Version control in Git
Hope you remember           `terraform apply` to reproduce
Pray staging matches prod   Identical by definition
```

### HCL — HashiCorp Configuration Language

```hcl
# Define what cloud provider to use
provider "aws" {
  region = "us-east-1"
}

# Define a resource
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name        = "learningos-web"
    Environment = "production"
  }
}
```

### The Terraform Workflow

```
terraform init      → Download providers and modules
terraform plan      → Preview what will change (dry run)
terraform apply     → Make the changes
terraform destroy   → Tear everything down
```

**Golden Rule**: Always `plan` before `apply`. Never apply without reviewing the plan.

### State

Terraform tracks what it manages in a **state file** (`terraform.tfstate`).

```
State file = Terraform's memory of what exists in AWS

Without state:
  - Terraform doesn't know what it created
  - It would try to create everything again
  - Or worse, it can't destroy anything
```

#### Remote State (Production)

```hcl
# Store state in S3, lock with DynamoDB
terraform {
  backend "s3" {
    bucket         = "learningos-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

**Why remote?**
- State file contains secrets → don't commit to Git
- Team collaboration → multiple engineers can `plan`/`apply`
- Locking → DynamoDB prevents concurrent modifications

### Variables and Outputs

```hcl
# variables.tf
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true    # Never shown in logs
}

# outputs.tf
output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}
```

### Modules

Reusable, composable infrastructure components:

```hcl
# modules/ecs-service/main.tf
resource "aws_ecs_service" "this" {
  name            = var.service_name
  cluster         = var.cluster_id
  task_definition = var.task_definition_arn
  desired_count   = var.desired_count
}

# root main.tf — use the module
module "backend" {
  source          = "./modules/ecs-service"
  service_name    = "learningos-backend"
  cluster_id      = aws_ecs_cluster.main.id
  desired_count   = 2
}
```

## LearningOS Terraform Structure (Sprint 8)

```text
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
├── modules/
│   ├── vpc/
│   ├── ecs/
│   ├── rds/
│   ├── alb/
│   └── ecr/
└── README.md
```

## Terraform in CI/CD

```yaml
# On PR: plan only (show what would change)
- name: Terraform Plan
  run: terraform plan -no-color
  # Review the plan in PR comments

# On merge to main: apply
- name: Terraform Apply
  run: terraform apply -auto-approve
```

**Never** auto-approve in production without human review.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| State in Git | Use remote backend (S3) |
| No state locking | Use DynamoDB |
| Hardcoded values | Use variables |
| One giant main.tf | Use modules |
| No `plan` before `apply` | Always review the plan |
| `terraform destroy` in prod | Add lifecycle `prevent_destroy` |

## Terraform vs Other IaC

| Tool | Language | Cloud | Approach |
|------|----------|-------|----------|
| Terraform | HCL | Any | Declarative |
| CloudFormation | JSON/YAML | AWS only | Declarative |
| Pulumi | TypeScript/Python | Any | Imperative |
| CDK | TypeScript/Python | AWS | Generates CloudFormation |

## Prerequisites for Sprint 8

- [ ] Complete Sprint 7 (manual AWS setup first — understand what Terraform will automate)
- [ ] Install Terraform CLI
- [ ] Understand AWS services being managed (VPC, ECS, RDS, ALB)
- [ ] S3 bucket for remote state

## Key Takeaway

Terraform is Git for infrastructure. Just like you'd never deploy application code by SSHing into a server and editing files, you should never create infrastructure by clicking in a console. **If it's not in code, it doesn't exist.**
