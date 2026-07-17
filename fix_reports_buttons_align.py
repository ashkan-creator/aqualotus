#!/usr/bin/env python3
"""
اسکریپت پچ: هم‌تراز و شیک کردن دکمه‌های «چاپ گزارش» و «بستن دوره فعلی»
اجرا از ریشه پروژه: python3 fix_reports_buttons_align.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-btnalign-backup"

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
# 1) index.css — یکسان‌سازی padding/border دو دکمه + حذف قانون موبایل قدیمی
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/index.css",
    """.btn-report-danger {
  background: linear-gradient(135deg, #b5451b 0%, #8a3414 100%);
  border: none;
  color: #fff;
  font-weight: 600;
  border-radius: 10px;
  padding: 10px 22px;
  transition: all 0.3s ease;
}
.btn-report-danger:hover {
  background: linear-gradient(135deg, #8a3414 0%, #b5451b 100%);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(181, 69, 27, 0.4);
}
.btn-report-danger:disabled {
  opacity: 0.6;
  transform: none;
}
.btn-report-outline {
  border: 2px solid var(--primary);
  color: var(--primary);
  background: transparent;
  font-weight: 600;
  border-radius: 10px;
  padding: 8px 20px;
  transition: all 0.3s ease;
}
.btn-report-outline:hover {
  background: var(--primary);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(45, 106, 79, 0.3);
}""",
    """.btn-report-danger,
.btn-report-outline {
  border-radius: 10px;
  padding: 9px 22px;
  font-weight: 600;
  font-size: 0.95rem;
  line-height: 1.4;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  white-space: nowrap;
}
.btn-report-danger {
  background: linear-gradient(135deg, #b5451b 0%, #8a3414 100%);
  color: #fff;
}
.btn-report-danger:hover {
  background: linear-gradient(135deg, #8a3414 0%, #b5451b 100%);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(181, 69, 27, 0.4);
}
.btn-report-danger:disabled {
  opacity: 0.6;
  transform: none;
}
.btn-report-outline {
  border-color: var(--primary);
  color: var(--primary);
  background: transparent;
}
.btn-report-outline:hover {
  background: var(--primary);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(45, 106, 79, 0.3);
}
.report-actions {
  display: flex;
  align-items: stretch;
  gap: 10px;
}""",
    "index.css: یکسان‌سازی padding/border دکمه‌های گزارش + کلاس report-actions",
)

# ─────────────────────────────────────────────────────────
# 2) index.css — حذف قانون موبایل قدیمی که تداخل داشت
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/index.css",
    """  .btn-report-danger,
  .btn-report-outline {
    width: 100%;
    padding: 10px 16px;
    font-size: 0.9rem;
  }""",
    """  .report-actions {
    flex-direction: column;
  }
  .btn-report-danger,
  .btn-report-outline {
    width: 100%;
  }""",
    "index.css: اصلاح قانون موبایل دکمه‌ها (استک عمودی تمام‌عرض)",
)

# ─────────────────────────────────────────────────────────
# 3) ReportsPage.jsx — چیدمان فلکس درست به‌جای me-2 / text-md-end
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "            <Col xs={12} md={4} className='text-md-end no-print'>\n"
    "              <Button className='btn-report-outline me-2' onClick={printHandler}>\n"
    "                🖨️ چاپ گزارش (PDF)\n"
    "              </Button>\n"
    "              <Button className='btn-report-danger' onClick={() => setShowCloseModal(true)}>\n"
    "                🔒 بستن دوره فعلی\n"
    "              </Button>\n"
    "            </Col>",
    "            <Col xs={12} md={4} className='no-print'>\n"
    "              <div className='report-actions justify-content-md-end'>\n"
    "                <Button className='btn-report-outline' onClick={printHandler}>\n"
    "                  🖨️ چاپ گزارش (PDF)\n"
    "                </Button>\n"
    "                <Button className='btn-report-danger' onClick={() => setShowCloseModal(true)}>\n"
    "                  🔒 بستن دوره فعلی\n"
    "                </Button>\n"
    "              </div>\n"
    "            </Col>",
    "ReportsPage.jsx: چیدمان فلکس هم‌تراز برای دکمه‌های چاپ/بستن دوره",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ هم‌ترازی دکمه‌های گزارش‌گیری")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("مرورگر رو رفرش کن (Ctrl+Shift+R) و دکمه‌ها رو تو دسکتاپ و موبایل چک کن.")
