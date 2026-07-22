#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
۱) حذف سفیدی پشت لوگوی png شفاف روی بنر کوییز (mix-blend-mode + background transparent)
۲) تغییر فونت متن بنر به "خودکار"
از داخل ~/aqualotus اجرا کن:
    python3 fix_quiz_banner_logo_font.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

PATH = "frontend/src/pages/HomePage.jsx"

OLD_BLOCK = """          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
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
                    fontFamily: "'Khodkar', 'Vazirmatn', sans-serif",
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
                    fontFamily: "'Khodkar', 'Vazirmatn', sans-serif",
                  }}
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
elif OLD_BLOCK.strip() in content:
    shutil.copy2(PATH, f"{PATH}.pre-quiz-banner-logofont-backup")
    content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {PATH}")
else:
    print(f"{BAD} بلاک قبلی دقیق پیدا نشد -- محتوای فعلی HomePage.jsx رو بفرست تا دستی چک کنم")

print("""
نکته ۱ (سفیدی پشت لوگو): از mix-blend-mode: multiply استفاده کردم که سفیدی پشت
لوگو رو با پس‌زمینه ترکیب می‌کنه و تقریباً محو می‌کنه. اگه لوگوت رنگ روشن/سفید
داره (نه تیره)، این ترفند برعکس جواب میده و باید یه راه دیگه بریم (بی‌زحمت بعد
از رفرش بگو نتیجه چطور شد).

نکته ۲ (فونت خودکار): این فونت رو مستقیم با CSS اعمال کردم (fontFamily) ولی
اگه فایل فونت "خودکار" (Khodkar) قبلاً جایی تو پروژه import/@font-face نشده
باشه، مرورگر فولبک می‌زنه به Vazirmatn و تغییری تو ظاهر نمی‌بینی. اگه فونت رو
از قبل تو پروژه نداری، بگو تا فایل .woff2 شو بگیرم و درست ایمپورتش کنم.
""")
