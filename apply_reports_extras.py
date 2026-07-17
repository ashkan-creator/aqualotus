#!/usr/bin/env python3
"""
اسکریپت پچ: تکمیل داشبورد گزارش‌گیری
- فرمت عدد کامل به‌جای خلاصه «هزار ت»
- پرفروش‌ترین محصولات (بازه زمانی)
- پرخریدترین مشتریان (بازه زمانی)
- دکمه چاپ گزارش (PDF از طریق چاپ مرورگر)
اجرا از ریشه پروژه: python3 apply_reports_extras.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-extras-backup"

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


def create_new_file(rel_path, content, label):
    path = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        results.append(("✓", f"{label} (از قبل وجود داشت، دست نخورد)"))
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    results.append(("✓", label))


# ─────────────────────────────────────────────────────────
# 1) reportController.js — دو تابع جدید (قبل از export)
# ─────────────────────────────────────────────────────────
NEW_CONTROLLER_FUNCS = """// @desc    پرفروش‌ترین محصولات در بازه زمانی
// @route   GET /api/reports/top-products?startDate=&endDate=&limit=
// @access  Private/Admin
const getTopProducts = asyncHandler(async (req, res) => {
  const { startDate, endDate, limit } = req.query
  if (!startDate || !endDate) {
    res.status(400)
    throw new Error('بازه زمانی الزامی است')
  }
  const start = new Date(startDate)
  const end = new Date(endDate)
  end.setHours(23, 59, 59, 999)
  const topLimit = Number(limit) || 5

  const result = await Order.aggregate([
    { $match: { createdAt: { $gte: start, $lte: end }, isPaid: true } },
    { $unwind: '$orderItems' },
    {
      $group: {
        _id: '$orderItems.product',
        name: { $first: '$orderItems.name' },
        image: { $first: '$orderItems.image' },
        totalQty: { $sum: '$orderItems.qty' },
        totalRevenue: { $sum: { $multiply: ['$orderItems.qty', '$orderItems.price'] } },
      },
    },
    { $sort: { totalQty: -1 } },
    { $limit: topLimit },
  ])

  res.json(result)
})

// @desc    پرخریدترین مشتریان در بازه زمانی
// @route   GET /api/reports/top-customers?startDate=&endDate=&limit=
// @access  Private/Admin
const getTopCustomers = asyncHandler(async (req, res) => {
  const { startDate, endDate, limit } = req.query
  if (!startDate || !endDate) {
    res.status(400)
    throw new Error('بازه زمانی الزامی است')
  }
  const start = new Date(startDate)
  const end = new Date(endDate)
  end.setHours(23, 59, 59, 999)
  const topLimit = Number(limit) || 5

  const result = await Order.aggregate([
    { $match: { createdAt: { $gte: start, $lte: end }, isPaid: true } },
    {
      $group: {
        _id: '$user',
        totalOrders: { $sum: 1 },
        totalSpent: { $sum: '$totalPrice' },
      },
    },
    { $sort: { totalSpent: -1 } },
    { $limit: topLimit },
    {
      $lookup: {
        from: 'users',
        localField: '_id',
        foreignField: '_id',
        as: 'userInfo',
      },
    },
    { $unwind: '$userInfo' },
    {
      $project: {
        _id: 1,
        totalOrders: 1,
        totalSpent: 1,
        name: '$userInfo.name',
        email: '$userInfo.email',
        phone: '$userInfo.phone',
      },
    },
  ])

  res.json(result)
})

