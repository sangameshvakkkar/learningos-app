output "ec2_public_ip" {
  description = "Public IP of the EC2 instance — access the app at http://<this-ip>"
  value       = module.ec2.public_ip
}

output "ec2_instance_id" {
  description = "EC2 instance ID"
  value       = module.ec2.instance_id
}

output "frontend_ecr_repo_url" {
  description = "ECR repository URL for the frontend image"
  value       = module.ecr.frontend_repo_url
}

output "backend_ecr_repo_url" {
  description = "ECR repository URL for the backend image"
  value       = module.ecr.backend_repo_url
}

output "github_actions_role_arn" {
  description = "IAM role ARN for GitHub Actions OIDC — add this to GitHub repo var ACTIONS_ROLE_ARN"
  value       = module.iam.github_actions_role_arn
}

output "secret_arn" {
  description = "ARN of the AWS Secrets Manager secret — fill values after terraform apply"
  value       = module.secrets.secret_arn
}

output "app_url" {
  description = "Application URL (HTTP, no domain)"
  value       = "http://${module.ec2.public_ip}"
}
