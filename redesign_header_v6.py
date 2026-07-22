#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بازطراحی هدر ورژن ۶ -- طبق لیست بازخورد اشکان:
- حذف نوشته‌ی AquaLotus کنار لوگو، بزرگ‌تر و بدون‌گرد کردن خود لوگو
- یکسان‌سازی سایز/ترازبندی همه‌ی دکمه‌های آیکونی (برای موبایل)
- جایگزینی همبرگر ایموجی+متن با آیکون واقعی
- آیکون‌های شیک‌تر (از همون react-icons، بدون پکیج جدید)
- نوبار بزرگ‌تر، فونت/اسپیسینگ بهتر، بدون‌بردر با هاور نرم
- کم کردن فاصله‌ی بالای هدر تا هیرو اسلایدر
از داخل ~/aqualotus اجرا کن:
    python3 redesign_header_v6.py
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

old_icon_import = "import { FaShoppingCart, FaUser } from 'react-icons/fa'"
new_icon_import = (
    "import { FaShoppingCart, FaUser } from 'react-icons/fa'\n"
    "import { FiMenu } from 'react-icons/fi'"
)
if "react-icons/fi" in hp:
    print("(رد شد، ایمپورت آیکون جدید قبلاً اضافه شده بود)")
elif old_icon_import in hp:
    hp = hp.replace(old_icon_import, new_icon_import, 1)
    changed = True
    print(f"{OK} ایمپورت FiMenu اضافه شد")
