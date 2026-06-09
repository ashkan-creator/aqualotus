import { apiSlice } from './apiSlice'

export const blogApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getPosts: builder.query({
      query: () => '/api/blog',
      providesTags: ['Blog'],
      keepUnusedDataFor: 30,
    }),
    getAllPosts: builder.query({
      query: () => '/api/blog/all',
      providesTags: ['Blog'],
      keepUnusedDataFor: 5,
    }),
    getPostById: builder.query({
      query: (id) => `/api/blog/${id}`,
      keepUnusedDataFor: 5,
    }),
    createPost: builder.mutation({
      query: (data) => ({ url: '/api/blog', method: 'POST', body: data }),
      invalidatesTags: ['Blog'],
    }),
    updatePost: builder.mutation({
      query: ({ id, ...data }) => ({ url: `/api/blog/${id}`, method: 'PUT', body: data }),
      invalidatesTags: ['Blog'],
    }),
    deletePost: builder.mutation({
      query: (id) => ({ url: `/api/blog/${id}`, method: 'DELETE' }),
      invalidatesTags: ['Blog'],
    }),
  }),
})

export const {
  useGetPostsQuery,
  useGetAllPostsQuery,
  useGetPostByIdQuery,
  useCreatePostMutation,
  useUpdatePostMutation,
  useDeletePostMutation,
} = blogApiSlice
