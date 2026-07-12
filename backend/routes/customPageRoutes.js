import express from 'express'
import {
  getCustomPageBySlug,
  getAllCustomPages,
  getCustomPageById,
  createCustomPage,
  updateCustomPage,
  deleteCustomPage,
} from '../controllers/customPageController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.route('/').post(protect, admin, createCustomPage)
router.get('/all', protect, admin, getAllCustomPages)
router.get('/id/:id', protect, admin, getCustomPageById)
router.route('/:id').put(protect, admin, updateCustomPage).delete(protect, admin, deleteCustomPage)
router.get('/:slug', getCustomPageBySlug)

export default router
