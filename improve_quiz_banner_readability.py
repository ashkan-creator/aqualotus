#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بهبود بنر کوییز: یه کادر نیمه‌شفاف پشت متن (خونا بشه) + لوگوی خود سایت روی عکس.
از داخل ~/aqualotus اجرا کن:
    python3 improve_quiz_banner_readability.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

PATH = "frontend/src/pages/HomePage.jsx"

OLD_BLOCK = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
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

if not os.path.exists(PATH):
    print(f"{BAD} فایل پیدا نشد: {PATH}")
    raise SystemExit(1)

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

if NEW_BLOCK.strip() in content:
    print(f"(رد شد، قبلاً اعمال شده) {PATH}")
elif OLD_BLOCK.strip() in content:
    shutil.copy2(PATH, f"{PATH}.pre-quiz-banner-readability-backup")
    content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {PATH}")
else:
    print(f"{BAD} بلاک قدیمی دقیق پیدا نشد -- شاید دستی ویرایشش کردی. محتوای فعلی HomePage.jsx رو بفرست تا دستی چک کنم")

print("\nنکته: این اسکریپت فرض کرده لوگوی سایت رو تو frontend/public/logo.png داری (چون تو HomePage.jsx قبلاً به https://aqualotus.ir/logo.png اشاره شده بود).")
print("اگه اسم/مسیر فایل لوگو فرق داره، بهم بگو تا مسیر src رو تو کد اصلاح کنم.")
print("تمام شد. فرانت رو رفرش کن.")
