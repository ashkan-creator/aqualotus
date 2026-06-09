import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Form, Button, Container, Card, Row, Col } from 'react-bootstrap'
import { toast } from 'react-toastify'
import { FaArrowRight } from 'react-icons/fa'
import {
  useGetUserDetailsQuery,
  useUpdateUserMutation,
} from '../../slices/usersApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const UserEditPage = () => {
  const { id: userId } = useParams()
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [isAdmin, setIsAdmin] = useState(false)

  const { data: user, isLoading, error } = useGetUserDetailsQuery(userId)
  const [updateUser, { isLoading: loadingUpdate }] = useUpdateUserMutation()

  useEffect(() => {
    if (user) {
      setName(user.name)
      setEmail(user.email)
      setIsAdmin(user.isAdmin)
    }
  }, [user])

  const submitHandler = async (e) => {
    e.preventDefault()
    try {
      await updateUser({ userId, name, email, isAdmin }).unwrap()
      toast.success('کاربر با موفقیت آپدیت شد')
      navigate('/admin/userlist')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در آپدیت کاربر')
    }
  }

  return (
    <Container className='py-4'>
      <Button
        variant='outline-secondary'
        className='mb-4'
        onClick={() => navigate('/admin/userlist')}
      >
        <FaArrowRight className='ms-1' /> بازگشت به لیست کاربران
      </Button>

      <Row className='justify-content-center'>
        <Col xs={12} md={6}>
          <Card className='auth-card'>
            <Card.Body className='p-4'>
              <h3 className='mb-4 text-center'>ویرایش کاربر</h3>

              {isLoading ? (
                <Loader />
              ) : error ? (
                <Message variant='danger'>{error?.data?.message || 'خطا در دریافت اطلاعات'}</Message>
              ) : (
                <Form onSubmit={submitHandler}>
                  <Form.Group className='mb-3'>
                    <Form.Label>نام</Form.Label>
                    <Form.Control
                      type='text'
                      placeholder='نام کاربر'
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                    />
                  </Form.Group>

                  <Form.Group className='mb-3'>
                    <Form.Label>ایمیل</Form.Label>
                    <Form.Control
                      type='email'
                      placeholder='ایمیل کاربر'
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </Form.Group>

                  <Form.Group className='mb-4'>
                    <Form.Check
                      type='checkbox'
                      label='ادمین'
                      checked={isAdmin}
                      onChange={(e) => setIsAdmin(e.target.checked)}
                    />
                  </Form.Group>

                  <Button
                    type='submit'
                    className='w-100 btn-aqualotus'
                    disabled={loadingUpdate}
                  >
                    {loadingUpdate ? 'در حال ذخیره...' : 'ذخیره تغییرات'}
                  </Button>
                </Form>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default UserEditPage