export { getReportStats, getCurrentPeriod, closePeriod, getClosedPeriods, getTopProducts, getTopCustomers }
"""

patch_file(
    "backend/controllers/reportController.js",
    "export { getReportStats, getCurrentPeriod, closePeriod, getClosedPeriods }",
    NEW_CONTROLLER_FUNCS.rstrip("\n"),
    "reportController.js: افزودن getTopProducts / getTopCustomers",
)

# ─────────────────────────────────────────────────────────
# 2) reportRoutes.js — import و روت‌های جدید
# ─────────────────────────────────────────────────────────
patch_file(
    "backend/routes/reportRoutes.js",
    "import {\n"
    "  getReportStats,\n"
    "  getCurrentPeriod,\n"
    "  closePeriod,\n"
    "  getClosedPeriods,\n"
    "} from '../controllers/reportController.js'",
    "import {\n"
    "  getReportStats,\n"
    "  getCurrentPeriod,\n"
    "  closePeriod,\n"
    "  getClosedPeriods,\n"
    "  getTopProducts,\n"
    "  getTopCustomers,\n"
    "} from '../controllers/reportController.js'",
    "reportRoutes.js: افزودن import getTopProducts / getTopCustomers",
)

patch_file(
    "backend/routes/reportRoutes.js",
    "router.get('/periods', protect, admin, getClosedPeriods)",
    "router.get('/periods', protect, admin, getClosedPeriods)\n"
    "router.get('/top-products', protect, admin, getTopProducts)\n"
    "router.get('/top-customers', protect, admin, getTopCustomers)",
    "reportRoutes.js: افزودن روت‌های top-products / top-customers",
)

# ─────────────────────────────────────────────────────────
# 3) reportsApiSlice.js — endpoint های جدید
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/slices/reportsApiSlice.js",
    "    getClosedPeriods: builder.query({\n"
    "      query: () => ({\n"
    "        url: `${REPORTS_URL}/periods`,\n"
    "      }),\n"
    "      keepUnusedDataFor: 5,\n"
    "    }),",
    "    getClosedPeriods: builder.query({\n"
    "      query: () => ({\n"
    "        url: `${REPORTS_URL}/periods`,\n"
    "      }),\n"
    "      keepUnusedDataFor: 5,\n"
    "    }),\n"
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
    "reportsApiSlice.js: افزودن getTopProducts / getTopCustomers",
)

patch_file(
    "frontend/src/slices/reportsApiSlice.js",
    "  useGetClosedPeriodsQuery,\n"
    "} = reportsApiSlice",
    "  useGetClosedPeriodsQuery,\n"
    "  useGetTopProductsQuery,\n"
    "  useGetTopCustomersQuery,\n"
    "} = reportsApiSlice",
    "reportsApiSlice.js: افزودن export هوک‌های جدید",
)

# ─────────────────────────────────────────────────────────
# 4) ReportsPage.jsx — فرمت عدد کامل به‌جای «هزار ت»
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      <div style={{ fontSize: 'clamp(0.9rem, 3vw, 1.4rem)', fontWeight: 'bold' }}>\n"
    "                        {(stats.totalRevenue / 1000).toFixed(0)} هزار ت\n"
    "                      </div>\n"
    "                      <div style={{ fontSize: '0.8rem', opacity: 0.9 }}>درآمد بازه</div>",
    "                      <div style={{ fontSize: 'clamp(0.85rem, 2.6vw, 1.25rem)', fontWeight: 'bold' }}>\n"
    "                        {stats.totalRevenue.toLocaleString('fa-IR')} تومان\n"
    "                      </div>\n"
    "                      <div style={{ fontSize: '0.8rem', opacity: 0.9 }}>درآمد بازه</div>",
    "ReportsPage.jsx: عدد کامل درآمد بازه (به‌جای هزار ت)",
)

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "                      <div style={{ fontSize: 'clamp(0.9rem, 3vw, 1.4rem)', fontWeight: 'bold' }}>\n"
    "                        {(stats.avgOrderValue / 1000).toFixed(0)} هزار ت\n"
    "                      </div>\n"
    "                      <div style={{ fontSize: '0.8rem', opacity: 0.9 }}>میانگین سفارش</div>",
    "                      <div style={{ fontSize: 'clamp(0.85rem, 2.6vw, 1.25rem)', fontWeight: 'bold' }}>\n"
    "                        {stats.avgOrderValue.toLocaleString('fa-IR')} تومان\n"
    "                      </div>\n"
    "                      <div style={{ fontSize: '0.8rem', opacity: 0.9 }}>میانگین سفارش</div>",
    "ReportsPage.jsx: عدد کامل میانگین سفارش (به‌جای هزار ت)",
)

# ─────────────────────────────────────────────────────────
# 5) ReportsPage.jsx — import هوک‌های جدید
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "import {\n"
    "  useGetReportStatsQuery,\n"
    "  useGetCurrentPeriodQuery,\n"
    "  useClosePeriodMutation,\n"
    "  useGetClosedPeriodsQuery,\n"
    "} from '../../slices/reportsApiSlice'",
    "import {\n"
    "  useGetReportStatsQuery,\n"
    "  useGetCurrentPeriodQuery,\n"
    "  useClosePeriodMutation,\n"
    "  useGetClosedPeriodsQuery,\n"
    "  useGetTopProductsQuery,\n"
    "  useGetTopCustomersQuery,\n"
    "} from '../../slices/reportsApiSlice'",
    "ReportsPage.jsx: import هوک‌های top products/customers",
)

# ─────────────────────────────────────────────────────────
# 6) ReportsPage.jsx — کوئری‌های جدید + دکمه چاپ
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "  const { data: closedPeriods, isLoading: closedLoading, refetch: refetchClosed } = useGetClosedPeriodsQuery()\n"
    "  const [closePeriod, { isLoading: closing }] = useClosePeriodMutation()",
    "  const { data: closedPeriods, isLoading: closedLoading, refetch: refetchClosed } = useGetClosedPeriodsQuery()\n"
    "  const { data: topProducts, isLoading: topProductsLoading } = useGetTopProductsQuery({ startDate, endDate, limit: 5 })\n"
    "  const { data: topCustomers, isLoading: topCustomersLoading } = useGetTopCustomersQuery({ startDate, endDate, limit: 5 })\n"
    "  const [closePeriod, { isLoading: closing }] = useClosePeriodMutation()\n\n"
    "  const printHandler = () => window.print()",
    "ReportsPage.jsx: افزودن کوئری‌های top products/customers و printHandler",
)

# ─────────────────────────────────────────────────────────
# 7) ReportsPage.jsx — دکمه چاپ کنار دکمه بستن دوره
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "            <Col xs={12} md={4} className='text-md-end'>\n"
    "              <Button variant='danger' onClick={() => setShowCloseModal(true)}>\n"
    "                🔒 بستن دوره فعلی\n"
    "              </Button>\n"
    "            </Col>",
    "            <Col xs={12} md={4} className='text-md-end no-print'>\n"
    "              <Button variant='outline-secondary' className='me-2' onClick={printHandler}>\n"
    "                🖨️ چاپ گزارش (PDF)\n"
    "              </Button>\n"
    "              <Button variant='danger' onClick={() => setShowCloseModal(true)}>\n"
    "                🔒 بستن دوره فعلی\n"
    "              </Button>\n"
    "            </Col>",
    "ReportsPage.jsx: افزودن دکمه چاپ گزارش",
)

# ─────────────────────────────────────────────────────────
# 8) ReportsPage.jsx — کلاس no-print روی بازه انتخاب تاریخ
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "        {/* بازه زمانی گزارش */}\n"
    "        <Card className='p-3 mb-4'>",
    "        {/* بازه زمانی گزارش */}\n"
    "        <Card className='p-3 mb-4 no-print'>",
    "ReportsPage.jsx: کلاس no-print روی کارت انتخاب بازه",
)

# ─────────────────────────────────────────────────────────
# 9) ReportsPage.jsx — بخش‌های پرفروش‌ترین محصولات و پرخریدترین مشتریان
#    (قبل از بخش آرشیو دوره‌های بسته‌شده)
# ─────────────────────────────────────────────────────────
TOP_SECTIONS = """        {/* پرفروش‌ترین محصولات و پرخریدترین مشتریان */}
        <Row className='g-4 mb-4'>
          <Col xs={12} lg={6}>
            <Card className='p-3 h-100'>
              <h6 className='mb-3'>🏆 پرفروش‌ترین محصولات (بازه انتخابی)</h6>
              {topProductsLoading ? (
                <Loader />
              ) : !topProducts?.length ? (
                <p className='text-muted mb-0'>داده‌ای برای این بازه یافت نشد</p>
              ) : (
                <div className='table-responsive'>
                  <Table striped hover size='sm'>
                    <thead>
                      <tr>
                        <th>محصول</th>
                        <th>تعداد فروش</th>
                        <th>درآمد</th>
                      </tr>
                    </thead>
                    <tbody>
                      {topProducts.map((p) => (
                        <tr key={p._id}>
                          <td>{p.name}</td>
                          <td>{p.totalQty.toLocaleString('fa-IR')}</td>
                          <td>{p.totalRevenue.toLocaleString('fa-IR')} تومان</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </div>
              )}
            </Card>
          </Col>
          <Col xs={12} lg={6}>
            <Card className='p-3 h-100'>
              <h6 className='mb-3'>👑 پرخریدترین مشتریان (بازه انتخابی)</h6>
              {topCustomersLoading ? (
                <Loader />
              ) : !topCustomers?.length ? (
                <p className='text-muted mb-0'>داده‌ای برای این بازه یافت نشد</p>
              ) : (
                <div className='table-responsive'>
                  <Table striped hover size='sm'>
                    <thead>
                      <tr>
                        <th>مشتری</th>
                        <th>تعداد سفارش</th>
                        <th>مجموع خرید</th>
                      </tr>
                    </thead>
                    <tbody>
                      {topCustomers.map((c) => (
                        <tr key={c._id}>
                          <td>{c.name}</td>
                          <td>{c.totalOrders.toLocaleString('fa-IR')}</td>
                          <td>{c.totalSpent.toLocaleString('fa-IR')} تومان</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </div>
              )}
            </Card>
          </Col>
        </Row>

        {/* آرشیو دوره‌های بسته‌شده */}"""

patch_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    "        {/* آرشیو دوره‌های بسته‌شده */}",
    TOP_SECTIONS,
    "ReportsPage.jsx: افزودن بخش‌های پرفروش‌ترین محصولات و پرخریدترین مشتریان",
)

# ─────────────────────────────────────────────────────────
# 10) index.css — استایل چاپ (print) + no-print
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/index.css",
    "@media (max-width: 576px) {\n"
    "  .auth-card .card-body {\n"
    "    padding: 1.5rem !important;\n"
    "  }\n"
    "  .auth-tabs.nav-pills .nav-link {\n"
    "    padding: 8px 16px;\n"
    "    font-size: 0.85rem;\n"
    "    margin: 0 2px;\n"
    "  }\n"
    "  .otp-input {\n"
    "    letter-spacing: 6px;\n"
    "    font-size: 1.2rem;\n"
    "  }\n"
    "}",
    "@media (max-width: 576px) {\n"
    "  .auth-card .card-body {\n"
    "    padding: 1.5rem !important;\n"
    "  }\n"
    "  .auth-tabs.nav-pills .nav-link {\n"
    "    padding: 8px 16px;\n"
    "    font-size: 0.85rem;\n"
    "    margin: 0 2px;\n"
    "  }\n"
    "  .otp-input {\n"
    "    letter-spacing: 6px;\n"
    "    font-size: 1.2rem;\n"
    "  }\n"
    "}\n"
    "/* ===== چاپ گزارش (PDF از طریق پرینت مرورگر) ===== */\n"
    "@media print {\n"
    "  .no-print,\n"
    "  header,\n"
    "  nav,\n"
    "  .navbar,\n"
    "  footer,\n"
    "  .modal,\n"
    "  .btn {\n"
    "    display: none !important;\n"
    "  }\n"
    "  body {\n"
    "    background: #fff !important;\n"
    "  }\n"
    "  .card {\n"
    "    box-shadow: none !important;\n"
    "    border: 1px solid #ddd !important;\n"
    "    break-inside: avoid;\n"
    "  }\n"
    "}",
    "index.css: افزودن استایل @media print",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ تکمیل داشبورد گزارش‌گیری")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("سرور رو ری‌استارت کن و صفحه گزارش‌گیری رو دوباره چک کن.")
