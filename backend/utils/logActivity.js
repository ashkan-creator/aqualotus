import ActivityLog from '../models/activityLogModel.js'

const logActivity = async (admin, action, targetType = '', targetId = '', details = '') => {
  try {
    await ActivityLog.create({
      admin: admin._id,
      adminName: admin.name,
      action,
      targetType,
      targetId,
      details,
    })
  } catch (err) {
    console.error('logActivity error:', err.message)
  }
}

export default logActivity
