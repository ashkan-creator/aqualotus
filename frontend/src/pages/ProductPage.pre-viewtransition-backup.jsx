import { useState, useRef, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  Row, Col, Image, ListGroup, Card, Button,
  Form, Container, Badge,
} from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { toast } from 'react-toastify'
import { Helmet } from 'react-helmet-async'
import { useGetProductDetailsQuery, useCreateReviewMutation } from '../slices/productsApiSlice'
import { useFlyToCart } from '../hooks/useFlyToCart'
import { addToCart } from '../slices/cartSlice'
import Rating from '../components/ui/Rating'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'
import StarRatingInput from '../components/ui/StarRatingInput'
import ReviewItem from '../components/ui/ReviewItem'
import { calcDiscountedPrice } from '../utils/cartUtils'

const careLevelConfig = {
  'آسان': { color: 'success', icon: '🟢' },
  'متوسط': { color: 'warning', icon: '🟡' },
  'سخت': { color: 'danger', icon: '🔴' },
}

const co2Label = (val) => {
  if (val === 'اختیاری') return 'غیر ضروری ولی تاثیرگذار در رشد و کیفیت'
  return val
}

/* دکمه فلش گالری: side = 'left' | 'right' */
const GalleryArrow = ({ side, onClick, label }) => (
  <button
    onClick={onClick}
    style={{
      position: 'absolute',
      top: '50%',
      transform: 'translateY(-50%)',
      [side]: '8px',
      background: 'rgba(0,0,0,0.52)',
      border: 'none',
      color: 'white',
      borderRadius: '50%',
      width: '38px',
      height: '38px',
      cursor: 'pointer',
      fontSize: '1.2rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2,
    }}
  >
    {label}
  </button>
)

