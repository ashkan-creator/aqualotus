import { Table, Button, Container, Badge, Card, Row, Col } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { FaEye } from 'react-icons/fa'
import { useGetOrdersQuery } from '../../slices/ordersApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const OrderListPage = () => {
  const { data: orders, isLoading, error } = useGetOrdersQuery()

  return (
    <Container className='py-4'>
      <h2 className='mb-4' style={{ fontSize: 'clamp(1.1rem, 4vw, 1.5rem)' }}>مدیریت سفارش‌ها</h2>

      {isLoading ? <Loader /> : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <>
          {/* دسکتاپ */}
          <div className='d-none d-md-block'>
            <Table striped hover responsive className='admin-table'>
              <thead>
                <tr>
                  <th>شناسه</th>
                  <th>کاربر</th>
                  <th>تاریخ</th>
                  <th>مبلغ</th>
                  <th>رسید</th>
                  <th>پرداخت</th>
                  <th>ارسال</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order._id}>
                    <td>#{order._id.slice(-6)}</td>
                    <td>{order.user?.name}</td>
                    <td>{new Date(order.createdAt).toLocaleDateString('fa-IR')}</td>
                    <td>{Math.round(order.totalPrice).toLocaleString('fa-IR')} تومان</td>
                    <td>
                      {order.paymentResult?.receiptImage
                        ? <Badge bg='info'>رسید دارد</Badge>
                        : <Badge bg='secondary'>ندارد</Badge>}
                    </td>
                    <td>
                      {order.isPaid
                        ? <Badge bg='success'>تأیید شده</Badge>
                        : <Badge bg='danger'>تأیید نشده</Badge>}
                    </td>
                    <td>
                      {order.isDelivered
                        ? <Badge bg='success'>ارسال شده</Badge>
                        : <Badge bg='warning'>در انتظار</Badge>}
                    </td>
                    <td>
                      <Link to={`/order/${order._id}`}>
                        <Button size='sm' className='btn-aqualotus'><FaEye /></Button>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>

          {/* موبایل */}
          <div className='d-md-none'>
            <Row className='g-3'>
              {orders.map((order) => (
                <Col xs={12} key={order._id}>
                  <Card className='shadow-sm'>
                    <Card.Body>
                      <div className='d-flex justify-content-between align-items-start mb-2'>
                        <div>
                          <div style={{ fontWeight: '600' }}>#{order._id.slice(-6)}</div>
                          <div style={{ fontSize: '0.85rem', color: '#666' }}>{order.user?.name}</div>
                          <div style={{ fontSize: '0.8rem', color: '#999' }}>
                            {new Date(order.createdAt).toLocaleDateString('fa-IR')}
                          </div>
                        </div>
                        <Link to={`/order/${order._id}`}>
                          <Button size='sm' className='btn-aqualotus'><FaEye /></Button>
                        </Link>
                      </div>
                      <div style={{ fontWeight: '600', color: '#2d6a4f', marginBottom: '8px' }}>
                        {Math.round(order.totalPrice).toLocaleString('fa-IR')} تومان
                      </div>
                      <div className='d-flex flex-wrap gap-2'>
                        {order.paymentResult?.receiptImage
                          ? <Badge bg='info'>رسید دارد</Badge>
                          : <Badge bg='secondary'>بدون رسید</Badge>}
                        {order.isPaid
                          ? <Badge bg='success'>پرداخت تأیید</Badge>
                          : <Badge bg='danger'>پرداخت نشده</Badge>}
                        {order.isDelivered
                          ? <Badge bg='success'>ارسال شده</Badge>
                          : <Badge bg='warning' text='dark'>در انتظار ارسال</Badge>}
                      </div>
                    </Card.Body>
                  </Card>
                </Col>
              ))}
            </Row>
          </div>
        </>
      )}
    </Container>
  )
}

export default OrderListPage
