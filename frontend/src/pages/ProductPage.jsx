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

const ProductPage = () => {
  const { id: productId } = useParams()
  const dispatch = useDispatch()

  const [qty, setQty] = useState(1)
  const [rating, setRating] = useState(0)
  const [comment, setComment] = useState('')

  const { data: product, isLoading, error, refetch } = useGetProductDetailsQuery(productId)
  const { userInfo } = useSelector((state) => state.auth)
  const isAdmin = userInfo?.isAdmin
  const [createReview, { isLoading: loadingReview }] = useCreateReviewMutation()

  const addToCartHandler = () => {
    dispatch(addToCart({
      _id: product._id,
      name: product.name,
      image: product.image,
      price: product.price,
      countInStock: product.countInStock,
      discount: product.discount,
      discountMinQty: product.discountMinQty,
      discountQtyPercent: product.discountQtyPercent,
      qty: Number(qty),
    }))
    toast.success('محصول به سبد خرید اضافه شد 🛒')
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
      <Link to='/' className='btn btn-outline-secondary mb-3'>
        بازگشت
      </Link>

      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <>
          <Row>
            <Col md={5}>
              <Image src={product.image} alt={product.name} fluid className='product-detail-img' />
              {product.video && (
                <div className='mt-3'>
                  <video controls className='w-100 rounded'>
                    <source src={product.video} />
                  </video>
                </div>
              )}
            </Col>

            <Col md={4}>
              <ListGroup variant='flush'>
                <ListGroup.Item>
                  <h3>{product.name}</h3>
                  <div className='d-flex gap-2 mt-2'>
                    {product.careLevel && (
                      <Badge bg={careLevelConfig[product.careLevel]?.color}>
                        {careLevelConfig[product.careLevel]?.icon} {product.careLevel}
                      </Badge>
                    )}
                  </div>
                </ListGroup.Item>

                <ListGroup.Item>
                  <Rating value={product.rating} text={`${product.numReviews} نظر`} />
                </ListGroup.Item>

                <ListGroup.Item>
                  <strong>توضیحات:</strong>
                  <p className='mt-2'>{product.description}</p>
                </ListGroup.Item>

                {product.category === 'گیاه زنده' && (
                  <ListGroup.Item>
                    <div className='plant-info'>
                      <div className='plant-info-item'>
                        <span>💡 نیاز نوری:</span>
                        <Badge bg='info'>{product.lightNeeds}</Badge>
                      </div>
                      <div className='plant-info-item mt-1'>
                        <span>💨 CO2:</span>
                        <Badge bg='secondary'>{product.co2Needs}</Badge>
                      </div>
                      <div className='plant-info-item mt-1'>
                        <span>🌱 رشد:</span>
                        <Badge bg='success'>{product.growthRate}</Badge>
                      </div>
                      {product.family && (
                        <div className='plant-info-item mt-1'>
                          <span>🌿 خانواده:</span>
                          <Badge bg='primary'>{product.family}</Badge>
                        </div>
                      )}
                      {product.position && product.position !== 'نامشخص' && (
                        <div className='plant-info-item mt-1'>
                          <span>📍 محل کاشت:</span>
                          <Badge bg='warning'>{product.position}</Badge>
                        </div>
                      )}
                    </div>
                  </ListGroup.Item>
                )}
              </ListGroup>
            </Col>

            <Col md={3}>
              <Card className='product-buy-card'>
                <ListGroup variant='flush'>
                  <ListGroup.Item>
                    <Row>
                      <Col>قیمت:</Col>
                      <Col>
                        {product.discount > 0 ? (
                          <div>
                            <span className='text-muted text-decoration-line-through d-block'>
                              {product.price.toLocaleString('fa-IR')} تومان
                            </span>
                            <span className='text-danger fw-bold'>
                              {Math.round(calcDiscountedPrice({ ...product, qty: 1 })).toLocaleString('fa-IR')} تومان
                            </span>
                          </div>
                        ) : (
                          <strong>{product.price.toLocaleString('fa-IR')} تومان</strong>
                        )}
                      </Col>
                    </Row>
                  </ListGroup.Item>

                  {product.discountMinQty > 0 && (
                    <ListGroup.Item className='text-success'>
                      <small>
                        🎁 خرید {product.discountMinQty}+ عدد: {product.discountQtyPercent}% تخفیف
                      </small>
                    </ListGroup.Item>
                  )}

                  <ListGroup.Item>
                    <Row>
                      <Col>وضعیت:</Col>
                      <Col>
                        {product.countInStock > 0 ? (
                          <Badge bg='success'>موجود</Badge>
                        ) : (
                          <Badge bg='danger'>ناموجود</Badge>
                        )}
                      </Col>
                    </Row>
                  </ListGroup.Item>

                  {product.countInStock > 0 && (
                    <ListGroup.Item>
                      <Row>
                        <Col>تعداد:</Col>
                        <Col>
                          <Form.Select
                            value={qty}
                            onChange={(e) => setQty(e.target.value)}
                          >
                            {[...Array(Math.min(product.countInStock, 10)).keys()].map((x) => (
                              <option key={x + 1} value={x + 1}>
                                {x + 1}
                              </option>
                            ))}
                          </Form.Select>
                        </Col>
                      </Row>
                    </ListGroup.Item>
                  )}

                  <ListGroup.Item>
                    <Button
  className='w-100 btn-aqualotus'
  disabled={product.countInStock === 0 || isAdmin}
  onClick={addToCartHandler}
>
  {isAdmin ? 'ادمین نمی‌تواند خرید کند' : 'افزودن به سبد خرید'}
</Button>
                  </ListGroup.Item>
                </ListGroup>
              </Card>
            </Col>
          </Row>

          <Row className='mt-5'>
            <Col md={6}>
              <h4>نظرات کاربران</h4>
              {product.reviews.length === 0 && (
                <Message>هنوز نظری ثبت نشده</Message>
              )}
              <ListGroup variant='flush'>
                {product.reviews.map((review) => (
                  <ListGroup.Item key={review._id}>
                    <strong>{review.name}</strong>
                    <Rating value={review.rating} />
                    <p className='mt-1'>{review.comment}</p>
                  </ListGroup.Item>
                ))}

                {userInfo && (
                  <ListGroup.Item>
                    <h5>نظر خود را بنویسید</h5>
                    <Form onSubmit={submitReviewHandler}>
                      <Form.Group className='mb-2'>
                        <Form.Label>امتیاز</Form.Label>
                        <Form.Select
                          value={rating}
                          onChange={(e) => setRating(Number(e.target.value))}
                        >
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
                        <Form.Control
                          as='textarea'
                          rows={3}
                          value={comment}
                          onChange={(e) => setComment(e.target.value)}
                        />
                      </Form.Group>
                      <Button
                        type='submit'
                        className='btn-aqualotus'
                        disabled={loadingReview}
                      >
                        ثبت نظر
                      </Button>
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