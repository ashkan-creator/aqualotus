#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ورژن ۱۰ هدر -- سه تا فیکس مبتنی بر کد واقعی (نه حدس):
۱) تداخل نام کاربر با سرچ‌بار: مشکل کلاسیک فلکس‌باکسه -- آیتم‌های فلکس بدون
   min-width:0 جمع نمی‌شن، فقط رو هم overlap می‌کنن. این رو درست می‌کنه.
۲) پنل نوتیفیکیشن (ادمین و مشتری) رو موبایل با top:64px هاردکد شده بود -- چون
   هدر خیلی بلندتر شده (لوگوی بزرگ‌تر و ...)، این عدد رو به‌روز می‌کنیم.
۳) نتایج زنده‌ی سرچ رو موبایل بزرگ‌تر و خواناتر می‌شن.
از داخل ~/aqualotus اجرا کن:
    python3 redesign_header_v10.py
"""

import os
import shutil

OK = "\u2713"
BAD = "\u2717"

HEADER = "frontend/src/components/layout/Header.jsx"
SEARCHBOX = "frontend/src/components/ui/SearchBox.jsx"
NOTIF_BELL = "frontend/src/components/ui/NotificationBell.jsx"
CUSTOMER_BELL_CSS = "frontend/src/components/ui/CustomerNotificationBell.css"
INDEX_CSS = "frontend/src/index.css"


def backup(path, tag):
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.pre-{tag}-backup")


def patch_str(path, old, new, tag, label):
    if not os.path.exists(path):
        print(f"{BAD} فایل پیدا نشد: {path}")
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if new.strip() in content and old.strip() not in content:
        print(f"(رد شد، قبلاً اعمال شده) {label}")
        return False
    if old not in content:
        print(f"{BAD} انکر پیدا نشد ({label}) -- محتوای فعلی {path} رو بفرست")
        return False
    backup(path, tag)
    content = content.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{OK} {label}")
    return True


# ------------------------------------------------------------------
# ۱) Header.jsx -- min-width:0 رو گروه آیکون‌ها (رفع overlap واقعی)
# ------------------------------------------------------------------
old_icons_group = "<div className='d-flex align-items-center ms-auto' style={{ gap: '8px' }}>"
new_icons_group = "<div className='d-flex align-items-center ms-auto' style={{ gap: '8px', minWidth: 0, flexShrink: 1 }}>"
patch_str(HEADER, old_icons_group, new_icons_group, "v10-minwidth", "min-width:0 به گروه آیکون‌ها اضافه شد (رفع overlap نام کاربر)")

old_search_desktop = "<div className='d-none d-md-flex aq-header-search-desktop' style={{ maxWidth: '260px', flexShrink: 0 }}>"
new_search_desktop = "<div className='d-none d-md-flex aq-header-search-desktop' style={{ maxWidth: '260px', flexShrink: 1, minWidth: '120px' }}>"
patch_str(HEADER, old_search_desktop, new_search_desktop, "v10-search-shrink", "سرچ دسکتاپ هم قابل کوچیک‌شدن شد (به‌جای overlap)")

# ------------------------------------------------------------------
# ۲) SearchBox.jsx -- عرض کامل + کلاس رو نتایج برای استایل موبایل
# ------------------------------------------------------------------
old_wrapper = "<div ref={wrapperRef} style={{ position: 'relative' }}>"
new_wrapper = "<div ref={wrapperRef} style={{ position: 'relative', width: '100%' }}>"
patch_str(SEARCHBOX, old_wrapper, new_wrapper, "v10-searchbox-width", "عرض کامل به SearchBox اضافه شد")

old_listgroup_style = """        <ListGroup
          style={{
            position: 'absolute',
            top: '100%',
            right: 0,
            left: 0,
            zIndex: 9999,
            maxHeight: '300px',
            overflowY: 'auto',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          }}
        >"""
new_listgroup_style = """        <ListGroup
          className='aq-search-results'
          style={{
            position: 'absolute',
            top: '100%',
            right: 0,
            left: 0,
            zIndex: 9999,
            maxHeight: '300px',
            overflowY: 'auto',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          }}
        >"""
patch_str(SEARCHBOX, old_listgroup_style, new_listgroup_style, "v10-searchbox-class", "کلاس aq-search-results به نتایج زنده اضافه شد")

# ------------------------------------------------------------------
# ۳) NotificationBell.jsx (ادمین) -- به‌روزرسانی top ثابت
# ------------------------------------------------------------------
old_top = "top: '64px',"
new_top = "top: '92px',"
patch_str(NOTIF_BELL, old_top, new_top, "v10-notif-top", "top پنل نوتیفیکیشن ادمین به‌روز شد (64px -> 92px)")

# ------------------------------------------------------------------
# ۴) CustomerNotificationBell.css -- به‌روزرسانی top تو مدیا کوئری موبایل
# ------------------------------------------------------------------
old_customer_top = "    top: 64px;"
new_customer_top = "    top: 92px;"
patch_str(CUSTOMER_BELL_CSS, old_customer_top, new_customer_top, "v10-customer-notif-top", "top پنل نوتیفیکیشن مشتری به‌روز شد (64px -> 92px)")

# ------------------------------------------------------------------
# ۵) index.css -- نتایج سرچ رو موبایل بزرگ‌تر
# ------------------------------------------------------------------
if not os.path.exists(INDEX_CSS):
    print(f"{BAD} فایل پیدا نشد: {INDEX_CSS}")
else:
    with open(INDEX_CSS, "r", encoding="utf-8") as f:
        css = f.read()
    marker = "/* --- header v10 redesign --- */"
    if marker in css:
        print("(رد شد، CSS ورژن ۱۰ قبلاً اضافه شده بود)")
    else:
        v10_css = f"""
{marker}
@media (max-width: 767px) {{
  .aq-search-results {{
    max-height: 60vh !important;
  }}
  .aq-search-results .list-group-item {{
    padding: 12px 14px !important;
  }}
  .aq-search-results img {{
    width: 52px !important;
    height: 52px !important;
  }}
  .aq-search-results div[style*='font-size: 0.9rem'] {{
    font-size: 1rem !important;
  }}
}}
"""
        backup(INDEX_CSS, "v10")
        css = css.rstrip() + "\n" + v10_css
        with open(INDEX_CSS, "w", encoding="utf-8") as f:
            f.write(css)
        print(f"{OK} CSS ورژن ۱۰ (نتایج سرچ موبایل بزرگ‌تر) اضافه شد")

print("\nتمام شد. سرور فرانت و بک‌اند رو کامل ری‌استارت کن، بعد Service Worker رو Unregister کن (Application tab)")
print("و Incognito چک کن. اگه بازم top نوتیفیکیشن دقیق نبود، بگو عدد دقیق بدم.")
