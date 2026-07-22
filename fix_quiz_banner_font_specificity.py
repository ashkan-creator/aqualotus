#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
۱) فونت: به‌جای style inline، یه کلاس CSS با !important می‌سازیم که رو
   قانون سراسری `* { font-family: 'Vazirmatn' !important }` برنده بشه.
۲) لوگو: به‌جای mix-blend-mode (که رو قسمت روشن عکس جواب نمی‌داد)، یه دایره‌ی
   تیره‌ی کوچیک فقط پشت خود آیکون لوگو می‌ذاریم.
از داخل ~/aqualotus اجرا کن:
    python3 fix_quiz_banner_font_specificity.py
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


# --- ۱) اضافه کردن کلاس‌های CSS به fonts.css ---
extra_css = """
.aq-quiz-banner-title,
.aq-quiz-banner-title * {
  font-family: 'MJGhalam', 'Vazirmatn', sans-serif !important;
}

.aq-quiz-banner-text,
.aq-quiz-banner-text * {
  font-family: 'MJGhalam', 'Vazirmatn', sans-serif !important;
}

.aq-quiz-banner-logo-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.35);
  margin-bottom: 6px;
}
"""

if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
else:
    with open(FONTS_CSS, "r", encoding="utf-8") as f:
        content = f.read()
    if ".aq-quiz-banner-title" in content:
        print(f"(رد شد، قبلاً اعمال شده) {FONTS_CSS}")
    else:
        backup(FONTS_CSS, "banner-specificity")
        content += extra_css
        with open(FONTS_CSS, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{OK} کلاس‌های جدید اضافه شد: {FONTS_CSS}")

# --- ۲) HomePage.jsx -- جایگزینی بلاک بنر ---
OLD_BLOCK = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
            <div
              className='position-relative rounded-4 overflow-hidden'
              style={{
                backgroundImage: "url('/images/quiz-banner.jpg?v=2')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                minHeight: '220px',
              }}
            >
              <div
                className='position-absolute text-center'
                style={{
                  top: '30%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  maxWidth: '90%',
                }}
              >
                <img
                  src='/logo.png'
                  alt='AquaLotus'
                  style={{
                    height: '60px',
                    marginBottom: '6px',
                    background: 'transparent',
                    mixBlendMode: 'multiply',
                  }}
                />
                <h4
                  className='mb-1'
                  style={{
                    color: '#fff',
                    textShadow: '0 2px 8px rgba(0,0,0,0.65)',
                    fontFamily: "'MJGhalam', 'Vazirmatn', sans-serif",
                  }}
                >
                  گیاه مناسب آکواریومت رو پیدا کن!
                </h4>
                <p
                  className='mb-0'
                  style={{
                    color: '#fff',
                    opacity: 0.95,
                    textShadow: '0 2px 8px rgba(0,0,0,0.65)',
                    fontFamily: "'MJGhalam', 'Vazirmatn', sans-serif",
                  }}
                >
                  با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
                </p>
              </div>
            </div>
          </Link>"""

NEW_BLOCK = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
            <div
              className='position-relative rounded-4 overflow-hidden'
              style={{
                backgroundImage: "url('/images/quiz-banner.jpg?v=3')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                minHeight: '220px',
              }}
            >
              <div
                className='position-absolute text-center d-flex flex-column align-items-center'
                style={{
                  top: '30%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  maxWidth: '90%',
                }}
              >
                <span className='aq-quiz-banner-logo-wrap'>
                  <img src='/logo.png' alt='AquaLotus' style={{ height: '48px' }} />
                </span>
                <h4
                  className='mb-1 aq-quiz-banner-title'
                  style={{ color: '#fff', textShadow: '0 2px 8px rgba(0,0,0,0.65)' }}
                >
                  گیاه مناسب آکواریومت رو پیدا کن!
                </h4>
                <p
                  className='mb-0 aq-quiz-banner-text'
                  style={{ color: '#fff', opacity: 0.95, textShadow: '0 2px 8px rgba(0,0,0,0.65)' }}
                >
                  با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
                </p>
              </div>
            </div>
          </Link>"""

if not os.path.exists(HOMEPAGE):
    print(f"{BAD} فایل پیدا نشد: {HOMEPAGE}")
else:
    with open(HOMEPAGE, "r", encoding="utf-8") as f:
        content = f.read()
    if NEW_BLOCK.strip() in content:
        print(f"(رد شد، قبلاً اعمال شده) {HOMEPAGE}")
    elif OLD_BLOCK.strip() in content:
        backup(HOMEPAGE, "banner-specificity")
        content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)
        with open(HOMEPAGE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{OK} پچ شد: {HOMEPAGE}")
    else:
        print(f"{BAD} بلاک قبلی دقیق پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست تا دستی چک کنم")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن و رو صفحه Ctrl+Shift+R بزن.")
print("فونت این بار باید حتماً عوض بشه چون دیگه رو !important سراسری سوار می‌شه، نه inline style.")
