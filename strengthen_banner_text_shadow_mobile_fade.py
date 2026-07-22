#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
۱) سایه‌ی متن رو قوی‌تر می‌کنه (همه‌ی خط‌ها: عنوان، زیرنویس، کلیک کنید)
۲) رو موبایل، چون متن رفته بالای عکس ولی فید فعلی فقط پایین رو تیره می‌کنه،
   یه گرادیانت تیره‌ی جدا برای بالای عکس (فقط موبایل) اضافه می‌کنه
از داخل ~/aqualotus اجرا کن:
    python3 strengthen_banner_text_shadow_mobile_fade.py
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


# --- ۱) HomePage.jsx: سایه‌ی قوی‌تر رو همه‌ی خط‌ها ---
if not os.path.exists(HOMEPAGE):
    print(f"{BAD} فایل پیدا نشد: {HOMEPAGE}")
    raise SystemExit(1)

with open(HOMEPAGE, "r", encoding="utf-8") as f:
    hp = f.read()

old_shadow = "0 2px 8px rgba(0,0,0,0.65)"
new_shadow = "0 1px 3px rgba(0,0,0,0.95), 0 2px 10px rgba(0,0,0,0.85)"

count = hp.count(old_shadow)
if count == 0:
    if new_shadow in hp:
        print("(رد شد، سایه‌ها قبلاً قوی‌تر شده بودن)")
    else:
        print(f"{BAD} سایه‌ی فعلی پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")
else:
    backup(HOMEPAGE, "banner-shadow-strong")
    hp = hp.replace(old_shadow, new_shadow)
    with open(HOMEPAGE, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} سایه‌ی متن قوی‌تر شد ({count} مورد)")

# --- ۲) fonts.css: گرادیانت تیره‌ی بالا فقط رو موبایل ---
if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
    raise SystemExit(1)

with open(FONTS_CSS, "r", encoding="utf-8") as f:
    css = f.read()

top_fade_marker = "/* --- quiz banner mobile top fade --- */"
if top_fade_marker in css:
    print("(رد شد، گرادیانت بالا قبلاً اضافه شده بود)")
else:
    top_fade_css = f"""
{top_fade_marker}
@media (max-width: 576px) {{
  .aq-quiz-banner-fade {{
    background: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 0.7) 0%,
      rgba(0, 0, 0, 0.35) 35%,
      rgba(0, 0, 0, 0) 60%
    );
  }}
}}
"""
    backup(FONTS_CSS, "banner-shadow-strong")
    css = css.rstrip() + "\n" + top_fade_css
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"{OK} گرادیانت تیره‌ی بالای عکس (فقط موبایل) اضافه شد: {FONTS_CSS}")

print("\nتمام شد. فرانت رو ری‌استارت کن، Ctrl+Shift+R بزن، هم دسکتاپ هم موبایل رو چک کن.")
