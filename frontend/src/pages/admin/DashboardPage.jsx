import { Container, Row, Col, Card, Table, Badge } from 'react-bootstrap'
import { FaShoppingBag, FaUsers, FaBox, FaClock } from 'react-icons/fa'
import { Link } from 'react-router-dom'
import { useGetProductsQuery } from '../../slices/productsApiSlice'
import { useGetUsersQuery } from '../../slices/usersApiSlice'
import { useGetOrdersQuery } from '../../slices/ordersApiSlice'
import Loader from '../../components/ui/Loader'

const DashboardPage = () => {
  const { data: productsData } = useGetProductsQuery({ admin: true })
  const { data: users } = useGetUsersQuery()
  const { data: orders } = useGetOrdersQuery()

  const totalRevenue = orders
    ? orders.filter((o) => o.isPaid).reduce((acc, o) => acc + o.totalPrice, 0)
    : 0

  const pendingOrders = orders ? orders.filter((o) => !o.isDelivered).length : 0

  const stats = [
    {
      title: 'کل فروش',
      value: totalRevenue.toLocaleString('fa-IR') + ' تومان',
      icon: <FaShoppingBag size={28} />,
      color: '#2d6a4f',
      link: '/admin/orderlist',
    },
    {
      title: 'کاربران',
      value: users?.length || 0,
      icon: <FaUsers size={28} />,
      color: '#0d4f8b',
      link: '/admin/userlist',
    },
    {
      title: 'محصولات',
      value: productsData?.products?.length || 0,
      icon: <FaBox size={28} />,
      color: '#6a4c2d',
      link: '/admin/productlist',
    },
    {
      title: 'سفارش در انتظار',
      value: pendingOrders,
      icon: <FaClock size={28} />,
      color: '#b5451b',
      link: '/admin/orderlist',
    },
  ]

  return (
    <Container className='py-4'>
      <h2 className='mb-4'>داشبورد مدیریت</h2>

      {/* کارت‌های آمار */}
      <Row className='g-3 mb-5'>
        {stats.map((stat, i) => (
          <Col key={i} xs={12} sm={6} lg={3}>
            <Link to={stat.link} style={{ textDecoration: 'none' }}>
              <Card className='h-100 text-white' style={{ background: stat.color }}>
                <Card.Body className='d-flex justify-content-between align-items-center p-4'>
                  <div>
                    <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{stat.value}</div>
                    <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>{stat.title}</div>
                  </div>
                  <div style={{ opacity: 0.8 }}>{stat.icon}</div>
                </Card.Body>
              </Card>
            </Link>
          </Col>
        ))}
      </Row>

      {/* آخرین سفارش‌ها */}
      <Row>
        <Col md={12}>
          <Card className='p-3'>
            <h5 className='mb-3'>📦 آخرین سفارش‌ها</h5>
            {!orders ? (
              <Loader />
            ) : (
              <Table striped hover responsive>
                <thead>
                  <tr>
                    <th>شناسه</th>
                    <th>کاربر</th>
                    <th>مبلغ</th>
                    <th>پرداخت</th>
                    <th>ارسال</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.slice(0, 8).map((order) => (
                    <tr key={order._id}>
                      <td>
                        <Link to={`/order/${order._id}`}>#{order._id.slice(-6)}</Link>
                      </td>
                      <td>{order.user?.name || '-'}</td>
                      <td>{order.totalPrice.toLocaleString('fa-IR')} تومان</td>
                      <td>
                        {order.isPaid ? (
                          <Badge bg='success'>پرداخت شده</Badge>
                        ) : (
                          <Badge bg='danger'>در انتظار</Badge>
                        )}
                      </td>
                      <td>
                        {order.isDelivered ? (
                          <Badge bg='success'>ارسال شده</Badge>
                        ) : (
                          <Badge bg='warning'>در انتظار</Badge>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            )}
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default DashboardPage
