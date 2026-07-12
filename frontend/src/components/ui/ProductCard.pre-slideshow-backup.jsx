import { useState, useEffect } from 'react'
import { Card, Badge } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom'
import Rating from './Rating'
import { calcDiscountedPrice } from '../../utils/cartUtils'
import { useScrollReveal } from '../../hooks/useScrollReveal'

const careLevelConfig = {
  'آسان': { color: 'success', icon: '🟢' },
  'متوسط': { color: 'warning', icon: '🟡' },
  'سخت': { color: 'danger', icon: '🔴' },
}

const ProductCard = ({ product }) => {
  const discountedPrice = calcDiscountedPrice({ ...product, qty: 1 })
  const hasDiscount = product.discount > 0
  const careConfig = careLevelConfig[product.careLevel] || careLevelConfig['آسان']
  const revealRef = useScrollReveal()
  const navigate = useNavigate()

  const allImages = [product.image, ...(product.images || [])].filter(Boolean)
  const [imgIndex, setImgIndex] = useState(0)
  const [fade, setFade] = useState(true)

  useEffect(() => {
    if (allImages.length <= 1) return
    const timer = setInterval(() => {
      setFade(false)
      setTimeout(() => {
        setImgIndex((i) => (i + 1) % allImages.length)
        setFade(true)
      }, 400)
    }, 6000)
    return () => clearInterval(timer)
  }, [allImages.length])

  const inStock = product.variants && product.variants.length > 0
    ? product.variants.some((v) => v.countInStock > 0)
    : product.countInStock > 0

  const handleCardClick = (e) => {
    if (e.target.closest('a')) return
    navigate(`/product/${product.slug || product._id}`)
  }

  return (
    <div ref={revealRef} className='aq-scroll-init h-100'>
      <Card
        className={`product-card aq-product-card h-100 ${!inStock ? 'aq-out-of-stock' : ''}`}
        onClick={handleCardClick}
        style={{ cursor: 'pointer' }}
      >
        <div className='aq-product-media' style={{ position: 'relative', overflow: 'hidden' }}>
          <Link to={`/product/${product.slug || product._id}`}>
            <Card.Img
              variant='top'
              src={allImages[imgIndex]}
              className='product-img'
              alt={product.name}
              loading='lazy'
              style={{
                opacity: fade ? 1 : 0,
                transition: 'opacity 0.4s ease',
                ...((!inStock) ? { filter: 'grayscale(100%) brightness(0.7)' } : {}),
              }}
            />
          </Link>

          {/* نشانگر چراغ موجودی */}
          <div style={{
            position: 'absolute', top: '10px', right: '10px',
            width: '10px', height: '10px', borderRadius: '50%',
            backgroundColor: inStock ? '#52b788' : '#6c757d',
            animation: inStock ? 'aq-pulse 2s infinite' : 'none',
          }} />

          {/* داته‌های تصویر در پایین */}
          {allImages.length > 1 && (
            <div style={{
              position: 'absolute', bottom: '30px', left: '50%', transform: 'translateX(-50%)',
              display: 'flex', gap: '4px',
            }}>
              {allImages.map((_, i) => (
                <div key={i} style={{
                  width: '5px', height: '5px', borderRadius: '50%',
                  background: i === imgIndex ? '#fff' : 'rgba(255,255,255,0.4)',
                  transition: 'background 0.3s',
                }} />
              ))}
            </div>
          )}

          {!inStock && (
            <div style={{
              position: 'absolute', inset: 0,
              background: 'rgba(0,0,0,0.35)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              borderRadius: '8px 8px 0 0',
            }}>
              <span style={{
                background: 'rgba(0,0,0,0.6)', color: '#ccc',
                padding: '4px 12px', borderRadius: '20px', fontSize: '0.8rem',
              }}>ناموجود</span>
            </div>
          )}

          <div className='aq-product-badge-slide' style={{
            position: 'absolute', bottom: 0, left: 0, right: 0,
            padding: '6px 10px',
            background: inStock
              ? 'linear-gradient(0deg, rgba(45,106,79,0.92), rgba(45,106,79,0))'
              : 'linear-gradient(0deg, rgba(80,80,80,0.92), rgba(80,80,80,0))',
            color: inStock ? '#fff' : '#bbb',
            fontSize: '0.75rem', textAlign: 'center',
          }}>
            {inStock ? '✓ موجود در انبار' : '✕ ناموجود'}
          </div>
        </div>

        <Card.Body className='d-flex flex-column' style={!inStock ? { opacity: 0.6 } : {}}>
          <div className='mb-2'>
            <Badge bg={careConfig.color} className='care-badge-card'>
              {careConfig.icon} {product.careLevel}
            </Badge>
            {hasDiscount && (
              <Badge bg='danger' className='me-1 discount-badge'>
                {product.discount}% تخفیف
              </Badge>
            )}
          </div>

          <Link to={`/product/${product.slug || product._id}`} className='product-title-link'>
            <Card.Title as='h6' className='product-title aq-display-title'>
              {product.name}
            </Card.Title>
          </Link>

          <Rating value={product.rating} text={`(${product.numReviews})`} />

          <div className='mt-auto pt-2'>
            {hasDiscount ? (
              <div>
                <span className='original-price text-muted text-decoration-line-through me-2'>
                  {product.price.toLocaleString('fa-IR')} تومان
                </span>
                <span className='discounted-price text-danger fw-bold'>
                  {Math.round(discountedPrice).toLocaleString('fa-IR')} تومان
                </span>
              </div>
            ) : (
              <span className='product-price'>
                {product.price.toLocaleString('fa-IR')} تومان
              </span>
            )}
            {product.discountMinQty > 0 && (
              <div className='qty-discount-hint mt-1'>
                <small className='text-success'>
                  🎁 خرید {product.discountMinQty}+ عدد: {product.discountQtyPercent}% تخفیف
                </small>
              </div>
            )}
          </div>
        </Card.Body>
      </Card>
    </div>
  )
}

export default ProductCard
