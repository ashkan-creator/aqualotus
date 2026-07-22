#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بازطراحی هدر (ورژن ۵): نوبار شناور و شیشه‌ای (Glassmorphism) با رنگ‌های فعلی برند،
+ منوی مرکزی جدید (محصولات / مجله / درباره ما / تماس با ما) فقط تو دسکتاپ بزرگ.
درِور کشویی موبایل دست‌نخورده می‌مونه.
از داخل ~/aqualotus اجرا کن:
    python3 redesign_header_v5.py
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


# ------------------------------------------------------------------
# ۱) Header.jsx -- ساختار جدید ردیف اصلی نوبار
# ------------------------------------------------------------------
if not os.path.exists(HEADER):
    print(f"{BAD} فایل پیدا نشد: {HEADER}")
    raise SystemExit(1)

with open(HEADER, "r", encoding="utf-8") as f:
    hp = f.read()

changed = False

old_import = "import { Navbar, Nav, Container, NavDropdown, Badge } from 'react-bootstrap'"
if old_import not in hp:
    print(f"{BAD} خط import react-bootstrap پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")
else:
    print(f"{OK} Nav از قبل import شده بود")

old_row_start = "          <div className='d-flex align-items-center w-100' style={{ gap: '8px' }}>\n\n            {/* آیکون کاربر و ورود */}"

new_row_start = """          <div className='d-flex align-items-center w-100 aq-navbar-row' style={{ gap: '8px' }}>

            {/* لوگو و برند — راست */}
            <LinkContainer to='/'>
              <Navbar.Brand className='brand-logo d-flex align-items-center me-0' style={{ gap: '6px', flexShrink: 0 }}>
                <img
                  src='/logo.png'
                  alt='AquaLotus'
                  style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover' }}
                />
                <span className='d-none d-sm-inline' style={{ fontWeight: '600', fontSize: '1rem' }}>AquaLotus</span>
              </Navbar.Brand>
            </LinkContainer>

            {/* منوی اصلی — وسط، فقط دسکتاپ بزرگ */}
            <Nav className='d-none d-lg-flex mx-auto aq-navbar-center-nav'>
              <LinkContainer to='/'><Nav.Link>محصولات</Nav.Link></LinkContainer>
              <LinkContainer to='/blog'><Nav.Link>مجله آکواریوم و گیاهان</Nav.Link></LinkContainer>
              <LinkContainer to='/about'><Nav.Link>درباره ما</Nav.Link></LinkContainer>
              <LinkContainer to='/contact'><Nav.Link>تماس با ما</Nav.Link></LinkContainer>
            </Nav>

            {/* آیکون کاربر و ورود */}"""

if new_row_start.strip() in hp:
    print("(رد شد، ردیف اصلی قبلاً بازطراحی شده بود)")
elif old_row_start in hp:
    hp = hp.replace(old_row_start, new_row_start, 1)
    changed = True
    print(f"{OK} ردیف اصلی نوبار بازطراحی شد (لوگو + منوی مرکزی اضافه شد)")
else:
    print(f"{BAD} بلاک شروع ردیف اصلی پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_logo_block = """            {/* لوگو */}
            <LinkContainer to='/'>
              <Navbar.Brand className='brand-logo d-flex align-items-center me-0' style={{ gap: '6px', flexShrink: 0 }}>
                <img
                  src='/logo.png'
                  alt='AquaLotus'
                  style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover' }}
                />
                <span className='d-none d-sm-inline' style={{ fontWeight: '600', fontSize: '1rem' }}>AquaLotus</span>
              </Navbar.Brand>
            </LinkContainer>

            {/* سرچ — وسط، فقط دسکتاپ */}
            <div className='d-none d-md-flex flex-grow-1 mx-2'>
              <SearchBox />
            </div>"""

new_logo_block = """            {/* سرچ — فقط دسکتاپ، مینیمال */}
            <div className='d-none d-md-flex' style={{ maxWidth: '260px', flexShrink: 0 }}>
              <SearchBox />
            </div>"""

if new_logo_block.strip() in hp:
    print("(رد شد، بلاک قدیمی لوگو قبلاً حذف شده بود)")
elif old_logo_block in hp:
    hp = hp.replace(old_logo_block, new_logo_block, 1)
    changed = True
    print(f"{OK} بلاک تکراری لوگو حذف و سرچ مینیمال شد")
else:
    print(f"{BAD} بلاک قدیمی لوگو/سرچ پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

if changed:
    backup(HEADER, "redesign-v5")
    with open(HEADER, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} پچ شد: {HEADER}")

# ------------------------------------------------------------------
# ۲) index.css -- بلاک جدید و متمرکز شناور/شیشه‌ای (انتهای فایل، مارکر جدا)
# ------------------------------------------------------------------
if not os.path.exists(INDEX_CSS):
    print(f"{BAD} فایل پیدا نشد: {INDEX_CSS}")
    raise SystemExit(1)

with open(INDEX_CSS, "r", encoding="utf-8") as f:
    css = f.read()

marker = "/* --- header v5 redesign --- */"
if marker in css:
    print("(رد شد، CSS بازطراحی هدر قبلاً اضافه شده بود)")
else:
    header_css = f"""
{marker}
.aq-sticky-header {{
  padding: 10px 12px 0;
}}

.aqualotus-navbar {{
  background: rgba(17, 51, 41, 0.78);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
  max-width: 1320px;
  margin: 0 auto;
}}

.brand-logo {{
  font-size: 1.3rem;
}}

.aq-navbar-center-nav .nav-link {{
  color: rgba(255, 255, 255, 0.88) !important;
  font-weight: 500;
  padding: 8px 16px !important;
  border-radius: 999px;
  transition: all 0.3s ease;
}}

.aq-navbar-center-nav .nav-link:hover {{
  color: #fff !important;
  background: rgba(255, 255, 255, 0.12);
}}

@media (max-width: 767px) {{
  .aq-sticky-header {{
    padding: 6px 6px 0;
  }}
  .aqualotus-navbar {{
    border-radius: 14px;
  }}
}}
"""
    backup(INDEX_CSS, "redesign-v5")
    css = css.rstrip() + "\n" + header_css
    with open(INDEX_CSS, "w", encoding="utf-8") as f:
        f.write(css)
    print(f"{OK} CSS بازطراحی هدر اضافه شد: {INDEX_CSS}")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن و Ctrl+Shift+R بزن.")
print("درِور کشویی موبایل (دسته‌بندی) دست‌نخورده موند -- فقط منوی مرکزی جدید فقط تو دسکتاپ بزرگ (lg+) دیده می‌شه.")
print("نکته: چون هدر شناور شد، ممکنه AnnouncementBar زیرش یه‌کم فاصله عجیب داشته باشه -- بعد از دیدن نتیجه بگو تا تنظیمش کنم.")
