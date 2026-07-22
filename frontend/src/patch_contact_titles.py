#!/usr/bin/env python3
"""
Patch: fix white-text on page titles + extend dark-matte-glass to ContactPage
- AboutPage.jsx: add .aq-page-title class to the "درباره ما" heading (was outside the glass box)
- ContactPage.jsx: add .aq-page-title class to the "تماس با ما" heading,
  and .aq-contact-card class to the existing Bootstrap Card wrapping contact info
- Appends a new versioned CSS marker block to index.css (does NOT touch old blocks)
- Backs up every file before touching it, reports ✓/✗ per file
"""
import shutil
import sys
from pathlib import Path

FILES = {
    "about": Path("pages/AboutPage.jsx"),
    "contact": Path("pages/ContactPage.jsx"),
    "css": Path("index.css"),
}

CSS_MARKER = "/* --- contact-and-titles-dark-glass v1 --- */"

CSS_BLOCK = f"""

{CSS_MARKER}
.aq-page-title {{
  color: #fff !important;
}}

.aq-contact-card {{
  background: rgba(10, 10, 10, 0.5) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  --bs-card-color: #fff;
  color: #fff !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
}}
"""

results = []


def backup(path: Path):
    bak = path.with_suffix(path.suffix + ".pre-contacttitles-backup")
    shutil.copy2(path, bak)
    return bak


def patch_about_title():
    p = FILES["about"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")
    old = "<h2 className='mb-4 text-center'>درباره ما</h2>"
    new = "<h2 className='mb-4 text-center aq-page-title'>درباره ما</h2>"
    if content.count(old) != 1:
        results.append((str(p), False, f"لنگر یافت‌شده: {content.count(old)} بار (باید ۱ بار باشه)"))
        return
    backup(p)
    p.write_text(content.replace(old, new), encoding="utf-8")
    results.append((str(p), True, "کلاس aq-page-title به تیتر اضافه شد"))


def patch_contact():
    p = FILES["contact"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")

    old_title = "<h2 className='mb-4 text-center'>تماس با ما</h2>"
    new_title = "<h2 className='mb-4 text-center aq-page-title'>تماس با ما</h2>"

    old_card = "<Card className='p-4'>"
    new_card = "<Card className='p-4 aq-contact-card'>"

    if content.count(old_title) != 1:
        results.append((str(p), False, f"لنگر تیتر یافت‌شده: {content.count(old_title)} بار"))
        return
    if content.count(old_card) != 1:
        results.append((str(p), False, f"لنگر کارت یافت‌شده: {content.count(old_card)} بار"))
        return

    backup(p)
    content = content.replace(old_title, new_title)
    content = content.replace(old_card, new_card)
    p.write_text(content, encoding="utf-8")
    results.append((str(p), True, "تیتر سفید شد + کلاس aq-contact-card به کارت اضافه شد"))


def patch_css():
    p = FILES["css"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")
    if CSS_MARKER in content:
        results.append((str(p), False, "مارکر از قبل هست — اسکریپت قبلاً اجرا شده"))
        return
    backup(p)
    p.write_text(content + CSS_BLOCK, encoding="utf-8")
    results.append((str(p), True, "بلاک CSS جدید اضافه شد"))


def main():
    patch_about_title()
    patch_contact()
    patch_css()

    print("\n=== گزارش نهایی ===")
    all_ok = True
    for path, ok, msg in results:
        mark = "✓" if ok else "✗"
        print(f"{mark} {path} — {msg}")
        if not ok:
            all_ok = False

    if all_ok:
        print("\n✓ همه چیز موفق — سرور Vite رو کامل ری‌استارت کن و تو Incognito تست کن")
    else:
        print("\n✗ حداقل یکی از پچ‌ها اعمال نشد — فایل‌های موفق قبلی همچنان اعمال شدن، بک‌آپ‌ها رو چک کن")
        sys.exit(1)


if __name__ == "__main__":
    main()
