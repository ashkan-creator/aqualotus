import mongoose from 'mongoose'

const activityLogSchema = new mongoose.Schema(
  {
    admin: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    adminName: { type: String, required: true },
    action: { type: String, required: true },
    targetType: { type: String },
    targetId: { type: String },
    details: { type: String },
  },
  { timestamps: true }
)

const ActivityLog = mongoose.model('ActivityLog', activityLogSchema)
export default ActivityLog
