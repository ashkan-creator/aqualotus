#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch: Redesign ProductCard with 3D Tilt Interactive Effect
Target: frontend/src/components/ui/ProductCard.jsx
Adds: 3D tilt on mouse move, glassmorphism header, gradient overlay, image zoom
Preserves: All existing functionality (wishlist, slideshow, badges, rating, etc.)
"""

import os
import shutil
import sys

BASE_DIR = os.path.expanduser("~/aqualotus/frontend")
TARGET_FILE = os.path.join(BASE_DIR, "src", "components", "ui", "ProductCard.jsx")
CSS_FILE = os.path.join(BASE_DIR, "src", "index.css")

# --- Backup ---
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

# --- New ProductCard.jsx ---
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

  // --- 3D Tilt State ---
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
      toast.error(err?.data?.message || 'خطا در عملیات علاقه‌مندی')
    }
  }

  // --- 3D Tilt Handlers ---
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
              {/* Previous image for crossfade */}
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
              {/* Current image with zoom on hover */}
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
            background: 'linear-gradient(to top, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.2) 40%, rgba(0,0,0,0) 70%)',
            pointerEvents: 'none',
            zIndex: 2,
          }} />

          {/* Stock Indicator */}
          <div style={{
            position: 'absolute', top: '12px', right: '12px', zIndex: 5,
            width: '10px', height: '10px', borderRadius: '50%',
            backgroundColor: inStock ? '#52b788' : '#6c757d',
            animation: inStock ? 'aq-pulse 2s infinite' : 'none',
          }} />

          {/* Wishlist Button */}
          <button
            onClick={handleWishlistClick}
            aria-label='افزودن به علاقه‌مندی‌ها'
            className='aq-wishlist-btn-3d'
            style={{
              position: 'absolute', top: '12px', left: '12px', zIndex: 5,
              background: 'rgba(255,255,255,0.9)', border: 'none', borderRadius: '50%',
              width: '36px', height: '36px', display: 'flex', alignItems: 'center', justifyContent: 'center',
              cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
              transition: 'transform 0.2s, background 0.2s',
            }}
            onMouseOver={(e) => (e.currentTarget.style.transform = 'scale(1.15)')}
            onMouseOut={(e) => (e.currentTarget.style.transform = 'scale(1)')}
          >
            {isWishlisted ? (
              <FaHeart style={{ color: '#e63946', fontSize: '1.1rem' }} />
            ) : (
              <FaRegHeart style={{ color: '#555', fontSize: '1.1rem' }} />
            )}
          </button>

          {/* Slideshow Dots */}
          {allImages.length > 1 && (
            <div style={{
              position: 'absolute', bottom: '12px', left: '50%', transform: 'translateX(-50%)', zIndex: 5,
              display: 'flex', gap: '5px',
            }}>
              {allImages.map((_, i) => (
                <div key={i} style={{
                  width: '6px', height: '6px', borderRadius: '50%',
                  background: i === imgIndex ? '#fff' : 'rgba(255,255,255,0.4)',
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
                padding: '5px 14px', borderRadius: '20px', fontSize: '0.8rem',
              }}>ناموجود</span>
            </div>
          )}

          {/* Glassmorphism Header - Floating on image */}
          <div style={{
            position: 'absolute', top: '50px', left: '12px', right: '12px', zIndex: 3,
            padding: '10px 14px',
            borderRadius: '14px',
            border: '1px solid rgba(255,255,255,0.12)',
            background: 'rgba(0,0,0,0.35)',
            backdropFilter: 'blur(12px)',
            WebkitBackdropFilter: 'blur(12px)',
            color: '#fff',
            transform: 'translateZ(30px)',
          }}>
            <div className="d-flex justify-content-between align-items-start">
              <div style={{ flex: 1, minWidth: 0 }}>
                <h6 style={{
                  margin: 0, fontSize: '0.95rem', fontWeight: 700,
                  lineHeight: 1.3, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  {product.name}
                </h6>
                <p style={{
                  margin: '4px 0 0', fontSize: '0.7rem', color: 'rgba(255,255,255,0.7)',
                  overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  {product.position || product.careLevel || ''}
                </p>
              </div>
              <div style={{ marginRight: '8px', flexShrink: 0 }}>
                <img
                  src="/logo.png"
                  alt="AquaLotus"
                  style={{ height: '16px', width: 'auto', opacity: 0.8 }}
                  onError={(e) => { e.target.style.display = 'none' }}
                />
              </div>
            </div>
          </div>

          {/* Price Tag */}
          <div style={{
            position: 'absolute', top: '108px', left: '12px', zIndex: 3,
            transform: 'translateZ(20px)',
          }}>
            <div style={{
              borderRadius: '20px',
              background: 'rgba(0,0,0,0.45)',
              padding: '4px 12px',
              fontSize: '0.85rem', fontWeight: 600, color: '#fff',
              backdropFilter: 'blur(8px)',
              WebkitBackdropFilter: 'blur(8px)',
            }}>
              {hasDiscount
                ? `${Math.round(discountedPrice).toLocaleString('fa-IR')} تومان`
                : `${product.price.toLocaleString('fa-IR')} تومان`
              }
            </div>
          </div>
        </div>

        {/* Card Body - Below image */}
        <div style={{
          padding: '14px 16px',
          background: 'rgba(10,10,10,0.6)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          borderTop: '1px solid rgba(255,255,255,0.06)',
        }}>
          <div className='d-flex align-items-center gap-2 mb-2'>
            <Badge bg={careConfig.color} className='care-badge-card' style={{ fontSize: '0.7rem' }}>
              {careConfig.icon} {product.careLevel}
            </Badge>
            {hasDiscount && (
              <Badge bg='danger' className='discount-badge' style={{ fontSize: '0.7rem' }}>
                {product.discount}% تخفیف
              </Badge>
            )}
          </div>

          <Rating value={product.rating} text={`(${product.numReviews})`} />

          <div className='mt-2'>
            {hasDiscount ? (
              <div className="d-flex align-items-center gap-2">
                <span className='discounted-price text-danger fw-bold' style={{ fontSize: '0.95rem' }}>
                  {Math.round(discountedPrice).toLocaleString('fa-IR')} تومان
                </span>
                <span className='original-price text-muted text-decoration-line-through' style={{ fontSize: '0.8rem' }}>
                  {product.price.toLocaleString('fa-IR')}
                </span>
              </div>
            ) : (
              <span className='product-price fw-bold' style={{ fontSize: '0.95rem' }}>
                {product.price.toLocaleString('fa-IR')} تومان
              </span>
            )}
            {product.discountMinQty > 0 && (
              <div className='qty-discount-hint mt-1'>
                <small className='text-success' style={{ fontSize: '0.7rem' }}>
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

# --- CSS additions ---
NEW_CSS = r'''

/* --- productcard-3dtilt v1 --- */
.aq-product-card-3d {
  background: rgba(15, 15, 15, 0.55);
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

/* Responsive: disable 3D tilt on mobile */
@media (max-width: 768px) {
  .aq-product-card-3d {
    transform: none !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  }
}
'''

def patch_productcard():
    ok = True
    if not backup_file(TARGET_FILE, "productcard-3dtilt"):
        ok = False
    if not backup_file(CSS_FILE, "productcard-3dtilt"):
        ok = False

    if not ok:
        print("[ABORT] Backup failed.")
        sys.exit(1)

    # Write new ProductCard.jsx
    try:
        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            f.write(NEW_PRODUCTCARD)
        print(f"  [WRITE] {os.path.basename(TARGET_FILE)}")
    except Exception as e:
        print(f"  [ERROR] Writing {TARGET_FILE}: {e}")
        sys.exit(1)

    # Append CSS to index.css
    try:
        with open(CSS_FILE, 'a', encoding='utf-8') as f:
            f.write(NEW_CSS)
        print(f"  [APPEND] CSS to {os.path.basename(CSS_FILE)}")
    except Exception as e:
        print(f"  [ERROR] Appending CSS: {e}")
        sys.exit(1)

    print("\n✓ ProductCard 3D Tilt patch applied successfully!")
    print("  Next steps:")
    print("    1. In VS Code: Reload from Disk if prompted")
    print("    2. Restart Vite server (Ctrl+C then npm run dev)")
    print("    3. Test in Incognito window")

if __name__ == '__main__':
    patch_productcard()
