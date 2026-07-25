provider "aws" {
  region = var.aws_region

  # Default tags applied to ALL resources in this workspace automatically
  default_tags {
    tags = {
      application    = "learning-os"
      application_id = "APP000260725"
      environment    = var.environment
      cost_center    = "LOS-001"
      ManagedBy      = "terraform"
    }
  }
}

# ──────────────────────────────────────────────────────────────
# Root module — wires all child modules together
# ──────────────────────────────────────────────────────────────

module "vpc" {
  source = "../../modules/vpc"
  app_name    = var.app_name
  environment = var.environment
  vpc_cidr    = var.vpc_cidr
  subnet_cidr = var.subnet_cidr
  aws_az      = var.aws_az
}

module "security" {
  source = "../../modules/security"
  app_name    = var.app_name
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
}

module "ecr" {
  source = "../../modules/ecr"
  app_name              = var.app_name
  environment           = var.environment
  image_retention_count = var.image_retention_count
}

module "iam" {
  source = "../../modules/iam"
  app_name    = var.app_name
  environment = var.environment
  # OIDC: allow GitHub Actions to assume the deploy role without long-lived keys
  github_repo = var.github_repo
}

module "secrets" {
  source = "../../modules/secrets"
  app_name    = var.app_name
  environment = var.environment
}

module "ec2" {
  source = "../../modules/ec2"
  app_name             = var.app_name
  environment          = var.environment
  aws_region           = var.aws_region
  subnet_id            = module.vpc.subnet_id
  security_group_id    = module.security.sg_id
  key_name             = var.key_name
  instance_type        = var.instance_type
  instance_profile_name = module.iam.instance_profile_name
  secret_id            = module.secrets.secret_id
  frontend_repo_url    = module.ecr.frontend_repo_url
  backend_repo_url     = module.ecr.backend_repo_url
}
