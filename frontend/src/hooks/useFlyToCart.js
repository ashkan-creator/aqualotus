import { useCallback } from 'react'

export const useFlyToCart = () => {
  const flyToCart = useCallback((sourceElement, imageSrc) => {
    const cartIcon = document.getElementById('cart-icon-target')
    if (!cartIcon || !sourceElement) return

    const sourceRect = sourceElement.getBoundingClientRect()
    const cartRect = cartIcon.getBoundingClientRect()

    const flyEl = document.createElement('div')
    flyEl.className = 'aq-fly-item'

    const size = 60
    flyEl.style.cssText = `
      width: ${size}px;
      height: ${size}px;
      left: ${sourceRect.left + sourceRect.width / 2 - size / 2}px;
      top: ${sourceRect.top + window.scrollY + sourceRect.height / 2 - size / 2}px;
      background: url(${imageSrc}) center/cover no-repeat;
      border-radius: 50%;
      position: fixed;
      z-index: 9998;
      pointer-events: none;
      transition: all 0.8s cubic-bezier(0.22, 1, 0.36, 1);
      opacity: 1;
    `

    document.body.appendChild(flyEl)

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const targetX = cartRect.left + cartRect.width / 2 - size / 2
        const targetY = cartRect.top + cartRect.height / 2 - size / 2
        flyEl.style.left = `${targetX}px`
        flyEl.style.top = `${targetY}px`
        flyEl.style.width = '20px'
        flyEl.style.height = '20px'
        flyEl.style.opacity = '0'
        flyEl.style.borderRadius = '50%'
      })
    })

    setTimeout(() => {
      flyEl.remove()
    }, 900)
  }, [])

  return flyToCart
}
