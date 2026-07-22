#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_header_dark_glass.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_header_dark_glass.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_header_dark_glass.py

فقط index.css رو append می‌کنه (طبق الگوی همیشگی پروژه — بلاک نسخه‌دار جدید،
بدون دست‌زدن به بلاک‌های قدیمی .aqualotus-navbar).
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
marker = "/* --- header aurora color v22 --- */"

if marker in content:
    print("✗ این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    sys.exit(1)

backup = css_path.with_suffix(css_path.suffix + ".pre-headerauroracolor-backup")
shutil.copy2(css_path, backup)

extra_css = f'''

{marker}
.aqualotus-navbar {{
  background: rgba(10, 10, 10, 0.5) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}}
'''

with open(css_path, "a", encoding="utf-8") as f:
    f.write(extra_css)

print(f"✓ index.css append شد — بک‌آپ: {backup.name}")
print("\nقدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
