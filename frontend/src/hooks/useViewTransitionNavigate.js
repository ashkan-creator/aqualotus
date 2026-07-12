import { useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { flushSync } from 'react-dom'
import { setSuppressPageTransition } from '../slices/uiSlice'

/**
 * useViewTransitionNavigate
 * ----------------------------
 * ناوبری رو داخل document.startViewTransition اجرا می‌کنه تا افکت
 * مورف/کراس‌فید بومی مرورگر فعال بشه.
 *
 * نکته‌ی مهم: در طول این ناوبری، Framer Motion (PageTransition) رو
 * موقتاً کاملاً از مدار خارج می‌کنیم (suppressPageTransition=true)،
 * چون کراس‌فید Framer باعث می‌شه صفحه‌ی قدیم و جدید یه لحظه هم‌زمان
 * تو DOM بمونن — و چون هر دو یه view-transition-name یکسان دارن،
 * مرورگر این رو نامعتبر می‌دونه و کل مورف رو لغو می‌کنه.
 */
export const useViewTransitionNavigate = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()

  return (to) => {
    const prefersReducedMotion =
      window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches

    if (!document.startViewTransition || prefersReducedMotion) {
      navigate(to)
      return
    }

    dispatch(setSuppressPageTransition(true))

    const transition = document.startViewTransition(() => {
      flushSync(() => {
        navigate(to)
      })
    })

    const resetSuppress = () => dispatch(setSuppressPageTransition(false))
    transition.finished.then(resetSuppress).catch(resetSuppress)
    // fallback ایمنی در صورتی که finished به هر دلیلی resolve نشه
    setTimeout(resetSuppress, 1500)
  }
}
