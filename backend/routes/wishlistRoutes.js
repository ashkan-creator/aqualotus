import express from 'express'
import { getMyWishlist, addToWishlist, removeFromWishlist } from '../controllers/wishlistController.js'
import { protect } from '../middleware/authMiddleware.js'

const router = express.Router()

router.get('/', protect, getMyWishlist)
router.post('/', protect, addToWishlist)
router.delete('/:productId', protect, removeFromWishlist)

export default router
