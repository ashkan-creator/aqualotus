#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
حذف کامل لوگو از بنر کوییز -- فقط متن (عنوان + زیرنویس) می‌مونه.
از داخل ~/aqualotus اجرا کن:
    python3 remove_quiz_banner_logo.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

PATH = "frontend/src/pages/HomePage.jsx"

# دو حالت ممکن (بسته به این‌که enlarge_quiz_banner.py اجرا شده بود یا نه)
LOGO_BLOCK_48 = """                <span className='aq-quiz-banner-logo-wrap'>
                  <img src='/logo.png' alt='AquaLotus' style={{ height: '48px' }} />
                </span>
"""
LOGO_BLOCK_68 = """                <span className='aq-quiz-banner-logo-wrap'>
                  <img src='/logo.png' alt='AquaLotus' style={{ height: '68px' }} />
                </span>
"""

if not os.path.exists(PATH):
    print(f"{BAD} فایل پیدا نشد: {PATH}")
    raise SystemExit(1)

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

removed = False
if LOGO_BLOCK_48 in content:
    shutil.copy2(PATH, f"{PATH}.pre-remove-banner-logo-backup")
    content = content.replace(LOGO_BLOCK_48, "", 1)
    removed = True
elif LOGO_BLOCK_68 in content:
    shutil.copy2(PATH, f"{PATH}.pre-remove-banner-logo-backup")
    content = content.replace(LOGO_BLOCK_68, "", 1)
    removed = True

if removed:
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} لوگو از بنر حذف شد: {PATH}")
elif "aq-quiz-banner-logo-wrap" not in content:
    print("(رد شد، لوگو از قبل حذف شده بود)")
else:
    print(f"{BAD} بلاک لوگو دقیق پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست تا دستی حذفش کنم")

print("\nتمام شد. فرانت رو ری‌استارت کن و Ctrl+Shift+R بزن.")
