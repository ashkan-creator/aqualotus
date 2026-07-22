#!/usr/bin/env python3
"""
Patch: add the animated aurora beam effect behind the header navbar
- Reuses the existing AuroraGridBackground component (no duplication)
- Wraps it in a new .aq-header-aurora-wrapper scoped to the header's height
- Hides the floor-grid + main-column pieces for this wrapper only (they're
  designed for a full-height page section, not a ~65px navbar) and keeps
  only the rising beams, sized to 100% of the header's height
- Backs up every file before touching it, reports ✓/✗ per file
"""
import shutil
import sys
from pathlib import Path

FILES = {
    "header": Path("components/layout/Header.jsx"),
    "css": Path("index.css"),
}

CSS_MARKER = "/* --- header-aurora-beams v1 --- */"

CSS_BLOCK = f"""

{CSS_MARKER}
.aq-header-aurora-wrapper {{
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}}
.aq-header-aurora-wrapper .aq-aurora-floor,
.aq-header-aurora-wrapper .aq-aurora-main-column {{
  display: none;
}}
.aq-header-aurora-wrapper .aq-aurora-beam {{
  height: 100%;
}}
"""

results = []


def backup(path: Path):
    bak = path.with_suffix(path.suffix + ".pre-headeraurora-backup")
    shutil.copy2(path, bak)
    return bak


def patch_header():
    p = FILES["header"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")

    old_import = "import AnnouncementBar from '../ui/AnnouncementBar'"
    new_import = "import AnnouncementBar from '../ui/AnnouncementBar'\nimport AuroraGridBackground from '../ui/AuroraGridBackground'"

    old_jsx = (
        "  return (\n"
        "    <header className='aq-sticky-header' style={{ zIndex: 1050, position: 'relative' }}>\n"
        "      <Navbar className='aqualotus-navbar py-1' style={{ direction: 'rtl', minHeight: '65px' }}>"
    )
    new_jsx = (
        "  return (\n"
        "    <header className='aq-sticky-header' style={{ zIndex: 1050, position: 'relative' }}>\n"
        "      <div className='aq-header-aurora-wrapper' aria-hidden='true'>\n"
        "        <AuroraGridBackground beamCount={20} />\n"
        "      </div>\n"
        "      <Navbar className='aqualotus-navbar py-1' style={{ direction: 'rtl', minHeight: '65px', position: 'relative', zIndex: 1 }}>"
    )

    if content.count(old_import) != 1:
        results.append((str(p), False, f"لنگر ایمپورت یافت‌شده: {content.count(old_import)} بار"))
        return
    if content.count(old_jsx) != 1:
        results.append((str(p), False, f"لنگر JSX یافت‌شده: {content.count(old_jsx)} بار"))
        return

    backup(p)
    content = content.replace(old_import, new_import)
    content = content.replace(old_jsx, new_jsx)
    p.write_text(content, encoding="utf-8")
    results.append((str(p), True, "ایمپورت + wrapper اورورا به هدر اضافه شد"))


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
    patch_header()
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
        print("  اگه بازم خطا/فلش دیدی، کنسول مرورگر (F12) رو باز بذار و متن دقیق خطا رو برام بفرست")
    else:
        print("\n✗ حداقل یکی از پچ‌ها اعمال نشد")
        sys.exit(1)


if __name__ == "__main__":
    main()
