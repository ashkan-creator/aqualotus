#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
کش‌باست کردن آدرس عکس موبایل بنر (که تا الان هیچ‌وقت ?v نداشت، برای همین مرورگر
داشت نسخه‌ی قدیمی/خراب رو کش می‌کرد).
از داخل ~/aqualotus اجرا کن:
    python3 cachebust_mobile_banner.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

FONTS_CSS = "frontend/src/fonts.css"

if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
    raise SystemExit(1)

with open(FONTS_CSS, "r", encoding="utf-8") as f:
    content = f.read()

old = "url('/images/quiz-banner-mobile.jpg')"
new = "url('/images/quiz-banner-mobile.jpg?v=2')"

if new in content:
    print("(رد شد، قبلاً کش‌باست شده بود)")
elif old in content:
    shutil.copy2(FONTS_CSS, f"{FONTS_CSS}.pre-mobile-cachebust-backup")
    content = content.replace(old, new, 1)
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {FONTS_CSS}")
else:
    print(f"{BAD} آدرس عکس موبایل پیدا نشد -- محتوای فعلی fonts.css رو بفرست")

print("\nتمام شد. یه Hard Refresh دیگه بزن (Ctrl+Shift+R) یا یه پنجره Incognito جدید باز کن.")
