import express from 'express'
import {
  getNotifications,
  getUnreadCount,
  markNotificationRead,
  markAllNotificationsRead,
  getMyNotifications,
  getMyUnreadCount,
  markMyNotificationRead,
  markAllMyNotificationsRead,
} from '../controllers/notificationController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

// نوتیفیکیشن‌های ادمین
router.get('/', protect, admin, getNotifications)
router.get('/unread-count', protect, admin, getUnreadCount)
router.put('/read-all', protect, admin, markAllNotificationsRead)
router.put('/:id/read', protect, admin, markNotificationRead)

// نوتیفیکیشن‌های مشتری
router.get('/mine', protect, getMyNotifications)
router.get('/mine/unread-count', protect, getMyUnreadCount)
router.put('/mine/read-all', protect, markAllMyNotificationsRead)
router.put('/mine/:id/read', protect, markMyNotificationRead)

export default router
