import logActivity from '../utils/logActivity.js'
import asyncHandler from 'express-async-handler'
import Product from '../models/productModel.js'
import Notification from '../models/notificationModel.js'

const getProducts = asyncHandler(async (req, res) => {
  const pageSize = Number(process.env.PAGINATION_LIMIT) || 8
  const page = Number(req.query.pageNumber) || 1

  // ادمین همه رو می‌بینه
  if (req.query.admin === 'true') {
    const products = await Product.find({}).sort({ createdAt: -1 })
    return res.json({ products, page: 1, pages: 1 })
  }

  // فیلترها
  const filter = {}

  if (req.query.keyword) {
    filter.name = { $regex: req.query.keyword, $options: 'i' }
  }
  if (req.query.position) {
    filter.position = req.query.position
  }
  if (req.query.cultivationType) {
    filter.cultivationType = req.query.cultivationType
  }
  if (req.query.needsSoil !== undefined && req.query.needsSoil !== '') {
    filter.needsSoil = req.query.needsSoil === 'true'
  }
  if (req.query.careLevel) {
    filter.careLevel = req.query.careLevel
  }
  if (req.query.category) {
    filter.category = req.query.category
  }
  if (req.query.minPrice || req.query.maxPrice) {
    filter.price = {}
    if (req.query.minPrice) filter.price.$gte = Number(req.query.minPrice)
    if (req.query.maxPrice) filter.price.$lte = Number(req.query.maxPrice)
  }

  const count = await Product.countDocuments(filter)
  const products = await Product.find(filter).sort({ createdAt: -1 })
    .limit(pageSize)
    .skip(pageSize * (page - 1))

  res.json({ products, page, pages: Math.ceil(count / pageSize) })
})

