# syntax=docker/dockerfile:1

# ---------- مرحله ۱: بیلد فرانت‌اَند ----------
FROM node:20-bookworm-slim AS frontend-build
WORKDIR /app/frontend

ENV NODE_ENV=development

COPY frontend/package*.json ./
RUN npm install --include=dev

COPY frontend/ ./
RUN npm run build

# ---------- مرحله ۲: اجرای پروژه با Node 20 ----------
FROM node:20-bookworm-slim
WORKDIR /app

ENV NODE_ENV=production

COPY package*.json ./
RUN npm ci --omit=dev

COPY backend/ ./backend/
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

EXPOSE 80
ENV PORT=80

CMD ["node", "backend/server.js"]
