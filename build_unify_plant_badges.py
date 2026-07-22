#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_unify_plant_badges.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_unify_plant_badges.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_unify_plant_badges.py
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
page_path = ROOT / "frontend" / "src" / "pages" / "ProductPage.jsx"
css_path = ROOT / "frontend" / "src" / "index.css"

results = []


def report(label, ok, note):
    results.append((label, ok, note))


# ---------------------------------------------------------------------------
# 1. ProductPage.jsx — unify badges
# ---------------------------------------------------------------------------
if page_path.exists():
    content = page_path.read_text(encoding="utf-8")
    backup = page_path.with_suffix(page_path.suffix + ".pre-unifybadge-backup")

    replacements = [
        ("<Badge bg='info'>{product.lightNeeds}</Badge>",
         "<Badge className='aq-plant-badge'>{product.lightNeeds}</Badge>"),
        ("<Badge bg='secondary'>{co2Label(product.co2Needs)}</Badge>",
         "<Badge className='aq-plant-badge'>{co2Label(product.co2Needs)}</Badge>"),
        ("<Badge bg='success'>{product.growthRate}</Badge>",
         "<Badge className='aq-plant-badge'>{product.growthRate}</Badge>"),
        ("<Badge bg='primary'>{product.family}</Badge>",
         "<Badge className='aq-plant-badge'>{product.family}</Badge>"),
        ("<Badge bg='warning' text='dark'>{product.position}</Badge>",
         "<Badge className='aq-plant-badge'>{product.position}</Badge>"),
        ("<Badge bg='success'>{product.cultivationType}</Badge>",
         "<Badge className='aq-plant-badge'>{product.cultivationType}</Badge>"),
        ("<Badge bg={product.needsSoil ? 'warning' : 'secondary'} text='dark'>",
         "<Badge className='aq-plant-badge'>"),
        ("<Badge bg='light' text='dark'>{product.brand}</Badge>",
         "<Badge className='aq-plant-badge'>{product.brand}</Badge>"),
    ]

    all_ok = True
    for old, new in replacements:
        count = content.count(old)
        if count != 1:
            all_ok = False
            report("ProductPage.jsx", False, f"لنگر پیدا نشد یا تکراری بود (تعداد: {count}): {old[:60]}...")
            break

    if all_ok:
        shutil.copy2(page_path, backup)
        for old, new in replacements:
            content = content.replace(old, new)
        page_path.write_text(content, encoding="utf-8")
        report("ProductPage.jsx", True, f"{len(replacements)} بج یکدست شد — بک‌آپ: {backup.name}")
else:
    report("ProductPage.jsx", False, f"فایل پیدا نشد: {page_path}")

# ---------------------------------------------------------------------------
# 2. index.css — new unified badge style
# ---------------------------------------------------------------------------
if css_path.exists():
    content = css_path.read_text(encoding="utf-8")
    marker = "/* --- unified plant badges v1 --- */"
    if marker in content:
        report("index.css", False, "این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    else:
        backup = css_path.with_suffix(css_path.suffix + ".pre-unifybadge-css-backup")
        shutil.copy2(css_path, backup)
        extra_css = f'''

{marker}
.aq-plant-badge {{
  background: rgba(45, 106, 79, 0.12) !important;
  color: #2d6a4f !important;
  border: 1px solid rgba(45, 106, 79, 0.35);
  font-weight: 500;
}}
'''
        with open(css_path, "a", encoding="utf-8") as f:
            f.write(extra_css)
        report("index.css", True, f"استایل append شد — بک‌آپ: {backup.name}")
else:
    report("index.css", False, f"فایل پیدا نشد: {css_path}")

# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("گزارش نهایی:")
print("=" * 60)
ok_count = 0
for label, ok, note in results:
    mark = "✓" if ok else "✗"
    print(f"{mark} {label} — {note}")
    if ok:
        ok_count += 1
print("=" * 60)
if ok_count == len(results):
    print("همه‌چیز با موفقیت اعمال شد.")
    print("قدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
else:
    print(f"⚠️  {len(results) - ok_count} مورد ناموفق بود.")
    sys.exit(1)
