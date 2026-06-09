import express from 'express'
import { getSettings, updateSetting } from '../controllers/settingsController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()
router.route('/').get(getSettings)
router.route('/:key').put(protect, admin, updateSetting)

export default router
