#!/usr/bin/env python3
"""
اسکریپت پچ: داشبورد آمار و گزارش‌گیری ادمین (بازه زمانی + بستن دوره)
اجرا از ریشه پروژه: python3 apply_reports_dashboard.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-reports-backup"

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
# 1) reportPeriodModel.js (جدید)
# ─────────────────────────────────────────────────────────
create_new_file(
    "backend/models/reportPeriodModel.js",
    """import mongoose from 'mongoose'

const reportPeriodSchema = new mongoose.Schema(
  {
    startDate: { type: Date, required: true },
    endDate: { type: Date, required: true },
    totalOrders: { type: Number, default: 0 },
    paidOrders: { type: Number, default: 0 },
    deliveredOrders: { type: Number, default: 0 },
    totalRevenue: { type: Number, default: 0 },
    closedBy: { type: String, default: '' },
    note: { type: String, default: '' },
  },
  { timestamps: true }
)

const ReportPeriod = mongoose.model('ReportPeriod', reportPeriodSchema)
export default ReportPeriod
""",
    "reportPeriodModel.js ساخته شد",
)

# ─────────────────────────────────────────────────────────
# 2) reportController.js (جدید)
# ─────────────────────────────────────────────────────────
create_new_file(
    "backend/controllers/reportController.js",
    """import asyncHandler from 'express-async-handler'
import Order from '../models/orderModel.js'
import Settings from '../models/settingsModel.js'
import ReportPeriod from '../models/reportPeriodModel.js'
import logActivity from '../utils/logActivity.js'

const PERIOD_KEY = 'currentPeriodStart'

const computeStats = (orders) => {
  const totalOrders = orders.length
  const paidOrders = orders.filter((o) => o.isPaid).length
  const deliveredOrders = orders.filter((o) => o.isDelivered).length
  const totalRevenue = orders
    .filter((o) => o.isPaid)
    .reduce((acc, o) => acc + o.totalPrice, 0)
  return { totalOrders, paidOrders, deliveredOrders, totalRevenue }
}

// @desc    آمار بازه زمانی دلخواه
// @route   GET /api/reports/stats?startDate=&endDate=
// @access  Private/Admin
const getReportStats = asyncHandler(async (req, res) => {
  const { startDate, endDate } = req.query
  if (!startDate || !endDate) {
    res.status(400)
    throw new Error('بازه زمانی الزامی است')
  }
  const start = new Date(startDate)
  const end = new Date(endDate)
  end.setHours(23, 59, 59, 999)

  const orders = await Order.find({
    createdAt: { $gte: start, $lte: end },
  }).select('totalPrice isPaid isDelivered createdAt')

  const { totalOrders, paidOrders, deliveredOrders, totalRevenue } = computeStats(orders)
  const avgOrderValue = paidOrders > 0 ? Math.round(totalRevenue / paidOrders) : 0

  const dailyMap = {}
  orders.forEach((o) => {
    const day = o.createdAt.toISOString().slice(0, 10)
    if (!dailyMap[day]) dailyMap[day] = { date: day, orders: 0, revenue: 0 }
    dailyMap[day].orders += 1
    if (o.isPaid) dailyMap[day].revenue += o.totalPrice
  })
  const daily = Object.values(dailyMap).sort((a, b) => a.date.localeCompare(b.date))

  res.json({
    startDate: start,
    endDate: end,
    totalOrders,
    paidOrders,
    deliveredOrders,
    totalRevenue,
    avgOrderValue,
    daily,
  })
})

// @desc    دریافت تاریخ شروع دوره فعلی
// @route   GET /api/reports/current-period
// @access  Private/Admin
const getCurrentPeriod = asyncHandler(async (req, res) => {
  let setting = await Settings.findOne({ key: PERIOD_KEY })
  if (!setting) {
    setting = await Settings.create({ key: PERIOD_KEY, value: new Date().toISOString() })
  }
  res.json({ startDate: setting.value })
})

