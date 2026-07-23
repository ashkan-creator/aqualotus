#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

PROJECT_ROOT = os.getcwd()
DOCKERFILE = os.path.join(PROJECT_ROOT, "Dockerfile")
IMPORT_JS_DIR = os.path.join(PROJECT_ROOT, "data_export")
IMPORT_JS = os.path.join(IMPORT_JS_DIR, "import-data.js")

results = []

def report(step, ok, detail=""):
    mark = "✓" if ok else "❌"
    results.append(f"{mark} {step}" + (f" — {detail}" if detail else ""))
    print(f"{mark} {step}" + (f" — {detail}" if detail else ""))

def backup(path):
    if os.path.exists(path):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bpath = f"{path}.pre-fix-backup-{ts}"
        shutil.copy2(path, bpath)
        return bpath
    return None

NEW_IMPORT_JS = """import mongoose from 'mongoose'
import fs from 'fs'
import path from 'path'

const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/aqualotus'
const DATA_DIR = '/app/data_export'

async function importAll() {
  await mongoose.connect(MONGO_URI)
  const db = mongoose.connection.db
  const files = fs.readdirSync(DATA_DIR).filter((f) => f.endsWith('.json'))
  for (const file of files) {
    const col = file.replace('.json', '')
    const count = await db.collection(col).countDocuments()
    if (count === 0) {
      const docs = JSON.parse(fs.readFileSync(path.join(DATA_DIR, file), 'utf8'))
      if (docs.length > 0) await db.collection(col).insertMany(docs)
      console.log('Imported: ' + col + ' (' + docs.length + ' docs)')
    } else {
      console.log('Skipped: ' + col + ' (already has ' + count + ' docs)')
    }
  }
  await mongoose.disconnect()
}

importAll().catch((e) => {
  console.error(e)
  process.exit(1)
})
"""

NEW_DOCKERFILE = """# syntax=docker/dockerfile:1

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
RUN apt-get update && apt-get install -y curl gnupg ca-certificates && \\
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \\
    apt-get install -y nodejs && \\
    curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg && \\
    echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list && \\
    apt-get update && \\
    apt-get install -y mongodb-org && \\
    mkdir -p /data/db/mongo /data/db/uploads && \\
    chmod 777 /data/db/mongo /data/db/uploads && \\
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

# کپی داده‌های صادراتی برای ایمپورت
COPY data_export/ ./data_export/

# ایجاد سیم‌لینک برای ماندگاری فایل‌های آپلود شده روی یک دیسک
RUN rm -rf /app/uploads && ln -s /data/db/uploads /app/uploads

# اسکریپت استارت هم‌زمان دیتابیس، ایمپورت داده‌ها و اجرای سرور
RUN echo '#!/bin/sh\\n\\
mkdir -p /data/db/mongo /data/db/uploads\\n\\
chmod 777 /data/db/mongo /data/db/uploads\\n\\
mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db/mongo\\n\\
sleep 3\\n\\
node /app/data_export/import-data.js\\n\\
cp -r /app/data_export/uploads/* /data/db/uploads/ 2>/dev/null || true\\n\\
node backend/server.js' > /app/start.sh && \\
    chmod +x /app/start.sh

EXPOSE 80

CMD ["/bin/sh", "/app/start.sh"]
"""

def fix_import_js():
    os.makedirs(IMPORT_JS_DIR, exist_ok=True)
    bpath = backup(IMPORT_JS)
    if bpath:
        report("بک‌آپ import-data.js", True, bpath)
    with open(IMPORT_JS, "w", encoding="utf-8") as f:
        f.write(NEW_IMPORT_JS)
    report("اصلاح و بروزرسانی import-data.js (سینتکس ESM)", True)

def fix_dockerfile():
    bpath = backup(DOCKERFILE)
    if bpath:
        report("بک‌آپ Dockerfile", True, bpath)
    with open(DOCKERFILE, "w", encoding="utf-8") as f:
        f.write(NEW_DOCKERFILE)
    report("اصلاح و بازنویسی کامل Dockerfile (مسیرهای /data/db/mongo و /data/db/uploads)", True)

def main():
    print(f"شروع اصلاحات در مسیر: {PROJECT_ROOT}\n")
    fix_import_js()
    fix_dockerfile()

    print("\n--- خلاصه وضعیت ---")
    for r in results:
        print(r)

if __name__ == "__main__":
    main()
