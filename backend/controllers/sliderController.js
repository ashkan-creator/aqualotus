import asyncHandler from 'express-async-handler'
import Slider from '../models/sliderModel.js'

// @desc    دریافت همه اسلایدهای فعال
// @route   GET /api/sliders
// @access  Public
const getSliders = asyncHandler(async (req, res) => {
  const sliders = await Slider.find({ isActive: true }).sort({ order: 1 })
  res.json(sliders)
})

// @desc    دریافت همه اسلایدها برای ادمین
// @route   GET /api/sliders/all
// @access  Private/Admin
const getAllSliders = asyncHandler(async (req, res) => {
  const sliders = await Slider.find({}).sort({ order: 1 })
  res.json(sliders)
})

// @desc    ساخت اسلاید جدید
// @route   POST /api/sliders
// @access  Private/Admin
const createSlider = asyncHandler(async (req, res) => {
  const { title, image, link, order } = req.body
  const slider = await Slider.create({ title, image, link, order })
  res.status(201).json(slider)
})

// @desc    آپدیت اسلاید
// @route   PUT /api/sliders/:id
// @access  Private/Admin
const updateSlider = asyncHandler(async (req, res) => {
  const slider = await Slider.findById(req.params.id)
  if (slider) {
    slider.title = req.body.title ?? slider.title
    slider.image = req.body.image ?? slider.image
    slider.link = req.body.link ?? slider.link
    slider.isActive = req.body.isActive ?? slider.isActive
    slider.order = req.body.order ?? slider.order
    const updated = await slider.save()
    res.json(updated)
  } else {
    res.status(404)
    throw new Error('اسلاید پیدا نشد')
  }
})

// @desc    حذف اسلاید
// @route   DELETE /api/sliders/:id
// @access  Private/Admin
const deleteSlider = asyncHandler(async (req, res) => {
  const slider = await Slider.findById(req.params.id)
  if (slider) {
    await Slider.deleteOne({ _id: slider._id })
    res.json({ message: 'اسلاید حذف شد' })
  } else {
    res.status(404)
    throw new Error('اسلاید پیدا نشد')
  }
})

export { getSliders, getAllSliders, createSlider, updateSlider, deleteSlider }
