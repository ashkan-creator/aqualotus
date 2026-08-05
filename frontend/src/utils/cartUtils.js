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

// قوانین قیمت‌گذاری سفارش
export const MIN_ORDER_AMOUNT = 1500000
export const PACKAGING_FEE = 300000
export const FREE_PACKAGING_THRESHOLD = 10000000

export const updateCart = (state) => {
  // محاسبه جمع کل با تخفیف
  state.itemsPrice = state.cartItems.reduce(
    (acc, item) => acc + calcDiscountedPrice(item) * item.qty,
    0
  )
  // هزینه ارسال
  state.shippingPrice = state.itemsPrice > 500000 ? 0 : 35000
  // هزینه بسته‌بندی — رایگان برای سفارش‌های بالای ۱۰ میلیون تومان
  state.packagingPrice = state.itemsPrice >= FREE_PACKAGING_THRESHOLD ? 0 : PACKAGING_FEE
  // جمع نهایی
  state.totalPrice = state.itemsPrice + state.shippingPrice + state.packagingPrice
  localStorage.setItem('cart', JSON.stringify(state))
  return state
}