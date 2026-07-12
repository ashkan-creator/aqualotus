import { useNavigate } from 'react-router-dom'
import { flushSync } from 'react-dom'

/**
 * useViewTransitionNavigate
 * ----------------------------
 * جایگزین useNavigate که ناوبری رو داخل document.startViewTransition
 * اجرا می‌کنه تا افکت مورف/کراس‌فید مرورگر فعال بشه.
 * اگه مرورگر ساپورت نکنه (یا کاربر reduced-motion خواسته)، مثل قبل
 * navigate می‌کنه — بدون هیچ خطایی.
 */
export const useViewTransitionNavigate = () => {
  const navigate = useNavigate()

  return (to) => {
    const prefersReducedMotion =
      window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches

    if (!document.startViewTransition || prefersReducedMotion) {
      navigate(to)
      return
    }

    document.startViewTransition(() => {
      flushSync(() => {
        navigate(to)
      })
    })
  }
}
