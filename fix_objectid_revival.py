#!/usr/bin/env python3
"""
fix_objectid_revival.py

مشکل: فایل‌های data_export/*.json آی‌دی‌ها رو به‌فرم { "$oid": "..." } و
تاریخ‌ها رو به‌فرم { "$date": "..." } ذخیره کردن (فرمت درستیه برای export).
ولی import-data.js موقع خوندن این فایل‌ها، این فرمت رو به ObjectId/Date واقعی
تبدیل نمی‌کنه و مستقیم insertMany می‌کنه — نتیجه: تو دیتابیس، _id و بقیه‌ی
فیلدهای آی‌دی به‌جای ObjectId واقعی، یه شیء {$oid:...} ذخیره میشه. همین باعث
میشه صفحه‌ی ویرایش محصول «یافت نشد» بده، اسلایدرها لیست نشن، و چک ادمین بودن
کاربر لاگین‌شده fail بشه (چون کاربر با آی‌دی واقعی پیدا نمیشه).

این اسکریپت یه تابع revive() اضافه می‌کنه که قبل از insertMany، این فرمت‌ها
رو به ObjectId/Date/Buffer واقعی برمی‌گردونه.

اجرا: python3 fix_objectid_revival.py
باید از ریشه‌ی پروژه (~/aqualotus) اجرا بشه.

⚠️ بعد از اجرای این اسکریپت و push، حتماً باید دیتای خراب فعلی رو تو
دیتابیس زنده (روی رانفلر) پاک کنی، چون اسکریپت import اگه کالکشن خالی
نباشه اصلاً وارد نمی‌کنه (skip می‌کنه). دستور پاک‌کردن جدا داده میشه.
"""
import os
import shutil
from datetime import datetime

PROJECT_ROOT = os.getcwd()
IMPORT_JS = os.path.join(PROJECT_ROOT, "data_export", "import-data.js")

NEW_CONTENT = """import mongoose from 'mongoose'
import fs from 'fs'
import path from 'path'

const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/aqualotus'
const DATA_DIR = '/app/data_export'

function revive(value) {
  if (value === null || value === undefined) return value
  if (Array.isArray(value)) return value.map(revive)
  if (typeof value === 'object') {
    const keys = Object.keys(value)
    if (keys.length === 1 && typeof value.$oid === 'string') {
      return new mongoose.Types.ObjectId(value.$oid)
    }
    if (keys.length === 1 && typeof value.$date === 'string') {
      return new Date(value.$date)
    }
    if (keys.length === 1 && typeof value.$buffer === 'string') {
      return Buffer.from(value.$buffer, 'base64')
    }
    const out = {}
    for (const k of keys) out[k] = revive(value[k])
    return out
  }
  return value
}

async function importAll() {
  await mongoose.connect(MONGO_URI)
  const db = mongoose.connection.db
  const files = fs.readdirSync(DATA_DIR).filter((f) => f.endsWith('.json'))
  for (const file of files) {
    const col = file.replace('.json', '')
    const count = await db.collection(col).countDocuments()
    if (count === 0) {
      const raw = JSON.parse(fs.readFileSync(path.join(DATA_DIR, file), 'utf8'))
      const docs = raw.map(revive)
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


def report(step, ok, detail=""):
    mark = "✓" if ok else "❌"
    print(f"{mark} {step}" + (f" — {detail}" if detail else ""))


def main():
    print(f"شروع در مسیر: {PROJECT_ROOT}\n")

    if not os.path.exists(IMPORT_JS):
        report("پیدا کردن data_export/import-data.js", False, f"پیدا نشد: {IMPORT_JS}")
        return

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bpath = f"{IMPORT_JS}.pre-revive-backup-{ts}"
    shutil.copy2(IMPORT_JS, bpath)
    report("بک‌آپ import-data.js", True, bpath)

    with open(IMPORT_JS, "w", encoding="utf-8") as f:
        f.write(NEW_CONTENT)
    report("اضافه‌شدن تابع revive() برای تبدیل $oid/$date به نوع واقعی", True)

    print("\nقدم بعدی:")
    print("1) git add data_export/import-data.js && git commit -m 'fix objectid revival on import' && git push")
    print("2) قبل از ری‌دیپلوی، از ترمینال رانفلر دیتای خراب فعلی رو پاک کن (دستور جدا می‌فرستم)")
    print("3) بعد ری‌دیپلوی کن رو رانفلر")


if __name__ == "__main__":
    main()
