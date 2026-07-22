import express from 'express'
import {
  authUser,
  refreshToken,
  registerUser,
  logoutUser,
  getUserProfile,
  updateUserProfile,
  getUsers,
  deleteUser,
  getUserById,
  updateUser,
  googleLogin,
  getMyAddresses,
  addAddress,
  updateAddress,
  deleteAddress,
  forgotPassword,
  resetPassword,
  verifyOtpAndReset,
  requestLoginOtp,
  verifyLoginOtp,
} from '../controllers/userController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()

router.route('/').get(protect, admin, getUsers).post(registerUser)
router.post('/login', authUser)
router.post('/google', googleLogin)
router.post('/logout', logoutUser)
router.post('/refresh', refreshToken)
router.post('/forgot-password', forgotPassword)
router.post('/reset-password', resetPassword)
router.post('/verify-otp', verifyOtpAndReset)
router.post('/login-otp/request', requestLoginOtp)
router.post('/login-otp/verify', verifyLoginOtp)
router
  .route('/profile')
  .get(protect, getUserProfile)
  .put(protect, updateUserProfile)
router
  .route('/addresses')
  .get(protect, getMyAddresses)
  .post(protect, addAddress)
router
  .route('/addresses/:addressId')
  .put(protect, updateAddress)
  .delete(protect, deleteAddress)
router
  .route('/:id')
  .get(protect, admin, getUserById)
  .put(protect, admin, updateUser)
  .delete(protect, admin, deleteUser)

export default router
