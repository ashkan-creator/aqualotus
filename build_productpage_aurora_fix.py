#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_productpage_aurora_fix.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_productpage_aurora_fix.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_productpage_aurora_fix.py

کارها:
  1. frontend/src/pages/ProductPage.jsx:
     - ListGroup وسط (توضیحات/مشخصات) تو یه <div className='aq-product-info-panel'> پیچیده می‌شه
     - عنوان «نظرات کاربران» کلاس aq-reviews-heading می‌گیره
  2. frontend/src/index.css:
     - .product-buy-card شیشه‌ای می‌شه (backdrop-blur)
     - .aq-product-info-panel جدید اضافه می‌شه (همون افکت شیشه‌ای)
     - .aq-reviews-heading رنگ روشن می‌گیره
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
FRONTEND = ROOT / "frontend" / "src"

results = []


def report(label, ok, note):
    results.append((label, ok, note))


# ---------------------------------------------------------------------------
# 1. ProductPage.jsx
# ---------------------------------------------------------------------------
page_path = FRONTEND / "pages" / "ProductPage.jsx"

if page_path.exists():
    content = page_path.read_text(encoding="utf-8")
    backup = page_path.with_suffix(page_path.suffix + ".pre-aurorafix-backup")

    old_listgroup_open = "              <Col md={4}>\n                <ListGroup variant='flush'>"
    new_listgroup_open = "              <Col md={4}>\n                <div className='aq-product-info-panel'>\n                <ListGroup variant='flush'>"

    old_listgroup_close = "                </ListGroup>\n              </Col>\n\n              <Col md={3}>"
    new_listgroup_close = "                </ListGroup>\n                </div>\n              </Col>\n\n              <Col md={3}>"

    old_heading = "                <h4 className='mb-3'>نظرات کاربران</h4>"
    new_heading = "                <h4 className='mb-3 aq-reviews-heading'>نظرات کاربران</h4>"

    checks = {
        "listgroup_open": content.count(old_listgroup_open),
        "listgroup_close": content.count(old_listgroup_close),
        "heading": content.count(old_heading),
    }

    if all(v == 1 for v in checks.values()):
        shutil.copy2(page_path, backup)
        content = content.replace(old_listgroup_open, new_listgroup_open)
        content = content.replace(old_listgroup_close, new_listgroup_close)
        content = content.replace(old_heading, new_heading)
        page_path.write_text(content, encoding="utf-8")
        report("ProductPage.jsx", True, f"پچ شد — بک‌آپ: {backup.name}")
    else:
        report("ProductPage.jsx", False, f"لنگر(ها) پیدا نشد یا تکراری بود — {checks} — هیچ تغییری اعمال نشد")
else:
    report("ProductPage.jsx", False, f"فایل پیدا نشد: {page_path}")

# ---------------------------------------------------------------------------
# 2. index.css
# ---------------------------------------------------------------------------
index_css_path = FRONTEND / "index.css"

if index_css_path.exists():
    content = index_css_path.read_text(encoding="utf-8")

    if "/* --- product page aurora fix v1 --- */" in content:
        report("index.css", False, "این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    else:
        old_buy_card = (
            ".product-buy-card {\n"
            "  border: none;\n"
            "  border-radius: 16px;\n"
            "  box-shadow: var(--card-shadow);\n"
            "  position: sticky;\n"
            "  top: 20px;\n"
            "}"
        )
        new_buy_card = (
            ".product-buy-card {\n"
            "  border: none;\n"
            "  border-radius: 16px;\n"
            "  box-shadow: var(--card-shadow);\n"
            "  position: sticky;\n"
            "  top: 20px;\n"
            "  background: rgba(255, 255, 255, 0.85);\n"
            "  backdrop-filter: blur(10px);\n"
            "  -webkit-backdrop-filter: blur(10px);\n"
            "}"
        )

        if content.count(old_buy_card) == 1:
            backup = index_css_path.with_suffix(index_css_path.suffix + ".pre-aurorafix-css-backup")
            shutil.copy2(index_css_path, backup)
            content = content.replace(old_buy_card, new_buy_card)

            extra_css = '''

/* --- product page aurora fix v1 --- */
.aq-product-info-panel {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: var(--card-shadow);
  overflow: hidden;
}

.aq-product-info-panel .list-group-item {
  background: transparent;
  border-color: rgba(0, 0, 0, 0.08);
}

.aq-reviews-heading {
  color: #fff;
}
'''
            content += extra_css
            index_css_path.write_text(content, encoding="utf-8")
            report("index.css", True, f"پچ شد + استایل جدید append شد — بک‌آپ: {backup.name}")
        else:
            report("index.css", False, f"لنگر .product-buy-card پیدا نشد یا تکراریه (تعداد: {content.count(old_buy_card)}) — هیچ تغییری اعمال نشد")
else:
    report("index.css", False, f"فایل پیدا نشد: {index_css_path}")

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
    print("قدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito یه صفحه‌ی محصول رو چک کن.")
else:
    print(f"⚠️  {len(results) - ok_count} مورد ناموفق بود.")
    sys.exit(1)
