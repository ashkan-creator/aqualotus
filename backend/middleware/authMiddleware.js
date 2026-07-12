import jwt from 'jsonwebtoken'
import asyncHandler from 'express-async-handler'
import User from '../models/userModel.js'

const protect = asyncHandler(async (req, res, next) => {
  const token = req.cookies.jwt

  if (!token) {
    res.status(401)
    throw new Error('احراز هویت نشده، توکن وجود ندارد')
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    req.user = await User.findById(decoded.userId).select('-password')
    next()
  } catch (error) {
    // اگه access token منقضی شده، 401 با کد خاص بده
    if (error.name === 'TokenExpiredError') {
      res.status(401).json({ message: 'TOKEN_EXPIRED' })
    } else {
      res.status(401)
      throw new Error('توکن معتبر نیست')
    }
  }
})

const admin = (req, res, next) => {
  if (req.user && req.user.isAdmin) {
    next()
  } else {
    res.status(401)
    throw new Error('دسترسی فقط برای ادمین')
  }
}

export { protect, admin }
