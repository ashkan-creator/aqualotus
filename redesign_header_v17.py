#!/usr/bin/env python3
"""
اسکریپت هدر v17 (فقط CSS)
علت جابه‌جایی آیکون کاربر ادمین رو موبایل: باز شدن منوی بلند ادمین (۱۲ آیتم) باعث ظاهر/محو شدن
اسکرول‌بار عمودی می‌شه که عرض کل صفحه رو عوض می‌کنه و همه‌چیز می‌پره.
راه‌حل: با scrollbar-gutter: stable، جای اسکرول‌بار همیشه رزرو می‌شه، چه باشه چه نباشه — پس هیچ‌وقت عرض صفحه عوض نمی‌شه.
"""
import os
import shutil

CSS_PATH = os.path.join("frontend", "src", "index.css")
CSS_BACKUP = os.path.join("frontend", "src", "index.css.pre-v17-backup")

PATCH = """
/* --- header v17 redesign --- */
html {
  scrollbar-gutter: stable;
}
"""


def main():
    if not os.path.exists(CSS_PATH):
        print(f"✗ فایل {CSS_PATH} پیدا نشد. این اسکریپت رو تو ریشه‌ی پروژه (~/aqualotus) اجرا کن.")
        return

    with open(CSS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if "header v17 redesign" in content:
        print("✗ مارکر v17 قبلاً موجوده — چیزی دوباره اضافه نشد.")
        return

    shutil.copy2(CSS_PATH, CSS_BACKUP)
    print(f"✓ بک‌آپ گرفته شد: {CSS_BACKUP}")

    with open(CSS_PATH, "a", encoding="utf-8") as f:
        f.write(PATCH)

    print("✓ پچ v17 اضافه شد: جای اسکرول‌بار همیشه رزرو می‌شه (scrollbar-gutter: stable)")
    print(f"✓ فایل ذخیره شد: {CSS_PATH}")
    print("✓ تمام. یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")


if __name__ == "__main__":
    main()
