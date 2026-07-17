import jwt from 'jsonwebtoken'

const generateAccessToken = (userId) => {
  return jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: '15m' })
}

const generateRefreshToken = (userId, isAdmin) => {
  const expiresIn = isAdmin ? '1h' : '30m'
  return jwt.sign({ userId }, process.env.JWT_REFRESH_SECRET, { expiresIn })
}

const setTokenCookies = (res, userId, isAdmin) => {
  const accessToken = generateAccessToken(userId)
  const refreshToken = generateRefreshToken(userId, isAdmin)
  const refreshMaxAge = isAdmin ? 60 * 60 * 1000 : 30 * 60 * 1000 // ادمین ۱ ساعت، کاربر عادی ۳۰ دقیقه

  res.cookie('jwt', accessToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV !== 'development',
    sameSite: 'strict',
    maxAge: 15 * 60 * 1000, // 15 دقیقه
  })

  res.cookie('jwt_refresh', refreshToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV !== 'development',
    sameSite: 'strict',
    maxAge: refreshMaxAge,
    path: '/api/users/refresh',
  })
}

export { generateAccessToken, generateRefreshToken, setTokenCookies }
export default setTokenCookies