else:
    print(f"{BAD} خط ایمپورت آیکون پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_brand = """            <LinkContainer to='/'>
              <Navbar.Brand className='brand-logo d-flex align-items-center me-0' style={{ gap: '6px', flexShrink: 0 }}>
                <img
                  src='/logo.png'
                  alt='AquaLotus'
                  style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover' }}
                />
                <span className='d-none d-sm-inline' style={{ fontWeight: '600', fontSize: '1rem' }}>AquaLotus</span>
              </Navbar.Brand>
            </LinkContainer>"""

new_brand = """            <LinkContainer to='/'>
              <Navbar.Brand className='brand-logo d-flex align-items-center me-0' style={{ flexShrink: 0 }}>
                <img src='/logo.png' alt='AquaLotus' className='aq-brand-logo-img' />
              </Navbar.Brand>
            </LinkContainer>"""

if new_brand.strip() in hp:
    print("(رد شد، بلاک لوگو قبلاً بازطراحی شده بود)")
elif old_brand in hp:
    hp = hp.replace(old_brand, new_brand, 1)
    changed = True
    print(f"{OK} متن AquaLotus حذف شد، لوگو بدون‌گرد شد")
else:
    print(f"{BAD} بلاک لوگو پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_guest = """                <div style={{ cursor: 'pointer', padding: '4px' }} onClick={() => navigate('/login')}>
                  <FaUser style={{ color: 'rgba(255,255,255,0.9)', fontSize: '1.2rem' }} />
                </div>"""
new_guest = """                <div className='aq-navbar-icon-btn' onClick={() => navigate('/login')}>
                  <FaUser style={{ color: 'rgba(255,255,255,0.92)', fontSize: '1.05rem' }} />
                </div>"""
if new_guest.strip() in hp:
    print("(رد شد، دکمه کاربر مهمان قبلاً اصلاح شده بود)")
elif old_guest in hp:
    hp = hp.replace(old_guest, new_guest, 1)
    changed = True
    print(f"{OK} دکمه‌ی کاربر مهمان هم‌تراز شد")
else:
    print(f"{BAD} بلاک دکمه‌ی کاربر مهمان پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_cart = """                <div
                  id='cart-icon-target'
                  style={{ position: 'relative', cursor: 'pointer', padding: '4px' }}
                  onClick={() => navigate('/cart')}
                >
                  <FaShoppingCart style={{ color: 'rgba(255,255,255,0.9)', fontSize: '1.25rem' }} />"""
new_cart = """                <div
                  id='cart-icon-target'
                  className='aq-navbar-icon-btn'
                  style={{ position: 'relative' }}
                  onClick={() => navigate('/cart')}
                >
                  <FaShoppingCart style={{ color: 'rgba(255,255,255,0.92)', fontSize: '1.1rem' }} />"""
if new_cart.strip() in hp:
    print("(رد شد، دکمه سبد خرید قبلاً اصلاح شده بود)")
elif old_cart in hp:
    hp = hp.replace(old_cart, new_cart, 1)
    changed = True
    print(f"{OK} دکمه‌ی سبد خرید هم‌تراز شد")
else:
    print(f"{BAD} بلاک دکمه سبد خرید پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_customer_bell = "{userInfo && !userInfo.isAdmin && <CustomerNotificationBell />}"
new_customer_bell = "{userInfo && !userInfo.isAdmin && (\n                <div className='aq-navbar-icon-btn'><CustomerNotificationBell /></div>\n              )}"
if new_customer_bell.strip() in hp:
    print("(رد شد، بسته‌بندی بل مشتری قبلاً اضافه شده بود)")
elif old_customer_bell in hp:
    hp = hp.replace(old_customer_bell, new_customer_bell, 1)
    changed = True
    print(f"{OK} بل مشتری هم‌تراز شد")
else:
    print(f"{BAD} خط CustomerNotificationBell پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_admin_bell = "{userInfo?.isAdmin && <NotificationBell />}"
new_admin_bell = "{userInfo?.isAdmin && (\n                <div className='aq-navbar-icon-btn'><NotificationBell /></div>\n              )}"
if new_admin_bell.strip() in hp:
    print("(رد شد، بسته‌بندی بل ادمین قبلاً اضافه شده بود)")
elif old_admin_bell in hp:
    hp = hp.replace(old_admin_bell, new_admin_bell, 1)
    changed = True
    print(f"{OK} بل ادمین هم‌تراز شد")
else:
    print(f"{BAD} خط NotificationBell پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_hamburger = """              <button
              onClick={() => setDrawerOpen(true)}
              style={{
                background: 'rgba(255,255,255,0.15)', border: 'none',
                borderRadius: '8px', padding: '7px 10px', color: 'white',
                cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '5px',
                fontSize: '0.85rem', whiteSpace: 'nowrap', flexShrink: 0,
                transition: 'background 0.2s'
              }}
              onMouseOver={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.25)'}
              onMouseOut={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.15)'}
            >
              <span style={{ fontSize: '1.1rem', lineHeight: 1 }}>☰</span>
              <span className='d-none d-sm-inline'>دسته‌بندی</span>
            </button>"""
new_hamburger = """              <button
              onClick={() => setDrawerOpen(true)}
              className='aq-navbar-icon-btn aq-navbar-hamburger'
              style={{ background: 'rgba(255,255,255,0.12)', border: 'none', cursor: 'pointer', flexShrink: 0 }}
            >
              <FiMenu style={{ fontSize: '1.2rem', color: 'white' }} />
            </button>"""
if new_hamburger.strip() in hp:
    print("(رد شد، همبرگر قبلاً اصلاح شده بود)")
elif old_hamburger in hp:
    hp = hp.replace(old_hamburger, new_hamburger, 1)
    changed = True
    print(f"{OK} همبرگر با آیکون واقعی جایگزین شد")
else:
    print(f"{BAD} بلاک همبرگر پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

if changed:
    backup(HEADER, "redesign-v6")
    with open(HEADER, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} پچ شد: {HEADER}")

if not os.path.exists(INDEX_CSS):
    print(f"{BAD} فایل پیدا نشد: {INDEX_CSS}")
    raise SystemExit(1)

with open(INDEX_CSS, "r", encoding="utf-8") as f:
    css = f.read()

marker = "/* --- header v6 redesign --- */"
if marker in css:
    print("(رد شد، CSS ورژن ۶ قبلاً اضافه شده بود)")
else:
    header_css = f"""
{marker}
.aq-sticky-header {{
  padding: 6px 12px 0;
  margin-bottom: 0;
}}

.aqualotus-navbar {{
  padding: 6px 0 !important;
}}

.aq-brand-logo-img {{
  width: clamp(56px, 6vw, 76px);
  height: clamp(56px, 6vw, 76px);
  border-radius: 0;
  object-fit: contain;
  display: block;
}}

.aq-navbar-center-nav .nav-link {{
  white-space: nowrap;
  text-align: center;
  font-size: 0.98rem;
}}

.aq-navbar-icon-btn {{
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.25s ease, transform 0.2s ease;
  flex-shrink: 0;
}}

.aq-navbar-icon-btn:hover {{
  background: rgba(255, 255, 255, 0.14);
  transform: translateY(-1px);
}}

.aqualotus-navbar .dropdown-toggle {{
  display: flex !important;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  padding: 0 !important;
  border-radius: 50%;
  transition: background 0.25s ease, transform 0.2s ease;
}}
.aqualotus-navbar .dropdown-toggle:hover {{
  background: rgba(255, 255, 255, 0.14);
  transform: translateY(-1px);
}}
.aqualotus-navbar .dropdown-toggle::after {{
  display: none;
}}

.aq-navbar-hamburger {{
  border-radius: 50% !important;
}}

@media (max-width: 767px) {{
  .aq-sticky-header {{
    padding: 4px 6px 0;
  }}
  .aq-brand-logo-img {{
    width: 52px;
    height: 52px;
  }}
  .aq-navbar-row > div:last-child {{
    gap: 4px !important;
  }}
}}
"""
    backup(INDEX_CSS, "redesign-v6")
    css = css.rstrip() + "\n" + header_css
    with open(INDEX_CSS, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"{OK} CSS ورژن ۶ اضافه شد: {INDEX_CSS}")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن، Ctrl+Shift+R بزن.")
print("ترتیب آیکون‌های موبایل دست‌نخورده موند -- فقط سایز/ترازشون یکی شد.")
print("اگه لوگوی فعلی (logo.png) با border-radius:0 بد به‌نظر رسید (چون شاید خودش گرد نبوده)، بگو تا برگردونم.")
