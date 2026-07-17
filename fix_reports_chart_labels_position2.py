#!/usr/bin/env python3
"""
اسکریپت پچ: تنظیم دقیق‌تر موقعیت نوشته‌های محور X و Y نمودار گزارش‌گیری
اجرا از ریشه پروژه: python3 fix_reports_chart_labels_position2.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-chartlabels2-backup"

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
# 1) محور X — کمی راست‌تر (dx مثبت) تا مماس با خط تیک بشه
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                        tick={{ fontSize: 10, dy: 12 }}",
    "                        tick={{ fontSize: 10, dy: 12, dx: 8 }}",
    "ReportsPage.jsx: نوشته‌های محور X راست‌تر (dx: 8) تا مماس با خط تیک",
)

# ─────────────────────────────────────────────────────────
# 2) محور Y — چپ‌تر (dx منفی‌تر) + عرض بیشتر برای جا شدن
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      <YAxis tick={{ fontSize: 10, dx: -8 }} tickFormatter={formatAxisNumber} width={50} />",
    "                      <YAxis tick={{ fontSize: 10, dx: -14 }} tickFormatter={formatAxisNumber} width={58} />",
    "ReportsPage.jsx: نوشته‌های محور Y چپ‌تر (dx: -14) + عرض بیشتر",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ تنظیم دقیق‌تر نوشته‌های محور نمودار")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("مرورگر رو رفرش کن و نمودار رو چک کن.")
