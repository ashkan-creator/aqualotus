import express from 'express'
import { getActivityLogs } from '../controllers/activityLogController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.get('/', protect, admin, getActivityLogs)

export default router
