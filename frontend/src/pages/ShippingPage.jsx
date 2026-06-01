import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Form, Button, Container, Card, Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { saveShippingAddress } from '../slices/cartSlice'

const ShippingPage = () => {
  const { shippingAddress } = useSelector((state) => state.cart)

  const [address, setAddress] = useState(shippingAddress?.address || '')
  const [city, setCity] = useState(shippingAddress?.city || '')
  const [postalCode, setPostalCode] = useState(shippingAddress?.postalCode || '')

  const dispatch = useDispatch()
  const navigate = useNavigate()

  const submitHandler = (e) => {
    e.preventDefault()
    dispatch(saveShippingAddress({ address, city, postalCode, country: 'ایران' }))
    navigate('/placeorder')
  }

  return (
    <Container className='py-5'>
      <Row className='justify-content-center'>
        <Col xs={12} md={6}>
          <Card className='auth-card'>
            <Card.Body className='p-4'>
              <h2 className='mb-4 text-center'>آدرس ارسال</h2>
              <Form onSubmit={submitHandler}>
                <Form.Group className='mb-3'>
                  <Form.Label>آدرس کامل</Form.Label>
                  <Form.Control
                    as='textarea'
                    rows={3}
                    placeholder='آدرس کامل خود را وارد کنید'
                    value={address}
                    required
                    onChange={(e) => setAddress(e.target.value)}
                  />
                </Form.Group>

                <Form.Group className='mb-3'>
                  <Form.Label>شهر</Form.Label>
                  <Form.Control
                    type='text'
                    placeholder='شهر'
                    value={city}
                    required
                    onChange={(e) => setCity(e.target.value)}
                  />
                </Form.Group>

                <Form.Group className='mb-4'>
                  <Form.Label>کد پستی</Form.Label>
                  <Form.Control
                    type='text'
                    placeholder='کد پستی ۱۰ رقمی'
                    value={postalCode}
                    required
                    onChange={(e) => setPostalCode(e.target.value)}
                  />
                </Form.Group>
                  <div className='shipping-notice mb-4'>
  <div className='notice-item'>
    📦 سفارشات فقط به صورت <strong>پس کرایه</strong> ارسال می‌شوند و هزینه کرایه به عهده مشتری است.
  </div>
  <div className='notice-item mt-2'>
    🚚 ارسال به خارج از تهران: <strong>تیپاکس</strong> و <strong>پست پیشتاز</strong>
  </div>
  <div className='notice-item mt-2'>
    🛵 ارسال در تهران: <strong>اسنپ</strong> و <strong>الوپیک</strong>
  </div>
</div>
                <Button type='submit' className='w-100 btn-aqualotus'>
                  ادامه
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default ShippingPage