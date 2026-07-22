import { useState, useEffect } from 'react'
import { Card, Badge } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { FaHeart, FaRegHeart } from 'react-icons/fa'
import { toast } from 'react-toastify'
import {
  useGetMyWishlistQuery,
  useAddToWishlistMutation,
  useRemoveFromWishlistMutation,
} from '../../slices/wishlistApiSlice'
import { useViewTransitionNavigate } from '../../hooks/useViewTransitionNavigate'
import { apiSlice } from '../../slices/apiSlice'
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
  const navigate = useViewTransitionNavigate()
  const prefetchProduct = apiSlice.usePrefetch('getProductDetails')
  const { userInfo } = useSelector((state) => state.auth)
  const { data: wishlistProducts } = useGetMyWishlistQuery(undefined, { skip: !userInfo })
  const [addToWishlist] = useAddToWishlistMutation()
  const [removeFromWishlist] = useRemoveFromWishlistMutation()
  const isWishlisted = wishlistProducts?.some((p) => p._id === product._id)

  const productUrl = `/product/${product.slug || product._id}`
  const allImages = [product.image, ...(product.images || [])].filter(Boolean)
  const [imgIndex, setImgIndex] = useState(0)
  const [prevIndex, setPrevIndex] = useState(0)

  useEffect(() => {
    if (allImages.length <= 1) return
    const timer = setInterval(() => {
      const nextIndex = (imgIndex + 1) % allImages.length
      const preloadImg = new window.Image()
      preloadImg.src = allImages[nextIndex]
      const showNext = () => {
        setPrevIndex(imgIndex)
        setImgIndex(nextIndex)
      }
      if (preloadImg.complete) {
        showNext()
      } else {
        preloadImg.onload = showNext
        preloadImg.onerror = showNext
      }
    }, 6000)
    return () => clearInterval(timer)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [imgIndex, allImages.length])

  const inStock = product.variants && product.variants.length > 0
    ? product.variants.some((v) => v.countInStock > 0)
    : product.countInStock > 0

  const handleCardClick = (e) => {
    if (e.target.closest('a')) return
    navigate(productUrl)
  }

  const handleLinkClick = (e) => {
    e.preventDefault()
    navigate(productUrl)
  }

  const imgFilterStyle = !inStock ? { filter: 'grayscale(100%) brightness(0.7)' } : {}

  const handleWishlistClick = async (e) => {
    e.stopPropagation()
    e.preventDefault()
    if (!userInfo) {
      navigate('/login')
      return
    }
    try {
      if (isWishlisted) {
        await removeFromWishlist(product._id).unwrap()
        toast.success('از لیست علاقه‌مندی‌ها حذف شد')
      } else {
        await addToWishlist({ productId: product._id }).unwrap()
        toast.success('به لیست علاقه‌مندی‌ها اضافه شد')
      }
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در به‌روزرسانی علاقه‌مندی‌ها')
    }
  }

  return (
    <div ref={revealRef} className='aq-scroll-init h-100'>
      <Card
        className={`product-card aq-product-card h-100 ${!inStock ? 'aq-out-of-stock' : ''}`}
        onClick={handleCardClick}
        onMouseEnter={() => prefetchProduct(productUrl.split('/product/')[1])}
        onTouchStart={() => prefetchProduct(productUrl.split('/product/')[1])}
        style={{ cursor: 'pointer' }}
      >
        <div className='aq-product-media' style={{ position: 'relative', overflow: 'hidden' }}>
          <Link to={productUrl} onClick={handleLinkClick}>
            <div style={{ position: 'relative', width: '100%', height: '220px', overflow: 'hidden' }}>
              {/* لایه‌ی پس‌زمینه‌ی ثابت — همیشه یه عکس کامل زیر عکس در حال تعویض می‌مونه */}
              <img
                src={allImages[prevIndex]}
                alt=''
                aria-hidden='true'
                className='card-img-top product-img'
                style={{
                  position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
                  ...imgFilterStyle,
                }}
              />
              {/* عکس فعلی — با انیمیشن اسلاید وارد می‌شه، روی لایه‌ی پس‌زمینه */}
              <img
                key={imgIndex}
                src={allImages[imgIndex]}
                alt={product.name}
                loading='lazy'
                className='card-img-top product-img aq-slideshow-slide'
                style={{
                  position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
                  viewTransitionName: `product-img-${product._id}`,
                  ...imgFilterStyle,
                }}
              />
            </div>
          </Link>

          {/* نشانگر چراغ موجودی */}
          <div style={{
            position: 'absolute', top: '10px', right: '10px',
            width: '10px', height: '10px', borderRadius: '50%',
            backgroundColor: inStock ? '#52b788' : '#6c757d',
            animation: inStock ? 'aq-pulse 2s infinite' : 'none',
          }} />

          {/* دکمه‌ی علاقه‌مندی */}
          <button
            onClick={handleWishlistClick}
            aria-label='افزودن به علاقه‌مندی‌ها'
            style={{
              position: 'absolute', top: '10px', left: '10px', zIndex: 5,
              background: 'rgba(255,255,255,0.85)', border: 'none', borderRadius: '50%',
              width: '32px', height: '32px', display: 'flex', alignItems: 'center', justifyContent: 'center',
              cursor: 'pointer', boxShadow: '0 2px 6px rgba(0,0,0,0.15)',
              transition: 'transform 0.2s',
            }}
            onMouseOver={(e) => (e.currentTarget.style.transform = 'scale(1.1)')}
            onMouseOut={(e) => (e.currentTarget.style.transform = 'scale(1)')}
          >
            {isWishlisted ? (
              <FaHeart style={{ color: '#e63946', fontSize: '1rem' }} />
            ) : (
              <FaRegHeart style={{ color: '#555', fontSize: '1rem' }} />
            )}
          </button>

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

          <Link to={productUrl} onClick={handleLinkClick} className='product-title-link'>
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
