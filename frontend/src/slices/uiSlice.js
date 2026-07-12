import { createSlice } from '@reduxjs/toolkit'

const uiSlice = createSlice({
  name: 'ui',
  initialState: {
    // وقتی true باشه، یعنی یه ناوبری با View Transition API در جریانه
    // و باید Framer Motion (AnimatePresence/PageTransition) موقتاً
    // کاملاً از مدار خارج بشه تا صفحه‌ی قدیم/جدید هم‌پوشانی نداشته باشن.
    suppressPageTransition: false,
  },
  reducers: {
    setSuppressPageTransition: (state, action) => {
      state.suppressPageTransition = action.payload
    },
  },
})

export const { setSuppressPageTransition } = uiSlice.actions
export default uiSlice.reducer
