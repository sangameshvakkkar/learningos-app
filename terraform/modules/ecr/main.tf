resource "aws_ecr_repository" "frontend" {
  name                 = "${var.app_name}-${var.environment}-frontend"
  image_tag_mutability = "MUTABLE" # allows overwriting 'latest' tag

  image_scanning_configuration {
    scan_on_push = true # Trivy-compatible: ECR native scan on every push
  }

  tags = {
    Name        = "${var.app_name}-${var.environment}-frontend"
    App         = var.app_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_ecr_repository" "backend" {
  name                 = "${var.app_name}-${var.environment}-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "${var.app_name}-${var.environment}-backend"
    App         = var.app_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Lifecycle policy: keep only the N most recent images to stay within 500 MB free tier
resource "aws_ecr_lifecycle_policy" "frontend" {
  repository = aws_ecr_repository.frontend.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last ${var.image_retention_count} images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = var.image_retention_count
      }
      action = { type = "expire" }
    }]
  })
}

resource "aws_ecr_lifecycle_policy" "backend" {
  repository = aws_ecr_repository.backend.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last ${var.image_retention_count} images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = var.image_retention_count
      }
      action = { type = "expire" }
    }]
  })
}
