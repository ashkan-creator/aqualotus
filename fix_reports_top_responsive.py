#!/usr/bin/env python3
"""
اسکریپت پچ: نمای کارتی موبایل برای پرفروش‌ترین محصولات / پرخریدترین مشتریان
اجرا از ریشه پروژه: python3 fix_reports_top_responsive.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-topresponsive-backup"

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
# 1) ReportsPage.jsx — افزودن Badge به import
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "import { Container, Row, Col, Card, Table, Button, Form, Modal } from 'react-bootstrap'",
    "import { Container, Row, Col, Card, Table, Button, Form, Modal, Badge } from 'react-bootstrap'",
    "ReportsPage.jsx: افزودن Badge به import react-bootstrap",
)

# ─────────────────────────────────────────────────────────
# 2) ReportsPage.jsx — نمای موبایل پرفروش‌ترین محصولات
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "              {topProductsLoading ? (\n"
    "                <Loader />\n"
    "              ) : !topProducts?.length ? (\n"
    "                <p className='text-muted mb-0'>داده‌ای برای این بازه یافت نشد</p>\n"
    "              ) : (\n"
    "                <div className='table-responsive'>\n"
    "                  <Table striped hover size='sm' className='report-table'>\n"
    "                    <thead>\n"
    "                      <tr>\n"
    "                        <th>محصول</th>\n"
    "                        <th>تعداد فروش</th>\n"
    "                        <th>درآمد</th>\n"
    "                      </tr>\n"
    "                    </thead>\n"
    "                    <tbody>\n"
    "                      {topProducts\n"
    "                        .filter((p) => p && p._id)\n"
    "                        .map((p) => (\n"
    "                          <tr key={p._id}>\n"
    "                            <td>{p.name || '-'}</td>\n"
    "                            <td>{(p.totalQty ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                            <td>{(p.totalRevenue ?? 0).toLocaleString('fa-IR')} تومان</td>\n"
    "                          </tr>\n"
    "                        ))}\n"
    "                    </tbody>\n"
    "                  </Table>\n"
    "                </div>\n"
    "              )}",
    "              {topProductsLoading ? (\n"
    "                <Loader />\n"
    "              ) : !topProducts?.length ? (\n"
    "                <p className='text-muted mb-0'>داده‌ای برای این بازه یافت نشد</p>\n"
    "              ) : (\n"
    "                <>\n"
    "                  <div className='d-none d-md-block table-responsive'>\n"
    "                    <Table striped hover size='sm' className='report-table'>\n"
    "                      <thead>\n"
    "                        <tr>\n"
    "                          <th>محصول</th>\n"
    "                          <th>تعداد فروش</th>\n"
    "                          <th>درآمد</th>\n"
    "                        </tr>\n"
    "                      </thead>\n"
    "                      <tbody>\n"
    "                        {topProducts\n"
    "                          .filter((p) => p && p._id)\n"
    "                          .map((p) => (\n"
    "                            <tr key={p._id}>\n"
    "                              <td>{p.name || '-'}</td>\n"
    "                              <td>{(p.totalQty ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                              <td>{(p.totalRevenue ?? 0).toLocaleString('fa-IR')} تومان</td>\n"
    "                            </tr>\n"
    "                          ))}\n"
    "                      </tbody>\n"
    "                    </Table>\n"
    "                  </div>\n"
    "                  <div className='d-md-none'>\n"
    "                    <Row className='g-2'>\n"
    "                      {topProducts\n"
    "                        .filter((p) => p && p._id)\n"
    "                        .map((p) => (\n"
    "                          <Col xs={12} key={p._id}>\n"
    "                            <Card className='p-2 report-mini-card'>\n"
    "                              <div className='d-flex justify-content-between align-items-center gap-2'>\n"
    "                                <div className='flex-grow-1' style={{ minWidth: 0 }}>\n"
    "                                  <div className='report-mini-title'>{p.name || '-'}</div>\n"
    "                                  <div className='report-mini-sub'>\n"
    "                                    {(p.totalRevenue ?? 0).toLocaleString('fa-IR')} تومان\n"
    "                                  </div>\n"
    "                                </div>\n"
    "                                <Badge bg='success' className='report-mini-badge'>\n"
    "                                  {(p.totalQty ?? 0).toLocaleString('fa-IR')} فروش\n"
    "                                </Badge>\n"
    "                              </div>\n"
    "                            </Card>\n"
    "                          </Col>\n"
    "                        ))}\n"
    "                    </Row>\n"
    "                  </div>\n"
    "                </>\n"
    "              )}",
    "ReportsPage.jsx: نمای کارتی موبایل برای پرفروش‌ترین محصولات",
)

# ─────────────────────────────────────────────────────────
# 3) ReportsPage.jsx — نمای موبایل پرخریدترین مشتریان
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "              {topCustomersLoading ? (\n"
    "                <Loader />\n"
    "              ) : !topCustomers?.length ? (\n"
    "                <p className='text-muted mb-0'>داده‌ای برای این بازه یافت نشد</p>\n"
    "              ) : (\n"
    "                <div className='table-responsive'>\n"
    "                  <Table striped hover size='sm' className='report-table'>\n"
    "                    <thead>\n"
    "                      <tr>\n"
    "                        <th>مشتری</th>\n"
    "                        <th>تعداد سفارش</th>\n"
    "                        <th>مجموع خرید</th>\n"
    "                      </tr>\n"
    "                    </thead>\n"
    "                    <tbody>\n"
    "                      {topCustomers\n"
    "                        .filter((c) => c && c._id)\n"
    "                        .map((c) => (\n"
    "                          <tr key={c._id}>\n"
    "                            <td>{c.name || '-'}</td>\n"
    "                            <td>{(c.totalOrders ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                            <td>{(c.totalSpent ?? 0).toLocaleString('fa-IR')} تومان</td>\n"
    "                          </tr>\n"
    "                        ))}\n"
    "                    </tbody>\n"
    "                  </Table>\n"
    "                </div>\n"
    "              )}",
    "              {topCustomersLoading ? (\n"
    "                <Loader />\n"
    "              ) : !topCustomers?.length ? (\n"
    "                <p className='text-muted mb-0'>داده‌ای برای این بازه یافت نشد</p>\n"
    "              ) : (\n"
    "                <>\n"
    "                  <div className='d-none d-md-block table-responsive'>\n"
    "                    <Table striped hover size='sm' className='report-table'>\n"
    "                      <thead>\n"
    "                        <tr>\n"
    "                          <th>مشتری</th>\n"
    "                          <th>تعداد سفارش</th>\n"
    "                          <th>مجموع خرید</th>\n"
    "                        </tr>\n"
    "                      </thead>\n"
    "                      <tbody>\n"
    "                        {topCustomers\n"
    "                          .filter((c) => c && c._id)\n"
    "                          .map((c) => (\n"
    "                            <tr key={c._id}>\n"
    "                              <td>{c.name || '-'}</td>\n"
    "                              <td>{(c.totalOrders ?? 0).toLocaleString('fa-IR')}</td>\n"
    "                              <td>{(c.totalSpent ?? 0).toLocaleString('fa-IR')} تومان</td>\n"
    "                            </tr>\n"
    "                          ))}\n"
    "                      </tbody>\n"
    "                    </Table>\n"
    "                  </div>\n"
    "                  <div className='d-md-none'>\n"
    "                    <Row className='g-2'>\n"
    "                      {topCustomers\n"
    "                        .filter((c) => c && c._id)\n"
    "                        .map((c) => (\n"
    "                          <Col xs={12} key={c._id}>\n"
    "                            <Card className='p-2 report-mini-card'>\n"
    "                              <div className='d-flex justify-content-between align-items-center gap-2'>\n"
    "                                <div className='flex-grow-1' style={{ minWidth: 0 }}>\n"
    "                                  <div className='report-mini-title'>{c.name || '-'}</div>\n"
    "                                  <div className='report-mini-sub'>\n"
    "                                    {(c.totalSpent ?? 0).toLocaleString('fa-IR')} تومان\n"
    "                                  </div>\n"
    "                                </div>\n"
    "                                <Badge bg='primary' className='report-mini-badge'>\n"
    "                                  {(c.totalOrders ?? 0).toLocaleString('fa-IR')} سفارش\n"
    "                                </Badge>\n"
    "                              </div>\n"
    "                            </Card>\n"
    "                          </Col>\n"
    "                        ))}\n"
    "                    </Row>\n"
    "                  </div>\n"
    "                </>\n"
    "              )}",
    "ReportsPage.jsx: نمای کارتی موبایل برای پرخریدترین مشتریان",
)

# ─────────────────────────────────────────────────────────
# 4) index.css — استایل کارت‌های موبایل (تیتر بلند با سه‌نقطه، بج و...)
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/index.css",
    ".report-date-input {\n"
    "  width: 100%;\n"
    "  min-width: 0;\n"
    "  font-size: 0.95rem;\n"
    "}",
    ".report-date-input {\n"
    "  width: 100%;\n"
    "  min-width: 0;\n"
    "  font-size: 0.95rem;\n"
    "}\n"
    ".report-mini-card {\n"
    "  border-radius: 12px;\n"
    "  transition: transform 0.2s ease, box-shadow 0.2s ease;\n"
    "}\n"
    ".report-mini-card:active {\n"
    "  transform: scale(0.98);\n"
    "}\n"
    ".report-mini-title {\n"
    "  font-weight: 600;\n"
    "  font-size: 0.88rem;\n"
    "  overflow: hidden;\n"
    "  text-overflow: ellipsis;\n"
    "  white-space: nowrap;\n"
    "}\n"
    ".report-mini-sub {\n"
    "  font-size: 0.8rem;\n"
    "  color: var(--primary-dark);\n"
    "  font-weight: 600;\n"
    "  margin-top: 2px;\n"
    "}\n"
    ".report-mini-badge {\n"
    "  flex-shrink: 0;\n"
    "  white-space: nowrap;\n"
    "  font-size: 0.75rem;\n"
    "}",
    "index.css: استایل کارت‌های موبایل گزارش‌گیری (report-mini-*)",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ ریسپانسیو پرفروش‌ترین/پرخریدترین")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("مرورگر رو رفرش کن و تو حالت موبایل چک کن.")
