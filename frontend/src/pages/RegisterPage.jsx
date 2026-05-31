import { useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Form, Button, Row, Col, Container, Card } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { useRegisterMutation } from '../slices/usersApiSlice'
import { setCredentials } from '../slices/authSlice'
import { toast } from 'react-toastify'
import Loader from '../components/ui/Loader'
import { FaLeaf } from 'react-icons/fa'

const RegisterPage = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const dispatch = useDispatch()
  const navigate = useNavigate()

  const [register, { isLoading }] = useRegisterMutation()
  const { userInfo } = useSelector((state) => state.auth)

  const { search } = useLocation()
  const sp = new URLSearchParams(search)
  const redirect = sp.get('redirect') || '/'

  useEffect(() => {
    if (userInfo) navigate(redirect)
  }, [userInfo, redirect, navigate])

  const submitHandler = async (e) => {
    e.preventDefault()
    if (password !== confirmPassword) {
      toast.error('رمز عبور و تکرار آن یکسان نیستند')
      return
    }
    try {
      const res = await register({ name, email, password }).unwrap()
      dispatch(setCredentials({ ...res }))
      navigate(redirect)
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ثبت‌نام')
    }
  }

  return (
    <Container className='py-5'>
      <Row className='justify-content-center'>
        <Col xs={12} md={6} lg={5}>
          <Card className='auth-card'>
            <Card.Body className='p-4'>
              <div className='text-center mb-4'>
                <FaLeaf className='auth-icon' />
                <h2 className='auth-title'>ثبت‌نام</h2>
              </div>

              <Form onSubmit={submitHandler}>
                <Form.Group className='mb-3'>
                  <Form.Label>نام</Form.Label>
                  <Form.Control
                    type='text'
                    placeholder='نام خود را وارد کنید'
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </Form.Group>

                <Form.Group className='mb-3'>
                  <Form.Label>ایمیل</Form.Label>
                  <Form.Control
                    type='email'
                    placeholder='ایمیل خود را وارد کنید'
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </Form.Group>

                <Form.Group className='mb-3'>
                  <Form.Label>رمز عبور</Form.Label>
                  <Form.Control
                    type='password'
                    placeholder='رمز عبور را وارد کنید'
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </Form.Group>

                <Form.Group className='mb-4'>
                  <Form.Label>تکرار رمز عبور</Form.Label>
                  <Form.Control
                    type='password'
                    placeholder='رمز عبور را تکرار کنید'
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                  />
                </Form.Group>

                <Button
                  type='submit'
                  className='w-100 btn-aqualotus'
                  disabled={isLoading}
                >
                  {isLoading ? 'در حال ثبت‌نام...' : 'ثبت‌نام'}
                </Button>
              </Form>

              {isLoading && <Loader />}

              <Row className='mt-3'>
                <Col className='text-center'>
                  <span>حساب دارید؟ </span>
                  <Link to={redirect ? `/login?redirect=${redirect}` : '/login'}>
                    وارد شوید
                  </Link>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default RegisterPage