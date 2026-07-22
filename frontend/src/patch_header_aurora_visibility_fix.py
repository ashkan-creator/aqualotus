#!/usr/bin/env python3
"""
Corrective patch (v2) for the header aurora effect:
- Moves the .aq-header-aurora-wrapper from being a sibling BEFORE Navbar
  (inside the outer header padding area) to being the first child INSIDE
  Navbar — so the beams render within the navbar's own box, not just its
  outer margin.
- Adds position/z-index to Container so its content stacks above the beams.
- Does NOT add overflow:hidden to Navbar itself (that would clip the open
  user dropdown menu, which extends beyond the navbar's own height) — only
  the small wrapper div gets overflow:hidden, so beams are contained but
  the dropdown is untouched.
- Lowers the navbar's background gradient opacity (0.85/0.7 -> 0.55/0.4) by
  appending a later same-specificity !important rule, so the beams are
  actually visible through the navbar's own background, not just around it.
- Backs up every file before touching it, reports ✓/✗ per file
"""
import shutil
import sys
from pathlib import Path

FILES = {
    "header": Path("components/layout/Header.jsx"),
    "css": Path("index.css"),
}

CSS_MARKER = "/* --- header-aurora-visibility-fix v1 --- */"

CSS_BLOCK = f"""

{CSS_MARKER}
.aq-header-aurora-wrapper {{
  border-radius: inherit;
}}
.aqualotus-navbar {{
  background: linear-gradient(135deg, rgba(0, 40, 20, 0.55) 0%, rgba(0, 80, 40, 0.4) 100%) !important;
}}
"""

results = []


def backup(path: Path):
    bak = path.with_suffix(path.suffix + ".pre-headerauravis-backup")
    shutil.copy2(path, bak)
    return bak


def patch_header():
    p = FILES["header"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")

    old = (
        "      <div className='aq-header-aurora-wrapper' aria-hidden='true'>\n"
        "        <AuroraGridBackground beamCount={20} />\n"
        "      </div>\n"
        "      <Navbar className='aqualotus-navbar py-1' style={{ direction: 'rtl', minHeight: '65px', position: 'relative', zIndex: 1 }}>\n"
        "        <Container fluid='md'>"
    )
    new = (
        "      <Navbar className='aqualotus-navbar py-1' style={{ direction: 'rtl', minHeight: '65px', position: 'relative', zIndex: 1 }}>\n"
        "        <div className='aq-header-aurora-wrapper' aria-hidden='true'>\n"
        "          <AuroraGridBackground beamCount={20} />\n"
        "        </div>\n"
        "        <Container fluid='md' style={{ position: 'relative', zIndex: 1 }}>"
    )

    if content.count(old) != 1:
        results.append((str(p), False, f"لنگر یافت‌شده: {content.count(old)} بار (باید ۱ بار باشه) — احتمالاً patch_header_aurora.py هنوز اجرا نشده یا فایل فرق داره"))
        return

    backup(p)
    p.write_text(content.replace(old, new), encoding="utf-8")
    results.append((str(p), True, "wrapper اورورا از بیرون هدر به داخل خود Navbar منتقل شد"))


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
    results.append((str(p), True, "پس‌زمینه‌ی نوار نیمه‌شفاف‌تر شد + گوشه‌های لایه‌ی پرتوها هماهنگ شد"))


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
        print("  همزمان با تست، منوی کاربر (آیکون یوزر بالا سمت چپ) رو هم باز کن تا مطمئن شی هنوز درست کار می‌کنه")
    else:
        print("\n✗ حداقل یکی از پچ‌ها اعمال نشد")
        sys.exit(1)


if __name__ == "__main__":
    main()
