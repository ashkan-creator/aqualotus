#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch v2: ProductCard 3D Tilt - Refined Layout
Changes:
  1. Glass header: smaller, higher, next to wishlist button
  2. Smaller fonts in header
  3. Line 2: "محل کاشت: {position}"
  4. Remove cylindrical price box from image
  5. Higher card transparency (0.75)
  6. Price color: white (#fff)
"""

import os
import shutil
import sys

BASE_DIR = os.path.expanduser("~/aqualotus/frontend")
TARGET_FILE = os.path.join(BASE_DIR, "src", "components", "ui", "ProductCard.jsx")
CSS_FILE = os.path.join(BASE_DIR, "src", "index.css")

def backup_file(path, suffix):
    if os.path.exists(path):
        backup_path = path.replace(".jsx", f".pre-{suffix}-backup.jsx").replace(".css", f".pre-{suffix}-backup.css")
        if not os.path.exists(backup_path):
            shutil.copy2(path, backup_path)
            print(f"  [BACKUP] {os.path.basename(path)} -> {os.path.basename(backup_path)}")
        else:
            print(f"  [SKIP BACKUP] {os.path.basename(backup_path)} already exists")
        return True
    print(f"  [ERROR] File not found: {path}")
    return False

NEW_PRODUCTCARD = r'''import { useState, useEffect, useRef } from 'react'
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
  'آسان': { color: 'success', icon: '🌱' },
  'متوسط': { color: 'warning', icon: '⚡' },
  'سخت': { color: 'danger', icon: '🔥' },
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

  const cardRef = useRef(null)
  const [tiltStyle, setTiltStyle] = useState({})
  const [isHovered, setIsHovered] = useState(false)

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
      toast.error(err?.data?.message || 'خطا در عملیات علاقه‌مندی')
    }
  }

  const handleMouseMove = (e) => {
    if (!cardRef.current) return
    const { left, top, width, height } = cardRef.current.getBoundingClientRect()
    const x = e.clientX - left
    const y = e.clientY - top
    const rotateX = ((y - height / 2) / (height / 2)) * -8
    const rotateY = ((x - width / 2) / (width / 2)) * 8
    setTiltStyle({
      transform: `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.03, 1.03, 1.03)`,
      transition: 'transform 0.1s ease-out',
      boxShadow: `${-rotateY * 2}px ${rotateX * 2}px 30px rgba(0,0,0,0.4)`,
    })
  }

  const handleMouseEnter = () => {
    setIsHovered(true)
    prefetchProduct(productUrl.split('/product/')[1])
  }

  const handleMouseLeave = () => {
    setIsHovered(false)
    setTiltStyle({
      transform: 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)',
      transition: 'transform 0.5s ease-in-out, box-shadow 0.5s ease-in-out',
      boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
    })
  }

  return (
    <div ref={revealRef} className='aq-scroll-init h-100'>
      <div
        ref={cardRef}
        className={`aq-product-card-3d ${!inStock ? 'aq-out-of-stock' : ''}`}
        onClick={handleCardClick}
        onMouseMove={handleMouseMove}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onTouchStart={() => prefetchProduct(productUrl.split('/product/')[1])}
        style={{
          cursor: 'pointer',
          borderRadius: '20px',
          overflow: 'hidden',
          position: 'relative',
          transformStyle: 'preserve-3d',
          ...tiltStyle,
        }}
      >
        {/* Image Container */}
        <div className='aq-product-media-3d' style={{ position: 'relative', overflow: 'hidden', height: '260px' }}>
          <Link to={productUrl} onClick={handleLinkClick}>
            <div style={{ position: 'relative', width: '100%', height: '100%', overflow: 'hidden' }}>
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
              <img
                key={imgIndex}
                src={allImages[imgIndex]}
                alt={product.name}
                loading='lazy'
                className='card-img-top product-img aq-slideshow-slide'
                style={{
                  position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
                  viewTransitionName: `product-img-${product._id}`,
                  transform: isHovered ? 'scale(1.1)' : 'scale(1)',
                  transition: 'transform 0.6s ease-out',
                  ...imgFilterStyle,
                }}
              />
            </div>
          </Link>

          {/* Gradient Overlay */}
          <div style={{
            position: 'absolute', inset: 0,
            background: 'linear-gradient(to top, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.1) 50%, rgba(0,0,0,0) 70%)',
            pointerEvents: 'none',
            zIndex: 2,
          }} />

          {/* Stock Indicator */}
          <div style={{
            position: 'absolute', top: '10px', right: '10px', zIndex: 5,
            width: '8px', height: '8px', borderRadius: '50%',
            backgroundColor: inStock ? '#52b788' : '#6c757d',
            animation: inStock ? 'aq-pulse 2s infinite' : 'none',
          }} />

          {/* Wishlist Button */}
          <button
            onClick={handleWishlistClick}
            aria-label='افزودن به علاقه‌مندی‌ها'
            className='aq-wishlist-btn-3d'
            style={{
              position: 'absolute', top: '10px', left: '10px', zIndex: 5,
              background: 'rgba(255,255,255,0.9)', border: 'none', borderRadius: '50%',
              width: '32px', height: '32px', display: 'flex', alignItems: 'center', justifyContent: 'center',
              cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
              transition: 'transform 0.2s, background 0.2s',
            }}
            onMouseOver={(e) => (e.currentTarget.style.transform = 'scale(1.15)')}
            onMouseOut={(e) => (e.currentTarget.style.transform = 'scale(1)')}
          >
            {isWishlisted ? (
              <FaHeart style={{ color: '#e63946', fontSize: '1rem' }} />
            ) : (
              <FaRegHeart style={{ color: '#555', fontSize: '1rem' }} />
            )}
          </button>

          {/* Glassmorphism Header - Small, next to wishlist button */}
          <div style={{
            position: 'absolute', top: '10px', left: '50px', right: '24px', zIndex: 3,
            padding: '5px 10px',
            borderRadius: '10px',
            border: '1px solid rgba(255,255,255,0.1)',
            background: 'rgba(0,0,0,0.4)',
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
            color: '#fff',
            transform: 'translateZ(30px)',
          }}>
            <div className="d-flex justify-content-between align-items-center">
              <div style={{ flex: 1, minWidth: 0, overflow: 'hidden' }}>
                <h6 style={{
                  margin: 0, fontSize: '0.78rem', fontWeight: 700,
                  lineHeight: 1.2, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  {product.name}
                </h6>
                <p style={{
                  margin: '2px 0 0', fontSize: '0.62rem', color: 'rgba(255,255,255,0.75)',
                  overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  محل کاشت: {product.position || product.careLevel || '—'}
                </p>
              </div>
            </div>
          </div>

          {/* Slideshow Dots */}
          {allImages.length > 1 && (
            <div style={{
              position: 'absolute', bottom: '10px', left: '50%', transform: 'translateX(-50%)', zIndex: 5,
              display: 'flex', gap: '4px',
            }}>
              {allImages.map((_, i) => (
                <div key={i} style={{
                  width: '5px', height: '5px', borderRadius: '50%',
                  background: i === imgIndex ? '#fff' : 'rgba(255,255,255,0.35)',
                  transition: 'background 0.3s, transform 0.3s',
                  transform: i === imgIndex ? 'scale(1.3)' : 'scale(1)',
                }} />
              ))}
            </div>
          )}

          {/* Out of Stock Overlay */}
          {!inStock && (
            <div style={{
              position: 'absolute', inset: 0, zIndex: 4,
              background: 'rgba(0,0,0,0.35)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <span style={{
                background: 'rgba(0,0,0,0.6)', color: '#ccc',
                padding: '4px 12px', borderRadius: '20px', fontSize: '0.75rem',
              }}>ناموجود</span>
            </div>
          )}
        </div>

        {/* Card Body */}
        <div style={{
          padding: '12px 14px',
          background: 'rgba(10,10,10,0.75)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          borderTop: '1px solid rgba(255,255,255,0.06)',
        }}>
          <div className='d-flex align-items-center gap-2 mb-2'>
            <Badge bg={careConfig.color} className='care-badge-card' style={{ fontSize: '0.68rem' }}>
              {careConfig.icon} {product.careLevel}
            </Badge>
            {hasDiscount && (
              <Badge bg='danger' className='discount-badge' style={{ fontSize: '0.68rem' }}>
                {product.discount}% تخفیف
              </Badge>
            )}
          </div>

          <Rating value={product.rating} text={`(${product.numReviews})`} />

          <div className='mt-2'>
            {hasDiscount ? (
              <div className="d-flex align-items-center gap-2">
                <span className='discounted-price fw-bold' style={{ fontSize: '0.9rem', color: '#fff' }}>
                  {Math.round(discountedPrice).toLocaleString('fa-IR')} تومان
                </span>
                <span className='original-price text-muted text-decoration-line-through' style={{ fontSize: '0.75rem' }}>
                  {product.price.toLocaleString('fa-IR')}
                </span>
              </div>
            ) : (
              <span className='product-price fw-bold' style={{ fontSize: '0.9rem', color: '#fff' }}>
                {product.price.toLocaleString('fa-IR')} تومان
              </span>
            )}
            {product.discountMinQty > 0 && (
              <div className='qty-discount-hint mt-1'>
                <small className='text-success' style={{ fontSize: '0.68rem' }}>
                  🎁 از خرید {product.discountMinQty}+ عدد: {product.discountQtyPercent}% تخفیف
                </small>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProductCard
'''

NEW_CSS = r'''

/* --- productcard-3dtilt v2 --- */
.aq-product-card-3d {
  background: rgba(15, 15, 15, 0.75);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  will-change: transform;
}

.aq-product-card-3d:hover {
  border-color: rgba(255, 255, 255, 0.15);
}

.aq-product-card-3d.aq-out-of-stock {
  opacity: 0.75;
}

.aq-product-media-3d {
  border-radius: 20px 20px 0 0;
}

.aq-wishlist-btn-3d:hover {
  background: rgba(255, 255, 255, 1) !important;
}

/* Price color override */
.aq-product-card-3d .product-price,
.aq-product-card-3d .discounted-price {
  color: #fff !important;
}

/* Responsive: disable 3D tilt on mobile */
@media (max-width: 768px) {
  .aq-product-card-3d {
    transform: none !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  }
}
'''

def patch():
    ok = True
    if not backup_file(TARGET_FILE, "productcard-3dtilt-v2"):
        ok = False
    if not backup_file(CSS_FILE, "productcard-3dtilt-v2"):
        ok = False

    if not ok:
        print("[ABORT] Backup failed.")
        sys.exit(1)

    try:
        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            f.write(NEW_PRODUCTCARD)
        print(f"  [WRITE] {os.path.basename(TARGET_FILE)}")
    except Exception as e:
        print(f"  [ERROR] Writing {TARGET_FILE}: {e}")
        sys.exit(1)

    # Remove old v1 CSS block and append v2
    try:
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Remove old productcard-3dtilt v1 block
        if '/* --- productcard-3dtilt v1 --- */' in css_content:
            start = css_content.find('/* --- productcard-3dtilt v1 --- */')
            end = css_content.find('/* ---', start + 1)
            if end == -1:
                end = len(css_content)
            css_content = css_content[:start] + css_content[end:]
            print("  [CLEAN] Removed old v1 CSS block")
        
        with open(CSS_FILE, 'w', encoding='utf-8') as f:
            f.write(css_content.rstrip() + '\n' + NEW_CSS)
        print(f"  [APPEND] CSS v2 to {os.path.basename(CSS_FILE)}")
    except Exception as e:
        print(f"  [ERROR] Updating CSS: {e}")
        sys.exit(1)

    print("\n✓ ProductCard 3D Tilt v2 applied successfully!")
    print("  Next steps:")
    print("    1. In VS Code: Reload from Disk if prompted")
    print("    2. Restart Vite server (Ctrl+C then npm run dev)")
    print("    3. Test in Incognito window")

if __name__ == '__main__':
    patch()
