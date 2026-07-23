#!/usr/bin/env python3
"""
setup_docker_deploy.py
اسکریپت آماده‌سازی دیپلوی Docker برای AquaLotus (بسته‌بندی Node + MongoDB در یک کانتینر)

این اسکریپت:
1. backend/server.js رو بک‌آپ می‌گیره و یه بخش برای سرو کردن frontend/dist اضافه می‌کنه
2. Dockerfile می‌سازه (multi-stage: build فرانت + ایمیج نهایی مبتنی بر mongo:7 + node)
3. docker-entrypoint.sh می‌سازه (mongod رو بالا میاره، صبر می‌کنه، بعد node رو اجرا می‌کنه)
4. .dockerignore می‌سازه

اجرا: python3 setup_docker_deploy.py
باید از داخل پوشه‌ی ریشه‌ی پروژه (~/aqualotus) اجرا بشه.
"""
import os
import sys
import shutil
from datetime import datetime

PROJECT_ROOT = os.getcwd()
SERVER_JS = os.path.join(PROJECT_ROOT, "backend", "server.js")

results = []


def report(step, ok, detail=""):
    mark = "✓" if ok else "❌"
    results.append(f"{mark} {step}" + (f" — {detail}" if detail else ""))
    print(f"{mark} {step}" + (f" — {detail}" if detail else ""))


def backup(path):
    if not os.path.exists(path):
        return None
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = f"{path}.pre-docker-backup-{ts}"
    shutil.copy2(path, backup_path)
    return backup_path


def patch_server_js():
    if not os.path.exists(SERVER_JS):
        report("پیدا کردن backend/server.js", False, f"فایل پیدا نشد: {SERVER_JS}")
        return False

    with open(SERVER_JS, "r", encoding="utf-8") as f:
        content = f.read()

    anchor = "app.use(notFound)"
    if anchor not in content:
        report("پچ backend/server.js", False, "لنگر 'app.use(notFound)' پیدا نشد — دستی چک کن")
        return False

    if "frontend/dist" in content:
        report("پچ backend/server.js", True, "قبلاً پچ شده بود، رد شد")
        return True

    bpath = backup(SERVER_JS)
    report("بک‌آپ backend/server.js", True, bpath)

    static_block = (
        "// --- سرو فایل‌های استاتیک فرانت (production, single-container) ---\n"
        "app.use(express.static(path.join(__dirname, '../frontend/dist')))\n"
        "app.get(/^(?!\\/api|\\/uploads|\\/go|\\/sitemap\\.xml).*/, (req, res) => {\n"
        "  res.sendFile(path.join(__dirname, '../frontend/dist/index.html'))\n"
        "})\n\n"
    )

    new_content = content.replace(anchor, static_block + anchor, 1)

    with open(SERVER_JS, "w", encoding="utf-8") as f:
        f.write(new_content)

    report("پچ backend/server.js", True, "بخش سرو استاتیک فرانت اضافه شد")
    return True


DOCKERFILE_CONTENT = """# syntax=docker/dockerfile:1

# ---------- مرحله ۱: build فرانت (Vite) ----------
FROM node:20-bookworm-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---------- مرحله ۲: ایمیج نهایی (Mongo رسمی + Node) ----------
# از ایمیج رسمی mongo:7 شروع می‌کنیم (از طریق میرور داکر رانفلر قابل دسترسه)
# و Node رو از ریپازیتوری خود دبیان نصب می‌کنیم (بدون نیاز به دامنه‌ی فیلترشده‌ی nodesource)
FROM mongo:7

RUN apt-get update \\
    && apt-get install -y --no-install-recommends nodejs npm \\
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
"""

ENTRYPOINT_CONTENT = """#!/bin/bash
set -e

echo "در حال اجرای mongod..."
mongod --dbpath /data/db --bind_ip 127.0.0.1 &
MONGO_PID=$!

echo "منتظر آماده شدن MongoDB..."
until mongosh --quiet --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1; do
  sleep 1
done
echo "MongoDB آماده است."

echo "اجرای سرور Node..."
exec node backend/server.js
"""

DOCKERIGNORE_CONTENT = """node_modules
frontend/node_modules
frontend/dist
backend/node_modules
.env
.git
.gitignore
*.pre-*-backup*
*.log
"""


def write_file(path, content, label):
    existed = os.path.exists(path)
    if existed:
        bpath = backup(path)
        report(f"بک‌آپ {label}", True, bpath)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    report(f"ساخت/به‌روزرسانی {label}", True, path)


def main():
    print(f"شروع در مسیر: {PROJECT_ROOT}\n")

    if not os.path.isdir(os.path.join(PROJECT_ROOT, "backend")) or not os.path.isdir(
        os.path.join(PROJECT_ROOT, "frontend")
    ):
        print("❌ این اسکریپت باید از ریشه‌ی پروژه (~/aqualotus) اجرا بشه — پوشه‌ی backend یا frontend پیدا نشد.")
        sys.exit(1)

    patch_server_js()
    write_file(os.path.join(PROJECT_ROOT, "Dockerfile"), DOCKERFILE_CONTENT, "Dockerfile")
    write_file(
        os.path.join(PROJECT_ROOT, "docker-entrypoint.sh"),
        ENTRYPOINT_CONTENT,
        "docker-entrypoint.sh",
    )
    os.chmod(os.path.join(PROJECT_ROOT, "docker-entrypoint.sh"), 0o755)
    write_file(os.path.join(PROJECT_ROOT, ".dockerignore"), DOCKERIGNORE_CONTENT, ".dockerignore")

    print("\n--- خلاصه ---")
    for r in results:
        print(r)

    print(
        "\nقدم بعدی: تغییرات رو کامیت و پوش کن، بعد تو داشبورد رانفلر یه دیسک پرسیستنت رو مسیر /data/db بساز و سرویس رو ری‌دیپلوی کن."
    )


if __name__ == "__main__":
    main()
