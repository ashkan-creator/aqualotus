#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
۱) رجیستر فونت MJ Ghalam (دو فایل TTF) با @font-face و ایمپورت گلوبال
۲) اعمال فونت روی متن بنر کوییز (به‌جای Khodkar اشتباهی قبلی)
۳) کش-باست کردن آدرس عکس بنر تا مرورگر مجبور بشه نسخه جدید رو بگیره
از داخل ~/aqualotus اجرا کن (بعد از اینکه فونت‌ها رو تو frontend/public/fonts/ کپی کردی):
    python3 setup_mjghalam_font.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

FONT1 = "frontend/public/fonts/Mj_Ghalam-1.TTF"
FONT2 = "frontend/public/fonts/Mj_Ghalam-2.TTF"
FONTS_CSS = "frontend/src/fonts.css"
MAIN_JSX = "frontend/src/main.jsx"
HOMEPAGE = "frontend/src/pages/HomePage.jsx"


def backup(path, tag):
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.pre-{tag}-backup")


# --- چک فایل‌های فونت ---
for f in (FONT1, FONT2):
    if os.path.exists(f):
        print(f"{OK} فونت پیدا شد: {f}")
    else:
        print(f"{BAD} فونت پیدا نشد: {f} -- اول کپیش کن")

# --- ۱) fonts.css ---
fonts_css_content = """@font-face {
  font-family: 'MJGhalam';
  src: url('/fonts/Mj_Ghalam-1.TTF') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'MJGhalam';
  src: url('/fonts/Mj_Ghalam-2.TTF') format('truetype');
  font-weight: bold;
  font-style: normal;
}
"""
if os.path.exists(FONTS_CSS):
    with open(FONTS_CSS, "r", encoding="utf-8") as f:
        existing = f.read()
    if existing.strip() == fonts_css_content.strip():
        print(f"(رد شد، قبلاً اعمال شده) {FONTS_CSS}")
    else:
        backup(FONTS_CSS, "mjghalam-fontscss")
        with open(FONTS_CSS, "w", encoding="utf-8") as f:
            f.write(fonts_css_content)
        print(f"{OK} بازنویسی شد: {FONTS_CSS}")
else:
    os.makedirs(os.path.dirname(FONTS_CSS), exist_ok=True)
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(fonts_css_content)
    print(f"{OK} ساخته شد: {FONTS_CSS}")

# --- ۲) main.jsx -- ایمپورت fonts.css ---
if not os.path.exists(MAIN_JSX):
    print(f"{BAD} فایل پیدا نشد: {MAIN_JSX}")
else:
    with open(MAIN_JSX, "r", encoding="utf-8") as f:
        content = f.read()
    insertion = "\nimport './fonts.css'"
    anchor = "import './animations.css'"
    if insertion.strip() in content:
        print(f"(رد شد، قبلاً اعمال شده) {MAIN_JSX}")
    elif anchor not in content:
        print(f"{BAD} anchor پیدا نشد تو {MAIN_JSX} -- دستی چک کن")
    else:
        backup(MAIN_JSX, "mjghalam-mainjsx")
        content = content.replace(anchor, anchor + insertion, 1)
        with open(MAIN_JSX, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{OK} پچ شد: {MAIN_JSX}")

# --- ۳) HomePage.jsx -- فونت درست + کش‌باست عکس ---
if not os.path.exists(HOMEPAGE):
    print(f"{BAD} فایل پیدا نشد: {HOMEPAGE}")
else:
    with open(HOMEPAGE, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False

    # فونت اشتباهی قبلی رو با فونت درست عوض کن (اگه هست)
    wrong_font = "fontFamily: \"'Khodkar', 'Vazirmatn', sans-serif\""
    right_font = "fontFamily: \"'MJGhalam', 'Vazirmatn', sans-serif\""
    if wrong_font in content:
        content = content.replace(wrong_font, right_font)
        changed = True
        print(f"{OK} فونت از Khodkar به MJGhalam عوض شد (هر دو مورد)")
    elif right_font in content:
        print("(فونت قبلاً MJGhalam بود)")
    else:
        print(f"{BAD} رشته‌ی fontFamily پیدا نشد -- شاید نسخه‌ی فایل فرق داره، دستی چک کن")

    # کش‌باست عکس بنر
    old_img = "url('/images/quiz-banner.jpg')"
    new_img = "url('/images/quiz-banner.jpg?v=2')"
    if old_img in content:
        content = content.replace(old_img, new_img)
        changed = True
        print(f"{OK} آدرس عکس کش‌باست شد (?v=2)")
    elif new_img in content:
        print("(عکس قبلاً کش‌باست شده بود)")
    else:
        print(f"{BAD} آدرس عکس بنر پیدا نشد -- دستی چک کن")

    if changed:
        backup(HOMEPAGE, "mjghalam-homepage")
        with open(HOMEPAGE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{OK} پچ شد: {HOMEPAGE}")

print("\nتمام شد. سرور فرانت رو یه بار کامل ری‌استارت کن (نه فقط رفرش) چون فایل CSS جدید اضافه شد،")
print("بعد Ctrl+Shift+R بزن رو صفحه اصلی تا کش عکس/فونت مرورگر هم پاک بشه.")