/* Lightbox */
const Lightbox = ({ images, currentIndex, onClose, onPrev, onNext }) => {
  const [scale, setScale] = useState(1)
  const [pos, setPos] = useState({ x: 0, y: 0 })
  const [dragging, setDragging] = useState(false)
  const [startPos, setStartPos] = useState({ x: 0, y: 0 })
  const [lbFade, setLbFade] = useState(true)

  useEffect(() => {
    setLbFade(false)
    const t = setTimeout(() => { setScale(1); setPos({ x: 0, y: 0 }); setLbFade(true) }, 500)
    return () => clearTimeout(t)
  }, [currentIndex])

  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 'ArrowLeft') onPrev()
      if (e.key === 'ArrowRight') onNext()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [onClose, onPrev, onNext])

  const handleWheel = (e) => {
    e.preventDefault()
    setScale((s) => Math.min(4, Math.max(1, s - e.deltaY * 0.01)))
  }

  const lbBtn = (side) => ({
    position: 'absolute', top: '50%', transform: 'translateY(-50%)', [side]: '16px',
    background: 'rgba(255,255,255,0.15)', border: 'none', color: 'white',
    borderRadius: '50%', width: '48px', height: '48px', cursor: 'pointer',
    fontSize: '1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center',
  })

  return (
    <div onClick={onClose} style={{
      position: 'fixed', inset: 0, zIndex: 99999,
      background: 'rgba(0,0,0,0.92)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}>
      <button onClick={onClose} style={{
        position: 'absolute', top: '16px', left: '16px',
        background: 'rgba(255,255,255,0.15)', border: 'none', color: 'white',
        fontSize: '1.4rem', cursor: 'pointer', borderRadius: '50%',
        width: '44px', height: '44px', display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>×</button>

      <div style={{ position: 'absolute', top: '16px', right: '16px', display: 'flex', gap: '8px', alignItems: 'center' }}>
        <button onClick={(e) => { e.stopPropagation(); setScale(s => Math.min(4, s + 0.5)) }}
          style={{ background: 'rgba(255,255,255,0.15)', border: 'none', color: 'white', borderRadius: '8px', padding: '6px 14px', cursor: 'pointer' }}>+</button>
        <button onClick={(e) => { e.stopPropagation(); setScale(1); setPos({ x: 0, y: 0 }) }}
          style={{ background: 'rgba(255,255,255,0.15)', border: 'none', color: 'white', borderRadius: '8px', padding: '6px 14px', cursor: 'pointer' }}>−</button>
        <span style={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.85rem' }}>{Math.round(scale * 100)}%</span>
      </div>

      {images.length > 1 && <button onClick={(e) => { e.stopPropagation(); onPrev() }} style={lbBtn('left')}>&gt;</button>}

      <img
        src={images[currentIndex]} alt=''
        onClick={(e) => e.stopPropagation()}
        onMouseDown={(e) => { if (scale <= 1) return; setDragging(true); setStartPos({ x: e.clientX - pos.x, y: e.clientY - pos.y }) }}
        onMouseMove={(e) => { if (!dragging) return; setPos({ x: e.clientX - startPos.x, y: e.clientY - startPos.y }) }}
        onMouseUp={() => setDragging(false)}
        onMouseLeave={() => setDragging(false)}
        onWheel={handleWheel}
        style={{
          maxWidth: '90vw', maxHeight: '85vh', objectFit: 'contain', borderRadius: '8px',
          transform: `scale(${scale}) translate(${pos.x / scale}px, ${pos.y / scale}px)`,
          opacity: lbFade ? 1 : 0,
          transition: dragging ? 'none' : 'transform 0.3s ease, opacity 0.5s ease',
          cursor: scale > 1 ? (dragging ? 'grabbing' : 'grab') : 'default',
          userSelect: 'none',
        }}
      />

      {images.length > 1 && <button onClick={(e) => { e.stopPropagation(); onNext() }} style={lbBtn('right')}>&lt;</button>}

      <div style={{
        position: 'absolute', bottom: '16px', left: '50%', transform: 'translateX(-50%)',
        color: 'rgba(255,255,255,0.7)', fontSize: '0.85rem',
        background: 'rgba(0,0,0,0.4)', padding: '4px 14px', borderRadius: '20px',
      }}>
        {currentIndex + 1} / {images.length}
      </div>
    </div>
  )
}

const ProductPage = () => {
  const { id: productId } = useParams()
  const dispatch = useDispatch()

  const [qty, setQty] = useState(1)
  const [rating, setRating] = useState(0)
  const [comment, setComment] = useState('')
  const [selectedImage, setSelectedImage] = useState(null)
  const [selectedVariant, setSelectedVariant] = useState(null)
  const [lightboxOpen, setLightboxOpen] = useState(false)
  const [lightboxIndex, setLightboxIndex] = useState(0)
  const [galleryFade, setGalleryFade] = useState(true)

  const { data: product, isLoading, error, refetch } = useGetProductDetailsQuery(productId)
  const { userInfo } = useSelector((state) => state.auth)
  const isAdmin = userInfo?.isAdmin
  const [createReview, { isLoading: loadingReview }] = useCreateReviewMutation()
  const flyToCart = useFlyToCart()
  const productImageRef = useRef(null)

  const hasVariants = product?.variants && product.variants.length > 0
  const displayPrice = selectedVariant ? selectedVariant.price : product?.price
  const displayStock = selectedVariant ? selectedVariant.countInStock : product?.countInStock
  const allImages = product ? [product.image, ...(product.images || [])] : []

  const openLightbox = (img) => {
    const idx = allImages.indexOf(img)
    setLightboxIndex(idx >= 0 ? idx : 0)
    setLightboxOpen(true)
  }

  const lightboxPrev = () => setLightboxIndex((i) => (i - 1 + allImages.length) % allImages.length)
  const lightboxNext = () => setLightboxIndex((i) => (i + 1) % allImages.length)

  const galleryPrev = () => {
    setGalleryFade(false)
    setTimeout(() => {
      const idx = allImages.indexOf(selectedImage || product?.image)
      setSelectedImage(allImages[(idx - 1 + allImages.length) % allImages.length])
      setGalleryFade(true)
    }, 400)
  }
  const galleryNext = () => {
    setGalleryFade(false)
    setTimeout(() => {
      const idx = allImages.indexOf(selectedImage || product?.image)
      setSelectedImage(allImages[(idx + 1) % allImages.length])
      setGalleryFade(true)
    }, 400)
  }

  const addToCartHandler = () => {
    if (hasVariants && !selectedVariant) {
      toast.error('لطفاً سایز مورد نظر را انتخاب کنید')
      return
    }
    dispatch(addToCart({
      _id: product._id, name: product.name, image: product.image,
      price: displayPrice, countInStock: displayStock,
      discount: product.discount, discountMinQty: product.discountMinQty,
      discountQtyPercent: product.discountQtyPercent,
      qty: Number(qty),
      selectedSize: selectedVariant ? selectedVariant.size : null,
    }))
    flyToCart(productImageRef.current, product.image)
    toast.success('محصول به سبد خرید اضافه شد 🛒')
  }

  const submitReviewHandler = async (e) => {
    e.preventDefault()
    if (!rating) { toast.error('لطفاً امتیاز را انتخاب کنید'); return }
    try {
      const res = await createReview({ productId, rating, comment }).unwrap()
      refetch(); toast.success(res.message); setRating(0); setComment('')
    } catch (err) { toast.error(err?.data?.message || 'خطا در ثبت نظر') }
  }

  return (
    <Container className='py-4'>
      <Link to='/' className='btn btn-outline-secondary mb-3'>بازگشت</Link>
      {isLoading ? <Loader /> : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <>
          <Helmet>
            <title>{`${product.name} | خرید ${product.category} | AquaLotus`}</title>
            <meta name='description' content={product.description?.slice(0, 155)} />
            <meta name='keywords' content={`${product.name}, ${product.category}, ${product.brand || ''}, گیاه آکواریوم, خرید آنلاین`} />
            <meta name='robots' content='index, follow' />
            <meta property='og:title' content={`${product.name} | AquaLotus`} />
            <meta property='og:description' content={product.description?.slice(0, 155)} />
            <meta property='og:image' content={product.image} />
            <meta property='og:url' content={`https://aqualotus.ir/product/${product._id}`} />
            <meta property='og:type' content='product' />
            <meta property='og:site_name' content='AquaLotus' />
            <meta property='og:locale' content='fa_IR' />
            <meta name='twitter:card' content='summary_large_image' />
            <meta name='twitter:title' content={`${product.name} | AquaLotus`} />
            <meta name='twitter:description' content={product.description?.slice(0, 155)} />
            <meta name='twitter:image' content={product.image} />
            <link rel='canonical' href={`https://aqualotus.ir/product/${product._id}`} />
            <script type='application/ld+json'>{JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Product",
              "name": product.name,
              "image": [product.image, ...(product.images || [])],
              "description": product.description?.slice(0, 500),
              "sku": product._id,
              "brand": { "@type": "Brand", "name": "AquaLotus" },
              "category": product.category,
              "offers": {
                "@type": "Offer",
                "priceCurrency": "IRR",
                "price": product.price,
                "availability": product.countInStock > 0
                  ? "https://schema.org/InStock"
                  : "https://schema.org/OutOfStock",
                "url": `https://aqualotus.ir/product/${product._id}`,
                "seller": { "@type": "Organization", "name": "AquaLotus" }
              },
              ...(product.numReviews > 0 && {
                "aggregateRating": {
                  "@type": "AggregateRating",
                  "ratingValue": product.rating,
                  "reviewCount": product.numReviews,
                  "bestRating": "5",
                  "worstRating": "1"
                }
              }),
              ...(product.reviews?.filter(r => r.isApproved).slice(0, 5).length > 0 && {
                "review": product.reviews.filter(r => r.isApproved).slice(0, 5).map(r => ({
                  "@type": "Review",
                  "author": { "@type": "Person", "name": r.name },
                  "reviewRating": { "@type": "Rating", "ratingValue": r.rating },
                  "reviewBody": r.comment
                }))
              })
            })}</script>
            <script type='application/ld+json'>{JSON.stringify({
              "@context": "https://schema.org",
              "@type": "BreadcrumbList",
              "itemListElement": [
                { "@type": "ListItem", "position": 1, "name": "خانه", "item": "https://aqualotus.ir" },
                { "@type": "ListItem", "position": 2, "name": product.category, "item": `https://aqualotus.ir/filter?category=${product.category}` },
                { "@type": "ListItem", "position": 3, "name": product.name, "item": `https://aqualotus.ir/product/${product._id}` }
              ]
            })}</script>
          </Helmet>

          {lightboxOpen && (
            <Lightbox images={allImages} currentIndex={lightboxIndex}
              onClose={() => setLightboxOpen(false)}
              onPrev={lightboxPrev} onNext={lightboxNext} />
          )}

          <Row>
            <Col md={5}>
              <div style={{ position: 'relative', borderRadius: '10px', overflow: 'hidden' }}>
                <Image ref={productImageRef}
                  src={selectedImage || product.image} alt={product.name}
                  fluid className='rounded'
                  onClick={() => openLightbox(selectedImage || product.image)}
                  style={{ width: '100%', maxHeight: '420px', objectFit: 'cover', cursor: 'zoom-in', display: 'block', opacity: galleryFade ? 1 : 0, transition: 'opacity 0.5s ease' }}
                />
                <div style={{
                  position: 'absolute', bottom: '10px', right: '10px',
                  background: 'rgba(0,0,0,0.5)', color: 'white',
                  borderRadius: '8px', padding: '3px 10px', fontSize: '0.72rem', pointerEvents: 'none',
                }}>🔍 کلیک برای بزرگنمایی</div>

                {allImages.length > 1 && (
                  <>
                    <GalleryArrow side='right' onClick={galleryPrev} label='<' />
                    <GalleryArrow side='left' onClick={galleryNext} label='>' />
                  </>
                )}
              </div>

              {allImages.length > 1 && (
                <div className='d-flex gap-2 mt-2 flex-wrap'>
                  {allImages.map((img, idx) => (
                    <Image key={idx} src={img} onClick={() => setSelectedImage(img)} style={{
                      width: '68px', height: '68px', objectFit: 'cover', borderRadius: '8px', cursor: 'pointer',
                      border: (selectedImage || product.image) === img ? '2px solid #2d6a4f' : '2px solid transparent',
                      transition: 'border-color 0.2s, transform 0.15s',
                      transform: (selectedImage || product.image) === img ? 'scale(1.07)' : 'scale(1)',
                    }} />
                  ))}
                </div>
              )}

              {product.video && (
                <div className='mt-3'>
                  <video controls className='w-100 rounded'><source src={product.video} /></video>
                </div>
              )}
            </Col>

            <Col md={4}>
              <ListGroup variant='flush'>
                <ListGroup.Item>
                  <h3>{product.name}</h3>
                  <div className='d-flex gap-2 mt-2 flex-wrap'>
                    {product.careLevel && (
                      <Badge bg={careLevelConfig[product.careLevel]?.color}>
                        {careLevelConfig[product.careLevel]?.icon} {product.careLevel}
                      </Badge>
                    )}
                    {product.category && <Badge bg='info'>{product.category}</Badge>}
                  </div>
                </ListGroup.Item>
                <ListGroup.Item>
                  <Rating value={product.rating} text={`${product.numReviews} نظر`} />
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>توضیحات:</strong>
                  <p className='mt-2'>{product.description}</p>
                </ListGroup.Item>
                <ListGroup.Item>
                  <div className='d-flex flex-column gap-2'>
                    {product.category === 'گیاه زنده' && product.lightNeeds && (
                      <div className='d-flex align-items-center gap-2'><span>💡 نیاز نوری:</span><Badge bg='info'>{product.lightNeeds}</Badge></div>
                    )}
                    {product.category === 'گیاه زنده' && product.co2Needs && (
                      <div className='d-flex align-items-center gap-2'><span>💨 CO2:</span><Badge bg='secondary'>{co2Label(product.co2Needs)}</Badge></div>
                    )}
                    {product.category === 'گیاه زنده' && product.growthRate && (
                      <div className='d-flex align-items-center gap-2'><span>🌱 سرعت رشد:</span><Badge bg='success'>{product.growthRate}</Badge></div>
                    )}
                    {product.category === 'گیاه زنده' && product.family && (
                      <div className='d-flex align-items-center gap-2'><span>🌿 خانواده:</span><Badge bg='primary'>{product.family}</Badge></div>
                    )}
                    {product.category === 'گیاه زنده' && product.position && product.position !== 'نامشخص' && (
                      <div className='d-flex align-items-center gap-2'><span>📍 محل کاشت:</span><Badge bg='warning' text='dark'>{product.position}</Badge></div>
                    )}
                    {product.category === 'گیاه زنده' && product.cultivationType && (
                      <div className='d-flex align-items-center gap-2'><span>🪴 نوع کشت:</span><Badge bg='success'>{product.cultivationType}</Badge></div>
                    )}
                    {product.category === 'گیاه زنده' && product.needsSoil !== undefined && (
                      <div className='d-flex align-items-center gap-2'>
                        <span>🪨 نیاز به بستر:</span>
                        <Badge bg={product.needsSoil ? 'warning' : 'secondary'} text='dark'>
                          {product.needsSoil ? 'دارد' : 'ندارد'}
                        </Badge>
                      </div>
                    )}
                    {product.brand && (
                      <div className='d-flex align-items-center gap-2'><span>🏷️ منشأ:</span><Badge bg='light' text='dark'>{product.brand}</Badge></div>
                    )}
                  </div>
                </ListGroup.Item>
              </ListGroup>
            </Col>

            <Col md={3}>
              <Card className='product-buy-card'>
                <ListGroup variant='flush'>
                  {hasVariants && (
                    <ListGroup.Item>
                      <strong className='d-block mb-2'>📐 انتخاب سایز:</strong>
                      <div className='d-flex flex-wrap gap-2'>
                        {product.variants.map((v, idx) => (
                          <Button key={idx} size='sm'
                            variant={selectedVariant?.size === v.size ? 'success' : 'outline-success'}
                            onClick={() => { setSelectedVariant(v); setQty(1) }}
                            disabled={v.countInStock === 0} style={{ minWidth: '60px' }}
                          >
                            {v.size}
                            {v.countInStock === 0 && <small className='d-block' style={{ fontSize: '0.65rem' }}>ناموجود</small>}
                          </Button>
                        ))}
                      </div>
                    </ListGroup.Item>
                  )}
                  <ListGroup.Item>
                    <Row>
                      <Col>قیمت:</Col>
                      <Col>
                        {product.discount > 0 ? (
                          <div>
                            <span className='text-muted text-decoration-line-through d-block'>
                              {displayPrice?.toLocaleString('fa-IR')} تومان
                            </span>
                            <span className='text-danger fw-bold'>
                              {Math.round(calcDiscountedPrice({ ...product, price: displayPrice, qty: 1 })).toLocaleString('fa-IR')} تومان
                            </span>
                          </div>
                        ) : (
                          <strong>
                            {hasVariants && !selectedVariant
                              ? `از ${Math.min(...product.variants.map(v => v.price)).toLocaleString('fa-IR')}`
                              : displayPrice?.toLocaleString('fa-IR')
                            } تومان
                          </strong>
                        )}
                      </Col>
                    </Row>
                  </ListGroup.Item>
                  {product.discountMinQty > 0 && (
                    <ListGroup.Item className='text-success'>
                      <small>🎁 خرید {product.discountMinQty}+ عدد: {product.discountQtyPercent}% تخفیف</small>
                    </ListGroup.Item>
                  )}
                  <ListGroup.Item>
                    <Row>
                      <Col>وضعیت:</Col>
                      <Col>
                        {(!hasVariants || selectedVariant) ? (
                          displayStock > 0 ? <Badge bg='success'>موجود</Badge> : <Badge bg='danger'>ناموجود</Badge>
                        ) : <Badge bg='info'>سایز انتخاب کنید</Badge>}
                      </Col>
                    </Row>
                  </ListGroup.Item>
                  {displayStock > 0 && (!hasVariants || selectedVariant) && (
                    <ListGroup.Item>
                      <Row>
                        <Col>تعداد:</Col>
                        <Col>
                          <Form.Select value={qty} onChange={(e) => setQty(e.target.value)}>
                            {[...Array(Math.min(displayStock, 10)).keys()].map((x) => (
                              <option key={x + 1} value={x + 1}>{x + 1}</option>
                            ))}
                          </Form.Select>
                        </Col>
                      </Row>
                    </ListGroup.Item>
                  )}
                  <ListGroup.Item>
                    <Button className='w-100 btn-aqualotus'
                      disabled={isAdmin || (hasVariants && !selectedVariant) || displayStock === 0}
                      onClick={addToCartHandler}
                    >
                      {isAdmin ? 'ادمین نمی‌تواند خرید کند'
                        : hasVariants && !selectedVariant ? 'ابتدا سایز انتخاب کنید'
                        : 'افزودن به سبد خرید'}
                    </Button>
                  </ListGroup.Item>
                </ListGroup>
              </Card>
            </Col>
          </Row>

          <Row className='mt-5'>
            <Col md={7}>
              <h4 className='mb-3'>نظرات کاربران</h4>
              {product.reviews.filter((r) => r.isApproved).length === 0 && (
                <Message>هنوز نظری ثبت نشده</Message>
              )}
              {product.reviews.filter((r) => r.isApproved).map((review) => (
                <ReviewItem key={review._id} review={review} productId={productId} userInfo={userInfo} />
              ))}
              {userInfo && !isAdmin && (
                <Card className='p-3 mt-4'>
                  <h5>نظر خود را بنویسید</h5>
                  <Form onSubmit={submitReviewHandler}>
                    <Form.Group className='mb-3'>
                      <Form.Label className='d-block'>امتیاز</Form.Label>
                      <StarRatingInput value={rating} onChange={setRating} />
                    </Form.Group>
                    <Form.Group className='mb-2'>
                      <Form.Label>نظر</Form.Label>
                      <Form.Control as='textarea' rows={3} value={comment} onChange={(e) => setComment(e.target.value)} />
                    </Form.Group>
                    <Button type='submit' className='btn-aqualotus' disabled={loadingReview}>ثبت نظر</Button>
                  </Form>
                </Card>
              )}
            </Col>
          </Row>
        </>
      )}
    </Container>
  )
}

export default ProductPage
