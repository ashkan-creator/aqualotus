import { Table, Button, Container, Badge, Card, Row, Col } from 'react-bootstrap'
import { FaEdit, FaTrash, FaCheck, FaTimes } from 'react-icons/fa'
import { toast } from 'react-toastify'
import { useNavigate } from 'react-router-dom'
import {
  useGetUsersQuery,
  useDeleteUserMutation,
} from '../../slices/usersApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const UserListPage = () => {
  const navigate = useNavigate()
  const { data: users, isLoading, error, refetch } = useGetUsersQuery()
  const [deleteUser, { isLoading: loadingDelete }] = useDeleteUserMutation()

  const deleteUserHandler = async (id) => {
    if (window.confirm('آیا از حذف این کاربر مطمئن هستید؟')) {
      try {
        await deleteUser(id).unwrap()
        refetch()
        toast.success('کاربر حذف شد')
      } catch (err) {
        toast.error(err?.data?.message || 'خطا در حذف کاربر')
      }
    }
  }

  return (
    <Container className='py-4'>
      <h2 className='mb-4' style={{ fontSize: 'clamp(1.1rem, 4vw, 1.5rem)' }}>
        مدیریت کاربران ({users?.length || 0})
      </h2>
      {loadingDelete && <Loader />}
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
                  <th>نام</th>
                  <th>ایمیل</th>
                  <th>📱 تلفن</th>
                  <th>📍 آدرس</th>
                  <th>ادمین</th>
                  <th>تاریخ ثبت</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user._id}>
                    <td>#{user._id.slice(-6)}</td>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>
                      {user.phone
                        ? <a href={`tel:${user.phone}`} style={{ color: '#2d6a4f', textDecoration: 'none' }}>{user.phone}</a>
                        : <span className='text-muted' style={{ fontSize: '0.8rem' }}>ثبت نشده</span>}
                    </td>
                    <td style={{ maxWidth: '200px' }}>
                      {user.address
                        ? <small title={user.address}>{user.address.length > 40 ? user.address.slice(0, 40) + '...' : user.address}</small>
                        : <span className='text-muted' style={{ fontSize: '0.8rem' }}>ثبت نشده</span>}
                    </td>
                    <td>
                      {user.isAdmin ? <FaCheck className='text-success' /> : <FaTimes className='text-danger' />}
                    </td>
                    <td>{new Date(user.createdAt).toLocaleDateString('fa-IR')}</td>
                    <td>
                      <Button size='sm' variant='outline-primary' className='ms-1'
                        onClick={() => navigate(`/admin/user/${user._id}/edit`)}>
                        <FaEdit />
                      </Button>
                      <Button size='sm' variant='outline-danger'
                        onClick={() => deleteUserHandler(user._id)}
                        disabled={user.isAdmin}>
                        <FaTrash />
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>

          {/* موبایل */}
          <div className='d-md-none'>
            <Row className='g-3'>
              {users.map((user) => (
                <Col xs={12} key={user._id}>
                  <Card className='shadow-sm'>
                    <Card.Body>
                      <div className='d-flex justify-content-between align-items-start'>
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <div className='d-flex align-items-center gap-2 mb-1'>
                            <span style={{ fontWeight: '600' }}>{user.name}</span>
                            {user.isAdmin && <Badge bg='warning' text='dark'>ادمین</Badge>}
                          </div>
                          <div style={{ fontSize: '0.82rem', color: '#555', marginBottom: '2px' }}>{user.email}</div>
                          {user.phone && (
                            <a href={`tel:${user.phone}`} style={{ fontSize: '0.82rem', color: '#2d6a4f', textDecoration: 'none', display: 'block' }}>
                              📱 {user.phone}
                            </a>
                          )}
                          {user.address && (
                            <div style={{ fontSize: '0.78rem', color: '#888', marginTop: '2px' }}>
                              📍 {user.address.length > 50 ? user.address.slice(0, 50) + '...' : user.address}
                            </div>
                          )}
                          <div style={{ fontSize: '0.75rem', color: '#aaa', marginTop: '4px' }}>
                            {new Date(user.createdAt).toLocaleDateString('fa-IR')}
                          </div>
                        </div>
                        <div className='d-flex flex-column gap-2 ms-2'>
                          <Button size='sm' variant='outline-primary'
                            onClick={() => navigate(`/admin/user/${user._id}/edit`)}>
                            <FaEdit />
                          </Button>
                          <Button size='sm' variant='outline-danger'
                            onClick={() => deleteUserHandler(user._id)}
                            disabled={user.isAdmin}>
                            <FaTrash />
                          </Button>
                        </div>
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

export default UserListPage
