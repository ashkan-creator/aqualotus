#!/usr/bin/env python3
"""
اسکریپت پچ: جابجایی نوشته‌های محور X و Y نمودار گزارش‌گیری (پایین‌تر و چپ‌تر)
اجرا از ریشه پروژه: python3 fix_reports_chart_labels_position.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-chartlabels-backup"

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
# 1) محور X — نوشته‌ها پایین‌تر (dy بیشتر) + مارجین بیشتر
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      <XAxis\n"
    "                        dataKey='label'\n"
    "                        tick={{ fontSize: 10 }}\n"
    "                        interval={chartTickInterval}\n"
    "                        angle={-35}\n"
    "                        textAnchor='end'\n"
    "                        height={50}\n"
    "                      />",
    "                      <XAxis\n"
    "                        dataKey='label'\n"
    "                        tick={{ fontSize: 10, dy: 12 }}\n"
    "                        interval={chartTickInterval}\n"
    "                        angle={-35}\n"
    "                        textAnchor='end'\n"
    "                        height={60}\n"
    "                      />",
    "ReportsPage.jsx: نوشته‌های محور X پایین‌تر (dy: 12) + ارتفاع بیشتر",
)

# ─────────────────────────────────────────────────────────
# 2) محور Y — نوشته‌ها چپ‌تر (dx منفی) + عرض بیشتر
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      <YAxis tick={{ fontSize: 10 }} tickFormatter={formatAxisNumber} width={42} />",
    "                      <YAxis tick={{ fontSize: 10, dx: -8 }} tickFormatter={formatAxisNumber} width={50} />",
    "ReportsPage.jsx: نوشته‌های محور Y چپ‌تر (dx: -8) + عرض بیشتر",
)

# ─────────────────────────────────────────────────────────
# 3) هماهنگی مارجین پایین کانتینر با ارتفاع جدید محور X
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                  <ResponsiveContainer width='100%' height={270}>\n"
    "                    <AreaChart data={chartData} margin={{ top: 5, right: 5, left: 0, bottom: 30 }}>",
    "                  <ResponsiveContainer width='100%' height={280}>\n"
    "                    <AreaChart data={chartData} margin={{ top: 5, right: 5, left: 5, bottom: 15 }}>",
    "ReportsPage.jsx: هماهنگی مارجین کانتینر با موقعیت جدید نوشته‌ها",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ جابجایی نوشته‌های محور نمودار")
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
