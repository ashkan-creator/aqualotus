#!/usr/bin/env python3
"""
create_export_script.py
می‌سازه: backend/scripts/exportData.js
یه اسکریپت Node که با mongoose (که از قبل نصبه، نیاز به پکیج جدید نداره)
همه‌ی کالکشن‌های دیتابیس لوکال رو می‌خونه و به فایل‌های JSON تبدیل می‌کنه
(بدون نیاز به mongodump که تو ایران فیلتره).

اجرا: python3 create_export_script.py
باید از ریشه‌ی پروژه (~/aqualotus) اجرا بشه.
"""
import os
import shutil
from datetime import datetime

PROJECT_ROOT = os.getcwd()
SCRIPT_DIR = os.path.join(PROJECT_ROOT, "backend", "scripts")
TARGET = os.path.join(SCRIPT_DIR, "exportData.js")

results = []


def report(step, ok, detail=""):
    mark = "✓" if ok else "❌"
    results.append(f"{mark} {step}" + (f" — {detail}" if detail else ""))
    print(f"{mark} {step}" + (f" — {detail}" if detail else ""))


EXPORT_JS = """import mongoose from 'mongoose'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import dotenv from 'dotenv'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
dotenv.config({ path: path.join(__dirname, '../../.env') })

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/aqualotus'
const OUT_DIR = path.join(__dirname, '../../data_export')

function serialize(value) {
  if (value === null || value === undefined) return value
  if (value && typeof value === 'object' && value._bsontype && /objectid/i.test(value._bsontype)) {
    return { $oid: value.toString() }
  }
  if (value instanceof Date) return { $date: value.toISOString() }
  if (Buffer.isBuffer(value)) return { $buffer: value.toString('base64') }
  if (Array.isArray(value)) return value.map(serialize)
  if (typeof value === 'object') {
    const out = {}
    for (const k of Object.keys(value)) out[k] = serialize(value[k])
    return out
  }
  return value
}

async function main() {
  console.log('در حال اتصال به:', MONGO_URI)
  await mongoose.connect(MONGO_URI)
  console.log('متصل شد.')

  fs.mkdirSync(OUT_DIR, { recursive: true })

  const collections = await mongoose.connection.db.listCollections().toArray()
  let total = 0
  for (const c of collections) {
    const docs = await mongoose.connection.db.collection(c.name).find({}).toArray()
    const serialized = docs.map(serialize)
    fs.writeFileSync(path.join(OUT_DIR, `${c.name}.json`), JSON.stringify(serialized))
    console.log(`✓ ${c.name}: ${docs.length} سند`)
    total += docs.length
  }

  console.log(`\\nتمام شد. مجموع اسناد: ${total}`)
  console.log(`خروجی در پوشه: ${OUT_DIR}`)
  await mongoose.disconnect()
}

main().catch((e) => {
  console.error('❌ خطا:', e)
  process.exit(1)
})
"""


def main():
    print(f"شروع در مسیر: {PROJECT_ROOT}\n")

    if not os.path.isdir(os.path.join(PROJECT_ROOT, "backend")):
        print("❌ این اسکریپت باید از ریشه‌ی پروژه (~/aqualotus) اجرا بشه — پوشه‌ی backend پیدا نشد.")
        return

    os.makedirs(SCRIPT_DIR, exist_ok=True)

    if os.path.exists(TARGET):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bpath = f"{TARGET}.pre-export-backup-{ts}"
        shutil.copy2(TARGET, bpath)
        report("بک‌آپ exportData.js قبلی", True, bpath)

    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(EXPORT_JS)
    report("ساخت backend/scripts/exportData.js", True, TARGET)

    print("\n--- خلاصه ---")
    for r in results:
        print(r)

    print("\nقدم بعدی: از ریشه‌ی پروژه بزن:  node backend/scripts/exportData.js")


if __name__ == "__main__":
    main()
