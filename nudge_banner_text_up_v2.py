#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
متن بنر کوییز رو یه‌کم دیگه می‌بره بالاتر.
از داخل ~/aqualotus اجرا کن:
    python3 nudge_banner_text_up_v2.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

PATH = "frontend/src/pages/HomePage.jsx"

CANDIDATES = ["7%", "24%"]
TARGET = "32%"

if not os.path.exists(PATH):
    print(f"{BAD} فایل پیدا نشد: {PATH}")
    raise SystemExit(1)

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

done = False
for c in CANDIDATES:
    old = f"bottom: '{c}',"
    new = f"bottom: '{TARGET}',"
    if old in content:
        shutil.copy2(PATH, f"{PATH}.pre-banner-nudge-v2-backup")
        content = content.replace(old, new, 1)
        with open(PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{OK} پچ شد: bottom از {c} به {TARGET} تغییر کرد")
        done = True
        break

if not done:
    if f"bottom: '{TARGET}'," in content:
        print(f"(رد شد، از قبل رو {TARGET} بود)")
    else:
        print(f"{BAD} مقدار bottom فعلی پیدا نشد -- این خط رو از فایل بفرست: grep -n \"bottom:\" frontend/src/pages/HomePage.jsx")

print("\nتمام شد. فرانت رو ری‌استارت کن و Ctrl+Shift+R بزن.")
