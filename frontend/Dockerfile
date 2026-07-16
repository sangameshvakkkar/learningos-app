# ── Stage 1: Build ──────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci                            # why ci and not install?

COPY . .
RUN npm run build

# ── Stage 2: Serve ──────────────────────────────────
FROM nginx:alpine AS production   # what serves static files?

# Copy ONLY the build output from Stage 1
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
