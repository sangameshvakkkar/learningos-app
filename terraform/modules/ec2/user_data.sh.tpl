#!/bin/bash
# ──────────────────────────────────────────────────────────────────────────────
# LearningOS EC2 Bootstrap Script (user_data)
# Runs ONCE on first instance launch.
# Sets up Docker, fetches secrets from AWS Secrets Manager, starts containers.
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail
exec > >(tee /var/log/learningos-bootstrap.log | logger -t learningos-bootstrap) 2>&1

echo "==> [1/6] System update"
dnf update -y

echo "==> [2/6] Install Docker + AWS CLI + Python3"
dnf install -y docker python3 python3-pip aws-cli
systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

# Docker Compose v2 (plugin)
mkdir -p /usr/local/lib/docker/cli-plugins
curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

echo "==> [3/6] Create app directory"
APP_DIR="/opt/learningos"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

echo "==> [4/6] Fetch secrets from AWS Secrets Manager"
SECRET_JSON=$(aws secretsmanager get-secret-value \
  --secret-id "${secret_id}" \
  --region "${aws_region}" \
  --query SecretString \
  --output text)

# Write .env from secret JSON — ephemeral, never committed
python3 - <<'EOF'
import sys, json, os

secret = json.loads(os.environ.get('SECRET_JSON', '{}'))
env_path = '/opt/learningos/.env'
with open(env_path, 'w') as f:
    for k, v in secret.items():
        f.write(f"{k}={v}\n")
print(f"[secrets] wrote {len(secret)} variables to {env_path}")
EOF

export SECRET_JSON="$SECRET_JSON"
python3 /dev/stdin <<< "
import sys, json, os
secret = json.loads(os.environ['SECRET_JSON'])
with open('/opt/learningos/.env', 'w') as f:
    for k, v in secret.items():
        f.write(f'{k}={v}\n')
print(f'[secrets] {len(secret)} vars written')
"

echo "==> [5/6] Authenticate Docker to ECR"
aws ecr get-login-password --region "${aws_region}" | \
  docker login --username AWS --password-stdin "${frontend_repo}"

echo "==> [6/6] Write docker-compose and start services"
cat > "$APP_DIR/docker-compose.yml" <<COMPOSE
services:
  backend:
    image: ${backend_repo}:latest
    container_name: learningos-backend
    restart: unless-stopped
    env_file: .env
    expose:
      - "8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: ${frontend_repo}:latest
    container_name: learningos-frontend
    restart: unless-stopped
    ports:
      - "80:80"
    depends_on:
      backend:
        condition: service_healthy
COMPOSE

docker compose pull
docker compose up -d

echo "==> Bootstrap complete. App should be reachable on port 80."

# ──────────────────────────────────────────────────────────────────────────────
# Deploy script — used by GitHub Actions CI/CD on subsequent deployments
# Written to disk so CI can invoke via SSH:
#   ssh ec2-user@<IP> 'sudo /opt/learningos/deploy.sh'
# ──────────────────────────────────────────────────────────────────────────────
cat > "$APP_DIR/deploy.sh" <<'DEPLOY'
#!/bin/bash
set -euo pipefail
APP_DIR="/opt/learningos"
cd "$APP_DIR"

echo "[deploy] Refreshing secrets..."
SECRET_JSON=$(aws secretsmanager get-secret-value \
  --secret-id "${secret_id}" \
  --region "${aws_region}" \
  --query SecretString \
  --output text)
python3 - <<EOF
import sys, json, os
secret = json.loads(os.environ['SECRET_JSON'])
with open('/opt/learningos/.env', 'w') as f:
    for k, v in secret.items():
        f.write(f'{k}={v}\n')
EOF

echo "[deploy] Pulling latest images from ECR..."
aws ecr get-login-password --region "${aws_region}" | \
  docker login --username AWS --password-stdin "${frontend_repo}"
docker compose pull

echo "[deploy] Restarting containers..."
docker compose up -d --remove-orphans

echo "[deploy] Done."
DEPLOY

chmod +x "$APP_DIR/deploy.sh"
chown -R ec2-user:ec2-user "$APP_DIR"
