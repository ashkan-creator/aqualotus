#!/usr/bin/env python3
"""
Patch: extend dark-matte-glass style to QuizPage (last page on the list)
- Adds 'aq-quiz-page' to the outer Container (scopes the .text-muted override)
- Adds 'aq-quiz-card' to the question Card
- Reuses the existing .aq-page-title class (from patch_contact_titles.py) on
  the "گیاه‌های پیشنهادی برات" results heading
- Appends a new versioned CSS marker block to index.css (does NOT touch old blocks)
- Backs up every file before touching it, reports ✓/✗ per file
"""
import shutil
import sys
from pathlib import Path

FILES = {
    "quiz": Path("pages/QuizPage.jsx"),
    "css": Path("index.css"),
}

CSS_MARKER = "/* --- quiz-dark-glass v1 --- */"

CSS_BLOCK = f"""

{CSS_MARKER}
.aq-quiz-page .text-muted {{
  color: rgba(255, 255, 255, 0.65) !important;
}}

.aq-quiz-card {{
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
    bak = path.with_suffix(path.suffix + ".pre-quizdark-backup")
    shutil.copy2(path, bak)
    return bak


def patch_quiz():
    p = FILES["quiz"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")

    old_container = "<Container className='py-4'>"
    new_container = "<Container className='py-4 aq-quiz-page'>"

    old_card = "<Card className='text-center p-4 border-0 shadow-sm rounded-4'>"
    new_card = "<Card className='text-center p-4 border-0 shadow-sm rounded-4 aq-quiz-card'>"

    old_h3 = "<h3 className='text-center mb-4'>گیاه‌های پیشنهادی برات 🌿</h3>"
    new_h3 = "<h3 className='text-center mb-4 aq-page-title'>گیاه‌های پیشنهادی برات 🌿</h3>"

    checks = [
        ("کانتینر", old_container),
        ("کارت سوال", old_card),
        ("تیتر نتایج", old_h3),
    ]
    for label, anchor in checks:
        if content.count(anchor) != 1:
            results.append((str(p), False, f"لنگر «{label}» یافت‌شده: {content.count(anchor)} بار (باید ۱ بار باشه)"))
            return

    backup(p)
    content = content.replace(old_container, new_container)
    content = content.replace(old_card, new_card)
    content = content.replace(old_h3, new_h3)
    p.write_text(content, encoding="utf-8")
    results.append((str(p), True, "کانتینر، کارت سوال، و تیتر نتایج پچ شدن"))


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
    patch_quiz()
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
        print("\n✗ حداقل یکی از پچ‌ها اعمال نشد")
        sys.exit(1)


if __name__ == "__main__":
    main()
