#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
درست کردن بنر کوییز تو حالت موبایل/ریسپانسیو:
- فونت‌ها با clamp() ریسپانسیو می‌شن (رو موبایل خودکار کوچیک‌تر)
- یه پدینگ افقی امن به متن اضافه می‌شه تا به لبه نچسبه
- ارتفاع بنر رو موبایل بیشتر می‌شه تا متن جا بشه
از داخل ~/aqualotus اجرا کن:
    python3 fix_quiz_banner_mobile.py
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


# --- ۱) fonts.css: کلمپ فونت + مدیا کوئری ---
if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
    raise SystemExit(1)

with open(FONTS_CSS, "r", encoding="utf-8") as f:
    css_content = f.read()

old_sizes = """.aq-quiz-banner-title {
  font-size: 2.1rem !important;
}

.aq-quiz-banner-text {
  font-size: 1.3rem !important;
}"""

new_sizes = """.aq-quiz-banner-title {
  font-size: clamp(1.15rem, 4.5vw, 2.1rem) !important;
  line-height: 1.35;
}

.aq-quiz-banner-text {
  font-size: clamp(0.85rem, 3vw, 1.3rem) !important;
  line-height: 1.4;
}

.aq-quiz-banner-img {
  min-height: 220px;
}

@media (max-width: 576px) {
  .aq-quiz-banner-img {
    min-height: 260px;
  }
}"""

if new_sizes.strip() in css_content:
    print(f"(رد شد، قبلاً اعمال شده) {FONTS_CSS}")
elif old_sizes.strip() in css_content:
    backup(FONTS_CSS, "banner-mobile-fix")
    css_content = css_content.replace(old_sizes, new_sizes, 1)
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"{OK} پچ شد: {FONTS_CSS}")
else:
    print(f"{BAD} بلاک سایز فونت پیدا نشد -- محتوای فعلی fonts.css رو بفرست تا دستی چک کنم")

# --- ۲) HomePage.jsx: className عکس + پدینگ افقی متن ---
if not os.path.exists(HOMEPAGE):
    print(f"{BAD} فایل پیدا نشد: {HOMEPAGE}")
    raise SystemExit(1)

with open(HOMEPAGE, "r", encoding="utf-8") as f:
    content = f.read()

changed = False

# className رو به div پس‌زمینه‌ی عکس اضافه کن (برای مدیا کوئری minHeight)
old_img_div = "className='position-relative rounded-4 overflow-hidden'"
new_img_div = "className='position-relative rounded-4 overflow-hidden aq-quiz-banner-img'"
if new_img_div in content:
    pass
elif old_img_div in content:
    content = content.replace(old_img_div, new_img_div, 1)
    changed = True
    print(f"{OK} کلاس aq-quiz-banner-img اضافه شد")
else:
    print(f"{BAD} div پس‌زمینه‌ی عکس پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

# minHeight رو از استایل inline حذف کن چون الان از CSS میاد (تا مدیا کوئری بتونه اثر بذاره)
old_style = """              style={{
                backgroundImage: "url('/images/quiz-banner.jpg?v=4')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                minHeight: '220px',
              }}"""
new_style = """              style={{
                backgroundImage: "url('/images/quiz-banner.jpg?v=4')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
              }}"""
if new_style.strip() in content:
    pass
elif old_style.strip() in content:
    content = content.replace(old_style, new_style, 1)
    changed = True
    print(f"{OK} minHeight inline حذف شد (الان از CSS کنترل می‌شه)")
else:
    print(f"{BAD} استایل inline پس‌زمینه دقیق پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

# پدینگ افقی امن به کانتینر متن
old_text_wrap = "className='position-absolute text-center d-flex flex-column align-items-center'"
new_text_wrap = "className='position-absolute text-center d-flex flex-column align-items-center px-3'"
if new_text_wrap in content:
    pass
elif old_text_wrap in content:
    content = content.replace(old_text_wrap, new_text_wrap, 1)
    changed = True
    print(f"{OK} پدینگ افقی به متن اضافه شد")
else:
    print(f"{BAD} کانتینر متن پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست")

# maxWidth رو کمی محدودتر و امن‌تر کن برای موبایل
old_max = "maxWidth: '90%',"
new_max = "maxWidth: '92%',"
if old_max in content and new_max not in content:
    content = content.replace(old_max, new_max, 1)
    changed = True

if changed:
    backup(HOMEPAGE, "banner-mobile-fix")
    with open(HOMEPAGE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {HOMEPAGE}")

print("\nتمام شد. فرانت رو ری‌استارت کن و رو موبایل/DevTools ریسپانسیو تست کن (Ctrl+Shift+R).")
