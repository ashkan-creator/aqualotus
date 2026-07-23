# syntax=docker/dockerfile:1

# ---------- مرحله ۱: build فرانت (Vite) ----------
FROM node:20-bookworm-slim AS frontend-build
WORKDIR /app/frontend

# خنثی کردن تنظیمات پروداکشن سرور برای نصب قطعی Vite
ENV NODE_ENV=development

COPY frontend/package*.json ./
# فورس کردن نصب تمام پکیج‌های توسعه
RUN npm install --include=dev

COPY frontend/ ./
RUN npm run build

# ---------- مرحله ۲: ایمیج نهایی (Mongo رسمی + Node) ----------
FROM mongo:7

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# نصب وابستگی‌های بک‌اند برای حالت پروداکشن
ENV NODE_ENV=production
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
