import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const slides = [
  {
    id: 1,
    title: 'گیاهان زنده آکواریوم',
    subtitle: 'طبیعت رو به خونت بیار',
    buttonText: 'مشاهده گیاهان',
    link: '/search/گیاه زنده',
    bg: 'linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #52b788 100%)',
  },
  {
    id: 2,
    title: 'گیاهان آسان نگهداری',
    subtitle: 'مناسب برای مبتدیان',
    buttonText: 'مشاهده',
    link: '/search/آسان',
    bg: 'linear-gradient(135deg, #0d4f8b 0%, #1a6b9a 50%, #48cae4 100%)',
  },
  {
    id: 3,
    title: 'کود و لوازم جانبی',
    subtitle: 'همه چیز برای آکواریوم شما',
    buttonText: 'مشاهده محصولات',
    link: '/search/کود',
    bg: 'linear-gradient(135deg, #4a4e69 0%, #9a8c98 50%, #c9ada7 100%)',
  },
]

const HeroSlider = () => {
  const [current, setCurrent] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % slides.length)
    }, 4000)
    return () => clearInterval(timer)
  }, [])

  return (
    <div className='hero-slider'>
      {slides.map((slide, index) => (
        <div
          key={slide.id}
          className={`hero-slide ${index === current ? 'active' : ''}`}
          style={{ background: slide.bg }}
        >
          <div className='hero-content'>
            <h1 className='hero-title'>{slide.title}</h1>
            <p className='hero-subtitle'>{slide.subtitle}</p>
            <Link to={slide.link} className='hero-btn'>
              {slide.buttonText}
            </Link>
          </div>
        </div>
      ))}

      {/* نقاط ناوبری */}
      <div className='hero-dots'>
        {slides.map((_, index) => (
          <button
            key={index}
            className={`hero-dot ${index === current ? 'active' : ''}`}
            onClick={() => setCurrent(index)}
          />
        ))}
      </div>
    </div>
  )
}

export default HeroSlider