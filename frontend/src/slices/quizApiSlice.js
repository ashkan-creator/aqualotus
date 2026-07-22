import { apiSlice } from './apiSlice'

const QUIZ_URL = '/api/quiz'

export const quizApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getQuizResults: builder.mutation({
      query: (answers) => ({
        url: `${QUIZ_URL}/results`,
        method: 'POST',
        body: answers,
      }),
    }),
  }),
})

export const { useGetQuizResultsMutation } = quizApiSlice
