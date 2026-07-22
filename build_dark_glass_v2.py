#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_dark_glass_v2.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_dark_glass_v2.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_dark_glass_v2.py

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
marker = "/* --- product page dark glass v2 --- */"

if marker in content:
    print("✗ این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    sys.exit(1)

backup = css_path.with_suffix(css_path.suffix + ".pre-darkglass-v2-backup")
shutil.copy2(css_path, backup)

extra_css = f'''

{marker}
/* این بلاک رو بلاک قبلی (v1) رو override می‌کنه — مات‌تر و متن سفید قطعی‌تر */
.product-buy-card,
.aq-product-info-panel {{
  --bs-card-color: #fff;
  --bs-list-group-color: #fff;
  background: rgba(10, 10, 10, 0.82) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  color: #fff !important;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
}}

.product-buy-card .list-group-item,
.aq-product-info-panel .list-group-item,
.product-buy-card h3,
.product-buy-card strong,
.product-buy-card p,
.aq-product-info-panel h3,
.aq-product-info-panel strong,
.aq-product-info-panel p {{
  background: transparent;
  color: #fff !important;
  border-color: rgba(255, 255, 255, 0.12);
}}
'''

with open(css_path, "a", encoding="utf-8") as f:
    f.write(extra_css)

print(f"✓ index.css append شد — بک‌آپ: {backup.name}")
print("\nقدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
