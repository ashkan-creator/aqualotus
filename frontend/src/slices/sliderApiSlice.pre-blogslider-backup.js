import { apiSlice } from './apiSlice'

export const sliderApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getSliders: builder.query({
      query: () => '/api/sliders',
      providesTags: ['Slider'],
      keepUnusedDataFor: 30,
    }),
    getAllSliders: builder.query({
      query: () => '/api/sliders/all',
      providesTags: ['Slider'],
      keepUnusedDataFor: 5,
    }),
    createSlider: builder.mutation({
      query: (data) => ({ url: '/api/sliders', method: 'POST', body: data }),
      invalidatesTags: ['Slider'],
    }),
    updateSlider: builder.mutation({
      query: ({ id, ...data }) => ({ url: `/api/sliders/${id}`, method: 'PUT', body: data }),
      invalidatesTags: ['Slider'],
    }),
    deleteSlider: builder.mutation({
      query: (id) => ({ url: `/api/sliders/${id}`, method: 'DELETE' }),
      invalidatesTags: ['Slider'],
    }),
  }),
})

export const {
  useGetSlidersQuery,
  useGetAllSlidersQuery,
  useCreateSliderMutation,
  useUpdateSliderMutation,
  useDeleteSliderMutation,
} = sliderApiSlice
