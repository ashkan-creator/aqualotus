import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  Row, Col, Image, ListGroup, Card, Button,
  Form, Container, Badge,
} from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { toast } from 'react-toastify'
import { useGetProductDetailsQuery, useCreateReviewMutation } from '../slices/productsApiSlice'
import { addToCart } from '../slices/cartSlice'
import Rating from '../components/ui/Rating'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'
import { calcDiscountedPrice } from '../utils/cartUtils'

const careLevelConfig = {
  'آسان': { color: 'success', icon: '🟢' },
  'متوسط': { color: 'warning', icon: '🟡' },
  'سخت': { color: 'danger', icon: '🔴' },
}

const co2Label = (val) => {
  if (val === 'اختیاری') return 'غیر ضروری ولی تاثیر گذار در رشد و کیفیت'
  return val
}

const ProductPage = () => {
  const { id: productId } = useParams()
  const dispatch = useDispatch()

  const [qty, setQty] = useState(1)
  const [rating, setRating] = useState(0)
  const [comment, setComment] = useState('')
  const [selectedImage, setSelectedImage] = useState(null)
  const [selectedVariant, setSelectedVariant] = useState(null)

  const { data: product, isLoading, error, refetch } = useGetProductDetailsQuery(productId)
  const { userInfo } = useSelector((state) => state.auth)
  const isAdmin = userInfo?.isAdmin
  const [createReview, { isLoading: loadingReview }] = useCreateReviewMutation()

  const hasVariants = product?.variants && product.variants.length > 0

  // قیمت نمایشی
  const displayPrice = selectedVariant
    ? selectedVariant.price
    : product?.price

  // موجودی نمایشی
  const displayStock = selectedVariant
    ? selectedVariant.countInStock
    : product?.countInStock

  const addToCartHandler = () => {
    if (hasVariants && !selectedVariant) {
      toast.error('لطفاً سایز مورد نظر را انتخاب کنید')
      return
    }
    dispatch(addToCart({
      _id: product._id,
      name: product.name,
      image: product.image,
      price: displayPrice,
      countInStock: displayStock,
      discount: product.discount,
      discountMinQty: product.discountMinQty,
      discountQtyPercent: product.discountQtyPercent,
      qty: Number(qty),
      // سایز انتخاب شده
      selectedSize: selectedVariant ? selectedVariant.size : null,
    }))
    toast.success(`محصول${selectedVariant ? ` (${selectedVariant.size})` : ''} به سبد خرید اضافه شد 🛒`)
  }

  const submitReviewHandler = async (e) => {
    e.preventDefault()
    try {
      await createReview({ productId, rating, comment }).unwrap()
      refetch()
      toast.success('نظر شما ثبت شد')
      setRating(0)
      setComment('')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ثبت نظر')
    }
  }

  return (
    <Container className='py-4'>
      <Link to='/' className='btn btn-outline-secondary mb-3'>بازگشت</Link>

      {isLoading ? <Loader /> : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <>
          <Row>
            {/* تصاویر */}
            <Col md={5}>
              <Image
                src={selectedImage || product.image}
                alt={product.name}
                fluid
                className='rounded'
                style={{ width: '100%', maxHeight: '400px', objectFit: 'cover' }}
              />
              {product.images && product.images.length > 0 && (
                <div className='d-flex gap-2 mt-2 flex-wrap'>
                  <Image
                    src={product.image}
                    onClick={() => setSelectedImage(product.image)}
                    style={{
                      width: '70px', height: '70px', objectFit: 'cover',
                      borderRadius: '8px', cursor: 'pointer',
                      border: !selectedImage || selectedImage === product.image ? '2px solid #2d6a4f' : '2px solid transparent',
                    }}
                  />
                  {product.images.map((img, idx) => (
                    <Image
                      key={idx} src={img}
                      onClick={() => setSelectedImage(img)}
                      style={{
                        width: '70px', height: '70px', objectFit: 'cover',
                        borderRadius: '8px', cursor: 'pointer',
                        border: selectedImage === img ? '2px solid #2d6a4f' : '2px solid transparent',
                      }}
                    />
                  ))}
                </div>
              )}
              {product.video && (
                <div className='mt-3'>
                  <video controls className='w-100 rounded'>
                    <source src={product.video} />
                  </video>
                </div>
              )}
            </Col>

            {/* اطلاعات */}
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
                    {product.lightNeeds && (
                      <div className='d-flex align-items-center gap-2'>
                        <span>💡 نیاز نوری:</span>
                        <Badge bg='info'>{product.lightNeeds}</Badge>
                      </div>
                    )}
                    {product.co2Needs && (
                      <div className='d-flex align-items-center gap-2'>
                        <span>💨 CO2:</span>
                        <Badge bg='secondary'>{co2Label(product.co2Needs)}</Badge>
                      </div>
                    )}
                    {product.growthRate && (
                      <div className='d-flex align-items-center gap-2'>
                        <span>🌱 سرعت رشد:</span>
                        <Badge bg='success'>{product.growthRate}</Badge>
                      </div>
                    )}
                    {product.family && (
                      <div className='d-flex align-items-center gap-2'>
                        <span>🌿 خانواده:</span>
                        <Badge bg='primary'>{product.family}</Badge>
                      </div>
                    )}
                    {product.position && product.position !== 'نامشخص' && (
                      <div className='d-flex align-items-center gap-2'>
                        <span>📍 محل کاشت:</span>
                        <Badge bg='warning' text='dark'>{product.position}</Badge>
                      </div>
                    )}
                    {product.cultivationType && (
                      <div className='d-flex align-items-center gap-2'>
                        <span>🪴 نوع کشت:</span>
                        <Badge bg='success'>{product.cultivationType}</Badge>
                      </div>
                    )}
                    {product.needsSoil !== undefined && (
                      <div className='d-flex align-items-center gap-2'>
                        <span>🪨 نیاز به بستر:</span>
                        <Badge bg={product.needsSoil ? 'warning' : 'secondary'} text='dark'>
                          {product.needsSoil ? 'دارد' : 'ندارد'}
                        </Badge>
                      </div>
                    )}
                    {product.brand && (
                      <div className='d-flex align-items-center gap-2'>
                        <span>🏷️ منشأ:</span>
                        <Badge bg='light' text='dark'>{product.brand}</Badge>
                      </div>
                    )}
                  </div>
                </ListGroup.Item>
              </ListGroup>
            </Col>

            {/* کارت خرید */}
            <Col md={3}>
              <Card className='product-buy-card'>
                <ListGroup variant='flush'>

                  {/* انتخاب سایز */}
                  {hasVariants && (
                    <ListGroup.Item>
                      <strong className='d-block mb-2'>📐 انتخاب سایز:</strong>
                      <div className='d-flex flex-wrap gap-2'>
                        {product.variants.map((v, idx) => (
                          <Button
                            key={idx}
                            size='sm'
                            variant={selectedVariant?.size === v.size ? 'success' : 'outline-success'}
                            onClick={() => {
                              setSelectedVariant(v)
                              setQty(1)
                            }}
                            disabled={v.countInStock === 0}
                            style={{ minWidth: '60px' }}
                          >
                            {v.size}
                            {v.countInStock === 0 && <small className='d-block' style={{ fontSize: '0.65rem' }}>ناموجود</small>}
                          </Button>
                        ))}
                      </div>
                    </ListGroup.Item>
                  )}

                  {/* قیمت */}
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

                  {/* وضعیت موجودی */}
                  <ListGroup.Item>
                    <Row>
                      <Col>وضعیت:</Col>
                      <Col>
                        {(!hasVariants || selectedVariant) ? (
                          displayStock > 0 ? (
                            <Badge bg='success'>موجود</Badge>
                          ) : (
                            <Badge bg='danger'>ناموجود</Badge>
                          )
                        ) : (
                          <Badge bg='info'>سایز انتخاب کنید</Badge>
                        )}
                      </Col>
                    </Row>
                  </ListGroup.Item>

                  {/* تعداد */}
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
                    <Button
                      className='w-100 btn-aqualotus'
                      disabled={
                        isAdmin ||
                        (hasVariants && !selectedVariant) ||
                        displayStock === 0
                      }
                      onClick={addToCartHandler}
                    >
                      {isAdmin
                        ? 'ادمین نمی‌تواند خرید کند'
                        : hasVariants && !selectedVariant
                        ? 'ابتدا سایز انتخاب کنید'
                        : 'افزودن به سبد خرید'}
                    </Button>
                  </ListGroup.Item>
                </ListGroup>
              </Card>
            </Col>
          </Row>

          {/* نظرات */}
          <Row className='mt-5'>
            <Col md={6}>
              <h4>نظرات کاربران</h4>
              {product.reviews.length === 0 && <Message>هنوز نظری ثبت نشده</Message>}
              <ListGroup variant='flush'>
                {product.reviews.map((review) => (
                  <ListGroup.Item key={review._id}>
                    <strong>{review.name}</strong>
                    <Rating value={review.rating} />
                    <p className='mt-1'>{review.comment}</p>
                  </ListGroup.Item>
                ))}
                {userInfo && !isAdmin && (
                  <ListGroup.Item>
                    <h5>نظر خود را بنویسید</h5>
                    <Form onSubmit={submitReviewHandler}>
                      <Form.Group className='mb-2'>
                        <Form.Label>امتیاز</Form.Label>
                        <Form.Select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
                          <option value=''>انتخاب کنید</option>
                          <option value='1'>1 - ضعیف</option>
                          <option value='2'>2 - متوسط</option>
                          <option value='3'>3 - خوب</option>
                          <option value='4'>4 - عالی</option>
                          <option value='5'>5 - فوق‌العاده</option>
                        </Form.Select>
                      </Form.Group>
                      <Form.Group className='mb-2'>
                        <Form.Label>نظر</Form.Label>
                        <Form.Control as='textarea' rows={3} value={comment} onChange={(e) => setComment(e.target.value)} />
                      </Form.Group>
                      <Button type='submit' className='btn-aqualotus' disabled={loadingReview}>ثبت نظر</Button>
                    </Form>
                  </ListGroup.Item>
                )}
              </ListGroup>
            </Col>
          </Row>
        </>
      )}
    </Container>
  )
}

export default ProductPage
