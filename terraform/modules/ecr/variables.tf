variable "app_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "image_retention_count" {
  description = "Number of images to retain per ECR repository"
  type        = number
  default     = 5
}
