import express from 'express'
import {
  getSliders,
  getAllSliders,
  createSlider,
  updateSlider,
  deleteSlider,
} from '../controllers/sliderController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()
router.route('/').get(getSliders).post(protect, admin, createSlider)
router.get('/all', protect, admin, getAllSliders)
router.route('/:id').put(protect, admin, updateSlider).delete(protect, admin, deleteSlider)

export default router
