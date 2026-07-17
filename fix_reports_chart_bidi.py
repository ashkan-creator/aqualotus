#!/usr/bin/env python3
"""
اسکریپت پچ: رفع ریشه‌ای مشکل نمایش اعداد محور نمودار (باگ جهت‌دهی RTL/bidi)
اجرا از ریشه پروژه: python3 fix_reports_chart_bidi.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-chartbidi-backup"

results = []


def backup(path):
    if os.path.exists(path + BACKUP_SUFFIX):
        return
    shutil.copy2(path, path + BACKUP_SUFFIX)


def patch_file(rel_path, old, new, label):
    path = os.path.join(ROOT, rel_path)
    if not os.path.exists(path):
        results.append(("❌", f"{label} — فایل پیدا نشد: {rel_path}"))
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if old not in content:
        if new in content:
            results.append(("✓", f"{label} (قبلاً اعمال شده بود)"))
            return
        results.append(("❌", f"{label} — anchor پیدا نشد در {rel_path}"))
        return
    backup(path)
    content = content.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    results.append(("✓", label))


# ─────────────────────────────────────────────────────────
# 1) index.css — مجبور کردن تمام متن‌های نمودار (recharts) به جهت LTR
#    این ریشه اصلی به‌هم‌ریختگی اعداد محور Y بود
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/index.css",
    "/* ===== چاپ گزارش (PDF از طریق پرینت مرورگر) ===== */",
    """/* ===== رفع باگ جهت‌دهی RTL در متن نمودارها (recharts) ===== */
.recharts-wrapper text,
.recharts-cartesian-axis-tick text,
.recharts-text {
  direction: ltr;
  unicode-bidi: plaintext;
}
/* ===== چاپ گزارش (PDF از طریق پرینت مرورگر) ===== */""",
    "index.css: افزودن قانون direction:ltr برای متن‌های SVG نمودار (رفع باگ اصلی)",
)

# ─────────────────────────────────────────────────────────
# 2) ReportsPage.jsx — حذف dx/dy دستکاری‌شده قبلی (دیگه لازم نیست،
#    چون ریشه مشکل با CSS بالا حل شد) و برگردوندن به تنظیمات ساده و تمیز
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                        tick={{ fontSize: 10, dy: 12, dx: 8 }}",
    "                        tick={{ fontSize: 10, dy: 8 }}",
    "ReportsPage.jsx: ساده‌سازی تنظیمات محور X (حذف dx غیرلازم)",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      <YAxis tick={{ fontSize: 10, dx: -14 }} tickFormatter={formatAxisNumber} width={58} />",
    "                      <YAxis tick={{ fontSize: 10 }} tickFormatter={formatAxisNumber} width={48} />",
    "ReportsPage.jsx: ساده‌سازی تنظیمات محور Y (حذف dx غیرلازم)",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ رفع ریشه‌ای باگ اعداد محور نمودار")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("مرورگر رو رفرش کن (Ctrl+Shift+R) و نمودار رو دوباره چک کن.")
