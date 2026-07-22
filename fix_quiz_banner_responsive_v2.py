#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
درست کردن کامل بنر کوییز رو موبایل:
- عکس با aspect-ratio ریسپانسیو واقعی می‌شه (به‌جای minHeight ثابت)
- فونت‌ها رو موبایل بزرگ‌تر می‌شن (کف clamp بالاتر رفت)
- موقعیت متن هم رو موبایل با مدیا-کوئری جدا تنظیم می‌شه (نه فقط دسکتاپ)
از داخل ~/aqualotus اجرا کن:
    python3 fix_quiz_banner_responsive_v2.py
"""

import os
import re
import shutil

OK = "\u2713"
BAD = "\u2717"

HOMEPAGE = "frontend/src/pages/HomePage.jsx"
FONTS_CSS = "frontend/src/fonts.css"


def backup(path, tag):
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.pre-{tag}-backup")


if not os.path.exists(HOMEPAGE):
    print(f"{BAD} فایل پیدا نشد: {HOMEPAGE}")
    raise SystemExit(1)
if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
    raise SystemExit(1)

with open(HOMEPAGE, "r", encoding="utf-8") as f:
    hp = f.read()

# ------------------------------------------------------------------
# ۱) پیدا کردن بلاک فعلی بنر (هرجور که مونده -- خیلی حالت قبلی داشتیم)
# ------------------------------------------------------------------
link_start = hp.find("<Link to='/quiz'")
link_end = hp.find("</Link>", link_start)
if link_start == -1 or link_end == -1:
    print(f"{BAD} بلاک بنر کوییز پیدا نشد تو {HOMEPAGE} -- محتوای فعلی فایل رو بفرست")
    raise SystemExit(1)
link_end += len("</Link>")
old_block = hp[link_start:link_end]

# استخراج آدرس عکس فعلی (هر ورژن ?v=N که باشه)
m = re.search(r"url\('(/images/quiz-banner\.jpg[^']*)'\)", old_block)
img_url = m.group(1) if m else "/images/quiz-banner.jpg?v=5"
if img_url.split("v=")[-1].isdigit():
    new_v = int(img_url.split("v=")[-1]) + 1
    img_url = f"/images/quiz-banner.jpg?v={new_v}"

NEW_BLOCK = f"""          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
            <div
              className='position-relative rounded-4 overflow-hidden aq-quiz-banner-img'
              style={{{{
                backgroundImage: "url('{img_url}')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
              }}}}
            >
              <div className='aq-quiz-banner-fade' />
              <div className='aq-quiz-banner-content text-center d-flex flex-column align-items-center px-3'>
                <h4 className='mb-1 aq-quiz-banner-title' style={{{{ color: '#fff', textShadow: '0 2px 8px rgba(0,0,0,0.65)' }}}}>
                  گیاه مناسب آکواریومت رو پیدا کن!
                </h4>
                <p className='mb-0 aq-quiz-banner-text' style={{{{ color: '#fff', opacity: 0.95, textShadow: '0 2px 8px rgba(0,0,0,0.65)' }}}}>
                  با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
                </p>
              </div>
            </div>
          </Link>"""

if old_block.strip() == NEW_BLOCK.strip():
    print("(رد شد، قبلاً اعمال شده)")
else:
    backup(HOMEPAGE, "banner-responsive-v2")
    hp = hp.replace(old_block, NEW_BLOCK, 1)
    with open(HOMEPAGE, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} بلاک بنر بازنویسی شد: {HOMEPAGE}")

# ------------------------------------------------------------------
# ۲) fonts.css -- حذف کلاس‌های قدیمی بنر و جایگزینی با نسخه‌ی کامل و ریسپانسیو
# ------------------------------------------------------------------
with open(FONTS_CSS, "r", encoding="utf-8") as f:
    css = f.read()

# هر بلاک قدیمی مرتبط با بنر کوییز رو حذف کن (از اولین occurrence به بعد)
marker = "/* --- quiz banner --- */"
idx = css.find(marker)
if idx != -1:
    css = css[:idx].rstrip() + "\n"

banner_css = """
/* --- quiz banner --- */
.aq-quiz-banner-img {
  position: relative;
  aspect-ratio: 21 / 6;
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
  bottom: 18%;
  transform: translateX(-50%);
  max-width: 92%;
}

.aq-quiz-banner-title,
.aq-quiz-banner-title * {
  font-family: 'MJGhalam', 'Vazirmatn', sans-serif !important;
  font-size: clamp(1.4rem, 4.5vw, 2.1rem) !important;
  line-height: 1.35;
}

.aq-quiz-banner-text,
.aq-quiz-banner-text * {
  font-family: 'MJGhalam', 'Vazirmatn', sans-serif !important;
  font-size: clamp(1rem, 3.2vw, 1.3rem) !important;
  line-height: 1.4;
}

@media (max-width: 576px) {
  .aq-quiz-banner-img {
    aspect-ratio: 4 / 5;
    min-height: 320px;
  }

  .aq-quiz-banner-content {
    bottom: 10%;
  }
}
"""

css = css.rstrip() + "\n" + banner_css
backup(FONTS_CSS, "banner-responsive-v2")
with open(FONTS_CSS, "w", encoding="utf-8") as f:
    f.write(css)
print(f"{OK} کلاس‌های بنر تو fonts.css یکجا و ریسپانسیو بازنویسی شد")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن و Ctrl+Shift+R بزن.")
print("رو موبایل الان عکس نسبت 4:5 (بلندتر) می‌گیره تا جا برای متن بزرگ‌تر باز بشه.")
print("اگه بازم چیزی درست نبود، یه اسکرین‌شات از حالت موبایل بفرست.")
