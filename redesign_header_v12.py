#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ورژن ۱۲ هدر -- فقط یه تغییر دقیق:
منوی وسط با mx-auto (فاصله‌ی مساوی از هر دو طرف) تعریف شده بود که باعث یه فاصله‌ی
مصنوعی و بزرگ بین «تماس با ما» و آیکون‌ها می‌شد. با ms-auto فقط از سمت لوگو فاصله
می‌گیره و به آیکون‌ها/سرچ می‌چسبه.
از داخل ~/aqualotus اجرا کن:
    python3 redesign_header_v12.py
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

old_nav = "<Nav className='d-none d-lg-flex mx-auto aq-navbar-center-nav'>"
new_nav = "<Nav className='d-none d-lg-flex ms-auto aq-navbar-center-nav'>"
if new_nav in hp:
    print("(رد شد، قبلاً اصلاح شده بود)")
elif old_nav in hp:
    hp = hp.replace(old_nav, new_nav, 1)
    changed = True
    print(f"{OK} منوی وسط دیگه mx-auto نیست، ms-auto شد -- حالا به آیکون‌ها می‌چسبه")
else:
    print(f"{BAD} Nav منوی وسط پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

# برگردوندن مارجین دستی گروه آیکون‌ها به یه چیز کوچیک (چون دیگه لازم نیست خودش فاصله بگیره)
old_icons_group = "style={{ gap: '8px', minWidth: 0, flexShrink: 1, marginInlineStart: '24px' }}"
new_icons_group = "style={{ gap: '8px', minWidth: 0, flexShrink: 1 }}"
if new_icons_group in hp:
    print("(رد شد، مارجین گروه آیکون‌ها قبلاً برداشته شده بود)")
elif old_icons_group in hp:
    hp = hp.replace(old_icons_group, new_icons_group, 1)
    changed = True
    print(f"{OK} مارجین دستی گروه آیکون‌ها برداشته شد (دیگه لازم نیست)")
else:
    print(f"{BAD} استایل گروه آیکون‌ها پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

if changed:
    backup(HEADER, "redesign-v12")
    with open(HEADER, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} پچ شد: {HEADER}")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن، Ctrl+Shift+R بزن (یا Incognito).")
