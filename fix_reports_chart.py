#!/usr/bin/env python3
"""
اسکریپت پچ: رفع درهم‌تنیدگی نمودار «روند درآمد بازه انتخابی»
اجرا از ریشه پروژه: python3 fix_reports_chart.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-chart-backup"

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
# 1) افزودن تابع خلاصه‌ساز عدد و محاسبه فاصله برچسب‌ها (بعد از chartData)
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "  const chartData =\n"
    "    stats?.daily?.map((d) => ({\n"
    "      ...d,\n"
    "      label: new Date(d.date).toLocaleDateString('fa-IR', { month: 'short', day: 'numeric' }),\n"
    "    })) || []",
    "  const chartData =\n"
    "    stats?.daily?.map((d) => ({\n"
    "      ...d,\n"
    "      label: new Date(d.date).toLocaleDateString('fa-IR', { month: 'short', day: 'numeric' }),\n"
    "    })) || []\n\n"
    "  const chartTickInterval = chartData.length > 8 ? Math.ceil(chartData.length / 7) - 1 : 0\n\n"
    "  const formatAxisNumber = (value) => {\n"
    "    if (value >= 1000000) return (value / 1000000).toFixed(1).replace(/\\.0$/, '') + ' م'\n"
    "    if (value >= 1000) return Math.round(value / 1000) + ' ه'\n"
    "    return value.toLocaleString('fa-IR')\n"
    "  }",
    "ReportsPage.jsx: افزودن chartTickInterval و formatAxisNumber",
)

# ─────────────────────────────────────────────────────────
# 2) افزایش ارتفاع نمودار
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                  <ResponsiveContainer width='100%' height={220}>\n"
    "                    <AreaChart data={chartData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>",
    "                  <ResponsiveContainer width='100%' height={270}>\n"
    "                    <AreaChart data={chartData} margin={{ top: 5, right: 5, left: 0, bottom: 30 }}>",
    "ReportsPage.jsx: افزایش ارتفاع نمودار و مارجین پایین برای جا شدن برچسب‌های زاویه‌دار",
)

# ─────────────────────────────────────────────────────────
# 3) برچسب‌های محور X (تاریخ) — زاویه‌دار و با فاصله هوشمند
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      <XAxis dataKey='label' tick={{ fontSize: 11 }} />",
    "                      <XAxis\n"
    "                        dataKey='label'\n"
    "                        tick={{ fontSize: 10 }}\n"
    "                        interval={chartTickInterval}\n"
    "                        angle={-35}\n"
    "                        textAnchor='end'\n"
    "                        height={50}\n"
    "                      />",
    "ReportsPage.jsx: برچسب‌های محور X زاویه‌دار با فاصله هوشمند",
)

# ─────────────────────────────────────────────────────────
# 4) برچسب‌های محور Y (درآمد) — خلاصه‌شده
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      <YAxis tick={{ fontSize: 11 }} />",
    "                      <YAxis tick={{ fontSize: 10 }} tickFormatter={formatAxisNumber} width={42} />",
    "ReportsPage.jsx: خلاصه‌سازی اعداد محور Y",
)

# ─────────────────────────────────────────────────────────
# 5) تولتیپ — عدد کامل و دقیق موقع هاور
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      <Tooltip />",
    "                      <Tooltip\n"
    "                        formatter={(value) => [`${value.toLocaleString('fa-IR')} تومان`, 'درآمد']}\n"
    "                      />",
    "ReportsPage.jsx: تولتیپ با عدد کامل تومان موقع هاور",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ رفع درهم‌تنیدگی نمودار گزارش‌گیری")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("مرورگر رو رفرش کن و نمودار رو تو دسکتاپ و موبایل چک کن.")
