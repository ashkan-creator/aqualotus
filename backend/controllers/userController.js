import jwt from 'jsonwebtoken'
import asyncHandler from 'express-async-handler'
import { OAuth2Client } from 'google-auth-library'
import User from '../models/userModel.js'
import setTokenCookies, { generateAccessToken } from '../utils/generateToken.js'
import crypto from 'crypto'
import sendEmail from '../utils/sendEmail.js'
import sendSms from '../utils/sendSms.js'

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
  } catch (err) {
    console.error('خطای واقعی verifyIdToken گوگل:', err.message)
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

  setTokenCookies(res, user._id, user.isAdmin)
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
    setTokenCookies(res, user._id, user.isAdmin)
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
    setTokenCookies(res, user._id, user.isAdmin)
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

const getMyAddresses = asyncHandler(async (req, res) => {
  const user = await User.findById(req.user._id)
  res.json(user.addresses)
})

const addAddress = asyncHandler(async (req, res) => {
  const { title, province, city, address, postalCode, phone } = req.body
  const user = await User.findById(req.user._id)
  user.addresses.push({ title, province, city, address, postalCode, phone })
  await user.save()
  res.status(201).json(user.addresses)
})

const updateAddress = asyncHandler(async (req, res) => {
  const user = await User.findById(req.user._id)
  const addr = user.addresses.id(req.params.addressId)
  if (!addr) {
    res.status(404)
    throw new Error('آدرس پیدا نشد')
  }
  addr.title = req.body.title ?? addr.title
  addr.province = req.body.province ?? addr.province
  addr.city = req.body.city ?? addr.city
  addr.address = req.body.address ?? addr.address
  addr.postalCode = req.body.postalCode ?? addr.postalCode
  addr.phone = req.body.phone ?? addr.phone
  await user.save()
  res.json(user.addresses)
})

const deleteAddress = asyncHandler(async (req, res) => {
  const user = await User.findById(req.user._id)
  user.addresses.pull({ _id: req.params.addressId })
  await user.save()
  res.json(user.addresses)
})

const forgotPassword = asyncHandler(async (req, res) => {
  const { method, email, phone } = req.body

  if (method === 'email') {
    if (!email) {
      res.status(400)
      throw new Error('ایمیل الزامی است')
    }
    const user = await User.findOne({ email })
    if (!user) {
      return res.status(200).json({ message: 'اگر این ایمیل ثبت شده باشد، لینک بازیابی ارسال خواهد شد' })
    }
    const resetToken = crypto.randomBytes(32).toString('hex')
    user.resetPasswordToken = crypto.createHash('sha256').update(resetToken).digest('hex')
    user.resetPasswordExpire = Date.now() + 60 * 60 * 1000
    await user.save()

    const resetUrl = `${process.env.FRONTEND_URL}/reset-password/${resetToken}`
    try {
      await sendEmail({
        to: user.email,
        subject: 'بازیابی رمز عبور - AquaLotus',
        html: `<p>برای بازیابی رمز عبور خود روی لینک زیر کلیک کنید (اعتبار: ۱ ساعت):</p><p><a href="${resetUrl}">${resetUrl}</a></p><p>اگر این درخواست را نداده‌اید، این ایمیل را نادیده بگیرید.</p>`,
      })
      res.status(200).json({ message: 'لینک بازیابی به ایمیل شما ارسال شد' })
    } catch (err) {
      user.resetPasswordToken = null
      user.resetPasswordExpire = null
      await user.save()
      console.error('خطای ارسال ایمیل:', err.message)
      res.status(500)
      throw new Error('خطا در ارسال ایمیل. لطفاً دوباره تلاش کنید')
    }
  } else if (method === 'sms') {
    if (!phone) {
      res.status(400)
      throw new Error('شماره موبایل الزامی است')
    }
    const user = await User.findOne({ phone })
    if (!user) {
      return res.status(200).json({ message: 'اگر این شماره ثبت شده باشد، کد تایید ارسال خواهد شد' })
    }
    const otpCode = Math.floor(100000 + Math.random() * 900000).toString()
    user.resetOtpCode = otpCode
    user.resetOtpExpire = Date.now() + 10 * 60 * 1000
    user.resetOtpAttempts = 0
    await user.save()

    try {
      await sendSms({
        to: user.phone,
        message: `کد بازیابی رمز عبور شما در آکوالوتوس: ${otpCode}\nاین کد تا ۱۰ دقیقه معتبر است.`,
      })
      res.status(200).json({ message: 'کد تایید به شماره شما پیامک شد' })
    } catch (err) {
      user.resetOtpCode = null
      user.resetOtpExpire = null
      await user.save()
      console.error('خطای ارسال پیامک:', err.message)
      res.status(500)
      throw new Error('خطا در ارسال پیامک. لطفاً دوباره تلاش کنید')
    }
  } else {
    res.status(400)
    throw new Error('روش بازیابی نامعتبر است')
  }
})

const resetPassword = asyncHandler(async (req, res) => {
  const { token, password } = req.body
  if (!token || !password) {
    res.status(400)
    throw new Error('توکن و رمز عبور جدید الزامی است')
  }
  const hashedToken = crypto.createHash('sha256').update(token).digest('hex')
  const user = await User.findOne({
    resetPasswordToken: hashedToken,
    resetPasswordExpire: { $gt: Date.now() },
  })
  if (!user) {
    res.status(400)
    throw new Error('لینک بازیابی نامعتبر یا منقضی شده است')
  }
  user.password = password
  user.resetPasswordToken = null
  user.resetPasswordExpire = null
  await user.save()
  res.status(200).json({ message: 'رمز عبور با موفقیت تغییر کرد' })
})

const verifyOtpAndReset = asyncHandler(async (req, res) => {
  const { phone, otp, password } = req.body
  if (!phone || !otp || !password) {
    res.status(400)
    throw new Error('شماره موبایل، کد تایید و رمز عبور جدید الزامی است')
  }
  const user = await User.findOne({ phone })
  if (!user || !user.resetOtpCode || !user.resetOtpExpire) {
    res.status(400)
    throw new Error('درخواست بازیابی معتبری یافت نشد')
  }
  if (user.resetOtpExpire < Date.now()) {
    user.resetOtpCode = null
    user.resetOtpExpire = null
    await user.save()
    res.status(400)
    throw new Error('کد تایید منقضی شده است')
  }
  if (user.resetOtpAttempts >= 5) {
    user.resetOtpCode = null
    user.resetOtpExpire = null
    await user.save()
    res.status(400)
    throw new Error('تعداد تلاش‌های مجاز به پایان رسید. دوباره درخواست کد دهید')
  }
  if (user.resetOtpCode !== otp) {
    user.resetOtpAttempts += 1
    await user.save()
    res.status(400)
    throw new Error('کد تایید اشتباه است')
  }
  user.password = password
  user.resetOtpCode = null
  user.resetOtpExpire = null
  user.resetOtpAttempts = 0
  await user.save()
  res.status(200).json({ message: 'رمز عبور با موفقیت تغییر کرد' })
})

export {
  authUser,
  registerUser,
  logoutUser,
  refreshToken,
  googleLogin,
  getUserProfile,
  updateUserProfile,
  getUsers,
  deleteUser,
  getUserById,
  updateUser,
  getMyAddresses,
  addAddress,
  updateAddress,
  deleteAddress,
  forgotPassword,
  resetPassword,
  verifyOtpAndReset,
}
