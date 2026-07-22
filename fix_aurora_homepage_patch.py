#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_aurora_homepage_patch.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/fix_aurora_homepage_patch.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_aurora_homepage_patch.py

فقط frontend/src/pages/HomePage.jsx رو پچ می‌کنه (تورفتگی این نسخه بر اساس
خروجی واقعی cat -A تنظیم شده: 18 فاصله، نه 20).
AuroraGridBackground.jsx و index.css از اجرای قبلی درست ساخته/append شدن، اینجا لمس نمی‌شن.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
FRONTEND = ROOT / "frontend" / "src"

homepage_path = FRONTEND / "pages" / "HomePage.jsx"

if not homepage_path.exists():
    print(f"✗ فایل پیدا نشد: {homepage_path}")
    sys.exit(1)

content = homepage_path.read_text(encoding="utf-8")
backup = homepage_path.with_suffix(homepage_path.suffix + ".pre-aurorabg-fix-backup")

old_import = "import ProductCard from '../components/ui/ProductCard'"
new_import = (
    "import ProductCard from '../components/ui/ProductCard'\n"
    "import AuroraGridBackground from '../components/ui/AuroraGridBackground'"
)

old_grid = (
    "                  <Row className='g-3'>\n"
    "                    {data?.products?.map((product) => (\n"
    "                      <Col key={product._id} sm={12} md={6} lg={4} xl={3}>\n"
    "                        <ProductCard product={product} />\n"
    "                      </Col>\n"
    "                    ))}\n"
    "                  </Row>"
)
new_grid = (
    "                  <div className='aq-aurora-grid-wrapper'>\n"
    "                    <AuroraGridBackground />\n"
    "                    <div className='aq-aurora-grid-content'>\n"
    "                      <Row className='g-3'>\n"
    "                        {data?.products?.map((product) => (\n"
    "                          <Col key={product._id} sm={12} md={6} lg={4} xl={3}>\n"
    "                            <ProductCard product={product} />\n"
    "                          </Col>\n"
    "                        ))}\n"
    "                      </Row>\n"
    "                    </div>\n"
    "                  </div>"
)

if content.count(old_import) != 1:
    print(f"✗ لنگر import پیدا نشد یا تکراریه (تعداد: {content.count(old_import)}) — احتمالاً از اجرای قبلی اضافه شده، چک می‌کنم")
    if new_import in content:
        print("  -> import قبلاً درست اضافه شده، رد می‌شیم به بخش JSX")
        old_import = None
    else:
        sys.exit(1)

if content.count(old_grid) != 1:
    print(f"✗ لنگر JSX گرید پیدا نشد یا تکراریه (تعداد: {content.count(old_grid)}) — هیچ تغییری اعمال نشد")
    sys.exit(1)

shutil.copy2(homepage_path, backup)
if old_import:
    content = content.replace(old_import, new_import)
content = content.replace(old_grid, new_grid)
homepage_path.write_text(content, encoding="utf-8")

print(f"✓ HomePage.jsx پچ شد — بک‌آپ: {backup.name}")
print("\nقدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito تست کن.")
