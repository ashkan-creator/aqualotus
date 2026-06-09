import mongoose from 'mongoose'

const reviewSchema = new mongoose.Schema(
  {
    user: { type: mongoose.Schema.Types.ObjectId, required: true, ref: 'User' },
    name: { type: String, required: true },
    rating: { type: Number, required: true },
    comment: { type: String, required: true },
  },
  { timestamps: true }
)

// سایزبندی محصول
const variantSchema = new mongoose.Schema({
  size: { type: String, required: true },
  price: { type: Number, required: true },
  countInStock: { type: Number, required: true, default: 0 },
})

const productSchema = new mongoose.Schema(
  {
    user: { type: mongoose.Schema.Types.ObjectId, required: true, ref: 'User' },
    name: { type: String, required: true },
    image: { type: String, required: true },
    images: [{ type: String }],
    cultivationType: {
      type: String,
      enum: ['آبزی', 'هیدروپونیک', 'هر دو'],
      default: 'آبزی',
    },
    needsSoil: { type: Boolean, default: false },
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
    discount: { type: Number, default: 0 },
    discountMinQty: { type: Number, default: 0 },
    discountQtyPercent: { type: Number, default: 0 },
    video: { type: String, default: '' },
    careLevel: { type: String, enum: ['آسان', 'متوسط', 'سخت'], default: 'آسان' },
    lightNeeds: { type: String, enum: ['کم', 'متوسط', 'زیاد'], default: 'متوسط' },
    co2Needs: { type: String, enum: ['بدون CO2', 'اختیاری', 'ضروری'], default: 'اختیاری' },
    growthRate: { type: String, enum: ['کند', 'متوسط', 'سریع'], default: 'متوسط' },
    family: { type: String, default: '' },
    position: {
      type: String,
      enum: ['جلو', 'میانه', 'پشت', 'شناور', 'نامشخص'],
      default: 'نامشخص',
    },
    // سایزبندی - اگه خالی باشه یعنی محصول سایز ندارد
    variants: [variantSchema],
  },
  { timestamps: true }
)

const Product = mongoose.model('Product', productSchema)
export default Product
