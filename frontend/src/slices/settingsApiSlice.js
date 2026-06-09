import { apiSlice } from './apiSlice'

export const settingsApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getSettings: builder.query({
      query: () => '/api/settings',
      providesTags: ['Settings'],
      keepUnusedDataFor: 60,
    }),
    updateSetting: builder.mutation({
      query: ({ key, value }) => ({
        url: `/api/settings/${key}`,
        method: 'PUT',
        body: { value },
      }),
      invalidatesTags: ['Settings'],
    }),
  }),
})

export const { useGetSettingsQuery, useUpdateSettingMutation } = settingsApiSlice
