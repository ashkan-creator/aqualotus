import mongoose from 'mongoose'

const wishlistSchema = new mongoose.Schema(
  {
    user: { type: mongoose.Schema.Types.ObjectId, required: true, ref: 'User' },
    product: { type: mongoose.Schema.Types.ObjectId, required: true, ref: 'Product' },
  },
  { timestamps: true }
)

// جلوگیری از افزودن یک محصول به‌صورت تکراری برای یک کاربر
wishlistSchema.index({ user: 1, product: 1 }, { unique: true })

const Wishlist = mongoose.model('Wishlist', wishlistSchema)
export default Wishlist
