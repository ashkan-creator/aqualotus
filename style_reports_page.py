#!/usr/bin/env python3
"""
اسکریپت پچ: استایل صفحه گزارش‌گیری (هاور، دکمه‌های شیک، موشن، ریسپانسیو)
اجرا از ریشه پروژه: python3 style_reports_page.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-style-backup"

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
# 1) index.css — کلاس‌های جدید (کارت هاور، دکمه‌ها، fade-in، ریسپانسیو)
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/index.css",
    "/* ===== چاپ گزارش (PDF از طریق پرینت مرورگر) ===== */",
    """/* ===== گزارش‌گیری - کارت‌ها، دکمه‌ها، موشن، ریسپانسیو ===== */
.report-stat-card {
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  cursor: default;
}
.report-stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 22px rgba(0, 0, 0, 0.18);
}
.report-fade-in {
  animation: reportFadeInUp 0.45s ease both;
}
@keyframes reportFadeInUp {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}
.btn-report-danger {
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
}
.report-table tbody tr {
  transition: background 0.2s ease;
}
@media (max-width: 576px) {
  .report-stat-card .card-body {
    padding: 0.85rem !important;
  }
  .btn-report-danger,
  .btn-report-outline {
    width: 100%;
    padding: 10px 16px;
    font-size: 0.9rem;
  }
}
/* ===== چاپ گزارش (PDF از طریق پرینت مرورگر) ===== */""",
    "index.css: افزودن کلاس‌های هاور/دکمه/موشن/ریسپانسیو گزارش‌گیری",
)

# ─────────────────────────────────────────────────────────
# 2) ReportsPage.jsx — کلاس‌های کارت آمار + fade-in
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "        {/* دوره فعلی */}\n"
    "        <Card className='p-3 mb-4'>",
    "        {/* دوره فعلی */}\n"
    "        <Card className='p-3 mb-4 report-fade-in'>",
    "ReportsPage.jsx: fade-in روی کارت دوره فعلی",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                <Card className='h-100 text-white' style={{ background: '#2d6a4f' }}>",
    "                <Card className='h-100 text-white report-stat-card' style={{ background: '#2d6a4f' }}>",
    "ReportsPage.jsx: کلاس هاور روی کارت درآمد بازه",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                <Card className='h-100 text-white' style={{ background: '#0d4f8b' }}>",
    "                <Card className='h-100 text-white report-stat-card' style={{ background: '#0d4f8b' }}>",
    "ReportsPage.jsx: کلاس هاور روی کارت کل سفارش‌ها",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                <Card className='h-100 text-white' style={{ background: '#52b788' }}>",
    "                <Card className='h-100 text-white report-stat-card' style={{ background: '#52b788' }}>",
    "ReportsPage.jsx: کلاس هاور روی کارت پرداخت‌شده",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                <Card className='h-100 text-white' style={{ background: '#6a4c2d' }}>",
    "                <Card className='h-100 text-white report-stat-card' style={{ background: '#6a4c2d' }}>",
    "ReportsPage.jsx: کلاس هاور روی کارت میانگین سفارش",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "              <Card className='p-3 mb-4'>\n"
    "                  <h6 className='mb-3'>روند درآمد بازه انتخابی</h6>",
    "              <Card className='p-3 mb-4 report-fade-in'>\n"
    "                  <h6 className='mb-3'>روند درآمد بازه انتخابی</h6>",
    "ReportsPage.jsx: fade-in روی کارت نمودار",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "            <Card className='p-3 h-100'>\n"
    "              <h6 className='mb-3'>🏆 پرفروش‌ترین محصولات (بازه انتخابی)</h6>",
    "            <Card className='p-3 h-100 report-fade-in'>\n"
    "              <h6 className='mb-3'>🏆 پرفروش‌ترین محصولات (بازه انتخابی)</h6>",
    "ReportsPage.jsx: fade-in روی کارت پرفروش‌ترین محصولات",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "            <Card className='p-3 h-100'>\n"
    "              <h6 className='mb-3'>👑 پرخریدترین مشتریان (بازه انتخابی)</h6>",
    "            <Card className='p-3 h-100 report-fade-in'>\n"
    "              <h6 className='mb-3'>👑 پرخریدترین مشتریان (بازه انتخابی)</h6>",
    "ReportsPage.jsx: fade-in روی کارت پرخریدترین مشتریان",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "        <Card className='p-3'>\n"
    "          <h5 className='mb-3'>📁 آرشیو دوره‌های بسته‌شده</h5>",
    "        <Card className='p-3 report-fade-in'>\n"
    "          <h5 className='mb-3'>📁 آرشیو دوره‌های بسته‌شده</h5>",
    "ReportsPage.jsx: fade-in روی کارت آرشیو دوره‌ها",
)

# ─────────────────────────────────────────────────────────
# 3) ReportsPage.jsx — دکمه‌های شیک با موشن
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "              <Button variant='outline-secondary' className='me-2' onClick={printHandler}>\n"
    "                🖨️ چاپ گزارش (PDF)\n"
    "              </Button>\n"
    "              <Button variant='danger' onClick={() => setShowCloseModal(true)}>\n"
    "                🔒 بستن دوره فعلی\n"
    "              </Button>",
    "              <Button className='btn-report-outline me-2' onClick={printHandler}>\n"
    "                🖨️ چاپ گزارش (PDF)\n"
    "              </Button>\n"
    "              <Button className='btn-report-danger' onClick={() => setShowCloseModal(true)}>\n"
    "                🔒 بستن دوره فعلی\n"
    "              </Button>",
    "ReportsPage.jsx: دکمه‌های چاپ/بستن دوره با گرادیانت و موشن",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "          <Button variant='danger' onClick={closeHandler} disabled={closing}>\n"
    "            {closing ? 'در حال بستن...' : 'تایید و بستن دوره'}\n"
    "          </Button>",
    "          <Button className='btn-report-danger' onClick={closeHandler} disabled={closing}>\n"
    "            {closing ? 'در حال بستن...' : 'تایید و بستن دوره'}\n"
    "          </Button>",
    "ReportsPage.jsx: دکمه تایید بستن دوره تو مودال با موشن",
)

# ─────────────────────────────────────────────────────────
# 4) ReportsPage.jsx — کلاس جدول روی هر سه Table برای هاور ردیف
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                  <Table striped hover size='sm'>\n"
    "                    <thead>\n"
    "                      <tr>\n"
    "                        <th>محصول</th>",
    "                  <Table striped hover size='sm' className='report-table'>\n"
    "                    <thead>\n"
    "                      <tr>\n"
    "                        <th>محصول</th>",
    "ReportsPage.jsx: کلاس report-table روی جدول محصولات",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                  <Table striped hover size='sm'>\n"
    "                    <thead>\n"
    "                      <tr>\n"
    "                        <th>مشتری</th>",
    "                  <Table striped hover size='sm' className='report-table'>\n"
    "                    <thead>\n"
    "                      <tr>\n"
    "                        <th>مشتری</th>",
    "ReportsPage.jsx: کلاس report-table روی جدول مشتریان",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "              <Table striped hover>\n"
    "                <thead>\n"
    "                  <tr>\n"
    "                    <th>از تاریخ</th>",
    "              <Table striped hover className='report-table'>\n"
    "                <thead>\n"
    "                  <tr>\n"
    "                    <th>از تاریخ</th>",
    "ReportsPage.jsx: کلاس report-table روی جدول آرشیو",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ استایل صفحه گزارش‌گیری")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("مرورگر رو رفرش کن و ظاهر جدید رو تو دسکتاپ و موبایل چک کن.")
