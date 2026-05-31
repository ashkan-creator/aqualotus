import mongoose from 'mongoose'

const reviewSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      required: true,
      ref: 'User',
    },
    name: { type: String, required: true },
    rating: { type: Number, required: true },
    comment: { type: String, required: true },
  },
  { timestamps: true }
)

const productSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      required: true,
      ref: 'User',
    },
    name: { type: String, required: true },
    image: { type: String, required: true },
    brand: { type: String, required: true },
    category: {
      type: String,
      required: true,
      enum: ['گیاه زنده', 'کود و مکمل', 'بستر', 'لوازم جانبی'],
    },
    description: { type: String, required: true },
    reviews: [reviewSchema],
    rating: { type: Number, required: true, default: 0 },
    numReviews: { type: Number, required: true, default: 0 },
    price: { type: Number, required: true, default: 0 },
    countInStock: { type: Number, required: true, default: 0 },

    // سیستم تخفیف
    discount: { type: Number, default: 0 },
    discountMinQty: { type: Number, default: 0 },
    discountQtyPercent: { type: Number, default: 0 },

    // ویدیو معرفی محصول
    video: { type: String, default: '' },

    // سختی نگهداری
    careLevel: {
      type: String,
      enum: ['آسان', 'متوسط', 'سخت'],
      default: 'آسان',
    },

    // اطلاعات تکمیلی گیاه
    lightNeeds: {
      type: String,
      enum: ['کم', 'متوسط', 'زیاد'],
      default: 'متوسط',
    },
    co2Needs: {
      type: String,
      enum: ['بدون CO2', 'اختیاری', 'ضروری'],
      default: 'اختیاری',
    },
    growthRate: {
      type: String,
      enum: ['کند', 'متوسط', 'سریع'],
      default: 'متوسط',
    },

    // خانواده گیاه
    family: { type: String, default: '' },

    // محل کاشت در آکواریوم
    position: {
      type: String,
      enum: ['جلو', 'میانه', 'پشت', 'شناور', 'نامشخص'],
      default: 'نامشخص',
    },
  },
  { timestamps: true }
)

const Product = mongoose.model('Product', productSchema)
export default Product