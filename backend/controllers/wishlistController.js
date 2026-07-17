import asyncHandler from 'express-async-handler'
import Wishlist from '../models/wishlistModel.js'

// @desc    دریافت لیست علاقه‌مندی‌های کاربر
// @route   GET /api/wishlist
// @access  Private
const getMyWishlist = asyncHandler(async (req, res) => {
  const items = await Wishlist.find({ user: req.user._id })
    .sort({ createdAt: -1 })
    .populate('product')

  // فقط محصولاتی که هنوز وجود دارن (ممکنه محصول حذف شده باشه)
  const products = items.filter((item) => item.product).map((item) => item.product)
  res.json(products)
})

// @desc    افزودن محصول به علاقه‌مندی‌ها
// @route   POST /api/wishlist
// @access  Private
const addToWishlist = asyncHandler(async (req, res) => {
  const { productId } = req.body

  if (!productId) {
    res.status(400)
    throw new Error('شناسه محصول ارسال نشده است')
  }

  try {
    await Wishlist.create({ user: req.user._id, product: productId })
  } catch (err) {
    // اگه از قبل تو لیست بود (خطای ایندکس یکتا)، مشکلی نیست
    if (err.code !== 11000) {
      throw err
    }
  }

  res.status(201).json({ message: 'به علاقه‌مندی‌ها اضافه شد' })
})

// @desc    حذف محصول از علاقه‌مندی‌ها
// @route   DELETE /api/wishlist/:productId
// @access  Private
const removeFromWishlist = asyncHandler(async (req, res) => {
  await Wishlist.deleteOne({ user: req.user._id, product: req.params.productId })
  res.json({ message: 'از علاقه‌مندی‌ها حذف شد' })
})

export { getMyWishlist, addToWishlist, removeFromWishlist }
