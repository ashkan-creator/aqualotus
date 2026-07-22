#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
جایگزینی بنر گرادیانتی موقت کوییز تو صفحه اصلی، با عکس واقعی.
از داخل ~/aqualotus اجرا کن:
    python3 update_quiz_banner_image.py

قبلش عکس رو کپی کرده باشی به:
    frontend/public/images/quiz-banner.jpg
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

PATH = "frontend/src/pages/HomePage.jsx"
IMG_PATH = "frontend/public/images/quiz-banner.jpg"

OLD_BLOCK = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
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

NEW_BLOCK = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
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
    print(f"{BAD} عکس پیدا نشد تو {IMG_PATH} -- اول عکس رو اونجا کپی کن، بعد دوباره اسکریپت رو اجرا کن")
else:
    print(f"{OK} عکس پیدا شد: {IMG_PATH}")

if not os.path.exists(PATH):
    print(f"{BAD} فایل پیدا نشد: {PATH}")
elif not NEW_BLOCK.strip() in open(PATH, "r", encoding="utf-8").read() and OLD_BLOCK.strip() not in open(PATH, "r", encoding="utf-8").read():
    print(f"{BAD} نه بلاک قدیمی نه جدید پیدا شد تو {PATH} -- احتمالاً دستی تغییرش دادی، بگو تا دستی چک کنم")
else:
    with open(PATH, "r", encoding="utf-8") as f:
        content = f.read()
    if NEW_BLOCK.strip() in content:
        print(f"(رد شد، قبلاً اعمال شده) {PATH}")
    elif OLD_BLOCK.strip() in content:
        shutil.copy2(PATH, f"{PATH}.pre-quiz-banner-image-backup")
        content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)
        with open(PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{OK} پچ شد: {PATH}")
    else:
        print(f"{BAD} بلاک قدیمی رو دقیق پیدا نکردم -- احتمالاً دستی ویرایشش کردی، بفرست محتوای فعلی HomePage.jsx رو")

print("\nتمام شد. فرانت رو رفرش کن و صفحه اصلی رو ببین.")
