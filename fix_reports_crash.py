#!/usr/bin/env python3
"""
اسکریپت پچ: رفع کرش گذرای جدول پرفروش‌ترین محصولات/مشتریان
اجرا از ریشه پروژه: python3 fix_reports_crash.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-crashfix-backup"

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
# 1) جدول پرفروش‌ترین محصولات — مقادیر ایمن با fallback
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      {topProducts.map((p) => (\n"
    "                        <tr key={p._id}>\n"
    "                          <td>{p.name}</td>\n"
    "                          <td>{p.totalQty.toLocaleString('fa-IR')}</td>\n"
    "                          <td>{p.totalRevenue.toLocaleString('fa-IR')} تومان</td>\n"
    "                        </tr>\n"
    "                      ))}",
    "                      {topProducts\n"
    "                        .filter((p) => p && p._id)\n"
    "                        .map((p) => (\n"
    "                          <tr key={p._id}>\n"
    "                            <td>{p.name || '-'}</td>\n"
    "                            <td>{(p.totalQty ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                            <td>{(p.totalRevenue ?? 0).toLocaleString('fa-IR')} تومان</td>\n"
    "                          </tr>\n"
    "                        ))}",
    "ReportsPage.jsx: مقاوم‌سازی جدول پرفروش‌ترین محصولات در برابر داده ناقص",
)

# ─────────────────────────────────────────────────────────
# 2) جدول پرخریدترین مشتریان — مقادیر ایمن با fallback
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      {topCustomers.map((c) => (\n"
    "                        <tr key={c._id}>\n"
    "                          <td>{c.name}</td>\n"
    "                          <td>{c.totalOrders.toLocaleString('fa-IR')}</td>\n"
    "                          <td>{c.totalSpent.toLocaleString('fa-IR')} تومان</td>\n"
    "                        </tr>\n"
    "                      ))}",
    "                      {topCustomers\n"
    "                        .filter((c) => c && c._id)\n"
    "                        .map((c) => (\n"
    "                          <tr key={c._id}>\n"
    "                            <td>{c.name || '-'}</td>\n"
    "                            <td>{(c.totalOrders ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                            <td>{(c.totalSpent ?? 0).toLocaleString('fa-IR')} تومان</td>\n"
    "                          </tr>\n"
    "                        ))}",
    "ReportsPage.jsx: مقاوم‌سازی جدول پرخریدترین مشتریان در برابر داده ناقص",
)

# ─────────────────────────────────────────────────────────
# 3) کارت‌های آمار بالای صفحه — مقادیر ایمن با fallback
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                        {stats.totalRevenue.toLocaleString('fa-IR')} تومان",
    "                        {(stats.totalRevenue ?? 0).toLocaleString('fa-IR')} تومان",
    "ReportsPage.jsx: fallback برای stats.totalRevenue",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                        {stats.avgOrderValue.toLocaleString('fa-IR')} تومان",
    "                        {(stats.avgOrderValue ?? 0).toLocaleString('fa-IR')} تومان",
    "ReportsPage.jsx: fallback برای stats.avgOrderValue",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ رفع کرش گزارش‌گیری")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("مرورگر رو رفرش کن (Ctrl+Shift+R) و دوباره تست کن.")
