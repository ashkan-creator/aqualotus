import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useGetPostsQuery } from '../../slices/blogApiSlice'

/**
 * BlogHighlightsSlider
 * ----------------------
 * اسلایدری از آخرین پست‌های منتشرشده‌ی وبلاگ، زیر هیرو اسلایدر اصلی
 * صفحه‌ی خانه. اگه پستی وجود نداشته باشه، چیزی رندر نمی‌کنه.
 */
const MAX_POSTS = 5

const BlogHighlightsSlider = () => {
  const { data: posts } = useGetPostsQuery()
  const slides = (posts || []).slice(0, MAX_POSTS)
  const [current, setCurrent] = useState(0)

  useEffect(() => {
    if (slides.length <= 1) return
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % slides.length)
    }, 4500)
    return () => clearInterval(timer)
  }, [slides.length])

  if (slides.length === 0) return null

  return (
    <div className='hero-slider aq-blog-highlights-slider' style={{ marginTop: '8px' }}>
      {slides.map((post, index) => (
        <div
          key={post._id}
          className={`hero-slide ${index === current ? 'active' : ''}`}
          style={
            post.image
              ? { backgroundImage: `url(${post.image})`, backgroundSize: 'cover', backgroundPosition: 'center' }
              : { background: 'linear-gradient(135deg, #1b4332, #2d6a4f)' }
          }
        >
          <div className='hero-content' style={{ position: 'relative', zIndex: 1 }}>
            <span
              style={{
                display: 'inline-block', background: 'rgba(255,255,255,0.15)',
                padding: '4px 12px', borderRadius: '20px', fontSize: '0.75rem',
                marginBottom: '10px',
              }}
            >
              📝 از وبلاگ
            </span>
            <h2 className='hero-title aq-display-title aq-reveal aq-reveal-1' style={{ fontSize: 'clamp(1.2rem, 3.5vw, 1.9rem)' }}>
              {post.title}
            </h2>
            <Link to={`/blog/${post._id}`} className='hero-btn aq-reveal aq-reveal-3'>
              مطالعه مطلب
            </Link>
          </div>
        </div>
      ))}

      {slides.length > 1 && (
        <div className='hero-dots'>
          {slides.map((_, index) => (
            <button
              key={index}
              className={`hero-dot ${index === current ? 'active' : ''}`}
              onClick={() => setCurrent(index)}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default BlogHighlightsSlider
