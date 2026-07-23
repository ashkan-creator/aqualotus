# syntax=docker/dockerfile:1

# ---------- مرحله ۱: build فرانت (Vite) ----------
FROM node:20-bookworm-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm install vite
RUN npm run build

# ---------- مرحله ۲: ایمیج نهایی (Mongo رسمی + Node) ----------
# از ایمیج رسمی mongo:7 شروع می‌کنیم (از طریق میرور داکر رانفلر قابل دسترسه)
# و Node رو از ریپازیتوری خود دبیان نصب می‌کنیم (بدون نیاز به دامنه‌ی فیلترشده‌ی nodesource)
FROM mongo:7

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# نصب وابستگی‌های بک‌اند (فقط production)
COPY package*.json ./
RUN npm ci --omit=dev

# کپی کد بک‌اند
COPY backend/ ./backend/

# کپی خروجی build شده‌ی فرانت
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# اسکریپت شروع
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80
ENV PORT=80
ENV MONGO_URI=mongodb://127.0.0.1:27017/aqualotus

ENTRYPOINT ["/docker-entrypoint.sh"]
