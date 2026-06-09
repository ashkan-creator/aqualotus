import { apiSlice } from './apiSlice'

export const uploadApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    uploadVideo: builder.mutation({
      query: (data) => ({
        url: '/api/upload/video',
        method: 'POST',
        body: data,
      }),
    }),
  }),
})

export const { useUploadVideoMutation } = uploadApiSlice
