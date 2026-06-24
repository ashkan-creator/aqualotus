import { createSlice } from '@reduxjs/toolkit'
import { updateCart } from '../utils/cartUtils'

const initialState = localStorage.getItem('cart')
  ? JSON.parse(localStorage.getItem('cart'))
  : { cartItems: [], shippingAddress: {}, paymentMethod: 'کارت به کارت' }

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addToCart: (state, action) => {
      const item = action.payload

      // کلید ترکیبی: _id + selectedSize
      const existItem = state.cartItems.find(
        (x) => x._id === item._id && x.selectedSize === (item.selectedSize || null)
      )

      if (existItem) {
        // آپدیت آیتم موجود (همان _id و همان سایز)
        state.cartItems = state.cartItems.map((x) =>
          x._id === existItem._id && x.selectedSize === existItem.selectedSize
            ? item
            : x
        )
      } else {
        // اضافه کردن آیتم جدید (سایز متفاوت یا محصول جدید)
        state.cartItems = [...state.cartItems, item]
      }

      return updateCart(state)
    },

    removeFromCart: (state, action) => {
      const { id, selectedSize } = action.payload

      // حذف با _id + selectedSize (برای جلوگیری از حذف اشتباه سایز دیگر)
      state.cartItems = state.cartItems.filter(
        (x) => !(x._id === id && x.selectedSize === (selectedSize || null))
      )

      return updateCart(state)
    },

    saveShippingAddress: (state, action) => {
      state.shippingAddress = action.payload
      return updateCart(state)
    },

    savePaymentMethod: (state, action) => {
      state.paymentMethod = action.payload
      return updateCart(state)
    },

    clearCartItems: (state, action) => {
      state.cartItems = []
      return updateCart(state)
    },
  },
})

export const {
  addToCart,
  removeFromCart,
  saveShippingAddress,
  savePaymentMethod,
  clearCartItems,
} = cartSlice.actions

export default cartSlice.reducer
