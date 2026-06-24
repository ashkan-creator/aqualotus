import { Card, Badge } from 'react-bootstrap'
import { Link } from 'react-router-dom'
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

  const inStock = product.variants && product.variants.length > 0
    ? product.variants.some((v) => v.countInStock > 0)
    : product.countInStock > 0

  return (
    <div ref={revealRef} className='aq-scroll-init h-100'>
    <Card className='product-card aq-product-card h-100'>
      <div className='aq-product-media'>
        <Link to={`/product/${product._id}`}>
          <Card.Img
            variant='top'
            src={product.image}
            className='product-img'
            alt={product.name}
          />
        </Link>
        <div
          className='aq-product-badge-slide'
          style={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            padding: '6px 10px',
            background: inStock
              ? 'linear-gradient(0deg, rgba(45,106,79,0.92), rgba(45,106,79,0))'
              : 'linear-gradient(0deg, rgba(108,117,125,0.92), rgba(108,117,125,0))',
            color: '#fff',
            fontSize: '0.75rem',
            textAlign: 'center',
          }}
        >
          {inStock ? '✓ موجود در انبار' : 'ناموجود'}
        </div>
      </div>

      <Card.Body className='d-flex flex-column'>
        {/* بج سختی نگهداری */}
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

        <Link to={`/product/${product._id}`} className='product-title-link'>
          <Card.Title as='h6' className='product-title aq-display-title'>
            {product.name}
          </Card.Title>
        </Link>

        <Rating
          value={product.rating}
          text={`(${product.numReviews})`}
        />

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