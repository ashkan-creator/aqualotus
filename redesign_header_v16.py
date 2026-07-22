#!/usr/bin/env python3
"""
اسکریپت هدر v16 (فقط CSS، بدون دست‌زدن به JSX)
مشکل v15: justify-content:space-between کل فضای خالی رو یه‌جا (بین لوگو و محصولات) جمع کرد.
این نسخه به‌جاش فاصله‌ها رو دستی و کنترل‌شده تنظیم می‌کنه:
- فاصله‌ی لوگو تا «محصولات»: کم و ثابت
- فاصله‌ی «تماس با ما» تا آیکون کاربر: کمی بیشتر از قبل (نه چسبیده، نه خیلی دور)
- فاصله‌ی آیکون کاربر تا سرچ‌بار: بیشتر (بلاک از سرچ‌بار دورتر بشه)
"""
import os
import shutil

CSS_PATH = os.path.join("frontend", "src", "index.css")
CSS_BACKUP = os.path.join("frontend", "src", "index.css.pre-v16-backup")

PATCH = """
/* --- header v16 redesign --- */
.aq-navbar-row {
  justify-content: flex-start !important;
}

.aq-navbar-right-group {
  margin-inline-start: 20px;
}

.aq-navbar-right-group > *:nth-child(2) {
  margin-inline-start: 16px;
}

.aq-header-search-desktop {
  margin-inline-start: 32px !important;
}
"""


def main():
    if not os.path.exists(CSS_PATH):
        print(f"✗ فایل {CSS_PATH} پیدا نشد. این اسکریپت رو تو ریشه‌ی پروژه (~/aqualotus) اجرا کن.")
        return

    with open(CSS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if "header v16 redesign" in content:
        print("✗ مارکر v16 قبلاً موجوده — چیزی دوباره اضافه نشد.")
        return

    if "aq-navbar-right-group" not in content:
        print("✗ کلاس aq-navbar-right-group تو index.css/Header.jsx پیدا نشد — یعنی احتمالاً v15 هنوز اجرا نشده. اول v15 رو بزن.")
        return

    shutil.copy2(CSS_PATH, CSS_BACKUP)
    print(f"✓ بک‌آپ گرفته شد: {CSS_BACKUP}")

    with open(CSS_PATH, "a", encoding="utf-8") as f:
        f.write(PATCH)

    print("✓ پچ v16 اضافه شد: فاصله‌ی لوگو تا منو کم شد، فاصله‌ی تماس‌باما تا آیکون کاربر کمی بیشتر شد، فاصله‌ی آیکون کاربر تا سرچ‌بار بیشتر شد")
    print(f"✓ فایل ذخیره شد: {CSS_PATH}")
    print("✓ تمام. یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")


if __name__ == "__main__":
    main()
