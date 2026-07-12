import express from 'express'
import {
  getLinkPageBySlug,
  getAllLinkPages,
  getLinkPageById,
  createLinkPage,
  updateLinkPage,
  deleteLinkPage,
  addLink,
  updateLink,
  deleteLink,
} from '../controllers/linkPageController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.route('/').post(protect, admin, createLinkPage)
router.get('/all', protect, admin, getAllLinkPages)
router.get('/id/:id', protect, admin, getLinkPageById)
router.route('/:id').put(protect, admin, updateLinkPage).delete(protect, admin, deleteLinkPage)
router.post('/:id/links', protect, admin, addLink)
router.route('/:id/links/:linkId').put(protect, admin, updateLink).delete(protect, admin, deleteLink)
router.get('/:slug', getLinkPageBySlug)

export default router
