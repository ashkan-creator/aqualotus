#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
متن بنر کوییز رو یه‌کم می‌بره بالاتر (زیر لوگوی کوچیک خودِ عکس).
از داخل ~/aqualotus اجرا کن:
    python3 nudge_banner_text_up.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

PATH = "frontend/src/pages/HomePage.jsx"

OLD = """              <div
                className='position-absolute text-center d-flex flex-column align-items-center'
                style={{
                  bottom: '7%',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  maxWidth: '90%',
                }}
              >"""

NEW = """              <div
                className='position-absolute text-center d-flex flex-column align-items-center'
                style={{
                  bottom: '24%',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  maxWidth: '90%',
                }}
              >"""

if not os.path.exists(PATH):
    print(f"{BAD} فایل پیدا نشد: {PATH}")
    raise SystemExit(1)

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

if NEW.strip() in content:
    print("(رد شد، قبلاً اعمال شده)")
elif OLD.strip() in content:
    shutil.copy2(PATH, f"{PATH}.pre-banner-nudge-backup")
    content = content.replace(OLD, NEW, 1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {PATH}")
else:
    print(f"{BAD} بلاک موقعیت متن پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

print("\nتمام شد. فرانت رو ری‌استارت کن و Ctrl+Shift+R بزن.")
print("اگه بازم دقیق زیر لوگوی عکس ننشست، بگو چند درصد دیگه بالا/پایین بره تا bottom رو فاین-تیون کنم.")
