import express from 'express'
import {
  getReportStats,
  getCurrentPeriod,
  closePeriod,
  getClosedPeriods,
  getTopProducts,
  getTopCustomers,
} from '../controllers/reportController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.get('/stats', protect, admin, getReportStats)
router.get('/current-period', protect, admin, getCurrentPeriod)
router.post('/close-period', protect, admin, closePeriod)
router.get('/periods', protect, admin, getClosedPeriods)
router.get('/top-products', protect, admin, getTopProducts)
router.get('/top-customers', protect, admin, getTopCustomers)

export default router
