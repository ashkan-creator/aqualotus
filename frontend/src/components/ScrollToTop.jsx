import { useLayoutEffect } from 'react'
import { useLocation } from 'react-router-dom'

/**
 * ScrollToTop
 * -------------
 * با هر تغییر مسیر (pathname یا query)، صفحه رو به بالا اسکرول می‌کنه.
 * از useLayoutEffect استفاده می‌کنه (نه useEffect) تا این کار قبل از
 * رنگ‌آمیزی مرورگر انجام بشه — این برای هماهنگی با مورفِ View Transition
 * (که عکس نهایی صفحه رو بلافاصله بعد از رندر می‌گیره) ضروریه.
 */
const ScrollToTop = () => {
  const location = useLocation()

  useLayoutEffect(() => {
    // صفحه‌بندی محصولات (HomePage) خودش مسئول اسکرول به بالای گرید محصولاته، نه بالای کل صفحه -- پس اینجا براش کاری نمی‌کنیم
    const isProductPagination = /^\/(search\/[^/]+\/)?page\/\d+$/.test(location.pathname)
    if (isProductPagination) return
    window.scrollTo(0, 0)
  }, [location.pathname, location.search])

  return null
}

export default ScrollToTop
