#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
۱) عکس موبایل: زوم دستی (100%) رو برمی‌داریم، برمی‌گردونیم به cover طبیعی (بدون زوم)
۲) خط "کلیک کنید" رو بزرگ‌تر می‌کنیم، هم دسکتاپ هم موبایل
از داخل ~/aqualotus اجرا کن:
    python3 fix_quiz_banner_zoom_cta_size.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

FONTS_CSS = "frontend/src/fonts.css"

if not os.path.exists(FONTS_CSS):
    print(f"{BAD} فایل پیدا نشد: {FONTS_CSS}")
    raise SystemExit(1)

with open(FONTS_CSS, "r", encoding="utf-8") as f:
    content = f.read()

changed = False

# ۱) حذف زوم دستی عکس موبایل
old_zoom = "background-size: 100% !important;"
new_zoom = "background-size: cover !important;"
if new_zoom in content and old_zoom not in content:
    print("(رد شد، زوم قبلاً برداشته شده بود)")
elif old_zoom in content:
    content = content.replace(old_zoom, new_zoom, 1)
    changed = True
    print(f"{OK} زوم عکس موبایل برداشته شد (100% -> cover)")
else:
    print(f"{BAD} مقدار background-size فعلی پیدا نشد -- این خط رو بفرست: grep -n \"background-size\" frontend/src/fonts.css")

# ۲) بزرگ‌تر کردن فونت کلیک کنید -- دسکتاپ
old_cta_desktop = "font-size: 0.9rem !important;"
new_cta_desktop = "font-size: 1.15rem !important;"
if new_cta_desktop in content and old_cta_desktop not in content:
    print("(رد شد، سایز دسکتاپ کلیک‌کنید قبلاً بزرگ شده بود)")
elif old_cta_desktop in content:
    content = content.replace(old_cta_desktop, new_cta_desktop, 1)
    changed = True
    print(f"{OK} سایز دسکتاپ «کلیک کنید» بزرگ‌تر شد")
else:
    print(f"{BAD} سایز فعلی CTA دسکتاپ پیدا نشد -- محتوای فعلی fonts.css رو بفرست")

# ۳) بزرگ‌تر کردن فونت کلیک کنید -- موبایل
old_cta_mobile = "font-size: 0.95rem !important;"
new_cta_mobile = "font-size: 1.35rem !important;"
if new_cta_mobile in content and old_cta_mobile not in content:
    print("(رد شد، سایز موبایل کلیک‌کنید قبلاً بزرگ شده بود)")
elif old_cta_mobile in content:
    content = content.replace(old_cta_mobile, new_cta_mobile, 1)
    changed = True
    print(f"{OK} سایز موبایل «کلیک کنید» بزرگ‌تر شد")
else:
    print(f"{BAD} سایز فعلی CTA موبایل پیدا نشد -- محتوای فعلی fonts.css رو بفرست")

if changed:
    shutil.copy2(FONTS_CSS, f"{FONTS_CSS}.pre-zoom-cta-size-backup")
    with open(FONTS_CSS, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} پچ شد: {FONTS_CSS}")

print("\nتمام شد. فرانت رو ری‌استارت کن، Ctrl+Shift+R بزن.")
