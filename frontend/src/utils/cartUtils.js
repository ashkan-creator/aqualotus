// محاسبه قیمت با احتساب تخفیف
export const calcDiscountedPrice = (item) => {
  let price = item.price

  // تخفیف مستقیم
  if (item.discount > 0) {
    price = price * (1 - item.discount / 100)
  }

  // تخفیف تعداد
  if (item.discountMinQty > 0 && item.qty >= item.discountMinQty) {
    price = price * (1 - item.discountQtyPercent / 100)
  }

  return price
}

export const updateCart = (state) => {
  // محاسبه جمع کل با تخفیف
  state.itemsPrice = state.cartItems.reduce(
    (acc, item) => acc + calcDiscountedPrice(item) * item.qty,
    0
  )

  // هزینه ارسال
  state.shippingPrice = state.itemsPrice > 500000 ? 0 : 35000

  // جمع نهایی
  state.totalPrice = state.itemsPrice + state.shippingPrice

  localStorage.setItem('cart', JSON.stringify(state))
  return state
}