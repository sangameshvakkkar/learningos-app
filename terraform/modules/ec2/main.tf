# Fetch latest Amazon Linux 2023 AMI for ap-south-1 (free tier eligible)
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux_2023.id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.security_group_id]
  key_name               = var.key_name
  iam_instance_profile   = var.instance_profile_name

  # Bootstrap script: install Docker, fetch secrets, start containers
  user_data = templatefile("${path.module}/user_data.sh.tpl", {
    aws_region       = var.aws_region
    secret_id        = var.secret_id
    frontend_repo    = var.frontend_repo_url
    backend_repo     = var.backend_repo_url
  })

  # Ensure instance is replaced (not updated in-place) when user_data changes
  user_data_replace_on_change = true

  root_block_device {
    volume_size = 20   # GB — sufficient for OS + Docker images
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name = "${var.app_name}-${var.environment}-ec2"
  }
}

# Elastic IP — static public IP that survives EC2 stop/start
resource "aws_eip" "app" {
  instance = aws_instance.app.id
  domain   = "vpc"

  tags = {
    Name = "${var.app_name}-${var.environment}-eip"
  }
}
