#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اضافه کردن خط "کلیک کنید" زیر متن بنر کوییز (دسکتاپ و موبایل).
از داخل ~/aqualotus اجرا کن:
    python3 add_quiz_banner_cta_line.py
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


# --- ۱) HomePage.jsx: اضافه کردن پاراگراف "کلیک کنید" ---
if not os.path.exists(HOMEPAGE):
    print(f"{BAD} فایل پیدا نشد: {HOMEPAGE}")
    raise SystemExit(1)

with open(HOMEPAGE, "r", encoding="utf-8") as f:
    hp = f.read()

OLD_SUBTITLE = """                <p className='mb-0 aq-quiz-banner-text' style={{ color: '#fff', opacity: 0.95, textShadow: '0 2px 8px rgba(0,0,0,0.65)' }}>
                  با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
                </p>
              </div>"""

NEW_SUBTITLE = """                <p className='mb-0 aq-quiz-banner-text' style={{ color: '#fff', opacity: 0.95, textShadow: '0 2px 8px rgba(0,0,0,0.65)' }}>
                  با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
                </p>
                <p className='mb-0 mt-1 aq-quiz-banner-cta' style={{ color: '#fff', textShadow: '0 2px 8px rgba(0,0,0,0.65)' }}>
                  کلیک کنید
                </p>
              </div>"""

if NEW_SUBTITLE.strip() in hp:
    print("(رد شد، خط کلیک کنید قبلاً اضافه شده بود)")
elif OLD_SUBTITLE.strip() in hp:
    backup(HOMEPAGE, "banner-cta-line")
    hp = hp.replace(OLD_SUBTITLE, NEW_SUBTITLE, 1)
    with open(HOMEPAGE, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} خط «کلیک کنید» اضافه شد: {HOMEPAGE}")
else:
    print(f"{BAD} بلاک زیرنویس بنر پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

# --- ۲) fonts.css: کلاس aq-quiz-banner-cta ---
if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
    raise SystemExit(1)

with open(FONTS_CSS, "r", encoding="utf-8") as f:
    css = f.read()

if ".aq-quiz-banner-cta" in css:
    print("(رد شد، کلاس کلیک‌کنید قبلاً تو fonts.css بود)")
else:
    cta_css = """
.aq-quiz-banner-cta,
.aq-quiz-banner-cta * {
  font-family: 'MJGhalam', 'Vazirmatn', sans-serif !important;
  font-size: 0.9rem !important;
  opacity: 0.85;
}

@media (max-width: 576px) {
  .aq-quiz-banner-cta,
  .aq-quiz-banner-cta * {
    font-size: 0.95rem !important;
    white-space: nowrap;
  }
}
"""
    backup(FONTS_CSS, "banner-cta-line")
    css = css.rstrip() + "\n" + cta_css
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"{OK} کلاس aq-quiz-banner-cta اضافه شد: {FONTS_CSS}")

print("\nتمام شد. فرانت رو ری‌استارت کن، Ctrl+Shift+R بزن.")
