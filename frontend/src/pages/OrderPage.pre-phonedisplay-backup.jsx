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

const OrderTracker = ({ order }) => {
  const steps = [
    { label: 'ثبت سفارش', done: true, icon: '📝' },
    { label: 'آپلود رسید', done: !!order.paymentResult?.receiptImage, icon: '🧾' },
    { label: 'تأیید پرداخت', done: order.isPaid, icon: '✅' },
    { label: 'ارسال شده', done: order.isDelivered, icon: '📦' },
  ]
  const activeStep = steps.filter(s => s.done).length - 1

  return (
    <div style={{ margin: '0 0 28px', padding: '20px', background: '#f8fdf9', borderRadius: '12px', border: '1px solid #d8f0e4' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', position: 'relative' }}>
        <div style={{
          position: 'absolute', top: '20px', right: '10%', left: '10%', height: '3px',
          background: '#e0e0e0', zIndex: 0,
        }}>
          <div style={{
            height: '100%', background: '#2d6a4f',
            width: `${(activeStep / (steps.length - 1)) * 100}%`,
            transition: 'width 0.5s ease',
          }} />
        </div>
        {steps.map((step, i) => (
          <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', zIndex: 1, flex: 1 }}>
            <div style={{
              width: '40px', height: '40px', borderRadius: '50%',
              background: step.done ? '#2d6a4f' : '#e0e0e0',
              color: step.done ? 'white' : '#999',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '1.1rem', marginBottom: '8px',
              transition: 'background 0.3s',
              boxShadow: i === activeStep ? '0 0 0 3px rgba(45,106,79,0.25)' : 'none',
            }}>
              {step.icon}
            </div>
            <div style={{ fontSize: 'clamp(0.62rem, 2vw, 0.78rem)', color: step.done ? '#2d6a4f' : '#999', textAlign: 'center', fontWeight: step.done ? '600' : 'normal' }}>
              {step.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

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

  const printInvoice = () => {
    const items = order.orderItems.map((item) =>
      `<tr>
        <td>${item.name}${item.selectedSize ? ` (${item.selectedSize})` : ''}</td>
        <td style="text-align:center">${item.qty}</td>
        <td style="text-align:left">${item.price.toLocaleString('fa-IR')} ت</td>
        <td style="text-align:left">${(item.qty * item.price).toLocaleString('fa-IR')} ت</td>
      </tr>`
    ).join('')
    const html = `<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
<meta charset="UTF-8"/>
<title>فاکتور سفارش #${order._id.slice(-8)}</title>
<style>
  body { font-family: Tahoma, sans-serif; direction: rtl; margin: 0; padding: 24px; color: #222; background: #f4f4f4; }
  .invoice-box { max-width: 720px; margin: 0 auto; background: #fff; border: 1px solid #ddd; border-radius: 10px; padding: 28px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
  .invoice-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #2d6a4f; padding-bottom: 14px; margin-bottom: 18px; }
  h1 { color: #2d6a4f; font-size: 20px; margin: 0; }
  .meta { color: #555; font-size: 13px; line-height: 2; margin-bottom: 16px; }
  .info-box { background: #f9f9f9; border: 1px solid #eee; padding: 12px 14px; border-radius: 8px; margin-bottom: 18px; font-size: 13px; line-height: 1.9; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; border: 1px solid #ddd; }
  th, td { border: 1px solid #ddd; padding: 8px 10px; }
  th { background: #2d6a4f; color: white; text-align: right; font-size: 13px; }
  tbody tr:nth-child(even) { background: #fafafa; }
  .total-row { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; border-top: 2px solid #2d6a4f; padding-top: 12px; }
  .total { font-size: 16px; font-weight: bold; color: #2d6a4f; }
  .footer { margin-top: 30px; font-size: 12px; color: #999; text-align: center; border-top: 1px solid #eee; padding-top: 12px; }
  @media print {
    body { background: #fff; padding: 0; }
    .invoice-box { border: none; box-shadow: none; border-radius: 0; max-width: 100%; }
  }
</style>
</head>
<body>
  <div class="invoice-box">
    <div class="invoice-header">
      <h1>AquaLotus | فاکتور سفارش</h1>
      <div style="font-size:12px;color:#999">#${order._id.slice(-8)}</div>
    </div>
    <div class="meta">
      تاریخ: ${new Date(order.createdAt).toLocaleDateString('fa-IR')} ساعت ${new Date(order.createdAt).toLocaleTimeString('fa-IR', {hour:'2-digit',minute:'2-digit'})}<br/>
      مشتری: ${order.user.name}${order.shippingAddress.phone ? ` | تلفن: ${order.shippingAddress.phone}` : (order.user.phone ? ` | تلفن: ${order.user.phone}` : '')}
    </div>
    <div class="info-box">
      <strong>آدرس ارسال:</strong><br/>
      ${order.shippingAddress.address}، ${order.shippingAddress.city}${order.shippingAddress.province ? `، استان ${order.shippingAddress.province}` : ''}، کد پستی: ${order.shippingAddress.postalCode}
    </div>
    <table>
      <thead><tr><th>محصول</th><th>تعداد</th><th>قیمت واحد</th><th>جمع</th></tr></thead>
      <tbody>${items}</tbody>
    </table>
    <div class="total-row">
      <span style="font-size:13px;color:#666">جمع کل</span>
      <span class="total">${Math.round(order.totalPrice).toLocaleString('fa-IR')} تومان</span>
    </div>
    <div class="footer">AquaLotus.ir | فروشگاه گیاهان آبزی</div>
  </div>
</body>
</html>`
    const w = window.open('', '_blank')
    w.document.write(html)
    w.document.close()
    w.print()
  }

  return (
    <Container className='py-4'>
      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <>
          <div className='d-flex justify-content-between align-items-center flex-wrap gap-2 mb-1'>
            <h2 className='mb-0'>سفارش #{order._id.slice(-8)}</h2>
            <Button
              variant='outline-secondary'
              size='sm'
              onClick={printInvoice}
              style={{ whiteSpace: 'nowrap' }}
            >
              🖨️ چاپ / دانلود فاکتور
            </Button>
          </div>
          <OrderTracker order={order} />
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
                    {order.shippingAddress.city}
                    {order.shippingAddress.province && `، استان ${order.shippingAddress.province}`}،{' '}
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
                            {/* ✅ نمایش سایز - هم برای کاربر هم ادمین */}
                            {item.selectedSize && (
                              <div className='mt-1'>
                                <Badge bg='success'>📐 سایز: {item.selectedSize}</Badge>
                              </div>
                            )}
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
                        <strong>به نام:</strong> محمدحسین اکبری زرین
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
