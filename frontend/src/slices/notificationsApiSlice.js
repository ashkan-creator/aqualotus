import { apiSlice } from './apiSlice'

const NOTIFICATIONS_URL = '/api/notifications'

export const notificationsApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getNotifications: builder.query({
      query: () => ({ url: NOTIFICATIONS_URL }),
      providesTags: ['Notifications'],
      keepUnusedDataFor: 5,
    }),
    getUnreadCount: builder.query({
      query: () => ({ url: `${NOTIFICATIONS_URL}/unread-count` }),
      providesTags: ['Notifications'],
      keepUnusedDataFor: 5,
    }),
    markNotificationRead: builder.mutation({
      query: (id) => ({ url: `${NOTIFICATIONS_URL}/${id}/read`, method: 'PUT' }),
      invalidatesTags: ['Notifications'],
    }),
    markAllNotificationsRead: builder.mutation({
      query: () => ({ url: `${NOTIFICATIONS_URL}/read-all`, method: 'PUT' }),
      invalidatesTags: ['Notifications'],
    }),
    getMyNotifications: builder.query({
      query: () => ({ url: `${NOTIFICATIONS_URL}/mine` }),
      providesTags: ['Notifications'],
      keepUnusedDataFor: 5,
    }),
    getMyUnreadCount: builder.query({
      query: () => ({ url: `${NOTIFICATIONS_URL}/mine/unread-count` }),
      providesTags: ['Notifications'],
      keepUnusedDataFor: 5,
    }),
    markMyNotificationRead: builder.mutation({
      query: (id) => ({ url: `${NOTIFICATIONS_URL}/mine/${id}/read`, method: 'PUT' }),
      invalidatesTags: ['Notifications'],
    }),
    markAllMyNotificationsRead: builder.mutation({
      query: () => ({ url: `${NOTIFICATIONS_URL}/mine/read-all`, method: 'PUT' }),
      invalidatesTags: ['Notifications'],
    }),
  }),
})

export const {
  useGetNotificationsQuery,
  useGetUnreadCountQuery,
  useMarkNotificationReadMutation,
  useMarkAllNotificationsReadMutation,
  useGetMyNotificationsQuery,
  useGetMyUnreadCountQuery,
  useMarkMyNotificationReadMutation,
  useMarkAllMyNotificationsReadMutation,
} = notificationsApiSlice
