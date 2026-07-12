import asyncHandler from 'express-async-handler'
import crypto from 'crypto'
import LinkPage from '../models/linkPageModel.js'
import Product from '../models/productModel.js'
import logActivity from '../utils/logActivity.js'

const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:3000'

const generateShortCode = async () => {
  // eslint-disable-next-line no-constant-condition
  while (true) {
    const code = crypto.randomBytes(4).toString('hex')
    const exists = await LinkPage.findOne({ 'links.shortCode': code }).select('_id')
    if (!exists) return code
  }
}

const getLinkPageBySlug = asyncHandler(async (req, res) => {
  const page = await LinkPage.findOne({ slug: req.params.slug, isActive: true })
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  const activeLinks = page.links.filter((l) => l.isActive).sort((a, b) => a.order - b.order)

  const productIds = activeLinks.filter((l) => l.type === 'product' && l.productId).map((l) => l.productId)
  const products = productIds.length > 0 ? await Product.find({ _id: { $in: productIds } }) : []
  const productMap = {}
  products.forEach((p) => { productMap[p._id.toString()] = p })

  res.json({
    _id: page._id,
    slug: page.slug,
    title: page.title,
    bio: page.bio,
    avatar: page.avatar,
    links: activeLinks.map((l) => ({
      _id: l._id,
      label: l.label,
      icon: l.icon,
      order: l.order,
      type: l.type,
      shortUrl: `${FRONTEND_URL}/l/${l.shortCode}`,
      product: l.type === 'product' && l.productId ? productMap[l.productId.toString()] || null : null,
    })),
  })
})

const getAllLinkPages = asyncHandler(async (req, res) => {
  const pages = await LinkPage.find({}).sort({ createdAt: -1 })
  res.json(pages)
})

const getLinkPageById = asyncHandler(async (req, res) => {
  const page = await LinkPage.findById(req.params.id)
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  res.json(page)
})

const createLinkPage = asyncHandler(async (req, res) => {
  const { slug, title, bio, avatar } = req.body
  const exists = await LinkPage.findOne({ slug })
  if (exists) {
    res.status(400)
    throw new Error('این اسلاگ قبلاً استفاده شده')
  }
  const page = await LinkPage.create({ slug, title, bio, avatar: avatar || '', links: [] })
  await logActivity(req.user, 'ساخت صفحه لینک', 'LinkPage', page._id.toString(), page.slug)
  res.status(201).json(page)
})

const updateLinkPage = asyncHandler(async (req, res) => {
  const page = await LinkPage.findById(req.params.id)
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  page.title = req.body.title ?? page.title
  page.bio = req.body.bio ?? page.bio
  page.avatar = req.body.avatar ?? page.avatar
  page.isActive = req.body.isActive ?? page.isActive
  const updated = await page.save()
  await logActivity(req.user, 'ویرایش صفحه لینک', 'LinkPage', updated._id.toString(), updated.slug)
  res.json(updated)
})

const deleteLinkPage = asyncHandler(async (req, res) => {
  const page = await LinkPage.findById(req.params.id)
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  await LinkPage.deleteOne({ _id: page._id })
  await logActivity(req.user, 'حذف صفحه لینک', 'LinkPage', page._id.toString(), page.slug)
  res.json({ message: 'صفحه حذف شد' })
})

const addLink = asyncHandler(async (req, res) => {
  const page = await LinkPage.findById(req.params.id)
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  const { label, url, icon, type, productId } = req.body
  const shortCode = await generateShortCode()
  page.links.push({
    label,
    url,
    icon: icon || '',
    order: page.links.length,
    isActive: true,
    shortCode,
    clicks: 0,
    type: type || 'external',
    productId: productId || null,
  })
  await page.save()
  res.status(201).json(page)
})

const updateLink = asyncHandler(async (req, res) => {
  const page = await LinkPage.findById(req.params.id)
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  const link = page.links.id(req.params.linkId)
  if (!link) {
    res.status(404)
    throw new Error('لینک پیدا نشد')
  }
  link.label = req.body.label ?? link.label
  link.url = req.body.url ?? link.url
  link.icon = req.body.icon ?? link.icon
  link.order = req.body.order ?? link.order
  link.isActive = req.body.isActive ?? link.isActive
  await page.save()
  res.json(page)
})

const deleteLink = asyncHandler(async (req, res) => {
  const page = await LinkPage.findById(req.params.id)
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  page.links = page.links.filter((l) => l._id.toString() !== req.params.linkId)
  await page.save()
  res.json(page)
})

const redirectShortLink = asyncHandler(async (req, res) => {
  const page = await LinkPage.findOne({ 'links.shortCode': req.params.shortCode })
  if (!page) {
    return res.redirect(FRONTEND_URL)
  }
  const link = page.links.find((l) => l.shortCode === req.params.shortCode)
  if (!link) {
    return res.redirect(FRONTEND_URL)
  }
  link.clicks += 1
  await page.save()

  const target = link.url.startsWith('http') ? link.url : `${FRONTEND_URL}${link.url}`
  res.redirect(target)
})

export {
  getLinkPageBySlug,
  getAllLinkPages,
  getLinkPageById,
  createLinkPage,
  updateLinkPage,
  deleteLinkPage,
  addLink,
  updateLink,
  deleteLink,
  redirectShortLink,
}
