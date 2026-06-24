import express from 'express'
import {
  getNotifications,
  getUnreadCount,
  markNotificationRead,
  markAllNotificationsRead,
} from '../controllers/notificationController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.get('/', protect, admin, getNotifications)
router.get('/unread-count', protect, admin, getUnreadCount)
router.put('/read-all', protect, admin, markAllNotificationsRead)
router.put('/:id/read', protect, admin, markNotificationRead)

export default router
