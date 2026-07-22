#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ارتفاع بنر کوییز رو موبایل رو با ارتفاع هیرو اسلایدر (300px) یکی می‌کنه.
دسکتاپ دست‌نخورده می‌مونه.
از داخل ~/aqualotus اجرا کن:
    python3 match_mobile_banner_to_hero_height.py
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

old = "min-height: 420px;"
new = "min-height: 300px;"

if new in content and old not in content:
    print("(رد شد، قبلاً رو ۳۰۰px بود)")
elif old in content:
    shutil.copy2(FONTS_CSS, f"{FONTS_CSS}.pre-hero-height-match-backup")
    content = content.replace(old, new, 1)
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {FONTS_CSS} (۴۲۰px -> ۳۰۰px، هم‌اندازه‌ی hero-slider موبایل)")
else:
    print(f"{BAD} مقدار min-height موبایل پیدا نشد -- این خط رو بفرست: grep -n \"min-height\" frontend/src/fonts.css")

print("\nتمام شد. فرانت رو ری‌استارت کن، Ctrl+Shift+R بزن.")
print("چون قد کمتر شد، اگه متن/عکس جا نشدن یا فشرده به‌نظر رسیدن بگو تا تنظیمشون کنم.")
