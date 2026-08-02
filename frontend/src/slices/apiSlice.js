import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { BASE_URL, USERS_URL } from '../constants'
import { logout } from './authSlice'

const baseQuery = fetchBaseQuery({
  baseUrl: BASE_URL,
  credentials: 'include',
})

// توکن access فقط ۱۵ دقیقه اعتبار داره (عمداً کوتاهه). وقتی منقضی بشه،
// به‌جای این‌که کاربر با خطا مواجه بشه، خودکار از /api/users/refresh
// یه توکن تازه می‌گیریم (تا وقتی refresh token خودش معتبره: ۳۰ دقیقه
// کاربر عادی / ۱ ساعت ادمین) و درخواست اصلی رو بی‌سروصدا دوباره می‌فرستیم.
// فقط وقتی واقعاً logout می‌کنیم که خود refresh هم fail بشه.
const AUTH_ENTRY_ENDPOINTS = ['login', 'googleLogin', 'requestLoginOtp', 'verifyLoginOtp', 'register']

const baseQueryWithReauth = async (args, api, extraOptions) => {
  let result = await baseQuery(args, api, extraOptions)

  if (result?.error?.status === 401 && !AUTH_ENTRY_ENDPOINTS.includes(api.endpoint)) {
    const refreshResult = await baseQuery(
      { url: `${USERS_URL}/refresh`, method: 'POST' },
      api,
      extraOptions
    )
    if (refreshResult?.data) {
      result = await baseQuery(args, api, extraOptions)
    } else {
      api.dispatch(logout())
    }
  }

  return result
}

export const apiSlice = createApi({
  baseQuery: baseQueryWithReauth,
  tagTypes: ['Product', 'Order', 'User', 'Family', 'Settings', 'Slider', 'Blog', 'PendingReviews', 'Notifications', 'ActivityLog', 'LinkPage', 'CustomPage', 'Wishlist', 'Addresses'],
  endpoints: (builder) => ({}),
})
