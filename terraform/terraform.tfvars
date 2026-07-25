# Non-secret variable overrides — safe to commit
# Secrets (DATABASE_URL, SECRET_KEY) live in AWS Secrets Manager, NOT here.

aws_region   = "ap-south-1"
app_name     = "learningos"
environment  = "dev"
instance_type = "t2.micro"
key_name     = "learningos-dev-key"
github_repo  = "sangameshvakkkar/learningos-app"
