# Creates the Secrets Manager secret placeholder.
# The actual secret values are populated manually AFTER terraform apply:
#
#   aws secretsmanager put-secret-value \
#     --secret-id "learningos/dev/app" \
#     --region ap-south-1 \
#     --secret-string '{"DATABASE_URL":"...","SECRET_KEY":"...","CORS_ORIGINS":"..."}'

resource "aws_secretsmanager_secret" "app" {
  name        = "${var.app_name}/${var.environment}/app"
  description = "Application secrets for ${var.app_name} ${var.environment}: DATABASE_URL, SECRET_KEY, CORS_ORIGINS"

  # Allow immediate re-creation if secret is deleted (no recovery window in dev)
  recovery_window_in_days = 0

  tags = {
    App         = var.app_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
