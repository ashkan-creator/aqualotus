import asyncHandler from 'express-async-handler'
import Notification from '../models/notificationModel.js'

// ===== نوتیفیکیشن‌های ادمین =====

const getNotifications = asyncHandler(async (req, res) => {
  const notifications = await Notification.find({ user: null }).sort({ createdAt: -1 }).limit(50)
  res.json(notifications)
})

const getUnreadCount = asyncHandler(async (req, res) => {
  const count = await Notification.countDocuments({ user: null, isRead: false })
  res.json({ count })
})

const markNotificationRead = asyncHandler(async (req, res) => {
  const notification = await Notification.findOne({ _id: req.params.id, user: null })
  if (!notification) {
    res.status(404)
    throw new Error('نوتیفیکیشن پیدا نشد')
  }
  notification.isRead = true
  await notification.save()
  res.json({ message: 'نوتیفیکیشن خوانده شد' })
})

const markAllNotificationsRead = asyncHandler(async (req, res) => {
  await Notification.updateMany({ user: null, isRead: false }, { $set: { isRead: true } })
  res.json({ message: 'همه نوتیفیکیشن‌ها خوانده شد' })
})

// ===== نوتیفیکیشن‌های مشتری =====

const getMyNotifications = asyncHandler(async (req, res) => {
  const notifications = await Notification.find({ user: req.user._id }).sort({ createdAt: -1 }).limit(50)
  res.json(notifications)
})

const getMyUnreadCount = asyncHandler(async (req, res) => {
  const count = await Notification.countDocuments({ user: req.user._id, isRead: false })
  res.json({ count })
})

const markMyNotificationRead = asyncHandler(async (req, res) => {
  const notification = await Notification.findOne({ _id: req.params.id, user: req.user._id })
  if (!notification) {
    res.status(404)
    throw new Error('نوتیفیکیشن پیدا نشد')
  }
  notification.isRead = true
  await notification.save()
  res.json({ message: 'نوتیفیکیشن خوانده شد' })
})

const markAllMyNotificationsRead = asyncHandler(async (req, res) => {
  await Notification.updateMany({ user: req.user._id, isRead: false }, { $set: { isRead: true } })
  res.json({ message: 'همه نوتیفیکیشن‌ها خوانده شد' })
})

export {
  getNotifications,
  getUnreadCount,
  markNotificationRead,
  markAllNotificationsRead,
  getMyNotifications,
  getMyUnreadCount,
  markMyNotificationRead,
  markAllMyNotificationsRead,
}
