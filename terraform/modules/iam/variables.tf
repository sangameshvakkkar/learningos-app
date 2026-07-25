variable "app_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "github_repo" {
  description = "GitHub repo in 'owner/repo' format for OIDC trust policy"
  type        = string
}
