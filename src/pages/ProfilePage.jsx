import { useState, useEffect } from 'react'
import { Row, Col, Form, Button, Container, Card, Table, Badge, Nav } from 'react-bootstrap'
import { useSelector, useDispatch } from 'react-redux'
import { toast } from 'react-toastify'
import { useProfileMutation } from '../slices/usersApiSlice'
import { useGetMyOrdersQuery } from '../slices/ordersApiSlice'
import { setCredentials } from '../slices/authSlice'
import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'
import CustomerWishlistList from '../components/ui/CustomerWishlistList'
import CustomerAddressesList from '../components/ui/CustomerAddressesList'
import './ProfilePage.css'

const DashboardTab = ({ userInfo, orders, loadingOrders }) => {
  const lastOrder = orders && orders.length > 0 ? orders[0] : null
  return (
    <Card className='auth-card'>
      <Card.Body className='p-4'>
        <h5 className='mb-3'>خوش آمدید، {userInfo?.name}</h5>
        <p className='text-muted' style={{ fontSize: '14px' }}>خلاصه‌ای از وضعیت حساب کاربری شما</p>
        <hr />
        {loadingOrders ? (
          <Loader />
        ) : lastOrder ? (
          <div className='d-flex justify-content-between align-items-center flex-wrap gap-2'>
            <div>
              <div className='text-muted mb-1' style={{ fontSize: '13px' }}>آخرین سفارش</div>
              <strong>#{lastOrder._id.slice(-6)}</strong>
            </div>
            <Link to={`/order/${lastOrder._id}`}>
              <Button size='sm' className='btn-aqualotus'>مشاهده جزئیات</Button>
            </Link>
          </div>
        ) : (
          <Message>هنوز سفارشی ثبت نکرده‌اید</Message>
        )}
      </Card.Body>
    </Card>
  )
}

const OrdersTab = ({ orders, loadingOrders, error }) => {
  return (
    <>
      <h5 className='mb-3'>سفارش‌های من</h5>
      {loadingOrders ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : orders?.length === 0 ? (
        <Message>هنوز سفارشی ثبت نکرده‌اید</Message>
      ) : (
        <Table striped hover responsive className='orders-table'>
          <thead>
            <tr>
              <th>شناسه</th>
              <th>تاریخ</th>
              <th>مبلغ</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order._id}>
                <td>#{order._id.slice(-6)}</td>
                <td>{new Date(order.createdAt).toLocaleDateString('fa-IR')}</td>
                <td>{Math.round(order.totalPrice).toLocaleString('fa-IR')} تومان</td>
                <td>
                  <Link to={`/order/${order._id}`}>
                    <Button size='sm' className='btn-aqualotus'>جزئیات</Button>
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </>
  )
}

const ProfileFormTab = ({ userInfo }) => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const dispatch = useDispatch()
  const [updateProfile, { isLoading }] = useProfileMutation()

  useEffect(() => {
    if (userInfo) {
      setName(userInfo.name)
      setEmail(userInfo.email)
    }
  }, [userInfo])

  const submitHandler = async (e) => {
    e.preventDefault()
    if (password !== confirmPassword) {
      toast.error('رمز عبور و تکرار آن یکسان نیستند')
      return
    }
    try {
      const res = await updateProfile({ name, email, password }).unwrap()
      dispatch(setCredentials(res))
      toast.success('پروفایل با موفقیت آپدیت شد')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در آپدیت پروفایل')
    }
  }

  return (
    <Card className='auth-card'>
      <Card.Body className='p-4'>
        <h5 className='mb-4'>پروفایل و امنیت</h5>
        <Form onSubmit={submitHandler}>
          <Form.Group className='mb-3'>
            <Form.Label>نام</Form.Label>
            <Form.Control type='text' value={name} onChange={(e) => setName(e.target.value)} />
          </Form.Group>
          <Form.Group className='mb-3'>
            <Form.Label>ایمیل</Form.Label>
            <Form.Control type='email' value={email} onChange={(e) => setEmail(e.target.value)} />
          </Form.Group>
          <Form.Group className='mb-3'>
            <Form.Label>رمز عبور جدید</Form.Label>
            <Form.Control type='password' placeholder='خالی بگذارید اگر تغییر نمی‌دهید' value={password} onChange={(e) => setPassword(e.target.value)} />
          </Form.Group>
          <Form.Group className='mb-4'>
            <Form.Label>تکرار رمز عبور</Form.Label>
            <Form.Control type='password' placeholder='تکرار رمز عبور جدید' value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
          </Form.Group>
          <Button type='submit' className='w-100 btn-aqualotus' disabled={isLoading}>ذخیره تغییرات</Button>
        </Form>
      </Card.Body>
    </Card>
  )
}

const ProfilePage = () => {
  const [activeTab, setActiveTab] = useState('dashboard')
  const { userInfo } = useSelector((state) => state.auth)
  const { data: orders, isLoading: loadingOrders, error } = useGetMyOrdersQuery()

  const userTabs = [
    { key: 'dashboard', label: 'داشبورد', icon: 'fa-gauge-high' },
    { key: 'orders', label: 'سفارش‌های من', icon: 'fa-box' },
    { key: 'profile', label: 'پروفایل و امنیت', icon: 'fa-user-shield' },
    { key: 'wishlist', label: 'علاقه‌مندی‌ها', icon: 'fa-heart' },
    { key: 'addresses', label: 'آدرس‌های من', icon: 'fa-location-dot' },
  ]

  return (
    <>
      <Helmet><title>پنل کاربری | AquaLotus</title></Helmet>
      <Container className='py-4'>
        <h4 className='mb-4'>حساب کاربری</h4>
        <Row>
          <Col md={3} className='mb-3 mb-md-0'>
            <Card className='auth-card'>
              <Card.Body className='p-2'>
                <Nav variant='pills' className='customer-panel-nav flex-column' activeKey={activeTab} onSelect={(k) => setActiveTab(k)}>
                  {userTabs.map((tab) => (
                    <Nav.Item key={tab.key}>
                      <Nav.Link eventKey={tab.key}>
                        <i className={`fa-solid ${tab.icon} me-2`}></i>
                        {tab.label}
                      </Nav.Link>
                    </Nav.Item>
                  ))}
                </Nav>
              </Card.Body>
            </Card>
          </Col>
          <Col md={9}>
            {activeTab === 'dashboard' && <DashboardTab userInfo={userInfo} orders={orders} loadingOrders={loadingOrders} />}
            {activeTab === 'orders' && <OrdersTab orders={orders} loadingOrders={loadingOrders} error={error} />}
            {activeTab === 'profile' && <ProfileFormTab userInfo={userInfo} />}
            {activeTab === 'wishlist' && <CustomerWishlistList />}
            {activeTab === 'addresses' && <CustomerAddressesList />}
          </Col>
        </Row>
      </Container>
    </>
  )
}

export default ProfilePage