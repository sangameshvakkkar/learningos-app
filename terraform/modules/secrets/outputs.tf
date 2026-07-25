output "secret_id" {
  description = "Secret name/ID — used by EC2 fetch-secrets script"
  value       = aws_secretsmanager_secret.app.id
}

output "secret_arn" {
  description = "Full ARN of the secret"
  value       = aws_secretsmanager_secret.app.arn
}
