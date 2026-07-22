#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
۱) عکس: aspect-ratio که فاجعه شده بود رو برمی‌گردونیم به minHeight ساده
۲) دسکتاپ: متن رو یه‌کم می‌بریم بالاتر (bottom: 18% -> 30%)
۳) موبایل: عنوان رو تو یه خط نگه می‌داریم (white-space: nowrap) بدون تغییر سایز فونت،
   و جا رو براش بازتر می‌کنیم (max-width بیشتر، پدینگ کمتر)
از داخل ~/aqualotus اجرا کن:
    python3 fix_quiz_banner_responsive_v3.py
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
    min-height: 240px;
  }

  .aq-quiz-banner-content {
    bottom: 14%;
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
    backup(FONTS_CSS, "banner-responsive-v3")
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(new_css)
    print(f"{OK} پچ شد: {FONTS_CSS}")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن و Ctrl+Shift+R بزن (هم دسکتاپ هم موبایل رو چک کن).")
print("نکته: اگه رو گوشی‌های خیلی کوچیک (زیر ۳۶۰px) عنوان بازم کمی از لبه بزنه بیرون، بگو تا")
print("یه راه‌حل دیگه (نه کوچیک کردن فونت) پیدا کنیم -- مثلاً letter-spacing منفی یا کم کردن پدینگ بیشتر.")
