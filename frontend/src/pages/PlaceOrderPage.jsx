import { useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  Row, Col, ListGroup, Image, Button, Card, Container, Badge,
} from 'react-bootstrap'
import { useSelector, useDispatch } from 'react-redux'
import { toast } from 'react-toastify'
import { useCreateOrderMutation } from '../slices/ordersApiSlice'
import { clearCartItems } from '../slices/cartSlice'
import { calcDiscountedPrice } from '../utils/cartUtils'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'

const PlaceOrderPage = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()

  const cart = useSelector((state) => state.cart)
  const { cartItems, shippingAddress, itemsPrice, shippingPrice, totalPrice } = cart

  const [createOrder, { isLoading, error }] = useCreateOrderMutation()

  useEffect(() => {
    if (!shippingAddress?.address) navigate('/shipping')
  }, [shippingAddress, navigate])

  const placeOrderHandler = async () => {
    try {
      const res = await createOrder({
        // ✅ selectedSize همراه با هر آیتم ارسال میشه
        orderItems: cartItems.map((item) => ({
          ...item,
          selectedSize: item.selectedSize || '',
          price: Math.round(calcDiscountedPrice(item)),
        })),
        shippingAddress,
        paymentMethod: 'کارت به کارت',
        itemsPrice,
        shippingPrice,
        totalPrice,
      }).unwrap()
      dispatch(clearCartItems())
      navigate(`/order/${res._id}`)
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ثبت سفارش')
    }
  }

  return (
    <Container className='py-4'>
      <h2 className='mb-4'>تأیید سفارش</h2>
      <Row>
        <Col md={8}>
          <ListGroup variant='flush'>
            <ListGroup.Item>
              <h4>آدرس ارسال</h4>
              <p>
                {shippingAddress?.address}، {shippingAddress?.city}
                {shippingAddress?.province && `، استان ${shippingAddress.province}`}،{' '}
                کد پستی: {shippingAddress?.postalCode}
              </p>
            </ListGroup.Item>

            <ListGroup.Item>
              <h4>روش پرداخت</h4>
              <p>💳 کارت به کارت</p>
            </ListGroup.Item>

            <ListGroup.Item>
              <h4>اقلام سفارش</h4>
              {cartItems.length === 0 ? (
                <Message>سبد خرید خالی است</Message>
              ) : (
                <ListGroup variant='flush'>
                  {cartItems.map((item, index) => {
                    const discountedPrice = calcDiscountedPrice(item)
                    const hasDiscount = discountedPrice < item.price
                    return (
                      <ListGroup.Item key={index}>
                        <Row className='align-items-center'>
                          <Col md={2}>
                            <Image src={item.image} alt={item.name} fluid rounded />
                          </Col>
                          <Col>
                            <Link to={`/product/${item._id}`}>{item.name}</Link>
                            {/* ✅ نمایش سایز انتخاب شده */}
                            {item.selectedSize && (
                              <div className='mt-1'>
                                <Badge bg='success'>📐 سایز: {item.selectedSize}</Badge>
                              </div>
                            )}
                            {hasDiscount && (
                              <div>
                                <small className='text-danger'>
                                  {item.discount > 0
                                    ? `${item.discount}% تخفیف`
                                    : `تخفیف تعداد ${item.discountQtyPercent}%`}
                                </small>
                              </div>
                            )}
                          </Col>
                          <Col md={4} className='text-end'>
                            {hasDiscount ? (
                              <>
                                <small className='text-muted text-decoration-line-through d-block'>
                                  {item.qty} × {item.price.toLocaleString('fa-IR')}
                                </small>
                                <span className='text-danger'>
                                  {item.qty} × {Math.round(discountedPrice).toLocaleString('fa-IR')} ={' '}
                                  {(item.qty * Math.round(discountedPrice)).toLocaleString('fa-IR')} تومان
                                </span>
                              </>
                            ) : (
                              <span>
                                {item.qty} × {item.price.toLocaleString('fa-IR')} ={' '}
                                {(item.qty * item.price).toLocaleString('fa-IR')} تومان
                              </span>
                            )}
                          </Col>
                        </Row>
                      </ListGroup.Item>
                    )
                  })}
                </ListGroup>
              )}
            </ListGroup.Item>
          </ListGroup>
        </Col>

        <Col md={4}>
          <Card className='cart-summary'>
            <ListGroup variant='flush'>
              <ListGroup.Item>
                <h5>خلاصه سفارش</h5>
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col>جمع کالاها:</Col>
                  <Col className='text-end'>
                    {Math.round(itemsPrice).toLocaleString('fa-IR')} تومان
                  </Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col>هزینه ارسال:</Col>
                  <Col className='text-end'>
                    {shippingPrice === 0
                      ? 'رایگان 🎉'
                      : `${shippingPrice.toLocaleString('fa-IR')} تومان`}
                  </Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col><strong>جمع کل:</strong></Col>
                  <Col className='text-end'>
                    <strong>
                      {Math.round(totalPrice).toLocaleString('fa-IR')} تومان
                    </strong>
                  </Col>
                </Row>
              </ListGroup.Item>

              {error && (
                <ListGroup.Item>
                  <Message variant='danger'>
                    {error?.data?.message}
                  </Message>
                </ListGroup.Item>
              )}

              <ListGroup.Item>
                <Button
                  className='w-100 btn-aqualotus'
                  disabled={cartItems.length === 0 || isLoading}
                  onClick={placeOrderHandler}
                >
                  {isLoading ? 'در حال ثبت...' : 'ثبت سفارش'}
                </Button>
              </ListGroup.Item>
            </ListGroup>
          </Card>
        </Col>
      </Row>
      {isLoading && <Loader />}
    </Container>
  )
}

export default PlaceOrderPage
