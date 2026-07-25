# Non-secret variable overrides — safe to commit
# Secrets (DATABASE_URL, SECRET_KEY) live in AWS Secrets Manager, NOT here.

aws_region   = "ap-south-1"
app_name     = "learningos"
environment  = "dev"
instance_type = "t3.micro"
key_name     = "learningos-keypair"
github_repo  = "sangameshvakkkar/learningos-app"