// @desc    بستن دوره فعلی، آرشیو کردن آمار، و شروع دوره جدید از صفر
// @route   POST /api/reports/close-period
// @access  Private/Admin
const closePeriod = asyncHandler(async (req, res) => {
  const { note } = req.body

  let setting = await Settings.findOne({ key: PERIOD_KEY })
  const startDate = setting ? new Date(setting.value) : new Date(0)
  const endDate = new Date()

  const orders = await Order.find({
    createdAt: { $gte: startDate, $lte: endDate },
  }).select('totalPrice isPaid isDelivered')

  const { totalOrders, paidOrders, deliveredOrders, totalRevenue } = computeStats(orders)

  const archived = await ReportPeriod.create({
    startDate,
    endDate,
    totalOrders,
    paidOrders,
    deliveredOrders,
    totalRevenue,
    closedBy: req.user.name,
    note: note || '',
  })

  await Settings.findOneAndUpdate(
    { key: PERIOD_KEY },
    { value: endDate.toISOString() },
    { new: true, upsert: true }
  )

  await logActivity(
    req.user,
    'بستن دوره گزارش‌گیری',
    'ReportPeriod',
    archived._id.toString(),
    `${totalOrders} سفارش`
  )

  res.status(201).json(archived)
})

// @desc    لیست دوره‌های بسته‌شده (آرشیو)
// @route   GET /api/reports/periods
// @access  Private/Admin
const getClosedPeriods = asyncHandler(async (req, res) => {
  const periods = await ReportPeriod.find({}).sort({ endDate: -1 })
  res.json(periods)
})

export { getReportStats, getCurrentPeriod, closePeriod, getClosedPeriods }
""",
    "reportController.js ساخته شد",
)

# ─────────────────────────────────────────────────────────
# 3) reportRoutes.js (جدید)
# ─────────────────────────────────────────────────────────
create_new_file(
    "backend/routes/reportRoutes.js",
    """import express from 'express'
import {
  getReportStats,
  getCurrentPeriod,
  closePeriod,
  getClosedPeriods,
} from '../controllers/reportController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.get('/stats', protect, admin, getReportStats)
router.get('/current-period', protect, admin, getCurrentPeriod)
router.post('/close-period', protect, admin, closePeriod)
router.get('/periods', protect, admin, getClosedPeriods)

export default router
""",
    "reportRoutes.js ساخته شد",
)

# ─────────────────────────────────────────────────────────
# 4) server.js — import و mount روت جدید
# ─────────────────────────────────────────────────────────
patch_file(
    "backend/server.js",
    "import wishlistRoutes from './routes/wishlistRoutes.js'",
    "import wishlistRoutes from './routes/wishlistRoutes.js'\n"
    "import reportRoutes from './routes/reportRoutes.js'",
    "server.js: افزودن import reportRoutes",
)

patch_file(
    "backend/server.js",
    "app.use('/api/wishlist', wishlistRoutes)",
    "app.use('/api/wishlist', wishlistRoutes)\n"
    "app.use('/api/reports', reportRoutes)",
    "server.js: mount کردن /api/reports",
)

# ─────────────────────────────────────────────────────────
# 5) constants.js — REPORTS_URL
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/constants.js",
    "export const FAMILIES_URL = '/api/families'",
    "export const FAMILIES_URL = '/api/families'\n"
    "export const REPORTS_URL = '/api/reports'",
    "constants.js: افزودن REPORTS_URL",
)

# ─────────────────────────────────────────────────────────
# 6) reportsApiSlice.js (جدید)
# ─────────────────────────────────────────────────────────
create_new_file(
    "frontend/src/slices/reportsApiSlice.js",
    """import { apiSlice } from './apiSlice'
import { REPORTS_URL } from '../constants'

export const reportsApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getReportStats: builder.query({
      query: ({ startDate, endDate }) => ({
        url: `${REPORTS_URL}/stats`,
        params: { startDate, endDate },
      }),
      keepUnusedDataFor: 5,
    }),
    getCurrentPeriod: builder.query({
      query: () => ({
        url: `${REPORTS_URL}/current-period`,
      }),
      keepUnusedDataFor: 5,
    }),
    closePeriod: builder.mutation({
      query: (data) => ({
        url: `${REPORTS_URL}/close-period`,
        method: 'POST',
        body: data,
      }),
    }),
    getClosedPeriods: builder.query({
      query: () => ({
        url: `${REPORTS_URL}/periods`,
      }),
      keepUnusedDataFor: 5,
    }),
  }),
})

