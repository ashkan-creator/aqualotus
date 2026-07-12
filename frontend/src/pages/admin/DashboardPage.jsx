import { Container, Row, Col, Card, Table, Badge } from 'react-bootstrap'
import { FaShoppingBag, FaUsers, FaBox, FaClock } from 'react-icons/fa'
import { Link } from 'react-router-dom'
import {
  ResponsiveContainer, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  BarChart, Bar,
} from 'recharts'
import { useGetProductsQuery } from '../../slices/productsApiSlice'
import { useGetUsersQuery } from '../../slices/usersApiSlice'
import { useGetOrdersQuery } from '../../slices/ordersApiSlice'
import Loader from '../../components/ui/Loader'

const toPersianDate = (dateStr) => new Date(dateStr).toLocaleDateString('fa-IR', { month: 'short', day: 'numeric' })

const buildChartData = (orders) => {
  if (!orders) return []
  const map = {}
  orders.forEach((o) => {
    const day = toPersianDate(o.createdAt)
    if (!map[day]) map[day] = { date: day, سفارش: 0, درآمد: 0 }
    map[day]['سفارش'] += 1
    if (o.isPaid) map[day]['درآمد'] += Math.round(o.totalPrice / 1000)
  })
  return Object.values(map).slice(-14)
}

const DashboardPage = () => {
  const { data: productsData } = useGetProductsQuery({ admin: true })
  const { data: users } = useGetUsersQuery()
  const { data: orders } = useGetOrdersQuery()

  const totalRevenue = orders ? orders.filter((o) => o.isPaid).reduce((acc, o) => acc + o.totalPrice, 0) : 0
  const pendingOrders = orders ? orders.filter((o) => !o.isDelivered).length : 0
  const chartData = buildChartData(orders)

  const stats = [
    { title: 'کل فروش', value: (totalRevenue / 1000).toFixed(0) + ' هزار ت', icon: <FaShoppingBag size={22} />, color: '#2d6a4f', link: '/admin/orderlist' },
    { title: 'کاربران', value: users?.length || 0, icon: <FaUsers size={22} />, color: '#0d4f8b', link: '/admin/userlist' },
    { title: 'محصولات', value: productsData?.products?.length || 0, icon: <FaBox size={22} />, color: '#6a4c2d', link: '/admin/productlist' },
    { title: 'در انتظار', value: pendingOrders, icon: <FaClock size={22} />, color: '#b5451b', link: '/admin/orderlist' },
  ]

  return (
    <Container className='py-4'>
      <h2 className='mb-4' style={{ fontSize: 'clamp(1rem, 4vw, 1.5rem)' }}>داشبورد مدیریت</h2>

      {/* کارت‌های آمار */}
      <Row className='g-3 mb-4'>
        {stats.map((stat, i) => (
          <Col key={i} xs={6} lg={3}>
            <Link to={stat.link} style={{ textDecoration: 'none' }}>
              <Card className='h-100 text-white' style={{ background: stat.color }}>
                <Card.Body className='d-flex justify-content-between align-items-center p-3'>
                  <div>
                    <div style={{ fontSize: 'clamp(0.9rem, 3vw, 1.5rem)', fontWeight: 'bold', lineHeight: 1.2 }}>{stat.value}</div>
                    <div style={{ fontSize: 'clamp(0.65rem, 2vw, 0.85rem)', opacity: 0.9 }}>{stat.title}</div>
                  </div>
                  <div style={{ opacity: 0.8 }}>{stat.icon}</div>
                </Card.Body>
              </Card>
            </Link>
          </Col>
        ))}
      </Row>

      {/* نمودار سفارش‌ها */}
      {chartData.length > 0 && (
        <Row className='g-4 mb-4'>
          <Col xs={12} lg={8}>
            <Card className='p-3'>
              <h6 className='mb-3'>📈 درآمد ۱۴ روز گذشته (هزار تومان)</h6>
              <ResponsiveContainer width='100%' height={220}>
                <AreaChart data={chartData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                  <defs>
                    <linearGradient id='colorRev' x1='0' y1='0' x2='0' y2='1'>
                      <stop offset='5%' stopColor='#2d6a4f' stopOpacity={0.3} />
                      <stop offset='95%' stopColor='#2d6a4f' stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray='3 3' stroke='#f0f0f0' />
                  <XAxis dataKey='date' tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Area type='monotone' dataKey='درآمد' stroke='#2d6a4f' fill='url(#colorRev)' strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </Card>
          </Col>
          <Col xs={12} lg={4}>
            <Card className='p-3'>
              <h6 className='mb-3'>📦 تعداد سفارش</h6>
              <ResponsiveContainer width='100%' height={220}>
                <BarChart data={chartData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray='3 3' stroke='#f0f0f0' />
                  <XAxis dataKey='date' tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey='سفارش' fill='#52b788' radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </Col>
        </Row>
      )}

      {/* آخرین سفارش‌ها */}
      <Card className='p-3'>
        <h5 className='mb-3'>📦 آخرین سفارش‌ها</h5>
        {!orders ? <Loader /> : (
          <>
            <div className='d-none d-md-block'>
              <Table striped hover responsive>
                <thead>
                  <tr><th>شناسه</th><th>کاربر</th><th>مبلغ</th><th>پرداخت</th><th>ارسال</th></tr>
                </thead>
                <tbody>
                  {orders.slice(0, 8).map((order) => (
                    <tr key={order._id}>
                      <td><Link to={`/order/${order._id}`}>#{order._id.slice(-6)}</Link></td>
                      <td>{order.user?.name || '-'}</td>
                      <td>{order.totalPrice.toLocaleString('fa-IR')} تومان</td>
                      <td>{order.isPaid ? <Badge bg='success'>پرداخت</Badge> : <Badge bg='danger'>در انتظار</Badge>}</td>
                      <td>{order.isDelivered ? <Badge bg='success'>ارسال</Badge> : <Badge bg='warning'>در انتظار</Badge>}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
            <div className='d-md-none'>
              <Row className='g-2'>
                {orders.slice(0, 6).map((order) => (
                  <Col xs={12} key={order._id}>
                    <Link to={`/order/${order._id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                      <Card className='p-2'>
                        <div className='d-flex justify-content-between align-items-center'>
                          <div>
                            <div style={{ fontWeight: '600', fontSize: '0.9rem' }}>#{order._id.slice(-6)} — {order.user?.name || '-'}</div>
                            <div style={{ fontSize: '0.85rem', color: '#2d6a4f', fontWeight: '600' }}>{order.totalPrice.toLocaleString('fa-IR')} تومان</div>
                          </div>
                          <div className='d-flex flex-column gap-1 align-items-end'>
                            {order.isPaid ? <Badge bg='success'>پرداخت</Badge> : <Badge bg='danger'>در انتظار</Badge>}
                            {order.isDelivered ? <Badge bg='success'>ارسال</Badge> : <Badge bg='warning'>در انتظار</Badge>}
                          </div>
                        </div>
                      </Card>
                    </Link>
                  </Col>
                ))}
              </Row>
            </div>
          </>
        )}
      </Card>
    </Container>
  )
}

export default DashboardPage
