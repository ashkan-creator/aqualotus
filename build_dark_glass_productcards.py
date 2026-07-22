#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_dark_glass_productcards.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_dark_glass_productcards.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_dark_glass_productcards.py

فقط index.css رو append می‌کنه.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
css_path = ROOT / "frontend" / "src" / "index.css"

if not css_path.exists():
    print(f"✗ فایل پیدا نشد: {css_path}")
    sys.exit(1)

content = css_path.read_text(encoding="utf-8")
marker = "/* --- dark glass product cards v1 --- */"

if marker in content:
    print("✗ این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    sys.exit(1)

backup = css_path.with_suffix(css_path.suffix + ".pre-darkglass-cards-backup")
shutil.copy2(css_path, backup)

extra_css = f'''

{marker}
/* این بلاک رنگ سفید قبلی .product-card (از افکت اورورا) رو به تیره‌ی مات تغییر می‌ده */
.product-card {{
  --bs-card-color: #fff;
  background: rgba(10, 10, 10, 0.5) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}}

.product-card .product-title-link,
.product-card .product-title,
.product-card .product-price {{
  color: #fff !important;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
}}
'''

with open(css_path, "a", encoding="utf-8") as f:
    f.write(extra_css)

print(f"✓ index.css append شد — بک‌آپ: {backup.name}")
print("\nقدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
