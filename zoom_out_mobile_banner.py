#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
زوم اوت کردن عکس موبایل بنر (از ۳۰۰٪ به ۱۵۰٪).
از داخل ~/aqualotus اجرا کن:
    python3 zoom_out_mobile_banner.py
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

old = "background-size: 300% !important;"
new = "background-size: 150% !important;"

if new in content:
    print("(رد شد، قبلاً رو ۱۵۰٪ بود)")
elif old in content:
    shutil.copy2(FONTS_CSS, f"{FONTS_CSS}.pre-mobile-zoomout-backup")
    content = content.replace(old, new, 1)
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {FONTS_CSS} (۳۰۰٪ -> ۱۵۰٪)")
else:
    print(f"{BAD} مقدار background-size فعلی پیدا نشد -- این خط رو بفرست: grep -n \"background-size: .*%\" frontend/src/fonts.css")

print("\nتمام شد. فرانت رو ری‌استارت کن، Ctrl+Shift+R بزن.")
print("اگه بازم زیادی زوم بود یا کم بود، بگو چند درصد دقیق بشه (مثلاً ۱۲۰٪ یا ۱۰۰٪ که یعنی cover واقعی).")
