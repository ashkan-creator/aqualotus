#!/usr/bin/env python3
"""
اسکریپت پچ: رفع تداخل نام endpoint بین reportsApiSlice و productsApiSlice
اجرا از ریشه پروژه: python3 fix_reports_endpoint_collision.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-collision-backup"

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
# 1) reportsApiSlice.js — تغییر نام endpoint ها به اسم منحصربه‌فرد
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/slices/reportsApiSlice.js",
    "    getTopProducts: builder.query({\n"
    "      query: ({ startDate, endDate, limit }) => ({\n"
    "        url: `${REPORTS_URL}/top-products`,\n"
    "        params: { startDate, endDate, limit },\n"
    "      }),\n"
    "      keepUnusedDataFor: 5,\n"
    "    }),\n"
    "    getTopCustomers: builder.query({\n"
    "      query: ({ startDate, endDate, limit }) => ({\n"
    "        url: `${REPORTS_URL}/top-customers`,\n"
    "        params: { startDate, endDate, limit },\n"
    "      }),\n"
    "      keepUnusedDataFor: 5,\n"
    "    }),",
    "    getReportTopProducts: builder.query({\n"
    "      query: ({ startDate, endDate, limit }) => ({\n"
    "        url: `${REPORTS_URL}/top-products`,\n"
    "        params: { startDate, endDate, limit },\n"
    "      }),\n"
    "      keepUnusedDataFor: 5,\n"
    "    }),\n"
    "    getReportTopCustomers: builder.query({\n"
    "      query: ({ startDate, endDate, limit }) => ({\n"
    "        url: `${REPORTS_URL}/top-customers`,\n"
    "        params: { startDate, endDate, limit },\n"
    "      }),\n"
    "      keepUnusedDataFor: 5,\n"
    "    }),",
    "reportsApiSlice.js: تغییر نام endpoint به getReportTopProducts/getReportTopCustomers (رفع تداخل)",
)

patch_file(
    "frontend/src/slices/reportsApiSlice.js",
    "  useGetClosedPeriodsQuery,\n"
    "  useGetTopProductsQuery,\n"
    "  useGetTopCustomersQuery,\n"
    "} = reportsApiSlice",
    "  useGetClosedPeriodsQuery,\n"
    "  useGetReportTopProductsQuery,\n"
    "  useGetReportTopCustomersQuery,\n"
    "} = reportsApiSlice",
    "reportsApiSlice.js: تغییر نام هوک‌های export شده",
)

# ─────────────────────────────────────────────────────────
# 2) ReportsPage.jsx — استفاده از هوک‌های تغییرنام‌یافته
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "  useGetClosedPeriodsQuery,\n"
    "  useGetTopProductsQuery,\n"
    "  useGetTopCustomersQuery,\n"
    "} from '../../slices/reportsApiSlice'",
    "  useGetClosedPeriodsQuery,\n"
    "  useGetReportTopProductsQuery,\n"
    "  useGetReportTopCustomersQuery,\n"
    "} from '../../slices/reportsApiSlice'",
    "ReportsPage.jsx: import هوک‌های تغییرنام‌یافته",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "  const { data: topProducts, isLoading: topProductsLoading } = useGetTopProductsQuery({ startDate, endDate, limit: 5 })\n"
    "  const { data: topCustomers, isLoading: topCustomersLoading } = useGetTopCustomersQuery({ startDate, endDate, limit: 5 })",
    "  const { data: topProducts, isLoading: topProductsLoading } = useGetReportTopProductsQuery({ startDate, endDate, limit: 5 })\n"
    "  const { data: topCustomers, isLoading: topCustomersLoading } = useGetReportTopCustomersQuery({ startDate, endDate, limit: 5 })",
    "ReportsPage.jsx: استفاده از هوک‌های تغییرنام‌یافته",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ رفع تداخل endpoint")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("سرور رو کامل ری‌استارت کن (Ctrl+C بعد npm run dev) و تو یه تب جدید تست کن.")
