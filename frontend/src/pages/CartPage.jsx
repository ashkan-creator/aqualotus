import { Link, useNavigate } from 'react-router-dom'
import {
  Row, Col, ListGroup, Image, Button,
  Card, Container, Form, Badge,
} from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { FaTrash } from 'react-icons/fa'
import { addToCart, removeFromCart } from '../slices/cartSlice'
import Message from '../components/ui/Message'
import { calcDiscountedPrice } from '../utils/cartUtils'

const CartPage = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const { cartItems, itemsPrice, shippingPrice, totalPrice } = useSelector((state) => state.cart)

  const addToCartHandler = (product, qty) => {
    dispatch(addToCart({ ...product, qty }))
  }

  const removeFromCartHandler = (id, selectedSize) => {
    dispatch(removeFromCart({ id, selectedSize }))
  }

  const checkoutHandler = () => {
    navigate('/login?redirect=/shipping')
  }

  return (
    <Container className='py-4'>
      <h2 className='mb-4'>سبد خرید</h2>
      {cartItems.length === 0 ? (
        <Message>سبد خرید شما خالی است. <Link to='/'>بازگشت به فروشگاه</Link></Message>
      ) : (
        <Row>
          <Col md={8}>
            <ListGroup variant='flush'>
              {cartItems.map((item) => {
                const discountedPrice = calcDiscountedPrice(item)
                const hasDiscount = discountedPrice < item.price
                return (
                  <ListGroup.Item key={`${item._id}-${item.selectedSize || ''}`} className='cart-item'>
                    <Row className='align-items-center'>
                      <Col md={2}>
                        <Image src={item.image} alt={item.name} fluid rounded />
                      </Col>
                      <Col md={4}>
                        <Link to={`/product/${item._id}`}>{item.name}</Link>
                        {/* نمایش سایز */}
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
                      <Col md={2}>
                        {hasDiscount ? (
                          <div>
                            <small className='text-muted text-decoration-line-through d-block'>
                              {item.price.toLocaleString('fa-IR')}
                            </small>
                            <span className='text-danger'>
                              {Math.round(discountedPrice).toLocaleString('fa-IR')} تومان
                            </span>
                          </div>
                        ) : (
                          <span>{item.price.toLocaleString('fa-IR')} تومان</span>
                        )}
                      </Col>
                      <Col md={2}>
                        <Form.Select
                          value={item.qty}
                          onChange={(e) => addToCartHandler(item, Number(e.target.value))}
                        >
                          {[...Array(Math.min(item.countInStock, 10)).keys()].map((x) => (
                            <option key={x + 1} value={x + 1}>{x + 1}</option>
                          ))}
                        </Form.Select>
                      </Col>
                      <Col md={2}>
                        <Button
                          variant='outline-danger'
                          size='sm'
                          onClick={() => removeFromCartHandler(item._id, item.selectedSize)}
                        >
                          <FaTrash />
                        </Button>
                      </Col>
                    </Row>
                  </ListGroup.Item>
                )
              })}
            </ListGroup>
          </Col>

          <Col md={4}>
            <Card className='cart-summary'>
              <ListGroup variant='flush'>
                <ListGroup.Item>
                  <h5>خلاصه سفارش</h5>
                  {cartItems.map((item) => (
                    <div key={`${item._id}-${item.selectedSize}`} className='d-flex justify-content-between mt-1'>
                      <small>{item.name}{item.selectedSize ? ` (${item.selectedSize})` : ''} × {item.qty}</small>
                      <small>{Math.round(calcDiscountedPrice(item) * item.qty).toLocaleString('fa-IR')}</small>
                    </div>
                  ))}
                </ListGroup.Item>
                <ListGroup.Item>
                  <Row>
                    <Col>جمع کالاها:</Col>
                    <Col>{Math.round(itemsPrice).toLocaleString('fa-IR')} تومان</Col>
                  </Row>
                </ListGroup.Item>
                <ListGroup.Item>
                  <Row>
                    <Col>هزینه ارسال:</Col>
                    <Col>{shippingPrice === 0 ? 'رایگان 🎉' : `${shippingPrice.toLocaleString('fa-IR')} تومان`}</Col>
                  </Row>
                </ListGroup.Item>
                <ListGroup.Item>
                  <Row>
                    <Col><strong>جمع کل:</strong></Col>
                    <Col><strong>{Math.round(totalPrice).toLocaleString('fa-IR')} تومان</strong></Col>
                  </Row>
                </ListGroup.Item>
                {shippingPrice === 0 && (
                  <ListGroup.Item className='text-success text-center'>
                    <small>🎉 ارسال رایگان برای خرید بالای ۵۰۰,۰۰۰ تومان</small>
                  </ListGroup.Item>
                )}
                <ListGroup.Item>
                  <Button className='w-100 btn-aqualotus' disabled={cartItems.length === 0} onClick={checkoutHandler}>
                    ادامه خرید
                  </Button>
                </ListGroup.Item>
              </ListGroup>
            </Card>
          </Col>
        </Row>
      )}
    </Container>
  )
}

export default CartPage
