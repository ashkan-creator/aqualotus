#!/usr/bin/env python3
"""
اسکریپت پچ: ریسپانسیو کردن فیلدهای «از تاریخ / تا تاریخ» تو صفحه گزارش‌گیری
اجرا از ریشه پروژه: python3 fix_reports_date_responsive.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-daterespo-backup"

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
# 1) ReportsPage.jsx — تمام‌عرض تو موبایل، کنار هم از sm به بالا
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "          <Row className='g-3 align-items-end'>\n"
    "            <Col xs={6} md={3}>\n"
    "              <Form.Group>\n"
    "                <Form.Label>از تاریخ</Form.Label>\n"
    "                <Form.Control type='date' value={startDate} onChange={(e) => setStartDate(e.target.value)} />\n"
    "              </Form.Group>\n"
    "            </Col>\n"
    "            <Col xs={6} md={3}>\n"
    "              <Form.Group>\n"
    "                <Form.Label>تا تاریخ</Form.Label>\n"
    "                <Form.Control type='date' value={endDate} onChange={(e) => setEndDate(e.target.value)} />\n"
    "              </Form.Group>\n"
    "            </Col>\n"
    "          </Row>",
    "          <Row className='g-3 align-items-end'>\n"
    "            <Col xs={12} sm={6} md={3}>\n"
    "              <Form.Group>\n"
    "                <Form.Label>از تاریخ</Form.Label>\n"
    "                <Form.Control\n"
    "                  type='date'\n"
    "                  className='report-date-input'\n"
    "                  value={startDate}\n"
    "                  onChange={(e) => setStartDate(e.target.value)}\n"
    "                />\n"
    "              </Form.Group>\n"
    "            </Col>\n"
    "            <Col xs={12} sm={6} md={3}>\n"
    "              <Form.Group>\n"
    "                <Form.Label>تا تاریخ</Form.Label>\n"
    "                <Form.Control\n"
    "                  type='date'\n"
    "                  className='report-date-input'\n"
    "                  value={endDate}\n"
    "                  onChange={(e) => setEndDate(e.target.value)}\n"
    "                />\n"
    "              </Form.Group>\n"
    "            </Col>\n"
    "          </Row>",
    "ReportsPage.jsx: xs={12} sm={6} برای فیلدهای تاریخ (تمام‌عرض تو موبایل)",
)

# ─────────────────────────────────────────────────────────
# 2) index.css — استایل اختصاصی فیلد تاریخ برای ریسپانسیو بهتر
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/index.css",
    ".report-actions {\n"
    "  display: flex;\n"
    "  align-items: stretch;\n"
    "  gap: 10px;\n"
    "}",
    ".report-actions {\n"
    "  display: flex;\n"
    "  align-items: stretch;\n"
    "  gap: 10px;\n"
    "}\n"
    ".report-date-input {\n"
    "  width: 100%;\n"
    "  min-width: 0;\n"
    "  font-size: 0.95rem;\n"
    "}\n"
    "@media (max-width: 400px) {\n"
    "  .report-date-input {\n"
    "    font-size: 0.85rem;\n"
    "    padding-left: 6px;\n"
    "    padding-right: 6px;\n"
    "  }\n"
    "}",
    "index.css: استایل report-date-input برای ریسپانسیو بهتر فیلدهای تاریخ",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ ریسپانسیو فیلدهای تاریخ")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("مرورگر رو رفرش کن و تو حالت موبایل (F12 > Toggle device toolbar) چک کن.")
