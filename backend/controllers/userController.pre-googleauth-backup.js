import jwt from 'jsonwebtoken'
import asyncHandler from 'express-async-handler'
import { OAuth2Client } from 'google-auth-library'
import User from '../models/userModel.js'
import setTokenCookies, { generateAccessToken } from '../utils/generateToken.js'

const googleClient = new OAuth2Client(process.env.GOOGLE_CLIENT_ID)

const googleLogin = asyncHandler(async (req, res) => {
  const { credential } = req.body
  if (!credential) {
    res.status(400)
    throw new Error('توکن گوگل ارسال نشده')
  }

  let payload
  try {
    const ticket = await googleClient.verifyIdToken({
      idToken: credential,
      audience: process.env.GOOGLE_CLIENT_ID,
    })
    payload = ticket.getPayload()
  } catch {
    res.status(401)
    throw new Error('توکن گوگل نامعتبر است')
  }

  const { email, name, sub: googleId } = payload

  let user = await User.findOne({ email })
  if (!user) {
    user = await User.create({ name, email, googleId })
  } else if (!user.googleId) {
    user.googleId = googleId
    await user.save()
  }

  setTokenCookies(res, user._id)
  res.json({
    _id: user._id,
    name: user.name,
    email: user.email,
    phone: user.phone,
    address: user.address,
    isAdmin: user.isAdmin,
  })
})
import logActivity from '../utils/logActivity.js'

const authUser = asyncHandler(async (req, res) => {
  const { email, password } = req.body
  const user = await User.findOne({ email })
  if (user && (await user.matchPassword(password))) {
    setTokenCookies(res, user._id)
    res.json({
      _id: user._id,
      name: user.name,
      email: user.email,
      phone: user.phone,
      address: user.address,
      isAdmin: user.isAdmin,
    })
  } else {
    res.status(401)
    throw new Error('ایمیل یا رمز عبور اشتباه است')
  }
})

const registerUser = asyncHandler(async (req, res) => {
  const { name, email, password, phone, address } = req.body
  const userExists = await User.findOne({ email })
  if (userExists) {
    res.status(400)
    throw new Error('این ایمیل قبلاً ثبت شده است')
  }
  const user = await User.create({ name, email, password, phone, address })
  if (user) {
    setTokenCookies(res, user._id)
    res.status(201).json({
      _id: user._id,
      name: user.name,
      email: user.email,
      phone: user.phone,
      address: user.address,
      isAdmin: user.isAdmin,
    })
  } else {
    res.status(400)
    throw new Error('اطلاعات کاربر معتبر نیست')
  }
})

const logoutUser = asyncHandler(async (req, res) => {
  res.cookie('jwt', '', { httpOnly: true, expires: new Date(0) })
  res.cookie('jwt_refresh', '', { httpOnly: true, expires: new Date(0) })
  res.status(200).json({ message: 'با موفقیت خارج شدید' })
})

const refreshToken = asyncHandler(async (req, res) => {
  const token = req.cookies.jwt_refresh
  if (!token) {
    res.status(401)
    throw new Error('رفرش توکن وجود ندارد')
  }
  try {
    const decoded = jwt.verify(token, process.env.JWT_REFRESH_SECRET)
    const user = await User.findById(decoded.userId).select('-password')
    if (!user) {
      res.status(401)
      throw new Error('کاربر یافت نشد')
    }
    const newAccessToken = generateAccessToken(user._id)
    res.cookie('jwt', newAccessToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV !== 'development',
      sameSite: 'strict',
      maxAge: 15 * 60 * 1000,
    })
    res.json({
      _id: user._id,
      name: user.name,
      email: user.email,
      phone: user.phone,
      address: user.address,
      isAdmin: user.isAdmin,
    })
  } catch {
    res.status(401)
    throw new Error('رفرش توکن منقضی یا نامعتبر است')
  }
})

const getUserProfile = asyncHandler(async (req, res) => {
  const user = await User.findById(req.user._id)
  if (user) {
    res.json({
      _id: user._id,
      name: user.name,
      email: user.email,
      phone: user.phone,
      address: user.address,
      isAdmin: user.isAdmin,
    })
  } else {
    res.status(404)
    throw new Error('کاربر پیدا نشد')
  }
})

const updateUserProfile = asyncHandler(async (req, res) => {
  const user = await User.findById(req.user._id)
  if (user) {
    user.name = req.body.name || user.name
    user.email = req.body.email || user.email
    user.phone = req.body.phone || user.phone
    user.address = req.body.address || user.address
    if (req.body.password) user.password = req.body.password
    const updatedUser = await user.save()
    res.json({
      _id: updatedUser._id,
      name: updatedUser.name,
      email: updatedUser.email,
      phone: updatedUser.phone,
      address: updatedUser.address,
      isAdmin: updatedUser.isAdmin,
    })
  } else {
    res.status(404)
    throw new Error('کاربر پیدا نشد')
  }
})

const getUsers = asyncHandler(async (req, res) => {
  const users = await User.find({})
  res.json(users)
})

const deleteUser = asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id)
  if (user) {
    if (user.isAdmin) {
      res.status(400)
      throw new Error('امکان حذف ادمین وجود ندارد')
    }
    await User.deleteOne({ _id: user._id })
    await logActivity(req.user, 'حذف کاربر', 'User', user._id.toString(), user.name)
    res.json({ message: 'کاربر حذف شد' })
  } else {
    res.status(404)
    throw new Error('کاربر پیدا نشد')
  }
})

const getUserById = asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id).select('-password')
  if (user) {
    res.json(user)
  } else {
    res.status(404)
    throw new Error('کاربر پیدا نشد')
  }
})

const updateUser = asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id)
  if (user) {
    user.name = req.body.name || user.name
    user.email = req.body.email || user.email
    user.isAdmin = Boolean(req.body.isAdmin)
    const updatedUser = await user.save()
    await logActivity(req.user, 'ویرایش کاربر', 'User', updatedUser._id.toString(), updatedUser.name)
    res.json({
      _id: updatedUser._id,
      name: updatedUser.name,
      email: updatedUser.email,
      phone: updatedUser.phone,
      address: updatedUser.address,
      isAdmin: updatedUser.isAdmin,
    })
  } else {
    res.status(404)
    throw new Error('کاربر پیدا نشد')
  }
})

export {
  authUser,
  registerUser,
  logoutUser,
  refreshToken,
  getUserProfile,
  updateUserProfile,
  getUsers,
  deleteUser,
  getUserById,
  updateUser,
}
