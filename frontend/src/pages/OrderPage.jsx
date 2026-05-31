import { useEffect, useRef, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  Row, Col, ListGroup, Image, Button,
  Card, Container, Badge, Form,
} from 'react-bootstrap'
import { useSelector } from 'react-redux'
import { toast } from 'react-toastify'
import {
  useGetOrderDetailsQuery,
  useUploadReceiptMutation,
  useConfirmPaymentMutation,
  useDeliverOrderMutation,
} from '../slices/ordersApiSlice'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'

const OrderPage = () => {
  const { id: orderId } = useParams()
  const { userInfo } = useSelector((state) => state.auth)
  const fileInputRef = useRef(null)
  const [receiptNote, setReceiptNote] = useState('')

  const {
    data: order,
    isLoading,
    error,
    refetch,
  } = useGetOrderDetailsQuery(orderId)

  const [uploadReceipt, { isLoading: loadingUpload }] = useUploadReceiptMutation()
  const [confirmPayment, { isLoading: loadingConfirm }] = useConfirmPaymentMutation()
  const [deliverOrder, { isLoading: loadingDeliver }] = useDeliverOrderMutation()

  const uploadReceiptHandler = async (e) => {
    e.preventDefault()
    const file = fileInputRef.current?.files[0]
    if (!file) {
      toast.error('لطفاً تصویر رسید را انتخاب کنید')
      return
    }

    const formData = new FormData()
    formData.append('image', file)

    try {
      // آپلود عکس رسید
      const uploadRes = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })
      const uploadData = await uploadRes.json()

      await uploadReceipt({
        orderId,
        receiptImage: uploadData.image,
        receiptNote,
      }).unwrap()

      refetch()
      toast.success('رسید با موفقیت ارسال شد. منتظر تأیید ادمین باشید.')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در آپلود رسید')
    }
  }

  const confirmPaymentHandler = async () => {
    try {
      await confirmPayment(orderId).unwrap()
      refetch()
      toast.success('پرداخت تأیید شد')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در تأیید پرداخت')
    }
  }

  const deliverOrderHandler = async () => {
    try {
      await deliverOrder(orderId).unwrap()
      refetch()
      toast.success('سفارش ارسال شد')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ثبت ارسال')
    }
  }

  return (
    <Container className='py-4'>
      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <>
          <h2 className='mb-1'>سفارش #{order._id.slice(-8)}</h2>
          <p className='text-muted mb-4'>
            {new Date(order.createdAt).toLocaleDateString('fa-IR')}
          </p>

          <Row>
            <Col md={8}>
              <ListGroup variant='flush'>
                <ListGroup.Item>
                  <h4>آدرس ارسال</h4>
                  <p>
                    <strong>{order.user.name}</strong> |{' '}
                    {order.shippingAddress.address}،{' '}
                    {order.shippingAddress.city}،{' '}
                    کد پستی: {order.shippingAddress.postalCode}
                  </p>
                  {order.isDelivered ? (
                    <Badge bg='success'>
                      ارسال شده در {new Date(order.deliveredAt).toLocaleDateString('fa-IR')}
                    </Badge>
                  ) : (
                    <Badge bg='warning'>در انتظار ارسال</Badge>
                  )}
                </ListGroup.Item>

                <ListGroup.Item>
                  <h4>وضعیت پرداخت</h4>
                  {order.isPaid ? (
                    <Badge bg='success'>
                      پرداخت تأیید شده در {new Date(order.paidAt).toLocaleDateString('fa-IR')}
                    </Badge>
                  ) : order.paymentResult?.receiptImage ? (
                    <Badge bg='info'>رسید ارسال شده - در انتظار تأیید ادمین</Badge>
                  ) : (
                    <Badge bg='danger'>پرداخت نشده</Badge>
                  )}
                </ListGroup.Item>

                <ListGroup.Item>
                  <h4>اقلام سفارش</h4>
                  <ListGroup variant='flush'>
                    {order.orderItems.map((item, index) => (
                      <ListGroup.Item key={index}>
                        <Row className='align-items-center'>
                          <Col md={2}>
                            <Image src={item.image} alt={item.name} fluid rounded />
                          </Col>
                          <Col>
                            <Link to={`/product/${item.product}`}>{item.name}</Link>
                          </Col>
                          <Col md={4} className='text-end'>
                            {item.qty} × {item.price.toLocaleString('fa-IR')} ={' '}
                            {(item.qty * item.price).toLocaleString('fa-IR')} تومان
                          </Col>
                        </Row>
                      </ListGroup.Item>
                    ))}
                  </ListGroup>
                </ListGroup.Item>
              </ListGroup>
            </Col>

            <Col md={4}>
              <Card className='cart-summary mb-3'>
                <ListGroup variant='flush'>
                  <ListGroup.Item><h5>خلاصه سفارش</h5></ListGroup.Item>
                  <ListGroup.Item>
                    <Row>
                      <Col>جمع کالاها:</Col>
                      <Col className='text-end'>
                        {Math.round(order.itemsPrice).toLocaleString('fa-IR')} تومان
                      </Col>
                    </Row>
                  </ListGroup.Item>
                  <ListGroup.Item>
                    <Row>
                      <Col>ارسال:</Col>
                      <Col className='text-end'>
                        {order.shippingPrice === 0
                          ? 'رایگان 🎉'
                          : `${order.shippingPrice.toLocaleString('fa-IR')} تومان`}
                      </Col>
                    </Row>
                  </ListGroup.Item>
                  <ListGroup.Item>
                    <Row>
                      <Col><strong>جمع کل:</strong></Col>
                      <Col className='text-end'>
                        <strong>
                          {Math.round(order.totalPrice).toLocaleString('fa-IR')} تومان
                        </strong>
                      </Col>
                    </Row>
                  </ListGroup.Item>
                </ListGroup>
              </Card>

              {/* بخش پرداخت کارت به کارت */}
              {!order.isPaid && (
                <Card className='payment-card mb-3'>
                  <Card.Body>
                    <h5 className='mb-3'>💳 اطلاعات پرداخت</h5>
                    <div className='bank-info'>
                      <p className='mb-1'>
                        <strong>شماره کارت:</strong>
                      </p>
                      <p className='card-number'>
                        {import.meta.env.VITE_BANK_CARD_NUMBER || '6037-9982-8046-6227'}
                      </p>
                      <p className='mb-1'>
                        <strong>شماره شبا:</strong>
                      </p>
                      <p className='shaba-number'>
                        {import.meta.env.VITE_BANK_SHABA || 'IR290170000000364929005001'}
                      </p>
                      <p className='mb-1'>
                        <strong>به نام:</strong> اشکان
                      </p>
                      <p className='text-danger mt-2'>
                        <small>
                          لطفاً مبلغ{' '}
                          <strong>
                            {Math.round(order.totalPrice).toLocaleString('fa-IR')} تومان
                          </strong>{' '}
                          را واریز کنید
                        </small>
                      </p>
                    </div>

                    {!order.paymentResult?.receiptImage ? (
                      <Form onSubmit={uploadReceiptHandler} className='mt-3'>
                        <Form.Group className='mb-2'>
                          <Form.Label>تصویر رسید پرداخت</Form.Label>
                          <Form.Control
                            type='file'
                            accept='image/*'
                            ref={fileInputRef}
                          />
                        </Form.Group>
                        <Form.Group className='mb-2'>
                          <Form.Label>توضیحات (اختیاری)</Form.Label>
                          <Form.Control
                            as='textarea'
                            rows={2}
                            placeholder='مثلاً: ساعت واریز'
                            value={receiptNote}
                            onChange={(e) => setReceiptNote(e.target.value)}
                          />
                        </Form.Group>
                        <Button
                          type='submit'
                          className='w-100 btn-aqualotus'
                          disabled={loadingUpload}
                        >
                          {loadingUpload ? 'در حال ارسال...' : 'ارسال رسید'}
                        </Button>
                      </Form>
                    ) : (
                      <div className='mt-3 text-center'>
                        <Badge bg='info' className='p-2'>
                          ✅ رسید ارسال شد - منتظر تأیید ادمین
                        </Badge>
                        <div className='mt-2'>
                          <Image
                            src={order.paymentResult.receiptImage}
                            alt='رسید'
                            fluid
                            rounded
                            style={{ maxHeight: '150px' }}
                          />
                        </div>
                      </div>
                    )}
                  </Card.Body>
                </Card>
              )}

              {/* دکمه‌های ادمین */}
              {userInfo?.isAdmin && (
                <Card className='admin-actions'>
                  <Card.Body>
                    <h6 className='mb-3'>🔧 پنل ادمین</h6>
                    {order.paymentResult?.receiptImage && !order.isPaid && (
                      <>
                        <div className='mb-2'>
                          <p><strong>رسید مشتری:</strong></p>
                          <Image
                            src={order.paymentResult.receiptImage}
                            alt='رسید'
                            fluid
                            rounded
                          />
                          {order.paymentResult.receiptNote && (
                            <p className='mt-1'>
                              <small>توضیح: {order.paymentResult.receiptNote}</small>
                            </p>
                          )}
                        </div>
                        <Button
                          className='w-100 btn-aqualotus mb-2'
                          onClick={confirmPaymentHandler}
                          disabled={loadingConfirm}
                        >
                          {loadingConfirm ? 'در حال تأیید...' : '✅ تأیید پرداخت'}
                        </Button>
                      </>
                    )}
                    {order.isPaid && !order.isDelivered && (
                      <Button
                        className='w-100 btn-outline-aqualotus'
                        onClick={deliverOrderHandler}
                        disabled={loadingDeliver}
                      >
                        {loadingDeliver ? 'در حال ثبت...' : '📦 ثبت ارسال'}
                      </Button>
                    )}
                  </Card.Body>
                </Card>
              )}
            </Col>
          </Row>
        </>
      )}
    </Container>
  )
}

export default OrderPage