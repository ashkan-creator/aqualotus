#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
یه پدینگ ریز بین اسلایدر و بنر کوییز اضافه می‌کنه، و گوشه‌های گرد بنر رو برمی‌داره.
از داخل ~/aqualotus اجرا کن:
    python3 fix_quiz_banner_spacing_corners.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

PATH = "frontend/src/pages/HomePage.jsx"

if not os.path.exists(PATH):
    print(f"{BAD} فایل پیدا نشد: {PATH}")
    raise SystemExit(1)

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

changed = False

# ۱) حذف گوشه‌های گرد
old_rounded = "className='position-relative rounded-4 overflow-hidden aq-quiz-banner-img'"
new_rounded = "className='position-relative overflow-hidden aq-quiz-banner-img'"
if new_rounded in content:
    print("(رد شد، گوشه‌ها قبلاً گرد نبودن)")
elif old_rounded in content:
    content = content.replace(old_rounded, new_rounded, 1)
    changed = True
    print(f"{OK} گوشه‌های گرد برداشته شد")
else:
    print(f"{BAD} کلاس div عکس پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

# ۲) پدینگ/فاصله بالای بنر
old_link = "className='d-block text-decoration-none mb-3'"
new_link = "className='d-block text-decoration-none mt-2 mb-3'"
if new_link in content:
    print("(رد شد، فاصله‌ی بالا قبلاً اضافه شده بود)")
elif old_link in content:
    content = content.replace(old_link, new_link, 1)
    changed = True
    print(f"{OK} فاصله‌ی بالای بنر اضافه شد")
else:
    print(f"{BAD} کلاس Link بنر پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

if changed:
    shutil.copy2(PATH, f"{PATH}.pre-banner-spacing-corners-backup")
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {PATH}")

print("\nتمام شد. فرانت رو ری‌استارت کن، Ctrl+Shift+R بزن.")
