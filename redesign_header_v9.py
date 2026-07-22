#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ورژن ۹ هدر -- موبایل: یه آیکون کوچیک سرچ دقیقاً جای همبرگر می‌شینه، همبرگر یه پله
کنار می‌ره. با زدن آیکون سرچ، جعبه‌ی کامل سرچ (همونی که از قبل داشتیم) باز/بسته می‌شه.
از داخل ~/aqualotus اجرا کن:
    python3 redesign_header_v9.py
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

old_import = "import { FiMenu } from 'react-icons/fi'"
new_import = "import { FiMenu, FiSearch } from 'react-icons/fi'"
if "FiSearch" in hp:
    print("(رد شد، FiSearch از قبل ایمپورت شده بود)")
elif old_import in hp:
    hp = hp.replace(old_import, new_import, 1)
    changed = True
    print(f"{OK} FiSearch ایمپورت شد")
else:
    print(f"{BAD} خط ایمپورت FiMenu پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_state = "const [openSection, setOpenSection] = useState(null)"
new_state = "const [openSection, setOpenSection] = useState(null)\n  const [mobileSearchOpen, setMobileSearchOpen] = useState(false)"
if "mobileSearchOpen" in hp:
    print("(رد شد، استیت سرچ موبایل از قبل بود)")
elif old_state in hp:
    hp = hp.replace(old_state, new_state, 1)
    changed = True
    print(f"{OK} استیت mobileSearchOpen اضافه شد")
else:
    print(f"{BAD} خط استیت openSection پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_hamburger = """              <button
              onClick={() => setDrawerOpen(true)}
              className='aq-navbar-icon-btn aq-navbar-hamburger'
              style={{ background: 'rgba(255,255,255,0.12)', border: 'none', cursor: 'pointer', flexShrink: 0 }}
            >
              <FiMenu style={{ fontSize: '1.2rem', color: 'white' }} />
            </button>"""

new_hamburger = """              <button
              onClick={() => setDrawerOpen(true)}
              className='aq-navbar-icon-btn aq-navbar-hamburger'
              style={{ background: 'rgba(255,255,255,0.12)', border: 'none', cursor: 'pointer', flexShrink: 0 }}
            >
              <FiMenu style={{ fontSize: '1.2rem', color: 'white' }} />
            </button>
              <button
              className='aq-navbar-icon-btn d-md-none'
              onClick={() => setMobileSearchOpen((o) => !o)}
              style={{ background: 'rgba(255,255,255,0.12)', border: 'none', cursor: 'pointer', flexShrink: 0 }}
            >
              <FiSearch style={{ fontSize: '1.2rem', color: 'white' }} />
            </button>"""

if new_hamburger.strip() in hp:
    print("(رد شد، آیکون سرچ موبایل از قبل اضافه شده بود)")
elif old_hamburger in hp:
    hp = hp.replace(old_hamburger, new_hamburger, 1)
    changed = True
    print(f"{OK} آیکون سرچ کنار همبرگر اضافه شد")
else:
    print(f"{BAD} بلاک همبرگر پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

old_mobile_search = """          {/* سرچ — موبایل */}
          <div className='d-md-none aq-mobile-search-row' style={{ padding: '8px 4px 4px', width: '100%' }}>
            <SearchBox />
          </div>
        </Container>"""
new_mobile_search = """          {/* سرچ — موبایل (فقط وقتی آیکون سرچ زده بشه) */}
          {mobileSearchOpen && (
            <div className='d-md-none aq-mobile-search-row' style={{ padding: '8px 4px 4px', width: '100%' }}>
              <SearchBox />
            </div>
          )}
        </Container>"""

if new_mobile_search.strip() in hp:
    print("(رد شد، شرطی‌سازی سرچ موبایل از قبل بود)")
elif old_mobile_search in hp:
    hp = hp.replace(old_mobile_search, new_mobile_search, 1)
    changed = True
    print(f"{OK} سرچ موبایل شرطی (فقط با تپ آیکون) شد")
else:
    print(f"{BAD} بلاک سرچ موبایل پیدا نشد -- محتوای فعلی Header.jsx رو بفرست")

if changed:
    backup(HEADER, "redesign-v9")
    with open(HEADER, "w", encoding="utf-8") as f:
        f.write(hp)
    print(f"{OK} پچ شد: {HEADER}")

print("\nتمام شد. فرانت رو کامل ری‌استارت کن، Ctrl+Shift+R بزن (یا Incognito).")
print("رو موبایل، آیکون همبرگر و آیکون سرچ جدید کنار هم‌ان -- سرچ با تپ باز/بسته می‌شه.")
