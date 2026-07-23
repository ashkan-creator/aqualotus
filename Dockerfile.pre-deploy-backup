# syntax=docker/dockerfile:1

# ---------- مرحله ۱: بیلد فرانت‌اند ----------
FROM node:20-bookworm-slim AS frontend-build
WORKDIR /app/frontend

ENV NODE_ENV=development

COPY frontend/package*.json ./
RUN npm install --include=dev

COPY frontend/ ./
RUN npm run build

# ---------- مرحله ۲: ایمیج نهایی (Node 20 + MongoDB) ----------
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# نصب ابزارهای مورد نیاز، Node.js 20 و MongoDB
RUN apt-get update && apt-get install -y curl gnupg ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg && \
    echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list && \
    apt-get update && \
    apt-get install -y mongodb-org && \
    mkdir -p /data/db && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=80
ENV MONGO_URI=mongodb://127.0.0.1:27017/aqualotus

# نصب وابستگی‌های بک‌اند
COPY package*.json ./
RUN npm ci --omit=dev

# کپی کد بک‌اند و خروجی فرانت‌اند
COPY backend/ ./backend/
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# اسکریپت استارت هم‌زمان دیتابیس و نود
RUN echo '#!/bin/bin/sh\nmongod --fork --logpath /var/log/mongodb.log --dbpath /data/db\nnode backend/server.js' > /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 80

CMD ["/bin/sh", "/app/start.sh"]
