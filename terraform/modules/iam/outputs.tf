output "instance_profile_name" {
  description = "EC2 instance profile name — attached to the EC2 instance"
  value       = aws_iam_instance_profile.ec2.name
}

output "github_actions_role_arn" {
  description = "ARN for GitHub Actions OIDC role — add to GitHub repo var ACTIONS_ROLE_ARN"
  value       = aws_iam_role.github_actions.arn
}
