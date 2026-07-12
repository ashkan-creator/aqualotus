import { apiSlice } from './apiSlice'

export const activityLogApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getActivityLogs: builder.query({
      query: () => '/api/activity-logs',
      providesTags: ['ActivityLog'],
      keepUnusedDataFor: 30,
    }),
  }),
})

export const { useGetActivityLogsQuery } = activityLogApiSlice
