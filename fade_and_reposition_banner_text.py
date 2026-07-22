#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
۱) متن بنر کوییز رو می‌بره پایین‌تر (روی گرادیانت تیره‌ی پایین عکس)
۲) بزرگ‌ترش می‌کنه
۳) یه فید/گرادیانت تیره پشت متن اضافه می‌کنه برای خوانایی
از داخل ~/aqualotus اجرا کن:
    python3 fade_and_reposition_banner_text.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

HOMEPAGE = "frontend/src/pages/HomePage.jsx"
FONTS_CSS = "frontend/src/fonts.css"


def backup(path, tag):
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.pre-{tag}-backup")


# --- ۱) HomePage.jsx: گرادیانت + جابه‌جایی متن به پایین ---
if not os.path.exists(HOMEPAGE):
    print(f"{BAD} فایل پیدا نشد: {HOMEPAGE}")
    raise SystemExit(1)

with open(HOMEPAGE, "r", encoding="utf-8") as f:
    content = f.read()

OLD_POS_DIV = """              <div
                className='position-absolute text-center d-flex flex-column align-items-center'
                style={{
                  top: '30%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  maxWidth: '90%',
                }}
              >"""

NEW_POS_DIV = """              <div
                className='position-absolute bottom-0 start-0 w-100'
                style={{
                  height: '70%',
                  background: 'linear-gradient(to top, rgba(0,0,0,0.75), rgba(0,0,0,0) 75%)',
                  pointerEvents: 'none',
                }}
              />
              <div
                className='position-absolute text-center d-flex flex-column align-items-center'
                style={{
                  bottom: '7%',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  maxWidth: '90%',
                }}
              >"""

if NEW_POS_DIV.strip() in content:
    print("(رد شد، قبلاً اعمال شده)")
elif OLD_POS_DIV.strip() in content:
    backup(HOMEPAGE, "banner-fade-reposition")
    content = content.replace(OLD_POS_DIV, NEW_POS_DIV, 1)
    with open(HOMEPAGE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد (موقعیت + فید): {HOMEPAGE}")
else:
    print(f"{BAD} بلاک موقعیت متن پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

# --- ۲) fonts.css: بزرگ‌تر کردن فونت ---
if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
else:
    with open(FONTS_CSS, "r", encoding="utf-8") as f:
        css_content = f.read()
    old_sizes = """.aq-quiz-banner-title {
  font-size: 1.7rem !important;
}

.aq-quiz-banner-text {
  font-size: 1.15rem !important;
}"""
    new_sizes = """.aq-quiz-banner-title {
  font-size: 2.1rem !important;
}

.aq-quiz-banner-text {
  font-size: 1.3rem !important;
}"""
    if new_sizes.strip() in css_content:
        print("(رد شد، سایز فونت قبلاً بزرگ شده بود)")
    elif old_sizes.strip() in css_content:
        backup(FONTS_CSS, "banner-fade-reposition")
        css_content = css_content.replace(old_sizes, new_sizes, 1)
        with open(FONTS_CSS, "w", encoding="utf-8") as f:
            f.write(css_content)
        print(f"{OK} پچ شد (سایز فونت): {FONTS_CSS}")
    else:
        print(f"{BAD} بلاک سایز فونت پیدا نشد -- محتوای فعلی fonts.css رو بفرست")

print("\nتمام شد. فرانت رو ری‌استارت کن و Ctrl+Shift+R بزن.")
