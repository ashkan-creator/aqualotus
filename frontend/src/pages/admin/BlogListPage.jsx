import { Container, Table, Button, Badge } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { FaEdit, FaTrash, FaPlus } from 'react-icons/fa'
import { toast } from 'react-toastify'
import { useGetAllPostsQuery, useCreatePostMutation, useDeletePostMutation } from '../../slices/blogApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const BlogListPage = () => {
  const navigate = useNavigate()
  const { data: posts, isLoading, error, refetch } = useGetAllPostsQuery()
  const [createPost, { isLoading: loadingCreate }] = useCreatePostMutation()
  const [deletePost] = useDeletePostMutation()

  const createHandler = async () => {
    try {
      const post = await createPost({
        title: 'عنوان پست جدید',
        content: 'محتوای پست...',
        isPublished: false,
      }).unwrap()
      navigate(`/admin/blog/${post._id}/edit`)
    } catch {
      toast.error('خطا در ساخت پست')
    }
  }

  const deleteHandler = async (id) => {
    if (window.confirm('حذف شود؟')) {
      try {
        await deletePost(id).unwrap()
        refetch()
        toast.success('پست حذف شد')
      } catch {
        toast.error('خطا در حذف')
      }
    }
  }

  return (
    <Container className='py-4'>
      <div className='d-flex justify-content-between align-items-center mb-4'>
        <h2>مدیریت وبلاگ</h2>
        <Button className='btn-aqualotus' onClick={createHandler} disabled={loadingCreate}>
          <FaPlus className='ms-1' /> پست جدید
        </Button>
      </div>
      {isLoading ? <Loader /> : error ? <Message variant='danger'>خطا</Message> : (
        <Table striped hover responsive>
          <thead>
            <tr>
              <th>عنوان</th>
              <th>نویسنده</th>
              <th>تاریخ</th>
              <th>وضعیت</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {posts?.map((post) => (
              <tr key={post._id}>
                <td>{post.title}</td>
                <td>{post.user?.name}</td>
                <td>{new Date(post.createdAt).toLocaleDateString('fa-IR')}</td>
                <td>
                  {post.isPublished
                    ? <Badge bg='success'>منتشر شده</Badge>
                    : <Badge bg='secondary'>پیش‌نویس</Badge>}
                </td>
                <td>
                  <Button size='sm' variant='outline-primary' className='ms-1'
                    onClick={() => navigate(`/admin/blog/${post._id}/edit`)}>
                    <FaEdit />
                  </Button>
                  <Button size='sm' variant='outline-danger' onClick={() => deleteHandler(post._id)}>
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

export default BlogListPage
