import { apiSlice } from './apiSlice'
import { FAMILIES_URL } from '../constants'

export const familiesApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getFamilies: builder.query({
      query: () => ({ url: FAMILIES_URL }),
      providesTags: ['Family'],
      keepUnusedDataFor: 5,
    }),
    createFamily: builder.mutation({
      query: (data) => ({
        url: FAMILIES_URL,
        method: 'POST',
        body: data,
      }),
      invalidatesTags: ['Family'],
    }),
    updateFamily: builder.mutation({
      query: (data) => ({
        url: `${FAMILIES_URL}/${data.id}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: ['Family'],
    }),
    deleteFamily: builder.mutation({
      query: (id) => ({
        url: `${FAMILIES_URL}/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Family'],
    }),
  }),
})

export const {
  useGetFamiliesQuery,
  useCreateFamilyMutation,
  useUpdateFamilyMutation,
  useDeleteFamilyMutation,
} = familiesApiSlice