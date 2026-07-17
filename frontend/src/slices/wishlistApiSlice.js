import { apiSlice } from './apiSlice'

const WISHLIST_URL = '/api/wishlist'

export const wishlistApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMyWishlist: builder.query({
      query: () => ({ url: WISHLIST_URL }),
      providesTags: ['Wishlist'],
      keepUnusedDataFor: 5,
    }),
    addToWishlist: builder.mutation({
      query: (data) => ({ url: WISHLIST_URL, method: 'POST', body: data }),
      invalidatesTags: ['Wishlist'],
    }),
    removeFromWishlist: builder.mutation({
      query: (productId) => ({ url: `${WISHLIST_URL}/${productId}`, method: 'DELETE' }),
      invalidatesTags: ['Wishlist'],
    }),
  }),
})

export const {
  useGetMyWishlistQuery,
  useAddToWishlistMutation,
  useRemoveFromWishlistMutation,
} = wishlistApiSlice
