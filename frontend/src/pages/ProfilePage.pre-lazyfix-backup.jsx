import { useState, useEffect } from 'react'
import { Row, Col, Form, Button, Container, Card, Table, Badge } from 'react-bootstrap'
import { useSelector, useDispatch } from 'react-redux'
import { toast } from 'react-toastify'
import { useProfileMutation } from '../slices/usersApiSlice'
import { useGetMyOrdersQuery } from '../slices/ordersApiSlice'
import { setCredentials } from '../slices/authSlice'
import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'

const ProfilePage = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const dispatch = useDispatch()
  const { userInfo } = useSelector((state) => state.auth)

  const [updateProfile, { isLoading }] = useProfileMutation()
  const { data: orders, isLoading: loadingOrders, error } = useGetMyOrdersQuery()

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
      const res = await updateProfile({
        name,
        email,
        password,
      }).unwrap()
      dispatch(setCredentials(res))
      toast.success('پروفایل با موفقیت آپدیت شد')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در آپدیت پروفایل')
    }
  }

  return (
    <>
      <Helmet><title>پروفایل | AquaLotus</title></Helmet>
      <Container className='py-4'>
      <Row>
        <Col md={3}>
          <Card className='auth-card mb-3'>
            <Card.Body className='p-4'>
              <h4 className='mb-4'>پروفایل من</h4>
              <Form onSubmit={submitHandler}>
                <Form.Group className='mb-3'>
                  <Form.Label>نام</Form.Label>
                  <Form.Control
                    type='text'
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </Form.Group>

                <Form.Group className='mb-3'>
                  <Form.Label>ایمیل</Form.Label>
                  <Form.Control
                    type='email'
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </Form.Group>

                <Form.Group className='mb-3'>
                  <Form.Label>رمز عبور جدید</Form.Label>
                  <Form.Control
                    type='password'
                    placeholder='خالی بگذارید اگر تغییر نمی‌دهید'
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </Form.Group>

                <Form.Group className='mb-4'>
                  <Form.Label>تکرار رمز عبور</Form.Label>
                  <Form.Control
                    type='password'
                    placeholder='تکرار رمز عبور جدید'
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                </Form.Group>

                <Button
                  type='submit'
                  className='w-100 btn-aqualotus'
                  disabled={isLoading}
                >
                  {isLoading ? 'در حال ذخیره...' : 'ذخیره تغییرات'}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={9}>
          <h4 className='mb-3'>سفارش‌های من</h4>
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
                  <th>پرداخت</th>
                  <th>ارسال</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order._id}>
                    <td>#{order._id.slice(-6)}</td>
                    <td>
                      {new Date(order.createdAt).toLocaleDateString('fa-IR')}
                    </td>
                    <td>
                      {Math.round(order.totalPrice).toLocaleString('fa-IR')} تومان
                    </td>
                    <td>
                      {order.isPaid ? (
                        <Badge bg='success'>تأیید شده</Badge>
                      ) : order.paymentResult?.receiptImage ? (
                        <Badge bg='info'>در انتظار تأیید</Badge>
                      ) : (
                        <Badge bg='danger'>پرداخت نشده</Badge>
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
                          جزئیات
                        </Button>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Col>
      </Row>
    </Container>
    </>
  )
}

export default ProfilePage