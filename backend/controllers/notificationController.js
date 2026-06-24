import asyncHandler from 'express-async-handler'
import Notification from '../models/notificationModel.js'

const getNotifications = asyncHandler(async (req, res) => {
  const notifications = await Notification.find({}).sort({ createdAt: -1 }).limit(50)
  res.json(notifications)
})

const getUnreadCount = asyncHandler(async (req, res) => {
  const count = await Notification.countDocuments({ isRead: false })
  res.json({ count })
})

const markNotificationRead = asyncHandler(async (req, res) => {
  const notification = await Notification.findById(req.params.id)
  if (!notification) {
    res.status(404)
    throw new Error('نوتیفیکیشن پیدا نشد')
  }
  notification.isRead = true
  await notification.save()
  res.json({ message: 'نوتیفیکیشن خوانده شد' })
})

const markAllNotificationsRead = asyncHandler(async (req, res) => {
  await Notification.updateMany({ isRead: false }, { $set: { isRead: true } })
  res.json({ message: 'همه نوتیفیکیشن‌ها خوانده شد' })
})

export {
  getNotifications,
  getUnreadCount,
  markNotificationRead,
  markAllNotificationsRead,
}
