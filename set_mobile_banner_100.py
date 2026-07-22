#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
عکس موبایل بنر رو رو ۱۰۰٪ می‌ذاره.
از داخل ~/aqualotus اجرا کن:
    python3 set_mobile_banner_100.py
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

new = "background-size: 100% !important;"
candidates = [
    "background-size: 300% !important;",
    "background-size: 150% !important;",
    "background-size: contain !important;",
]

if new in content:
    print("(رد شد، قبلاً رو ۱۰۰٪ بود)")
else:
    replaced = False
    for old in candidates:
        if old in content:
            shutil.copy2(FONTS_CSS, f"{FONTS_CSS}.pre-mobile-100-backup")
            content = content.replace(old, new, 1)
            with open(FONTS_CSS, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"{OK} پچ شد: {FONTS_CSS} ({old} -> {new})")
            replaced = True
            break
    if not replaced:
        print(f"{BAD} مقدار فعلی background-size پیدا نشد -- این خط رو بفرست: grep -n \"background-size: .*%\\|background-size: contain\" frontend/src/fonts.css")

print("\nتمام شد. فرانت رو ری‌استارت کن، Ctrl+Shift+R بزن.")