export const {
  useGetReportStatsQuery,
  useGetCurrentPeriodQuery,
  useClosePeriodMutation,
  useGetClosedPeriodsQuery,
} = reportsApiSlice
""",
    "reportsApiSlice.js ساخته شد",
)

# ─────────────────────────────────────────────────────────
# 7) ReportsPage.jsx (جدید)
# ─────────────────────────────────────────────────────────
create_new_file(
    "frontend/src/pages/admin/ReportsPage.jsx",
    """import { useState } from 'react'
import { Container, Row, Col, Card, Table, Button, Form, Modal } from 'react-bootstrap'
import { toast } from 'react-toastify'
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
} from 'recharts'
import {
  useGetReportStatsQuery,
  useGetCurrentPeriodQuery,
  useClosePeriodMutation,
  useGetClosedPeriodsQuery,
} from '../../slices/reportsApiSlice'
import Loader from '../../components/ui/Loader'
import { Helmet } from 'react-helmet-async'

const toInputDate = (d) => new Date(d).toISOString().slice(0, 10)

const ReportsPage = () => {
  const today = toInputDate(new Date())
  const monthAgo = toInputDate(new Date(Date.now() - 29 * 24 * 60 * 60 * 1000))

  const [startDate, setStartDate] = useState(monthAgo)
  const [endDate, setEndDate] = useState(today)
  const [showCloseModal, setShowCloseModal] = useState(false)
  const [closeNote, setCloseNote] = useState('')

  const { data: stats, isLoading: statsLoading } = useGetReportStatsQuery({ startDate, endDate })
  const { data: currentPeriod, isLoading: periodLoading, refetch: refetchPeriod } = useGetCurrentPeriodQuery()
  const { data: closedPeriods, isLoading: closedLoading, refetch: refetchClosed } = useGetClosedPeriodsQuery()
  const [closePeriod, { isLoading: closing }] = useClosePeriodMutation()

  const closeHandler = async () => {
    try {
      await closePeriod({ note: closeNote }).unwrap()
      toast.success('دوره با موفقیت بسته و آرشیو شد')
      setShowCloseModal(false)
      setCloseNote('')
      refetchPeriod()
      refetchClosed()
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در بستن دوره')
    }
  }

  const chartData =
    stats?.daily?.map((d) => ({
      ...d,
      label: new Date(d.date).toLocaleDateString('fa-IR', { month: 'short', day: 'numeric' }),
    })) || []

  return (
    <>
      <Helmet><title>گزارش‌گیری | پنل ادمین</title></Helmet>
      <Container className='py-4'>
        <h2 className='mb-4' style={{ fontSize: 'clamp(1rem, 4vw, 1.5rem)' }}>📊 داشبورد آمار و گزارش‌گیری</h2>

        {/* دوره فعلی */}
        <Card className='p-3 mb-4'>
          <Row className='align-items-center g-3'>
            <Col xs={12} md={8}>
              <h6 className='mb-1'>دوره فعلی</h6>
              {periodLoading ? (
                <Loader />
              ) : (
                <p className='mb-0 text-muted' style={{ fontSize: '0.9rem' }}>
                  از تاریخ{' '}
                  {currentPeriod?.startDate
                    ? new Date(currentPeriod.startDate).toLocaleDateString('fa-IR')
                    : '-'}{' '}
                  تا امروز
                </p>
              )}
            </Col>
            <Col xs={12} md={4} className='text-md-end'>
              <Button variant='danger' onClick={() => setShowCloseModal(true)}>
                🔒 بستن دوره فعلی
              </Button>
            </Col>
          </Row>
        </Card>

        {/* بازه زمانی گزارش */}
        <Card className='p-3 mb-4'>
          <Row className='g-3 align-items-end'>
            <Col xs={6} md={3}>
              <Form.Group>
                <Form.Label>از تاریخ</Form.Label>
                <Form.Control type='date' value={startDate} onChange={(e) => setStartDate(e.target.value)} />
              </Form.Group>
            </Col>
            <Col xs={6} md={3}>
              <Form.Group>
                <Form.Label>تا تاریخ</Form.Label>
                <Form.Control type='date' value={endDate} onChange={(e) => setEndDate(e.target.value)} />
              </Form.Group>
            </Col>
          </Row>
        </Card>

        {/* کارت‌های آمار بازه انتخابی */}
        {statsLoading ? (
          <Loader />
        ) : (
          stats && (
            <>
              <Row className='g-3 mb-4'>
                <Col xs={6} lg={3}>
                  <Card className='h-100 text-white' style={{ background: '#2d6a4f' }}>
                    <Card.Body className='p-3'>
                      <div style={{ fontSize: 'clamp(0.9rem, 3vw, 1.4rem)', fontWeight: 'bold' }}>
                        {(stats.totalRevenue / 1000).toFixed(0)} هزار ت
                      </div>
                      <div style={{ fontSize: '0.8rem', opacity: 0.9 }}>درآمد بازه</div>
                    </Card.Body>
                  </Card>
                </Col>
                <Col xs={6} lg={3}>
                  <Card className='h-100 text-white' style={{ background: '#0d4f8b' }}>
                    <Card.Body className='p-3'>
                      <div style={{ fontSize: 'clamp(0.9rem, 3vw, 1.4rem)', fontWeight: 'bold' }}>
                        {stats.totalOrders}
                      </div>
                      <div style={{ fontSize: '0.8rem', opacity: 0.9 }}>کل سفارش‌ها</div>
                    </Card.Body>
                  </Card>
                </Col>
                <Col xs={6} lg={3}>
                  <Card className='h-100 text-white' style={{ background: '#52b788' }}>
                    <Card.Body className='p-3'>
                      <div style={{ fontSize: 'clamp(0.9rem, 3vw, 1.4rem)', fontWeight: 'bold' }}>
                        {stats.paidOrders}
                      </div>
                      <div style={{ fontSize: '0.8rem', opacity: 0.9 }}>پرداخت‌شده</div>
                    </Card.Body>
                  </Card>
                </Col>
                <Col xs={6} lg={3}>
                  <Card className='h-100 text-white' style={{ background: '#6a4c2d' }}>
                    <Card.Body className='p-3'>
                      <div style={{ fontSize: 'clamp(0.9rem, 3vw, 1.4rem)', fontWeight: 'bold' }}>
                        {(stats.avgOrderValue / 1000).toFixed(0)} هزار ت
                      </div>
                      <div style={{ fontSize: '0.8rem', opacity: 0.9 }}>میانگین سفارش</div>
                    </Card.Body>
                  </Card>
                </Col>
              </Row>

              {chartData.length > 0 && (
                <Card className='p-3 mb-4'>
                  <h6 className='mb-3'>روند درآمد بازه انتخابی</h6>
                  <ResponsiveContainer width='100%' height={220}>
                    <AreaChart data={chartData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                      <defs>
                        <linearGradient id='colorRepRev' x1='0' y1='0' x2='0' y2='1'>
                          <stop offset='5%' stopColor='#2d6a4f' stopOpacity={0.3} />
                          <stop offset='95%' stopColor='#2d6a4f' stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray='3 3' stroke='#f0f0f0' />
                      <XAxis dataKey='label' tick={{ fontSize: 11 }} />
                      <YAxis tick={{ fontSize: 11 }} />
                      <Tooltip />
                      <Area type='monotone' dataKey='revenue' stroke='#2d6a4f' fill='url(#colorRepRev)' strokeWidth={2} />
                    </AreaChart>
                  </ResponsiveContainer>
                </Card>
              )}
            </>
          )
        )}

        {/* آرشیو دوره‌های بسته‌شده */}
        <Card className='p-3'>
          <h5 className='mb-3'>📁 آرشیو دوره‌های بسته‌شده</h5>
          {closedLoading ? (
            <Loader />
          ) : !closedPeriods?.length ? (
            <p className='text-muted mb-0'>هنوز هیچ دوره‌ای بسته نشده است</p>
          ) : (
            <div className='table-responsive'>
              <Table striped hover>
                <thead>
                  <tr>
                    <th>از تاریخ</th>
                    <th>تا تاریخ</th>
                    <th>سفارش‌ها</th>
                    <th>پرداخت‌شده</th>
                    <th>درآمد</th>
                    <th>بسته‌شده توسط</th>
                    <th>یادداشت</th>
                  </tr>
                </thead>
                <tbody>
                  {closedPeriods.map((p) => (
                    <tr key={p._id}>
                      <td>{new Date(p.startDate).toLocaleDateString('fa-IR')}</td>
                      <td>{new Date(p.endDate).toLocaleDateString('fa-IR')}</td>
                      <td>{p.totalOrders}</td>
                      <td>{p.paidOrders}</td>
                      <td>{p.totalRevenue.toLocaleString('fa-IR')} تومان</td>
                      <td>{p.closedBy}</td>
                      <td>{p.note || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}
        </Card>
      </Container>

      {/* مودال تایید بستن دوره */}
      <Modal show={showCloseModal} onHide={() => setShowCloseModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>بستن دوره فعلی</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>
            با بستن دوره، آمار از تاریخ{' '}
            {currentPeriod?.startDate ? new Date(currentPeriod.startDate).toLocaleDateString('fa-IR') : '-'}{' '}
            تا الان آرشیو می‌شود و شمارنده «دوره فعلی» از همین لحظه صفر شده و از نو شروع می‌شود. این کار قابل بازگشت نیست.
          </p>
          <Form.Group>
            <Form.Label>یادداشت (اختیاری)</Form.Label>
            <Form.Control
              as='textarea'
              rows={2}
              value={closeNote}
              onChange={(e) => setCloseNote(e.target.value)}
              placeholder='مثلاً: پایان فصل بهار'
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant='secondary' onClick={() => setShowCloseModal(false)}>
            انصراف
          </Button>
          <Button variant='danger' onClick={closeHandler} disabled={closing}>
            {closing ? 'در حال بستن...' : 'تایید و بستن دوره'}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

export default ReportsPage
""",
    "ReportsPage.jsx ساخته شد",
)

# ─────────────────────────────────────────────────────────
# 8) main.jsx — lazy import و روت جدید
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/main.jsx",
    "const AdminDashboardPage = lazy(() => import('./pages/admin/DashboardPage'))",
    "const AdminDashboardPage = lazy(() => import('./pages/admin/DashboardPage'))\n"
    "const AdminReportsPage = lazy(() => import('./pages/admin/ReportsPage'))",
    "main.jsx: افزودن lazy import ReportsPage",
)

patch_file(
    "frontend/src/main.jsx",
    "          { path: 'dashboard', element: withSuspense(AdminDashboardPage) },",
    "          { path: 'dashboard', element: withSuspense(AdminDashboardPage) },\n"
    "          { path: 'reports', element: withSuspense(AdminReportsPage) },",
    "main.jsx: افزودن روت admin/reports",
)

# ─────────────────────────────────────────────────────────
# 9) Header.jsx — لینک منو
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/components/layout/Header.jsx",
    "                      <LinkContainer to='/admin/dashboard'><NavDropdown.Item>📊 داشبورد</NavDropdown.Item></LinkContainer>",
    "                      <LinkContainer to='/admin/dashboard'><NavDropdown.Item>📊 داشبورد</NavDropdown.Item></LinkContainer>\n"
    "                      <LinkContainer to='/admin/reports'><NavDropdown.Item>📈 گزارش‌گیری</NavDropdown.Item></LinkContainer>",
    "Header.jsx: افزودن لینک «گزارش‌گیری» به منوی ادمین",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ داشبورد آمار و گزارش‌گیری")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("سرور رو ری‌استارت کن (npm run dev) و از منوی ادمین وارد «📈 گزارش‌گیری» شو.")
