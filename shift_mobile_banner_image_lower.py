#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
عکس موبایل رو یه‌کم از پایین‌ترش نشون می‌ده (background-position بره رو bottom).
از داخل ~/aqualotus اجرا کن:
    python3 shift_mobile_banner_image_lower.py
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

old = "background-position: center !important;"
new = "background-position: center bottom !important;"

if new in content and old not in content:
    print("(رد شد، قبلاً از پایین نشون داده می‌شد)")
elif old in content:
    shutil.copy2(FONTS_CSS, f"{FONTS_CSS}.pre-shift-lower-backup")
    content = content.replace(old, new, 1)
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {FONTS_CSS} (center -> center bottom)")
else:
    print(f"{BAD} مقدار background-position پیدا نشد -- این خط رو بفرست: grep -n \"background-position\" frontend/src/fonts.css")

print("\nتمام شد. فرانت رو ری‌استارت کن، Ctrl+Shift+R بزن.")
print("اگه هنوز کافی نبود، بگو بیشتر بره پایین -- می‌تونم به‌جای bottom یه درصد دقیق (مثلاً center 75%) بذارم.")
