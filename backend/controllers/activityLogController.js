import asyncHandler from 'express-async-handler'
import ActivityLog from '../models/activityLogModel.js'

// @desc    دریافت لاگ فعالیت‌های ادمین
// @route   GET /api/activity-logs
// @access  Private/Admin
const getActivityLogs = asyncHandler(async (req, res) => {
  const logs = await ActivityLog.find({})
    .sort({ createdAt: -1 })
    .limit(100)
  res.json(logs)
})

export { getActivityLogs }
