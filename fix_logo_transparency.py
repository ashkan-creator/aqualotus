#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سفیدی پشت لوگو رو با پردازش واقعی عکس (نه ترفند CSS) از بین می‌بره:
پیکسل‌های نزدیک به سفید رو واقعاً شفاف می‌کنه.
از داخل ~/aqualotus اجرا کن:
    python3 fix_logo_transparency.py

اگه Pillow نصب نبود، اول این رو بزن:
    pip install Pillow --break-system-packages
"""

import os
import shutil

try:
    from PIL import Image
except ImportError:
    print("Pillow نصب نیست. اول این رو بزن:")
    print("    pip install Pillow --break-system-packages")
    raise SystemExit(1)

OK = "\u2713"
BAD = "\u2717"

LOGO_PATH = "frontend/public/logo.png"
WHITE_THRESHOLD = 235  # هرچی کمتر باشه، محدوده‌ی بیشتری رو "سفید" حساب می‌کنه

if not os.path.exists(LOGO_PATH):
    print(f"{BAD} فایل پیدا نشد: {LOGO_PATH}")
    raise SystemExit(1)

backup_path = f"{LOGO_PATH}.pre-transparency-fix-backup.png"
if not os.path.exists(backup_path):
    shutil.copy2(LOGO_PATH, backup_path)
    print(f"{OK} بک‌آپ گرفته شد: {backup_path}")

img = Image.open(LOGO_PATH).convert("RGBA")
pixels = img.getdata()

new_pixels = []
changed_count = 0
for r, g, b, a in pixels:
    if r >= WHITE_THRESHOLD and g >= WHITE_THRESHOLD and b >= WHITE_THRESHOLD:
        new_pixels.append((r, g, b, 0))
        changed_count += 1
    else:
        new_pixels.append((r, g, b, a))

img.putdata(new_pixels)
img.save(LOGO_PATH)

print(f"{OK} {changed_count} پیکسل سفید شفاف شد")
print(f"{OK} ذخیره شد: {LOGO_PATH}")
print("\nتمام شد. فرانت رو ری‌استارت کن، Ctrl+Shift+R بزن.")
print("اگه لبه‌ی لوگو یه هاله‌ی سفید محو داشت (نه کاملاً پاک)، بگو WHITE_THRESHOLD رو کمتر کنم (مثلاً 200).")
print("اگه بخشی از خودِ طرح لوگو (نه پس‌زمینه) هم سفید بود و شفاف شد، بگو threshold رو بالاتر ببرم (مثلاً 250).")
