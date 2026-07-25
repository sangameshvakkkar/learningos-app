# ──────────────────────────────────────────────────────────────
# EC2 Instance Role
# Grants the EC2 instance permission to:
#   - Pull images from ECR
#   - Read secrets from AWS Secrets Manager
# ──────────────────────────────────────────────────────────────

data "aws_iam_policy_document" "ec2_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2" {
  name               = "${var.app_name}-${var.environment}-ec2-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume.json

  tags = {
    Name = "${var.app_name}-${var.environment}-ec2-role"
  }
}

# ECR: allow EC2 to authenticate and pull images
resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# Secrets Manager: least-privilege read for app secrets only
data "aws_iam_policy_document" "secrets_read" {
  statement {
    effect    = "Allow"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:*:*:secret:${var.app_name}/${var.environment}/*"]
  }
}

resource "aws_iam_policy" "secrets_read" {
  name   = "${var.app_name}-${var.environment}-secrets-read"
  policy = data.aws_iam_policy_document.secrets_read.json
}

resource "aws_iam_role_policy_attachment" "secrets_read" {
  role       = aws_iam_role.ec2.name
  policy_arn = aws_iam_policy.secrets_read.arn
}

resource "aws_iam_instance_profile" "ec2" {
  name = "${var.app_name}-${var.environment}-ec2-profile"
  role = aws_iam_role.ec2.name
}

# ──────────────────────────────────────────────────────────────
# GitHub Actions OIDC Role
# Allows GitHub Actions workflows (on push to main) to assume
# this role and push to ECR — NO long-lived AWS keys in GitHub.
# ──────────────────────────────────────────────────────────────

data "aws_caller_identity" "current" {}

# GitHub's OIDC provider (create once per AWS account)
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = ["sts.amazonaws.com"]

  # GitHub's OIDC thumbprint (stable — GitHub rotates certs but keeps this thumbprint)
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

data "aws_iam_policy_document" "github_actions_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # Allow the specific repo's main and feature branches to assume this role for dev deployments
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = [
        "repo:${var.github_repo}:ref:refs/heads/main",
        "repo:${var.github_repo}:ref:refs/heads/develop",
        "repo:${var.github_repo}:ref:refs/heads/feature/*"
      ]
    }
  }
}

resource "aws_iam_role" "github_actions" {
  name               = "${var.app_name}-${var.environment}-github-actions-role"
  assume_role_policy = data.aws_iam_policy_document.github_actions_assume.json

  tags = {
    Name = "${var.app_name}-${var.environment}-github-actions-role"
  }
}

# GitHub Actions needs: ECR push + read (for docker build cache), EC2 SSH (done separately via key)
data "aws_iam_policy_document" "github_actions_ecr" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:PutImage",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "github_actions_ecr" {
  name   = "${var.app_name}-${var.environment}-github-actions-ecr"
  policy = data.aws_iam_policy_document.github_actions_ecr.json
}

resource "aws_iam_role_policy_attachment" "github_actions_ecr" {
  role       = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.github_actions_ecr.arn
}
