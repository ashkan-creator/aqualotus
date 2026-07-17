import jwt from 'jsonwebtoken'

const generateAccessToken = (userId) => {
  return jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: '15m' })
}

const generateRefreshToken = (userId) => {
  return jwt.sign({ userId }, process.env.JWT_REFRESH_SECRET, { expiresIn: '30d' })
}

const setTokenCookies = (res, userId) => {
  const accessToken = generateAccessToken(userId)
  const refreshToken = generateRefreshToken(userId)

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
    maxAge: 30 * 24 * 60 * 60 * 1000, // 30 روز
    path: '/api/users/refresh',
  })
}

export { generateAccessToken, generateRefreshToken, setTokenCookies }
export default setTokenCookies
