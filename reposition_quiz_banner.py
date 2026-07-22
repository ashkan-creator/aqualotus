#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
حذف کادر پشت متن بنر کوییز و بردن لوگو+متن بالاتر، طوری که لوگوی خودمون
دقیقاً روی لوگوی کوچیک برگ توی خودِ عکس بیفته.
از داخل ~/aqualotus اجرا کن:
    python3 reposition_quiz_banner.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

PATH = "frontend/src/pages/HomePage.jsx"

# نسخه‌ای که با کادر نیمه‌شفاف بود (improve_quiz_banner_readability.py)
OLD_BLOCK_CARD = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
            <div
              className='position-relative rounded-4 overflow-hidden'
              style={{
                backgroundImage: "url('/images/quiz-banner.jpg')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                minHeight: '220px',
              }}
            >
              <div
                className='position-absolute top-50 start-50 translate-middle text-center rounded-4 p-4'
                style={{
                  background: 'rgba(0,0,0,0.45)',
                  backdropFilter: 'blur(4px)',
                  WebkitBackdropFilter: 'blur(4px)',
                  maxWidth: '90%',
                }}
              >
                <img
                  src='/logo.png'
                  alt='AquaLotus'
                  style={{ height: '48px', marginBottom: '10px' }}
                />
                <h4 className='mb-1' style={{ color: '#fff' }}>
                  گیاه مناسب آکواریومت رو پیدا کن!
                </h4>
                <p className='mb-0' style={{ color: '#fff', opacity: 0.9 }}>
                  با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
                </p>
              </div>
            </div>
          </Link>"""

# نسخه‌ی ساده‌ی قبل‌تر (finalize_quiz_banner.py) -- برای احتیاط
OLD_BLOCK_PLAIN = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
            <div
              className='d-flex flex-column align-items-center justify-content-center text-center rounded-4 p-4'
              style={{
                backgroundImage: "url('/images/quiz-banner.jpg')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                minHeight: '220px',
                color: '#fff',
              }}
            >
              <h4 className='mb-1' style={{ color: '#fff' }}>
                گیاه مناسب آکواریومت رو پیدا کن!
              </h4>
              <p className='mb-0' style={{ color: '#fff', opacity: 0.9 }}>
                با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
              </p>
            </div>
          </Link>"""

NEW_BLOCK = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
            <div
              className='position-relative rounded-4 overflow-hidden'
              style={{
                backgroundImage: "url('/images/quiz-banner.jpg')",
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
                  style={{ height: '60px', marginBottom: '6px' }}
                />
                <h4 className='mb-1' style={{ color: '#fff', textShadow: '0 2px 8px rgba(0,0,0,0.65)' }}>
                  گیاه مناسب آکواریومت رو پیدا کن!
                </h4>
                <p
                  className='mb-0'
                  style={{ color: '#fff', opacity: 0.95, textShadow: '0 2px 8px rgba(0,0,0,0.65)' }}
                >
                  با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
                </p>
              </div>
            </div>
          </Link>"""

if not os.path.exists(PATH):
    print(f"{BAD} فایل پیدا نشد: {PATH}")
    raise SystemExit(1)

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

if NEW_BLOCK.strip() in content:
    print(f"(رد شد، قبلاً اعمال شده) {PATH}")
elif OLD_BLOCK_CARD.strip() in content:
    shutil.copy2(PATH, f"{PATH}.pre-quiz-banner-reposition-backup")
    content = content.replace(OLD_BLOCK_CARD, NEW_BLOCK, 1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد (از نسخه‌ی کادردار): {PATH}")
elif OLD_BLOCK_PLAIN.strip() in content:
    shutil.copy2(PATH, f"{PATH}.pre-quiz-banner-reposition-backup")
    content = content.replace(OLD_BLOCK_PLAIN, NEW_BLOCK, 1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد (از نسخه‌ی ساده): {PATH}")
else:
    print(f"{BAD} هیچ‌کدوم از بلاک‌های قبلی پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست تا دستی چک کنم")

print("\nتمام شد. فرانت رو رفرش کن.")
print("اگه لوگو هنوز دقیق روی لوگوی توی عکس نیفتاد، بگو چند درصد بالاتر/پایین‌تر بره (الان top: 30% گذاشتم).")
