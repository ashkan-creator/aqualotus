#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tweak_glass_opacity.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/tweak_glass_opacity.py ~/aqualotus/
    cd ~/aqualotus
    python3 tweak_glass_opacity.py
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
old = "background: rgba(10, 10, 10, 0.82) !important;"
new = "background: rgba(10, 10, 10, 0.68) !important;"

count = content.count(old)
if count != 1:
    print(f"✗ لنگر پیدا نشد یا تکراری بود (تعداد: {count}) — هیچ تغییری اعمال نشد")
    sys.exit(1)

backup = css_path.with_suffix(css_path.suffix + ".pre-opacitytweak-backup")
shutil.copy2(css_path, backup)
content = content.replace(old, new)
css_path.write_text(content, encoding="utf-8")

print(f"✓ شفافیت کم شد (0.82 -> 0.68) — بک‌آپ: {backup.name}")
print("\nقدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
