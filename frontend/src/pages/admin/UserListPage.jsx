import { Table, Button, Container, Badge } from 'react-bootstrap'
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
      <h2 className='mb-4'>مدیریت کاربران</h2>

      {loadingDelete && <Loader />}

      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <Table striped hover responsive className='admin-table'>
          <thead>
            <tr>
              <th>شناسه</th>
              <th>نام</th>
              <th>ایمیل</th>
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
                  {user.isAdmin ? (
                    <FaCheck className='text-success' />
                  ) : (
                    <FaTimes className='text-danger' />
                  )}
                </td>
                <td>
                  {new Date(user.createdAt).toLocaleDateString('fa-IR')}
                </td>
                <td>
                  <Button
                    size='sm'
                    variant='outline-primary'
                    className='ms-1'
                    onClick={() => navigate(`/admin/user/${user._id}/edit`)}
                  >
                    <FaEdit />
                  </Button>
                  <Button
                    size='sm'
                    variant='outline-danger'
                    onClick={() => deleteUserHandler(user._id)}
                    disabled={user.isAdmin}
                  >
                    <FaTrash />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  )
}

export default UserListPage