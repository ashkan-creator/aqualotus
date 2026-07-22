#!/usr/bin/env python3
"""
اسکریپت پچ: وسط‌چین کردن ستون‌های عددی جدول‌های پرفروش‌ترین/پرخریدترین
اجرا از ریشه پروژه: python3 center_reports_columns.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-centercols-backup"

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
# 1) جدول پرفروش‌ترین محصولات — هدر و سلول‌های عددی وسط‌چین
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                        <th>محصول</th>\n"
    "                        <th>تعداد فروش</th>\n"
    "                        <th>درآمد</th>",
    "                        <th>محصول</th>\n"
    "                        <th className='text-center'>تعداد فروش</th>\n"
    "                        <th className='text-center'>درآمد</th>",
    "ReportsPage.jsx: وسط‌چین هدر جدول محصولات",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                              <td>{p.name || '-'}</td>\n"
    "                              <td>{(p.totalQty ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                              <td>{(p.totalRevenue ?? 0).toLocaleString('fa-IR')} تومان</td>",
    "                              <td>{p.name || '-'}</td>\n"
    "                              <td className='text-center'>{(p.totalQty ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                              <td className='text-center'>{(p.totalRevenue ?? 0).toLocaleString('fa-IR')} تومان</td>",
    "ReportsPage.jsx: وسط‌چین سلول‌های جدول محصولات",
)

# ─────────────────────────────────────────────────────────
# 2) جدول پرخریدترین مشتریان — هدر و سلول‌های عددی وسط‌چین
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                        <th>مشتری</th>\n"
    "                        <th>تعداد سفارش</th>\n"
    "                        <th>مجموع خرید</th>",
    "                        <th>مشتری</th>\n"
    "                        <th className='text-center'>تعداد سفارش</th>\n"
    "                        <th className='text-center'>مجموع خرید</th>",
    "ReportsPage.jsx: وسط‌چین هدر جدول مشتریان",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                              <td>{c.name || '-'}</td>\n"
    "                              <td>{(c.totalOrders ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                              <td>{(c.totalSpent ?? 0).toLocaleString('fa-IR')} تومان</td>",
    "                              <td>{c.name || '-'}</td>\n"
    "                              <td className='text-center'>{(c.totalOrders ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                              <td className='text-center'>{(c.totalSpent ?? 0).toLocaleString('fa-IR')} تومان</td>",
    "ReportsPage.jsx: وسط‌چین سلول‌های جدول مشتریان",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ وسط‌چین کردن جداول گزارش‌گیری")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
