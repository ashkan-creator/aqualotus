import asyncHandler from 'express-async-handler'
import Settings from '../models/settingsModel.js'

// @desc    دریافت همه تنظیمات
// @route   GET /api/settings
// @access  Public
const getSettings = asyncHandler(async (req, res) => {
  const settings = await Settings.find({})
  const result = {}
  settings.forEach((s) => (result[s.key] = s.value))
  res.json(result)
})

// @desc    آپدیت یک تنظیم
// @route   PUT /api/settings/:key
// @access  Private/Admin
const updateSetting = asyncHandler(async (req, res) => {
  const { value } = req.body
  const setting = await Settings.findOneAndUpdate(
    { key: req.params.key },
    { value },
    { new: true, upsert: true }
  )
  res.json(setting)
})

export { getSettings, updateSetting }
