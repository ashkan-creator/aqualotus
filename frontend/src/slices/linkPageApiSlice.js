import { apiSlice } from './apiSlice'

export const linkPageApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getLinkPageBySlug: builder.query({
      query: (slug) => `/api/linkpages/${slug}`,
      providesTags: ['LinkPage'],
    }),
    getAllLinkPages: builder.query({
      query: () => '/api/linkpages/all',
      providesTags: ['LinkPage'],
    }),
    getLinkPageById: builder.query({
      query: (id) => `/api/linkpages/id/${id}`,
      providesTags: ['LinkPage'],
    }),
    createLinkPage: builder.mutation({
      query: (data) => ({ url: '/api/linkpages', method: 'POST', body: data }),
      invalidatesTags: ['LinkPage'],
    }),
    updateLinkPage: builder.mutation({
      query: ({ id, ...data }) => ({ url: `/api/linkpages/${id}`, method: 'PUT', body: data }),
      invalidatesTags: ['LinkPage'],
    }),
    deleteLinkPage: builder.mutation({
      query: (id) => ({ url: `/api/linkpages/${id}`, method: 'DELETE' }),
      invalidatesTags: ['LinkPage'],
    }),
    addLink: builder.mutation({
      query: ({ id, ...data }) => ({ url: `/api/linkpages/${id}/links`, method: 'POST', body: data }),
      invalidatesTags: ['LinkPage'],
    }),
    updateLink: builder.mutation({
      query: ({ id, linkId, ...data }) => ({
        url: `/api/linkpages/${id}/links/${linkId}`,
        method: 'PUT',
        body: data,
      }),
      invalidatesTags: ['LinkPage'],
    }),
    deleteLink: builder.mutation({
      query: ({ id, linkId }) => ({ url: `/api/linkpages/${id}/links/${linkId}`, method: 'DELETE' }),
      invalidatesTags: ['LinkPage'],
    }),
  }),
})

export const {
  useGetLinkPageBySlugQuery,
  useGetAllLinkPagesQuery,
  useGetLinkPageByIdQuery,
  useCreateLinkPageMutation,
  useUpdateLinkPageMutation,
  useDeleteLinkPageMutation,
  useAddLinkMutation,
  useUpdateLinkMutation,
  useDeleteLinkMutation,
} = linkPageApiSlice
