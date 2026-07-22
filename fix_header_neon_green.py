#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_header_neon_green.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/fix_header_neon_green.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_header_neon_green.py

بلاک قبلی (v22، خاکستری) رو با یه بلاک جدید override می‌کنه — این‌بار
پس‌زمینه‌ی سبز تیره‌ی نئونی (هم‌خانواده با رنگ خودِ انیمیشن اورورا #00ff7f)
به‌جای خاکستری، به‌علاوه یه گلوی سبز نئونی کمرنگ پایین هدر.
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
marker = "/* --- header aurora color v23 (neon green) --- */"

if marker in content:
    print("✗ این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    sys.exit(1)

backup = css_path.with_suffix(css_path.suffix + ".pre-headerneongreen-backup")
shutil.copy2(css_path, backup)

extra_css = f'''

{marker}
.aqualotus-navbar {{
  background: linear-gradient(135deg, rgba(0, 40, 20, 0.85) 0%, rgba(0, 80, 40, 0.7) 100%) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 2px 20px rgba(0, 255, 127, 0.25);
  border-bottom: 1px solid rgba(0, 255, 127, 0.35);
}}
'''

with open(css_path, "a", encoding="utf-8") as f:
    f.write(extra_css)

print(f"✓ index.css append شد — بک‌آپ: {backup.name}")
print("\nقدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
