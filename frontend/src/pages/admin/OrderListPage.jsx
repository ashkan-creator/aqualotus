import { Table, Button, Container, Badge } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { FaEye } from 'react-icons/fa'
import { useGetOrdersQuery } from '../../slices/ordersApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const OrderListPage = () => {
  const { data: orders, isLoading, error } = useGetOrdersQuery()

  return (
    <Container className='py-4'>
      <h2 className='mb-4'>مدیریت سفارش‌ها</h2>

      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
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
                <td>
                  {new Date(order.createdAt).toLocaleDateString('fa-IR')}
                </td>
                <td>
                  {Math.round(order.totalPrice).toLocaleString('fa-IR')} تومان
                </td>
                <td>
                  {order.paymentResult?.receiptImage ? (
                    <Badge bg='info'>رسید دارد</Badge>
                  ) : (
                    <Badge bg='secondary'>ندارد</Badge>
                  )}
                </td>
                <td>
                  {order.isPaid ? (
                    <Badge bg='success'>تأیید شده</Badge>
                  ) : (
                    <Badge bg='danger'>تأیید نشده</Badge>
                  )}
                </td>
                <td>
                  {order.isDelivered ? (
                    <Badge bg='success'>ارسال شده</Badge>
                  ) : (
                    <Badge bg='warning'>در انتظار</Badge>
                  )}
                </td>
                <td>
                  <Link to={`/order/${order._id}`}>
                    <Button size='sm' className='btn-aqualotus'>
                      <FaEye />
                    </Button>
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  )
}

export default OrderListPage