import asyncHandler from 'express-async-handler'
import Product from '../models/productModel.js'

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
  const products = await Product.find(filter)
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
    res.json({ message: 'محصول حذف شد' })
  } else {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
})

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
    }
    product.reviews.push(review)
    product.numReviews = product.reviews.length
    product.rating =
      product.reviews.reduce((acc, item) => item.rating + acc, 0) /
      product.reviews.length
    await product.save()
    res.status(201).json({ message: 'نظر شما ثبت شد' })
  } else {
    res.status(404)
    throw new Error('محصول پیدا نشد')
  }
})

const getTopProducts = asyncHandler(async (req, res) => {
  const products = await Product.find({}).sort({ rating: -1 }).limit(3)
  res.json(products)
})

export {
  getProducts, getProductById, createProduct,
  updateProduct, deleteProduct, createProductReview, getTopProducts,
}
