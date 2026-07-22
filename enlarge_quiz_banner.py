#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بزرگ‌تر کردن لوگو و متن بنر کوییز.
از داخل ~/aqualotus اجرا کن:
    python3 enlarge_quiz_banner.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

FONTS_CSS = "frontend/src/fonts.css"
HOMEPAGE = "frontend/src/pages/HomePage.jsx"


def backup(path, tag):
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.pre-{tag}-backup")


# --- ۱) fonts.css: بزرگ‌تر کردن دایره‌ی پشت لوگو ---
if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
else:
    with open(FONTS_CSS, "r", encoding="utf-8") as f:
        content = f.read()
    old = """.aq-quiz-banner-logo-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.35);
  margin-bottom: 6px;
}"""
    new = """.aq-quiz-banner-logo-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.35);
  margin-bottom: 8px;
}

.aq-quiz-banner-title {
  font-size: 1.7rem !important;
}

.aq-quiz-banner-text {
  font-size: 1.15rem !important;
}"""
    if new.strip() in content:
        print(f"(رد شد، قبلاً اعمال شده) {FONTS_CSS}")
    elif old.strip() in content:
        backup(FONTS_CSS, "banner-enlarge")
        content = content.replace(old, new, 1)
        with open(FONTS_CSS, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{OK} پچ شد: {FONTS_CSS}")
    else:
        print(f"{BAD} بلاک قدیمی پیدا نشد تو {FONTS_CSS} -- محتوای فعلیش رو بفرست")

# --- ۲) HomePage.jsx: بزرگ‌تر کردن خود لوگو (img) ---
if not os.path.exists(HOMEPAGE):
    print(f"{BAD} فایل پیدا نشد: {HOMEPAGE}")
else:
    with open(HOMEPAGE, "r", encoding="utf-8") as f:
        content = f.read()
    old_img = "<img src='/logo.png' alt='AquaLotus' style={{ height: '48px' }} />"
    new_img = "<img src='/logo.png' alt='AquaLotus' style={{ height: '68px' }} />"
    old_url = "url('/images/quiz-banner.jpg?v=3')"
    new_url = "url('/images/quiz-banner.jpg?v=4')"
    changed = False
    if old_img in content:
        content = content.replace(old_img, new_img, 1)
        changed = True
        print(f"{OK} سایز عکس لوگو بزرگ‌تر شد")
    elif new_img in content:
        print("(سایز لوگو قبلاً بزرگ شده بود)")
    else:
        print(f"{BAD} تگ img لوگو پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

    if old_url in content:
        content = content.replace(old_url, new_url, 1)
        changed = True
    elif new_url in content:
        pass
    else:
        print(f"{BAD} آدرس عکس بنر پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

    if changed:
        backup(HOMEPAGE, "banner-enlarge")
        with open(HOMEPAGE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{OK} پچ شد: {HOMEPAGE}")

print("\nتمام شد. فرانت رو ری‌استارت کن و Ctrl+Shift+R بزن.")
