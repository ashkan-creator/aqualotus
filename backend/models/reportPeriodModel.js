import mongoose from 'mongoose'

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
