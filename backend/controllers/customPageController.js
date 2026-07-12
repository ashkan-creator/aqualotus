import asyncHandler from 'express-async-handler'
import CustomPage from '../models/customPageModel.js'
import Slider from '../models/sliderModel.js'
import logActivity from '../utils/logActivity.js'

// اگه showInHomeSlider فعال باشه، یه Slider متناظر می‌سازه/آپدیت می‌کنه
// و اگه غیرفعال بشه، اون اسلاید رو حذف می‌کنه.
const syncHomeSlider = async (page) => {
  if (page.showInHomeSlider) {
    const sliderData = {
      title: page.heroTitle,
      subtitle: page.heroSubtitle,
      image: page.heroImage,
      link: `/pages/${page.slug}`,
      isActive: true,
      location: 'home',
    }
    if (page.linkedSliderId) {
      await Slider.findByIdAndUpdate(page.linkedSliderId, sliderData)
    } else {
      const slider = await Slider.create({ ...sliderData, order: 0 })
      page.linkedSliderId = slider._id
      await page.save()
    }
  } else if (page.linkedSliderId) {
    await Slider.deleteOne({ _id: page.linkedSliderId })
    page.linkedSliderId = null
    await page.save()
  }
}

const getCustomPageBySlug = asyncHandler(async (req, res) => {
  const page = await CustomPage.findOne({ slug: req.params.slug, isPublished: true })
    .populate('relatedProducts')
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  res.json(page)
})

const getAllCustomPages = asyncHandler(async (req, res) => {
  const pages = await CustomPage.find({}).sort({ createdAt: -1 })
  res.json(pages)
})

const getCustomPageById = asyncHandler(async (req, res) => {
  const page = await CustomPage.findById(req.params.id).populate('relatedProducts')
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  res.json(page)
})

const createCustomPage = asyncHandler(async (req, res) => {
  const { slug } = req.body
  const exists = await CustomPage.findOne({ slug })
  if (exists) {
    res.status(400)
    throw new Error('این اسلاگ قبلاً استفاده شده')
  }
  const page = await CustomPage.create({ slug })
  await logActivity(req.user, 'ساخت صفحه سفارشی', 'CustomPage', page._id.toString(), page.slug)
  res.status(201).json(page)
})

const updateCustomPage = asyncHandler(async (req, res) => {
  const page = await CustomPage.findById(req.params.id)
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  const fields = [
    'heroImage', 'heroTitle', 'heroSubtitle', 'heroButtonText', 'heroButtonLink',
    'sections', 'relatedProducts', 'showInHomeSlider', 'isPublished',
  ]
  fields.forEach((f) => {
    if (req.body[f] !== undefined) page[f] = req.body[f]
  })
  await syncHomeSlider(page)
  const updated = await page.save()
  await logActivity(req.user, 'ویرایش صفحه سفارشی', 'CustomPage', updated._id.toString(), updated.slug)
  res.json(updated)
})

const deleteCustomPage = asyncHandler(async (req, res) => {
  const page = await CustomPage.findById(req.params.id)
  if (!page) {
    res.status(404)
    throw new Error('صفحه پیدا نشد')
  }
  if (page.linkedSliderId) {
    await Slider.deleteOne({ _id: page.linkedSliderId })
  }
  await CustomPage.deleteOne({ _id: page._id })
  await logActivity(req.user, 'حذف صفحه سفارشی', 'CustomPage', page._id.toString(), page.slug)
  res.json({ message: 'صفحه حذف شد' })
})

export {
  getCustomPageBySlug,
  getAllCustomPages,
  getCustomPageById,
  createCustomPage,
  updateCustomPage,
  deleteCustomPage,
}
