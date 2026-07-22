#!/usr/bin/env python3
"""
Patch: darken/thicken the navbar gradient a bit (Ashkan found 0.55/0.4 too
light). Appends a new, later same-specificity !important rule with
0.68/0.52 alpha — a middle ground between the original opaque 0.85/0.7 and
the too-transparent 0.55/0.4 — so the beams stay visible but the green
color reads stronger.
Backs up index.css before touching it.
"""
import shutil
import sys
from pathlib import Path

CSS_FILE = Path("index.css")
MARKER = "/* --- header-navbar-opacity-tune v1 --- */"

NEW_CSS = f"""

{MARKER}
.aqualotus-navbar {{
  background: linear-gradient(135deg, rgba(0, 40, 20, 0.68) 0%, rgba(0, 80, 40, 0.52) 100%) !important;
}}
"""


def main():
    if not CSS_FILE.exists():
        print(f"✗ {CSS_FILE} پیدا نشد — این اسکریپت رو باید تو frontend/src اجرا کنی")
        sys.exit(1)

    content = CSS_FILE.read_text(encoding="utf-8")

    if MARKER in content:
        print(f"✗ مارکر {MARKER} از قبل تو فایل هست — اسکریپت قبلاً اجرا شده")
        sys.exit(1)

    backup_path = CSS_FILE.with_suffix(CSS_FILE.suffix + ".pre-navbaropacity-backup")
    shutil.copy2(CSS_FILE, backup_path)
    print(f"✓ بک‌آپ گرفته شد: {backup_path}")

    CSS_FILE.write_text(content + NEW_CSS, encoding="utf-8")
    print(f"✓ آلفای گرادیانت نوار از ۰.۵۵/۰.۴ به ۰.۶۸/۰.۵۲ افزایش پیدا کرد")
    print("✓ تمام — سرور Vite رو کامل ری‌استارت کن و تو Incognito تست کن")
    print("  اگه بازم کم/زیاده، بگو چقدر — این عدد رو دقیق‌تر می‌کنم")


if __name__ == "__main__":
    main()
