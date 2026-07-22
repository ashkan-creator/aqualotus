#!/usr/bin/env python3
"""
Patch: extend dark-matte-glass style to About page + Blog list + Blog post
- Wraps AboutPage's text in a new .aq-about-card div
- Adds .aq-blog-card class to the existing Bootstrap Card in BlogPage
- Wraps BlogPostPage's content in a new .aq-blogpost-card div
- Appends a new versioned CSS marker block to index.css (does NOT touch old blocks)
- Backs up every file before touching it, reports ✓/✗ per file
"""
import shutil
import sys
from pathlib import Path

FILES = {
    "about": Path("pages/AboutPage.jsx"),
    "bloglist": Path("pages/BlogPage.jsx"),
    "blogpost": Path("pages/BlogPostPage.jsx"),
    "css": Path("index.css"),
}

CSS_MARKER = "/* --- about-blog-dark-glass v1 --- */"

CSS_BLOCK = f"""

{CSS_MARKER}
.aq-about-card {{
  background: rgba(10, 10, 10, 0.5) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 28px 24px;
  color: #fff !important;
}}

.aq-blog-card {{
  background: rgba(10, 10, 10, 0.5) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  --bs-card-color: #fff;
  color: #fff !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
}}
.aq-blog-card .text-muted {{
  color: rgba(255, 255, 255, 0.65) !important;
}}

.aq-blogpost-card {{
  background: rgba(10, 10, 10, 0.5) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 28px 24px;
  color: #fff !important;
}}
.aq-blogpost-card .text-muted {{
  color: rgba(255, 255, 255, 0.65) !important;
}}
"""

results = []


def backup(path: Path):
    bak = path.with_suffix(path.suffix + ".pre-aboutblogdark-backup")
    shutil.copy2(path, bak)
    return bak


def patch_about():
    p = FILES["about"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")
    old = "        <Col md={8}>\n          <p>{settings?.about_text || 'آکوالوتوس یک فروشگاه تخصصی گیاهان آکواریوم است.'}</p>\n        </Col>"
    new = "        <Col md={8}>\n          <div className='aq-about-card'>\n            <p className='mb-0'>{settings?.about_text || 'آکوالوتوس یک فروشگاه تخصصی گیاهان آکواریوم است.'}</p>\n          </div>\n        </Col>"
    if old not in content:
        results.append((str(p), False, "لنگر پیدا نشد — فایل واقعی با نسخه‌ی دیده‌شده فرق داره"))
        return
    if content.count(old) > 1:
        results.append((str(p), False, "لنگر بیش از یک‌بار تکرار شده"))
        return
    backup(p)
    p.write_text(content.replace(old, new), encoding="utf-8")
    results.append((str(p), True, "باکس دور متن اضافه شد"))


def patch_bloglist():
    p = FILES["bloglist"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")
    old = "<Card className='h-100' style={{ borderRadius: '12px', overflow: 'hidden' }}>"
    new = "<Card className='h-100 aq-blog-card' style={{ borderRadius: '12px', overflow: 'hidden' }}>"
    if content.count(old) != 1:
        results.append((str(p), False, f"لنگر یافت‌شده: {content.count(old)} بار (باید دقیقاً ۱ بار باشه)"))
        return
    backup(p)
    p.write_text(content.replace(old, new), encoding="utf-8")
    results.append((str(p), True, "کلاس aq-blog-card به کارت‌های پست اضافه شد"))


def patch_blogpost():
    p = FILES["blogpost"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد"))
        return
    content = p.read_text(encoding="utf-8")

    open_old = "            </Helmet>\n\n            <h2 style={{ fontSize: 'clamp(1.2rem, 4vw, 1.8rem)', marginBottom: '0.5rem' }}>"
    open_new = "            </Helmet>\n\n            <div className='aq-blogpost-card'>\n            <h2 style={{ fontSize: 'clamp(1.2rem, 4vw, 1.8rem)', marginBottom: '0.5rem' }}>"

    close_old = "              </div>\n            )}\n          </Col>\n        </Row>"
    close_new = "              </div>\n            )}\n            </div>\n          </Col>\n        </Row>"

    if content.count(open_old) != 1:
        results.append((str(p), False, f"لنگر شروع یافت‌شده: {content.count(open_old)} بار"))
        return
    if content.count(close_old) != 1:
        results.append((str(p), False, f"لنگر پایان یافت‌شده: {content.count(close_old)} بار"))
        return

    backup(p)
    content = content.replace(open_old, open_new)
    content = content.replace(close_old, close_new)
    p.write_text(content, encoding="utf-8")
    results.append((str(p), True, "محتوای پست تو باکس aq-blogpost-card پیچیده شد"))


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
    patch_about()
    patch_bloglist()
    patch_blogpost()
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
