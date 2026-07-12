import { apiSlice } from './apiSlice'

export const customPageApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getCustomPageBySlug: builder.query({
      query: (slug) => `/api/custompages/${slug}`,
      providesTags: ['CustomPage'],
    }),
    getAllCustomPages: builder.query({
      query: () => '/api/custompages/all',
      providesTags: ['CustomPage'],
    }),
    getCustomPageById: builder.query({
      query: (id) => `/api/custompages/id/${id}`,
      providesTags: ['CustomPage'],
    }),
    createCustomPage: builder.mutation({
      query: (data) => ({ url: '/api/custompages', method: 'POST', body: data }),
      invalidatesTags: ['CustomPage'],
    }),
    updateCustomPage: builder.mutation({
      query: ({ id, ...data }) => ({ url: `/api/custompages/${id}`, method: 'PUT', body: data }),
      invalidatesTags: ['CustomPage', 'Slider'],
    }),
    deleteCustomPage: builder.mutation({
      query: (id) => ({ url: `/api/custompages/${id}`, method: 'DELETE' }),
      invalidatesTags: ['CustomPage', 'Slider'],
    }),
  }),
})

export const {
  useGetCustomPageBySlugQuery,
  useGetAllCustomPagesQuery,
  useGetCustomPageByIdQuery,
  useCreateCustomPageMutation,
  useUpdateCustomPageMutation,
  useDeleteCustomPageMutation,
} = customPageApiSlice
