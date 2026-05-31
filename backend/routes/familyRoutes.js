import express from 'express'
import {
  getFamilies,
  createFamily,
  updateFamily,
  deleteFamily,
} from '../controllers/familyController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.route('/')
  .get(getFamilies)
  .post(protect, admin, createFamily)

router.route('/:id')
  .put(protect, admin, updateFamily)
  .delete(protect, admin, deleteFamily)

export default router