#!/usr/bin/env python3
"""
اسکریپت پچ هدر — نسخه v13 + v14
۱. فاصله‌ی سرچ‌بار دسکتاپ از آیکون کاربر (سمت راستش)
۲. بزرگ‌تر کردن لوگو به ۱۴۰٪ اندازه‌ی فعلی
- قبل از تغییر، از index.css بک‌آپ می‌گیره
- در انتهای فایل، زیر مارکرهای نسخه‌دار جدید اضافه می‌کنه (بدون دست‌زدن به کد قبلی)
"""
import os
import shutil

CSS_PATH = os.path.join("frontend", "src", "index.css")
BACKUP_PATH = os.path.join("frontend", "src", "index.css.pre-v13-v14-backup")

PATCH = """
/* --- header v13 redesign --- */
.aq-header-search-desktop {
  margin-inline-start: 14px;
}

/* --- header v14 redesign --- */
.aq-brand-logo-img {
  width: clamp(78px, 8.4vw, 106px);
  height: clamp(78px, 8.4vw, 106px);
}

@media (max-width: 767px) {
  .aq-brand-logo-img {
    width: 73px;
    height: 73px;
  }
}
"""


def main():
    if not os.path.exists(CSS_PATH):
        print(f"✗ فایل {CSS_PATH} پیدا نشد. این اسکریپت رو تو ریشه‌ی پروژه (~/aqualotus) اجرا کن.")
        return

    try:
        shutil.copy2(CSS_PATH, BACKUP_PATH)
        print(f"✓ بک‌آپ گرفته شد: {BACKUP_PATH}")
    except Exception as e:
        print(f"✗ خطا در گرفتن بک‌آپ: {e}")
        return

    try:
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        if "header v13 redesign" in content or "header v14 redesign" in content:
            print("✗ به‌نظر می‌رسه این پچ قبلاً زده شده (مارکر v13 یا v14 پیدا شد). چیزی دوباره اضافه نشد.")
            return

        with open(CSS_PATH, "a", encoding="utf-8") as f:
            f.write(PATCH)

        print(f"✓ پچ v13 (فاصله سرچ‌بار) اضافه شد")
        print(f"✓ پچ v14 (بزرگ‌تر شدن لوگو به ۱۴۰٪) اضافه شد")
        print(f"✓ فایل ذخیره شد: {CSS_PATH}")
        print("✓ تمام. یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
    except Exception as e:
        print(f"✗ خطا در نوشتن فایل: {e}")
        print(f"  فایل اصلی از رو بک‌آپ ({BACKUP_PATH}) قابل بازیابیه.")


if __name__ == "__main__":
    main()
