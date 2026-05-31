import mongoose from 'mongoose'

const familySchema = new mongoose.Schema(
  {
    name: { type: String, required: true, unique: true }, // نام خانواده (آنوبیاس، موس...)
    description: { type: String, default: '' },           // توضیحات
    icon: { type: String, default: '🌿' },               // آیکون
    category: {                                           // دسته کلی
      type: String,
      enum: ['گیاه زنده', 'کود و مکمل', 'بستر', 'لوازم جانبی'],
      default: 'گیاه زنده',
    },
  },
  { timestamps: true }
)

const Family = mongoose.model('Family', familySchema)
export default Family