#!/usr/bin/env python3
"""
Patch: extend dark-matte-glass style to FilterSidebar
- Appends a new versioned CSS marker block to index.css (does NOT touch old blocks)
- Backs up index.css before touching it
"""
import shutil
import sys
from pathlib import Path

CSS_FILE = Path("index.css")
MARKER = "/* --- filter-sidebar-dark-glass v1 --- */"

NEW_CSS = f"""

{MARKER}
.aq-filter-card {{
  background: rgba(10, 10, 10, 0.5) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  --bs-card-color: #fff;
  color: #fff !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
}}
.aq-filter-header {{
  border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
}}
.aq-filter-header h6 {{
  color: #fff !important;
}}
.aq-filter-title-badge {{
  background: rgba(255, 255, 255, 0.1) !important;
}}
.aq-filter-clear-all {{
  color: #ff8080 !important;
}}

/* price box */
.aq-price-box {{
  background: rgba(255, 255, 255, 0.06) !important;
}}
.aq-price-box .text-muted {{
  color: rgba(255, 255, 255, 0.65) !important;
}}

/* pills (inactive state only — active/green pill untouched) */
.aq-filter-pill {{
  background: rgba(255, 255, 255, 0.06) !important;
  color: #fff !important;
  border: 1px solid rgba(255, 255, 255, 0.18) !important;
}}
.aq-filter-pill:hover {{
  background: rgba(255, 255, 255, 0.14) !important;
}}
.aq-filter-pill.active {{
  background: var(--primary, #2d6a4f) !important;
  color: #fff !important;
  border-color: var(--primary, #2d6a4f) !important;
}}

/* accordion items */
.aq-filter-accordion-item {{
  background: transparent !important;
}}
.aq-filter-accordion-item .accordion-button {{
  background: rgba(255, 255, 255, 0.06) !important;
  color: #fff !important;
}}
.aq-filter-accordion-item .accordion-button:not(.collapsed) {{
  background: rgba(255, 255, 255, 0.12) !important;
  color: #fff !important;
}}
.aq-filter-accordion-item .accordion-button::after {{
  filter: invert(1) grayscale(1) brightness(2);
}}
.aq-filter-accordion-item .accordion-body {{
  background: transparent !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-top: none !important;
  color: #fff !important;
}}

/* chips (active filter tags above accordion) unchanged — already green/white, reads fine on dark */
"""

def main():
    if not CSS_FILE.exists():
        print(f"✗ {CSS_FILE} پیدا نشد — این اسکریپت رو باید تو frontend/src اجرا کنی")
        sys.exit(1)

    content = CSS_FILE.read_text(encoding="utf-8")

    if MARKER in content:
        print(f"✗ مارکر {MARKER} از قبل تو فایل هست — اسکریپت قبلاً اجرا شده، برای جلوگیری از تکرار متوقف شد")
        sys.exit(1)

    backup_path = CSS_FILE.with_suffix(CSS_FILE.suffix + ".pre-filterdark-backup")
    shutil.copy2(CSS_FILE, backup_path)
    print(f"✓ بک‌آپ گرفته شد: {backup_path}")

    CSS_FILE.write_text(content + NEW_CSS, encoding="utf-8")
    print(f"✓ بلاک جدید CSS به انتهای {CSS_FILE} اضافه شد")
    print("✓ تمام — حالا سرور Vite رو کامل ری‌استارت کن (Ctrl+C و npm run dev) و تو Incognito تست کن")

if __name__ == "__main__":
    main()
