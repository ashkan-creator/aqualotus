#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ورژن ۸ هدر:
- برگردوندن سرچ‌بار موبایل به جای اصلیش (زیر ردیف آیکون‌ها) -- عذرخواهی بابت v7
- حذف mix-blend-mode:multiply از لوگو (چون رو پس‌زمینه‌ی تیره برعکس جواب داد و تیره‌ش کرد)
- جلوگیری از تداخل نام کاربر (وقتی لاگینی) با سرچ‌بار: تک‌خط + بیضی + فاصله‌ی بیشتر
از داخل ~/aqualotus اجرا کن:
    python3 redesign_header_v8.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

HEADER = "frontend/src/components/layout/Header.jsx"
INDEX_CSS = "frontend/src/index.css"


def backup(path, tag):
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.pre-{tag}-backup")


if not os.path.exists(HEADER):
    print(f"{BAD} فایل پیدا نشد: {HEADER}")
    raise SystemExit(1)

with open(HEADER, "r", encoding="utf-8") as f:
    hp = f.read()

changed = False

v7_insert = """        <Container fluid='md'>
          {/* سرچ — موبایل (بالای ردیف آیکون‌ها) */}
          <div className='d-md-none aq-mobile-search-row' style={{ padding: '4px 4px 8px', width: '100%' }}>
            <SearchBox />
          </div>

          <div className='d-flex align-items-center w-100 aq-navbar-row' style={{ gap: '8px' }}>"""
v5_original = """        <Container fluid='md'>
          <div className='d-flex align-items-center w-100 aq-navbar-row' style={{ gap: '8px' }}>"""

if v5_original in hp:
    print("(رد شد، سرچ‌بار موبایل از قبل تو جای اصلیش بود)")
elif v7_insert in hp:
    hp = hp.replace(v7_insert, v5_original, 1)
    changed = True
    print(f"{OK} سرچ‌بار موبایل از بالا برداشته شد")
else:
    print(f"{BAD} نقطه‌ی شروع Container پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

closing_container_only = "        </Container>"
bottom_search_block = """          {/* سرچ — موبایل */}
          <div className='d-md-none aq-mobile-search-row' style={{ padding: '8px 4px 4px', width: '100%' }}>
            <SearchBox />
          </div>
        </Container>"""

if "{/* سرچ — موبایل */}" in hp:
    print("(رد شد، سرچ‌بار موبایل از قبل پایین بود)")
else:
    idx = hp.rfind(closing_container_only)
    if idx == -1:
        print(f"{BAD} تگ بسته‌ی Container پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")
    else:
        hp = hp[:idx] + bottom_search_block + hp[idx + len(closing_container_only):]
        changed = True
        print(f"{OK} سرچ‌بار موبایل به زیر ردیف اصلی برگردوندیم")

old_username = "<span className='d-none d-sm-inline'>{userInfo.name}</span>"
new_username = "<span className='d-none d-sm-inline aq-navbar-username'>{userInfo.name}</span>"
if new_username in hp:
    print("(رد شد، کلاس نام کاربر قبلاً اضافه شده بود)")
elif old_username in hp:
    hp = hp.replace(old_username, new_username, 1)
    changed = True
    print(f"{OK} کلاس محدودکننده به نام کاربر اضافه شد")
else:
    print(f"{BAD} span نام کاربر پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

if changed:
    backup(HEADER, "redesign-v8")
    with open(HEADER, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} پچ شد: {HEADER}")

if not os.path.exists(INDEX_CSS):
    print(f"{BAD} فایل پیدا نشد: {INDEX_CSS}")
    raise SystemExit(1)

with open(INDEX_CSS, "r", encoding="utf-8") as f:
    css = f.read()

marker = "/* --- header v8 redesign --- */"
if marker in css:
    print("(رد شد، CSS ورژن ۸ قبلاً اضافه شده بود)")
else:
    header_css = f"""
{marker}
.aq-brand-logo-img {{
  mix-blend-mode: normal;
  background: transparent;
}}

.aq-navbar-username {{
  display: inline-block;
  max-width: 90px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
}}

.aq-navbar-row > div:last-child {{
  margin-inline-start: 10px;
}}
"""
    backup(INDEX_CSS, "redesign-v8")
    css = css.rstrip() + "\n" + header_css
    with open(INDEX_CSS, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"{OK} CSS ورژن ۸ اضافه شد: {INDEX_CSS}")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن، Ctrl+Shift+R بزن.")
print("برای سفیدی پشت لوگو، اسکریپت جدا (fix_logo_transparency.py) رو هم اجرا کن.")
