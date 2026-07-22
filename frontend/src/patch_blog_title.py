#!/usr/bin/env python3
"""
Patch: fix white-text on BlogPage's "وبلاگ" heading
- Reuses the .aq-page-title CSS class already added to index.css by
  patch_contact_titles.py — no new CSS needed here.
- If .aq-page-title is somehow missing from index.css (e.g. this script
  is run standalone, out of order), it adds a minimal fallback rule.
"""
import shutil
import sys
from pathlib import Path

FILES = {
    "bloglist": Path("pages/BlogPage.jsx"),
    "css": Path("index.css"),
}

FALLBACK_MARKER = "/* --- blogpage-title-fallback v1 --- */"
FALLBACK_CSS = f"""

{FALLBACK_MARKER}
.aq-page-title {{
  color: #fff !important;
}}
"""

results = []


def backup(path: Path):
    bak = path.with_suffix(path.suffix + ".pre-blogtitle-backup")
    shutil.copy2(path, bak)
    return bak


def patch_bloglist_title():
    p = FILES["bloglist"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")
    old = "<h2 className='mb-4'>وبلاگ</h2>"
    new = "<h2 className='mb-4 aq-page-title'>وبلاگ</h2>"
    if content.count(old) != 1:
        results.append((str(p), False, f"لنگر یافت‌شده: {content.count(old)} بار (باید ۱ بار باشه)"))
        return
    backup(p)
    p.write_text(content.replace(old, new), encoding="utf-8")
    results.append((str(p), True, "کلاس aq-page-title به تیتر «وبلاگ» اضافه شد"))


def ensure_css_fallback():
    p = FILES["css"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")
    if ".aq-page-title" in content:
        results.append((str(p), True, "کلاس aq-page-title از قبل تو CSS هست — چیزی اضافه نشد"))
        return
    if FALLBACK_MARKER in content:
        results.append((str(p), False, "مارکر فال‌بک از قبل هست"))
        return
    backup(p)
    p.write_text(content + FALLBACK_CSS, encoding="utf-8")
    results.append((str(p), True, "کلاس aq-page-title تو CSS پیدا نشد — یه نسخه‌ی فال‌بک اضافه شد"))


def main():
    patch_bloglist_title()
    ensure_css_fallback()

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
        print("\n✗ حداقل یکی از پچ‌ها اعمال نشد")
        sys.exit(1)


if __name__ == "__main__":
    main()
