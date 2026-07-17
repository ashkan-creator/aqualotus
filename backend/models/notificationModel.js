import mongoose from 'mongoose'

const notificationSchema = new mongoose.Schema(
  {
    type: {
      type: String,
      required: true,
      enum: ['new_review', 'new_reply', 'new_order', 'low_stock', 'new_message', 'order_confirmed', 'order_delivered'],
    },
    title: { type: String, required: true },
    message: { type: String, required: true },
    link: { type: String, default: '' },
    isRead: { type: Boolean, default: false },
    relatedId: { type: mongoose.Schema.Types.ObjectId, default: null },
    user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', default: null },
  },
  { timestamps: true }
)

const Notification = mongoose.model('Notification', notificationSchema)
export default Notification
