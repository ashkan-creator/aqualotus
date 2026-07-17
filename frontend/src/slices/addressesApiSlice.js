import { apiSlice } from './apiSlice'

const ADDRESSES_URL = '/api/users/addresses'

export const addressesApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMyAddresses: builder.query({
      query: () => ({ url: ADDRESSES_URL }),
      providesTags: ['Addresses'],
      keepUnusedDataFor: 5,
    }),
    addAddress: builder.mutation({
      query: (data) => ({ url: ADDRESSES_URL, method: 'POST', body: data }),
      invalidatesTags: ['Addresses'],
    }),
    updateAddress: builder.mutation({
      query: ({ addressId, ...data }) => ({
        url: `${ADDRESSES_URL}/${addressId}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: ['Addresses'],
    }),
    deleteAddress: builder.mutation({
      query: (addressId) => ({ url: `${ADDRESSES_URL}/${addressId}`, method: 'DELETE' }),
      invalidatesTags: ['Addresses'],
    }),
  }),
})

export const {
  useGetMyAddressesQuery,
  useAddAddressMutation,
  useUpdateAddressMutation,
  useDeleteAddressMutation,
} = addressesApiSlice
