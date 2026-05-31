import asyncHandler from 'express-async-handler'
import Family from '../models/familyModel.js'

// @desc    دریافت همه خانواده‌ها
// @route   GET /api/families
// @access  Public
const getFamilies = asyncHandler(async (req, res) => {
  const families = await Family.find({}).sort({ name: 1 })
  res.json(families)
})

// @desc    ساخت خانواده جدید
// @route   POST /api/families
// @access  Private/Admin
const createFamily = asyncHandler(async (req, res) => {
  const { name, description, icon, category } = req.body
  const exists = await Family.findOne({ name })
  if (exists) {
    res.status(400)
    throw new Error('این خانواده قبلاً ثبت شده')
  }
  const family = await Family.create({ name, description, icon, category })
  res.status(201).json(family)
})

// @desc    آپدیت خانواده
// @route   PUT /api/families/:id
// @access  Private/Admin
const updateFamily = asyncHandler(async (req, res) => {
  const family = await Family.findById(req.params.id)
  if (family) {
    family.name = req.body.name || family.name
    family.description = req.body.description || family.description
    family.icon = req.body.icon || family.icon
    family.category = req.body.category || family.category
    const updated = await family.save()
    res.json(updated)
  } else {
    res.status(404)
    throw new Error('خانواده پیدا نشد')
  }
})

// @desc    حذف خانواده
// @route   DELETE /api/families/:id
// @access  Private/Admin
const deleteFamily = asyncHandler(async (req, res) => {
  const family = await Family.findById(req.params.id)
  if (family) {
    await Family.deleteOne({ _id: family._id })
    res.json({ message: 'خانواده حذف شد' })
  } else {
    res.status(404)
    throw new Error('خانواده پیدا نشد')
  }
})

export { getFamilies, createFamily, updateFamily, deleteFamily }