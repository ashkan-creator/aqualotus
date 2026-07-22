#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ورژن ۱۱ هدر (طبق پیشنهاد اشکان):
- گروه آیکون‌ها (و نام کاربر) رو به دکمه‌ی «تماس با ما» نزدیک‌تر می‌کنه
- سرچ‌بار دسکتاپ رو یه‌کم (خیلی کم) کوچیک‌تر می‌کنه
از داخل ~/aqualotus اجرا کن:
    python3 redesign_header_v11.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

HEADER = "frontend/src/components/layout/Header.jsx"


def backup(path, tag):
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.pre-{tag}-backup")


if not os.path.exists(HEADER):
    print(f"{BAD} فایل پیدا نشد: {HEADER}")
    raise SystemExit(1)

with open(HEADER, "r", encoding="utf-8") as f:
    hp = f.read()

changed = False

old_icons_group = "<div className='d-flex align-items-center ms-auto' style={{ gap: '8px', minWidth: 0, flexShrink: 1 }}>"
new_icons_group = "<div className='d-flex align-items-center' style={{ gap: '8px', minWidth: 0, flexShrink: 1, marginInlineStart: '24px' }}>"
if new_icons_group in hp:
    print("(رد شد، فاصله‌ی گروه آیکون‌ها قبلاً اصلاح شده بود)")
elif old_icons_group in hp:
    hp = hp.replace(old_icons_group, new_icons_group, 1)
    changed = True
    print(f"{OK} گروه آیکون‌ها به تماس با ما نزدیک‌تر شد")
else:
    print(f"{BAD} div گروه آیکون‌ها پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_search = "<div className='d-none d-md-flex aq-header-search-desktop' style={{ maxWidth: '260px', flexShrink: 1, minWidth: '120px' }}>"
new_search = "<div className='d-none d-md-flex aq-header-search-desktop' style={{ maxWidth: '210px', flexShrink: 1, minWidth: '110px' }}>"
if new_search in hp:
    print("(رد شد، سرچ‌بار قبلاً کوچیک‌تر شده بود)")
elif old_search in hp:
    hp = hp.replace(old_search, new_search, 1)
    changed = True
    print(f"{OK} سرچ‌بار دسکتاپ کمی کوچیک‌تر شد (260px -> 210px)")
else:
    print(f"{BAD} div سرچ دسکتاپ پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

if changed:
    backup(HEADER, "redesign-v11")
    with open(HEADER, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} پچ شد: {HEADER}")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن، Ctrl+Shift+R بزن (یا Incognito).")
