#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نسخه نهایی بنر کوییز صفحه اصلی: متن سفید روی خودِ عکس (overlay).
از داخل ~/aqualotus اجرا کن:
    python3 finalize_quiz_banner.py

قبلش عکس جدید رو کپی کرده باشی روی:
    frontend/public/images/quiz-banner.jpg
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

PATH = "frontend/src/pages/HomePage.jsx"
IMG_PATH = "frontend/public/images/quiz-banner.jpg"

NEW_BLOCK = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
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

# دو نسخه‌ی قبلی که ممکنه الان تو فایل باشه (گرادیانت اول، یا نسخه‌ی متن-زیر-عکس)
OLD_BLOCK_GRADIENT = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
            <div
              className='d-flex flex-column align-items-center justify-content-center text-center rounded-4 p-4'
              style={{
                background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))',
                minHeight: '180px',
                color: '#fff',
              }}
            >
              <div style={{ fontSize: '2rem' }}>🌿</div>
              <h4 className='mt-2 mb-1' style={{ color: '#fff' }}>
                گیاه مناسب آکواریومت رو پیدا کن!
              </h4>
              <p className='mb-0' style={{ color: '#fff', opacity: 0.9 }}>
                با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
              </p>
            </div>
          </Link>"""

OLD_BLOCK_BELOW = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
            <div
              className='rounded-4'
              style={{
                backgroundImage: "url('/images/quiz-banner.jpg')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                minHeight: '220px',
              }}
            />
            <div className='text-center mt-2'>
              <h4 className='mb-1' style={{ color: 'var(--primary-dark)' }}>
                گیاه مناسب آکواریومت رو پیدا کن!
              </h4>
              <p className='text-muted mb-0'>
                با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
              </p>
            </div>
          </Link>"""

if not os.path.exists(IMG_PATH):
    print(f"{BAD} عکس پیدا نشد تو {IMG_PATH} -- اول عکس رو اونجا کپی کن، بعد دوباره اجرا کن")
    raise SystemExit(1)
print(f"{OK} عکس پیدا شد: {IMG_PATH}")

if not os.path.exists(PATH):
    print(f"{BAD} فایل پیدا نشد: {PATH}")
    raise SystemExit(1)

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

if NEW_BLOCK.strip() in content:
    print(f"(رد شد، قبلاً اعمال شده) {PATH}")
elif OLD_BLOCK_GRADIENT.strip() in content:
    shutil.copy2(PATH, f"{PATH}.pre-quiz-banner-final-backup")
    content = content.replace(OLD_BLOCK_GRADIENT, NEW_BLOCK, 1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد (از نسخه گرادیانت): {PATH}")
elif OLD_BLOCK_BELOW.strip() in content:
    shutil.copy2(PATH, f"{PATH}.pre-quiz-banner-final-backup")
    content = content.replace(OLD_BLOCK_BELOW, NEW_BLOCK, 1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد (از نسخه متن-زیر-عکس): {PATH}")
else:
    print(f"{BAD} هیچ‌کدوم از بلاک‌های قبلی پیدا نشد -- احتمالاً دستی ویرایش شده، محتوای فعلی HomePage.jsx رو بفرست")

print("\nتمام شد. فرانت رو رفرش کن و صفحه اصلی رو ببین.")
