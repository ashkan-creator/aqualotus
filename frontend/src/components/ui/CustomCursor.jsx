import { useEffect, useRef } from 'react'

const CustomCursor = () => {
  const dotRef = useRef(null)
  const ringRef = useRef(null)
  const posRef = useRef({ x: 0, y: 0 })
  const ringPosRef = useRef({ x: 0, y: 0 })

  useEffect(() => {
    if (window.matchMedia('(hover: none), (pointer: coarse)').matches) {
      return
    }

    const dot = dotRef.current
    const ring = ringRef.current
    if (!dot || !ring) return

    let rafId

    const handleMove = (e) => {
      posRef.current = { x: e.clientX, y: e.clientY }
      dot.style.transform = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%, -50%)`
    }

    const animateRing = () => {
      ringPosRef.current.x += (posRef.current.x - ringPosRef.current.x) * 0.18
      ringPosRef.current.y += (posRef.current.y - ringPosRef.current.y) * 0.18
      ring.style.transform = `translate(${ringPosRef.current.x}px, ${ringPosRef.current.y}px) translate(-50%, -50%)`
      rafId = requestAnimationFrame(animateRing)
    }

    const handleDown = () => ring.classList.add('is-clicking')
    const handleUp = () => ring.classList.remove('is-clicking')

    const handleOver = (e) => {
      if (e.target.closest('a, button, [role="button"], input, select, textarea, .aq-product-card')) {
        ring.classList.add('is-active')
      }
    }
    const handleOut = (e) => {
      if (e.target.closest('a, button, [role="button"], input, select, textarea, .aq-product-card')) {
        ring.classList.remove('is-active')
      }
    }

    window.addEventListener('mousemove', handleMove)
    window.addEventListener('mousedown', handleDown)
    window.addEventListener('mouseup', handleUp)
    window.addEventListener('mouseover', handleOver)
    window.addEventListener('mouseout', handleOut)
    rafId = requestAnimationFrame(animateRing)

    return () => {
      window.removeEventListener('mousemove', handleMove)
      window.removeEventListener('mousedown', handleDown)
      window.removeEventListener('mouseup', handleUp)
      window.removeEventListener('mouseover', handleOver)
      window.removeEventListener('mouseout', handleOut)
      cancelAnimationFrame(rafId)
    }
  }, [])

  return (
    <>
      <div ref={ringRef} className='aq-cursor-ring' />
      <div ref={dotRef} className='aq-cursor-dot' />
    </>
  )
}

export default CustomCursor
