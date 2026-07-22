#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_dark_glass_boxes.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_dark_glass_boxes.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_dark_glass_boxes.py

فقط index.css رو append می‌کنه (کلاس‌ها از قبل رو JSX هستن، چیزی عوض نمی‌شه اونجا).
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
marker = "/* --- product page dark glass v1 --- */"

if marker in content:
    print("✗ این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    sys.exit(1)

backup = css_path.with_suffix(css_path.suffix + ".pre-darkglass-backup")
shutil.copy2(css_path, backup)

extra_css = f'''

{marker}
.product-buy-card,
.aq-product-info-panel {{
  background: rgba(0, 0, 0, 0.55) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  color: #fff;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
}}

.product-buy-card .list-group-item,
.aq-product-info-panel .list-group-item {{
  background: transparent;
  border-color: rgba(255, 255, 255, 0.12);
}}

.aq-plant-badge {{
  background: rgba(116, 198, 157, 0.18) !important;
  color: #95d5b2 !important;
  border: 1px solid rgba(116, 198, 157, 0.45);
  text-shadow: none;
}}
'''

with open(css_path, "a", encoding="utf-8") as f:
    f.write(extra_css)

print(f"✓ index.css append شد — بک‌آپ: {backup.name}")
print("\nقدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
