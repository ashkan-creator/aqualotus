import express from 'express'
import {
  getProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct,
  createProductReview,
  getTopProducts,
  addReviewReply,
  approveProductReview,
  rejectProductReview,
  approveReviewReply,
  rejectReviewReply,
  getPendingReviews,
} from '../controllers/productController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.route('/').get(getProducts).post(protect, admin, createProduct)
router.get('/top', getTopProducts)
router.get('/reviews/pending', protect, admin, getPendingReviews)
router
  .route('/:id')
  .get(getProductById)
  .put(protect, admin, updateProduct)
  .delete(protect, admin, deleteProduct)
router.route('/:id/reviews').post(protect, createProductReview)
router.route('/:id/reviews/:reviewId/approve').put(protect, admin, approveProductReview)
router.route('/:id/reviews/:reviewId/reject').delete(protect, admin, rejectProductReview)
router.route('/:id/reviews/:reviewId/replies').post(protect, addReviewReply)
router.route('/:id/reviews/:reviewId/replies/:replyId/approve').put(protect, admin, approveReviewReply)
router.route('/:id/reviews/:reviewId/replies/:replyId/reject').delete(protect, admin, rejectReviewReply)

export default router