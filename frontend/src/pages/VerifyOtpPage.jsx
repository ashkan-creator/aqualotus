import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Form, Button, Row, Col, Container, Card } from 'react-bootstrap'
import { useVerifyOtpAndResetMutation } from '../slices/usersApiSlice'
import { toast } from 'react-toastify'
import Loader from '../components/ui/Loader'
import { FaLeaf } from 'react-icons/fa'
import { Helmet } from 'react-helmet-async'

const VerifyOtpPage = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const phone = location.state?.phone || ''

  const [otp, setOtp] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const [verifyOtpAndReset, { isLoading }] = useVerifyOtpAndResetMutation()

  const submitHandler = async (e) => {
    e.preventDefault()
    if (password !== confirmPassword) {
      toast.error('رمز عبور و تکرار آن یکسان نیستند')
      return
    }
    try {
      await verifyOtpAndReset({ phone, otp, password }).unwrap()
      toast.success('رمز عبور با موفقیت تغییر کرد')
      navigate('/login')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در تایید کد')
    }
  }

  if (!phone) {
    return (
      <Container className='py-5'>
        <Row className='justify-content-center'>
          <Col xs={12} md={6} lg={5} className='text-center'>
            <p>شماره موبایلی برای تایید یافت نشد.</p>
            <Link to='/forgot-password' className='auth-link'>بازگشت به بازیابی رمز عبور</Link>
          </Col>
        </Row>
      </Container>
    )
  }

  return (
    <>
      <Helmet><title>تایید کد | AquaLotus</title></Helmet>
      <Container className='py-5'>
        <Row className='justify-content-center'>
          <Col xs={12} md={6} lg={5}>
            <Card className='auth-card'>
              <Card.Body className='p-4'>
                <div className='text-center mb-4'>
                  <FaLeaf className='auth-icon' />
                  <h2 className='auth-title'>تایید کد پیامکی</h2>
                  <p className='text-muted' style={{ fontSize: '0.9rem' }}>
                    کد ارسال شده به {phone} را وارد کنید
                  </p>
                </div>

                <Form onSubmit={submitHandler}>
                  <Form.Group className='mb-3'>
                    <Form.Label>کد تایید</Form.Label>
                    <Form.Control
                      type='text'
                      inputMode='numeric'
                      maxLength={6}
                      className='otp-input'
                      value={otp}
                      onChange={(e) => setOtp(e.target.value)}
                      required
                    />
                  </Form.Group>

                  <Form.Group className='mb-3'>
                    <Form.Label>رمز عبور جدید</Form.Label>
                    <Form.Control
                      type='password'
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      minLength={6}
                    />
                  </Form.Group>

                  <Form.Group className='mb-4'>
                    <Form.Label>تکرار رمز عبور جدید</Form.Label>
                    <Form.Control
                      type='password'
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                      minLength={6}
                    />
                  </Form.Group>

                  <Button type='submit' className='w-100 btn-aqualotus' disabled={isLoading}>
                    {isLoading ? 'در حال ثبت...' : 'تایید و تغییر رمز عبور'}
                  </Button>
                </Form>

                {isLoading && <Loader />}

                <Row className='mt-3'>
                  <Col className='text-center'>
                    <Link to='/forgot-password' className='auth-link'>ارسال مجدد کد</Link>
                  </Col>
                </Row>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  )
}

export default VerifyOtpPage
