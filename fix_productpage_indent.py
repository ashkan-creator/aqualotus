#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_productpage_indent.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/fix_productpage_indent.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_productpage_indent.py

فقط ProductPage.jsx رو پچ می‌کنه (index.css از اجرای قبلی درست شد، اینجا لمس نمی‌شه).
تورفتگی این نسخه بر اساس خروجی واقعی cat -A تنظیم شده.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
page_path = ROOT / "frontend" / "src" / "pages" / "ProductPage.jsx"

if not page_path.exists():
    print(f"✗ فایل پیدا نشد: {page_path}")
    sys.exit(1)

content = page_path.read_text(encoding="utf-8")
backup = page_path.with_suffix(page_path.suffix + ".pre-aurorafix-indent-backup")

old_listgroup_open = "            <Col md={4}>\n              <ListGroup variant='flush'>"
new_listgroup_open = "            <Col md={4}>\n              <div className='aq-product-info-panel'>\n              <ListGroup variant='flush'>"

old_listgroup_close = "              </ListGroup>\n            </Col>\n\n            <Col md={3}>"
new_listgroup_close = "              </ListGroup>\n              </div>\n            </Col>\n\n            <Col md={3}>"

old_heading = "              <h4 className='mb-3'>نظرات کاربران</h4>"
new_heading = "              <h4 className='mb-3 aq-reviews-heading'>نظرات کاربران</h4>"

checks = {
    "listgroup_open": content.count(old_listgroup_open),
    "listgroup_close": content.count(old_listgroup_close),
    "heading": content.count(old_heading),
}

if not all(v == 1 for v in checks.values()):
    print(f"✗ لنگر(ها) پیدا نشد یا تکراری بود — {checks} — هیچ تغییری اعمال نشد")
    sys.exit(1)

shutil.copy2(page_path, backup)
content = content.replace(old_listgroup_open, new_listgroup_open)
content = content.replace(old_listgroup_close, new_listgroup_close)
content = content.replace(old_heading, new_heading)
page_path.write_text(content, encoding="utf-8")

print(f"✓ ProductPage.jsx پچ شد — بک‌آپ: {backup.name}")
print("\nقدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
