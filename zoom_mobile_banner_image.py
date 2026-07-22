#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
زوم کردن عکس موبایل بنر کوییز (تا ۳ برابر) -- چون کیفیت عکس بالاست، افت کیفیت نداره.
از داخل ~/aqualotus اجرا کن:
    python3 zoom_mobile_banner_image.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

FONTS_CSS = "frontend/src/fonts.css"


def backup(path, tag):
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.pre-{tag}-backup")


if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
    raise SystemExit(1)

with open(FONTS_CSS, "r", encoding="utf-8") as f:
    css = f.read()

marker = "/* --- quiz banner --- */"
idx = css.find(marker)
if idx == -1:
    print(f"{BAD} مارکر '{marker}' تو fonts.css پیدا نشد -- محتوای فعلی فایل رو بفرست")
    raise SystemExit(1)

base_css = css[:idx].rstrip() + "\n"

banner_css = """
/* --- quiz banner --- */
.aq-quiz-banner-img {
  position: relative;
  min-height: 220px;
}

.aq-quiz-banner-fade {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.75), rgba(0,0,0,0) 70%);
  pointer-events: none;
}

.aq-quiz-banner-content {
  position: absolute;
  left: 50%;
  bottom: 30%;
  transform: translateX(-50%);
  max-width: 92%;
}

.aq-quiz-banner-title,
.aq-quiz-banner-title * {
  font-family: 'MJGhalam', 'Vazirmatn', sans-serif !important;
  font-size: clamp(1.4rem, 4.5vw, 2.1rem) !important;
  line-height: 1.35;
  white-space: nowrap;
}

.aq-quiz-banner-text,
.aq-quiz-banner-text * {
  font-family: 'MJGhalam', 'Vazirmatn', sans-serif !important;
  font-size: clamp(1rem, 3.2vw, 1.3rem) !important;
  line-height: 1.4;
}

@media (max-width: 576px) {
  .aq-quiz-banner-img {
    min-height: 420px;
    background-image: url('/images/quiz-banner-mobile.jpg') !important;
    background-size: 300% !important;
    background-position: center !important;
  }

  .aq-quiz-banner-content {
    bottom: 17%;
    max-width: 98%;
    padding-left: 4px;
    padding-right: 4px;
  }
}
"""

new_css = base_css + banner_css

if new_css.strip() == css.strip():
    print("(رد شد، قبلاً اعمال شده)")
else:
    backup(FONTS_CSS, "banner-mobile-zoom3x")
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(new_css)
    print(f"{OK} پچ شد: {FONTS_CSS}")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن و Ctrl+Shift+R بزن، موبایل رو چک کن.")
print("اگه ۳ برابر زیادی زوم بود یا زیادی کم بود، بگو عدد دقیق (مثلاً ۲۰۰٪ یا ۲۵۰٪) رو بدم.")
