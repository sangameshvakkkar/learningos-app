terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "learningos-tfstate-dev"
    key          = "learningos/dev/terraform.tfstate"
    region       = "ap-south-1"
    use_lockfile = true # Native S3 locking — no DynamoDB needed (Terraform >= 1.10)
  }
}
