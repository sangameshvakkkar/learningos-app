variable "app_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "subnet_id" {
  description = "Public subnet ID to launch the EC2 instance in"
  type        = string
}

variable "security_group_id" {
  description = "Security group ID to attach to the instance"
  type        = string
}

variable "key_name" {
  description = "EC2 key pair name for SSH access"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "instance_profile_name" {
  description = "IAM instance profile name to attach"
  type        = string
}

variable "secret_id" {
  description = "AWS Secrets Manager secret ID containing app secrets"
  type        = string
}

variable "frontend_repo_url" {
  description = "ECR repository URL for the frontend image"
  type        = string
}

variable "backend_repo_url" {
  description = "ECR repository URL for the backend image"
  type        = string
}
