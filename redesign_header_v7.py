#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ورژن ۷ هدر -- ریزه‌کاری‌های بعد از v6:
- رفع سفیدی پشت لوگوی PNG ترنسپرنت (mix-blend-mode)
- برگردوندن نوبار به حالت لبه‌به‌لبه (بدون گردی/مارجین) تا بار RGB هم کامل تا دو طرف بره
- فاصله‌ی بیشتر بین آیکون کاربر و سرچ‌بار (دسکتاپ)
- موبایل: جابه‌جایی سرچ‌بار به بالای ردیف آیکون‌ها
- موبایل: کوچیک‌تر کردن متن placeholder سرچ‌بار
از داخل ~/aqualotus اجرا کن:
    python3 redesign_header_v7.py
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

old_insert_point = "        <Container fluid='md'>\n          <div className='d-flex align-items-center w-100 aq-navbar-row' style={{ gap: '8px' }}>"
new_insert_point = """        <Container fluid='md'>
          {/* سرچ — موبایل (بالای ردیف آیکون‌ها) */}
          <div className='d-md-none aq-mobile-search-row' style={{ padding: '4px 4px 8px', width: '100%' }}>
            <SearchBox />
          </div>

          <div className='d-flex align-items-center w-100 aq-navbar-row' style={{ gap: '8px' }}>"""

if new_insert_point.strip() in hp:
    print("(رد شد، سرچ‌بار موبایل قبلاً بالا منتقل شده بود)")
elif old_insert_point in hp:
    hp = hp.replace(old_insert_point, new_insert_point, 1)
    changed = True
    print(f"{OK} سرچ‌بار موبایل به بالای ردیف آیکون‌ها منتقل شد")
else:
    print(f"{BAD} نقطه‌ی شروع Container پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_bottom_search = """          {/* سرچ — موبایل */}
          <div className='d-md-none' style={{ padding: '8px 4px 4px', width: '100%' }}>
            <SearchBox />
          </div>
        </Container>"""
new_bottom_search = "        </Container>"

if new_bottom_search in hp and old_bottom_search not in hp:
    print("(رد شد، سرچ‌بار موبایل قبلاً از پایین حذف شده بود)")
elif old_bottom_search in hp:
    hp = hp.replace(old_bottom_search, new_bottom_search, 1)
    changed = True
    print(f"{OK} سرچ‌بار موبایل از جای قدیمی حذف شد")
else:
    print(f"{BAD} بلاک قدیمی سرچ‌بار موبایل پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_search_desktop = "<div className='d-none d-md-flex' style={{ maxWidth: '260px', flexShrink: 0 }}>"
new_search_desktop = "<div className='d-none d-md-flex aq-header-search-desktop' style={{ maxWidth: '260px', flexShrink: 0 }}>"
if new_search_desktop in hp:
    print("(رد شد، کلاس فاصله‌ی سرچ دسکتاپ قبلاً اضافه شده بود)")
elif old_search_desktop in hp:
    hp = hp.replace(old_search_desktop, new_search_desktop, 1)
    changed = True
    print(f"{OK} کلاس فاصله‌گذاری به سرچ دسکتاپ اضافه شد")
else:
    print(f"{BAD} div سرچ دسکتاپ پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

if changed:
    backup(HEADER, "redesign-v7")
    with open(HEADER, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} پچ شد: {HEADER}")

if not os.path.exists(INDEX_CSS):
    print(f"{BAD} فایل پیدا نشد: {INDEX_CSS}")
    raise SystemExit(1)

with open(INDEX_CSS, "r", encoding="utf-8") as f:
    css = f.read()

marker = "/* --- header v7 redesign --- */"
if marker in css:
    print("(رد شد، CSS ورژن ۷ قبلاً اضافه شده بود)")
else:
    header_css = f"""
{marker}
.aq-sticky-header {{
  padding: 0 !important;
}}

.aqualotus-navbar {{
  border-radius: 0 !important;
  max-width: 100% !important;
  margin: 0 !important;
}}

.aq-brand-logo-img {{
  background: transparent;
  mix-blend-mode: multiply;
}}

.aq-header-search-desktop {{
  margin-inline-end: 18px;
}}

@media (max-width: 767px) {{
  .aq-mobile-search-row input::placeholder {{
    font-size: 0.85rem;
  }}
  .aq-mobile-search-row input {{
    font-size: 0.85rem;
  }}
}}
"""
    backup(INDEX_CSS, "redesign-v7")
    css = css.rstrip() + "\n" + header_css
    with open(INDEX_CSS, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"{OK} CSS ورژن ۷ اضافه شد: {INDEX_CSS}")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن، Ctrl+Shift+R بزن.")
print("نکته: اگه mix-blend-mode:multiply لوگو رو تیره/عجیب کرد، بگو تا با یه روش دیگه حلش کنم.")
