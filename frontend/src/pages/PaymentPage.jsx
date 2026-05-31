import { useNavigate } from 'react-router-dom'
import { Button, Container, Card, Row, Col } from 'react-bootstrap'
import { useDispatch } from 'react-redux'
import { savePaymentMethod } from '../slices/cartSlice'

const PaymentPage = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const submitHandler = () => {
    dispatch(savePaymentMethod('کارت به کارت'))
    navigate('/placeorder')
  }

  return (
    <Container className='py-5'>
      <Row className='justify-content-center'>
        <Col xs={12} md={6}>
          <Card className='auth-card'>
            <Card.Body className='p-4 text-center'>
              <h2 className='mb-4'>روش پرداخت</h2>
              <div className='payment-method-card p-4 mb-4'>
                <div className='payment-icon mb-3'>💳</div>
                <h4>کارت به کارت</h4>
                <p className='text-muted'>
                  پس از ثبت سفارش، اطلاعات کارت بانکی نمایش داده می‌شود.
                  رسید پرداخت را آپلود کنید تا سفارش تأیید شود.
                </p>
              </div>
              <Button className='w-100 btn-aqualotus' onClick={submitHandler}>
                ادامه
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default PaymentPage