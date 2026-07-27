import { apiSlice } from './apiSlice'
import { PRODUCTS_URL, UPLOAD_URL } from '../constants'

export const productsApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getProducts: builder.query({
      query: (params = {}) => ({
        url: PRODUCTS_URL,
        params: {
          keyword: params.keyword || '',
          pageNumber: params.pageNumber || '',
          admin: params.admin || false,
          position: params.position || '',
          cultivationType: params.cultivationType || '',
          needsSoil: params.needsSoil ?? '',
          careLevel: params.careLevel || '',
          category: params.category || '',
          minPrice: params.minPrice || '',
          maxPrice: params.maxPrice || '',
          sortBy: params.sortBy || 'newest',
        },
      }),
      providesTags: (result) =>
        result
          ? [
              ...result.products.map(({ _id }) => ({ type: 'Product', id: _id })),
              { type: 'Product', id: 'LIST' },
            ]
          : [{ type: 'Product', id: 'LIST' }],
      keepUnusedDataFor: 5,
    }),
    getProductDetails: builder.query({
      query: (productId) => ({ url: `${PRODUCTS_URL}/${productId}` }),
      providesTags: (result, error, productId) => [{ type: 'Product', id: productId }],
      keepUnusedDataFor: 5,
    }),
    createProduct: builder.mutation({
      query: () => ({ url: PRODUCTS_URL, method: 'POST' }),
      invalidatesTags: [{ type: 'Product', id: 'LIST' }, 'ActivityLog'],
    }),
    updateProduct: builder.mutation({
      query: (data) => ({ url: `${PRODUCTS_URL}/${data.productId}`, method: 'PUT', body: data }),
      invalidatesTags: (result, error, { productId }) => [
        { type: 'Product', id: productId },
        { type: 'Product', id: 'LIST' },
        'ActivityLog',
      ],
    }),
    uploadProductImage: builder.mutation({
      query: (data) => ({ url: UPLOAD_URL, method: 'POST', body: data }),
    }),
    deleteProduct: builder.mutation({
      query: (productId) => ({ url: `${PRODUCTS_URL}/${productId}`, method: 'DELETE' }),
      invalidatesTags: [{ type: 'Product', id: 'LIST' }, 'ActivityLog'],
    }),
    createReview: builder.mutation({
      query: (data) => ({ url: `${PRODUCTS_URL}/${data.productId}/reviews`, method: 'POST', body: data }),
      invalidatesTags: (result, error, { productId }) => [{ type: 'Product', id: productId }],
    }),
    addReviewReply: builder.mutation({
      query: (data) => ({
        url: `${PRODUCTS_URL}/${data.productId}/reviews/${data.reviewId}/replies`,
        method: 'POST',
        body: { comment: data.comment },
      }),
      invalidatesTags: (result, error, { productId }) => [{ type: 'Product', id: productId }],
    }),
    getPendingReviews: builder.query({
      query: () => ({ url: `${PRODUCTS_URL}/reviews/pending` }),
      providesTags: ['PendingReviews'],
      keepUnusedDataFor: 5,
    }),
    approveReview: builder.mutation({
      query: (data) => ({
        url: `${PRODUCTS_URL}/${data.productId}/reviews/${data.reviewId}/approve`,
        method: 'PUT',
      }),
      invalidatesTags: (result, error, { productId }) => [
        { type: 'Product', id: productId },
        'PendingReviews',
      ],
    }),
    rejectReview: builder.mutation({
      query: (data) => ({
        url: `${PRODUCTS_URL}/${data.productId}/reviews/${data.reviewId}/reject`,
        method: 'DELETE',
      }),
      invalidatesTags: (result, error, { productId }) => [
        { type: 'Product', id: productId },
        'PendingReviews',
      ],
    }),
    approveReply: builder.mutation({
      query: (data) => ({
        url: `${PRODUCTS_URL}/${data.productId}/reviews/${data.reviewId}/replies/${data.replyId}/approve`,
        method: 'PUT',
      }),
      invalidatesTags: (result, error, { productId }) => [
        { type: 'Product', id: productId },
        'PendingReviews',
      ],
    }),
    rejectReply: builder.mutation({
      query: (data) => ({
        url: `${PRODUCTS_URL}/${data.productId}/reviews/${data.reviewId}/replies/${data.replyId}/reject`,
        method: 'DELETE',
      }),
      invalidatesTags: (result, error, { productId }) => [
        { type: 'Product', id: productId },
        'PendingReviews',
      ],
    }),
    getTopProducts: builder.query({
      query: () => ({ url: `${PRODUCTS_URL}/top` }),
      keepUnusedDataFor: 5,
    }),
  }),
})

export const {
  useGetProductsQuery,
  useGetProductDetailsQuery,
  useCreateProductMutation,
  useUpdateProductMutation,
  useUploadProductImageMutation,
  useDeleteProductMutation,
  useCreateReviewMutation,
  useAddReviewReplyMutation,
  useGetPendingReviewsQuery,
  useApproveReviewMutation,
  useRejectReviewMutation,
  useApproveReplyMutation,
  useRejectReplyMutation,
  useGetTopProductsQuery,
} = productsApiSlice