const getProductById = asyncHandler(async (req, res) => {
  const product = await Product.findById(req.params.id)
  if (product) {
    res.json(product)
  } else {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
})

const createProduct = asyncHandler(async (req, res) => {
  const product = new Product({
    name: 'محصول نمونه',
    price: 100000,
    user: req.user._id,
    image: '/images/sample.jpg',
    images: [],
    brand: 'برند نمونه',
    category: 'گیاه زنده',
    countInStock: 10,
    numReviews: 0,
    description: 'توضیحات نمونه',
  })
  const createdProduct = await product.save()
  res.status(201).json(createdProduct)
})

const updateProduct = asyncHandler(async (req, res) => {
  const {
    name, price, description, image, images, video,
    brand, category, countInStock,
    discount, discountMinQty, discountQtyPercent,
    careLevel, lightNeeds, co2Needs, growthRate,
    family, position, cultivationType, needsSoil, variants,
  } = req.body

  const product = await Product.findById(req.params.id)
  if (product) {
    const LOW_STOCK_THRESHOLD = 10

    // ذخیره موجودی قبلی برای مقایسه بعد از سیو
    const prevCountInStock = product.countInStock
    const prevVariantStocks = {}
    ;(product.variants || []).forEach((v) => {
      prevVariantStocks[v.size] = v.countInStock
    })

    product.name = name ?? product.name
    product.price = price ?? product.price
    product.description = description ?? product.description
    product.image = image ?? product.image
    product.images = images ?? product.images
    product.video = video ?? product.video
    product.brand = brand ?? product.brand
    product.category = category ?? product.category
    product.countInStock = countInStock ?? product.countInStock
    product.discount = discount ?? product.discount
    product.discountMinQty = discountMinQty ?? product.discountMinQty
    product.discountQtyPercent = discountQtyPercent ?? product.discountQtyPercent
    product.careLevel = careLevel ?? product.careLevel
    product.lightNeeds = lightNeeds ?? product.lightNeeds
    product.co2Needs = co2Needs ?? product.co2Needs
    product.growthRate = growthRate ?? product.growthRate
    product.family = family ?? product.family
    product.position = position ?? product.position
    product.cultivationType = cultivationType ?? product.cultivationType
    product.needsSoil = needsSoil ?? product.needsSoil
    product.variants = variants ?? product.variants
    const updatedProduct = await product.save()

    if (updatedProduct.variants && updatedProduct.variants.length > 0) {
      for (const v of updatedProduct.variants) {
        const prevStock = prevVariantStocks[v.size]
        const justCrossedThreshold =
          (prevStock === undefined || prevStock >= LOW_STOCK_THRESHOLD) &&
          v.countInStock > 0 &&
          v.countInStock < LOW_STOCK_THRESHOLD
        if (justCrossedThreshold) {
          await Notification.create({
            type: 'low_stock',
            title: 'موجودی رو به اتمام',
            message: `موجودی "${updatedProduct.name}" (سایز ${v.size}) فقط ${v.countInStock} عدد باقی مانده`,
            link: `/admin/product/${updatedProduct._id}/edit`,
            relatedId: updatedProduct._id,
          })
        }
      }
    } else {
      const justCrossedThreshold =
        prevCountInStock >= LOW_STOCK_THRESHOLD &&
        updatedProduct.countInStock > 0 &&
        updatedProduct.countInStock < LOW_STOCK_THRESHOLD
      if (justCrossedThreshold) {
        await Notification.create({
          type: 'low_stock',
          title: 'موجودی رو به اتمام',
          message: `موجودی "${updatedProduct.name}" فقط ${updatedProduct.countInStock} عدد باقی مانده`,
          link: `/admin/product/${updatedProduct._id}/edit`,
          relatedId: updatedProduct._id,
        })
      }
    }

    res.json(updatedProduct)
  } else {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
})

const deleteProduct = asyncHandler(async (req, res) => {
  const product = await Product.findById(req.params.id)
  if (product) {
    await Product.deleteOne({ _id: product._id })
    await logActivity(req.user, 'حذف محصول', 'Product', product._id.toString(), product.name)
    res.json({ message: 'محصول حذف شد' })
  } else {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
})

const recalcProductRating = (product) => {
  const approvedReviews = product.reviews.filter((r) => r.isApproved)
  product.numReviews = approvedReviews.length
  product.rating = approvedReviews.length
    ? approvedReviews.reduce((acc, item) => item.rating + acc, 0) / approvedReviews.length
    : 0
}

const createProductReview = asyncHandler(async (req, res) => {
  const { rating, comment } = req.body
  const product = await Product.findById(req.params.id)
  if (product) {
    const alreadyReviewed = product.reviews.find(
      (r) => r.user.toString() === req.user._id.toString()
    )
    if (alreadyReviewed) {
      res.status(400)
      throw new Error('شما قبلاً نظر خود را ثبت کرده‌اید')
    }
    const review = {
      name: req.user.name,
      rating: Number(rating),
      comment,
      user: req.user._id,
      isApproved: false,
      replies: [],
    }
    product.reviews.push(review)
    recalcProductRating(product)
    await product.save()

    await Notification.create({
      type: 'new_review',
      title: 'نظر جدید در انتظار تایید',
      message: `${req.user.name} روی محصول "${product.name}" نظر ثبت کرد`,
      link: `/product/${product._id}`,
      relatedId: product._id,
    })

    res.status(201).json({ message: 'نظر شما ثبت شد و پس از تایید ادمین نمایش داده می‌شود' })
  } else {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
})

const addReviewReply = asyncHandler(async (req, res) => {
  const { comment } = req.body
  const product = await Product.findById(req.params.id)
  if (!product) {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
  const review = product.reviews.find((r) => r._id.toString() === req.params.reviewId)
  if (!review) {
    res.status(404)
    throw new Error('نظر پیدا نشد')
  }
  const isAdmin = !!req.user.isAdmin
  const reply = {
    name: req.user.name,
    comment,
    user: req.user._id,
    isAdmin,
    isApproved: isAdmin,
  }
  review.replies.push(reply)
  await product.save()

  if (!isAdmin) {
    await Notification.create({
      type: 'new_reply',
      title: 'پاسخ جدید در انتظار تایید',
      message: `${req.user.name} روی یک نظر در محصول "${product.name}" پاسخ ثبت کرد`,
      link: `/product/${product._id}`,
      relatedId: product._id,
    })
  }

  res.status(201).json({
    message: isAdmin ? 'پاسخ شما ثبت شد' : 'پاسخ شما ثبت شد و پس از تایید ادمین نمایش داده می‌شود',
  })
})

const approveProductReview = asyncHandler(async (req, res) => {
  const product = await Product.findById(req.params.id)
  if (!product) {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
  const review = product.reviews.find((r) => r._id.toString() === req.params.reviewId)
  if (!review) {
    res.status(404)
    throw new Error('نظر پیدا نشد')
  }
  review.isApproved = true
  recalcProductRating(product)
  await product.save()
  res.json({ message: 'نظر تایید شد' })
})

const rejectProductReview = asyncHandler(async (req, res) => {
  const product = await Product.findById(req.params.id)
  if (!product) {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
  product.reviews = product.reviews.filter((r) => r._id.toString() !== req.params.reviewId)
  recalcProductRating(product)
  await product.save()
  res.json({ message: 'نظر رد و حذف شد' })
})

const approveReviewReply = asyncHandler(async (req, res) => {
  const product = await Product.findById(req.params.id)
  if (!product) {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
  const review = product.reviews.find((r) => r._id.toString() === req.params.reviewId)
  if (!review) {
    res.status(404)
    throw new Error('نظر پیدا نشد')
  }
  const reply = review.replies.find((r) => r._id.toString() === req.params.replyId)
  if (!reply) {
    res.status(404)
    throw new Error('پاسخ پیدا نشد')
  }
  reply.isApproved = true
  await product.save()
  res.json({ message: 'پاسخ تایید شد' })
})

const rejectReviewReply = asyncHandler(async (req, res) => {
  const product = await Product.findById(req.params.id)
  if (!product) {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
  const review = product.reviews.find((r) => r._id.toString() === req.params.reviewId)
  if (!review) {
    res.status(404)
    throw new Error('نظر پیدا نشد')
  }
  review.replies = review.replies.filter((r) => r._id.toString() !== req.params.replyId)
  await product.save()
  res.json({ message: 'پاسخ رد و حذف شد' })
})

const getPendingReviews = asyncHandler(async (req, res) => {
  const products = await Product.find({
    $or: [{ 'reviews.isApproved': false }, { 'reviews.replies.isApproved': false }],
  }).select('name image reviews')

  const pendingReviews = []
  const pendingReplies = []

  products.forEach((product) => {
    product.reviews.forEach((review) => {
      if (!review.isApproved) {
        pendingReviews.push({
          productId: product._id,
          productName: product.name,
          productImage: product.image,
          reviewId: review._id,
          name: review.name,
          rating: review.rating,
          comment: review.comment,
          createdAt: review.createdAt,
        })
      }
      review.replies.forEach((reply) => {
        if (!reply.isApproved) {
          pendingReplies.push({
            productId: product._id,
            productName: product.name,
            productImage: product.image,
            reviewId: review._id,
            replyId: reply._id,
            name: reply.name,
            comment: reply.comment,
            originalComment: review.comment,
            createdAt: reply.createdAt,
          })
        }
      })
    })
  })

  pendingReviews.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
  pendingReplies.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))

  res.json({ pendingReviews, pendingReplies })
})

const getTopProducts = asyncHandler(async (req, res) => {
  const products = await Product.find({}).sort({ rating: -1 }).limit(3)
  res.json(products)
})

export {
  getProducts, getProductById, createProduct,
  updateProduct, deleteProduct, createProductReview, getTopProducts,
  addReviewReply, approveProductReview, rejectProductReview,
  approveReviewReply, rejectReviewReply, getPendingReviews,
}
