variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "ap-south-1"
}

variable "app_name" {
  description = "Application name — used as prefix for all resource names"
  type        = string
  default     = "learningos"
}

variable "environment" {
  description = "Deployment environment (dev / staging / prod)"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "aws_az" {
  description = "Availability zone for the public subnet"
  type        = string
  default     = "ap-south-1a"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro" # Free-tier eligible in ap-south-1 (new AWS credit plan)
}

variable "key_name" {
  description = "Name of the EC2 key pair to use for SSH access"
  type        = string
  default     = "learningos-keypair"
}

variable "image_retention_count" {
  description = "Number of Docker images to retain in ECR (lifecycle policy)"
  type        = number
  default     = 5
}

variable "github_repo" {
  description = "GitHub repo in 'owner/repo' format — used for OIDC trust policy"
  type        = string
  default     = "sangameshvakkkar/learningos-app"
}
