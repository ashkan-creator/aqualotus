import express from 'express'
import {
  addOrderItems,
  getOrderById,
  updateOrderToPaid,
  confirmOrderPayment,
  updateOrderToDelivered,
  getMyOrders,
  getOrders,
} from '../controllers/orderController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.route('/').post(protect, addOrderItems).get(protect, admin, getOrders)
router.route('/myorders').get(protect, getMyOrders)
router.route('/:id').get(protect, getOrderById)
router.route('/:id/pay').put(protect, updateOrderToPaid)
router.route('/:id/confirm').put(protect, admin, confirmOrderPayment)
router.route('/:id/deliver').put(protect, admin, updateOrderToDelivered)

export default router