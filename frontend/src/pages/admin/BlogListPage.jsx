import { Container, Table, Button, Badge, Card, Row, Col } from 'react-bootstrap'
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
      const post = await createPost({ title: 'عنوان پست جدید', content: 'محتوای پست...', isPublished: false }).unwrap()
      navigate(`/admin/blog/${post._id}/edit`)
    } catch { toast.error('خطا در ساخت پست') }
  }

  const deleteHandler = async (id) => {
    if (window.confirm('حذف شود؟')) {
      try {
        await deletePost(id).unwrap()
        refetch()
        toast.success('پست حذف شد')
      } catch { toast.error('خطا در حذف') }
    }
  }

  return (
    <Container className='py-4'>
      <div className='d-flex justify-content-between align-items-center mb-4'>
        <h2 style={{ fontSize: 'clamp(1rem, 4vw, 1.5rem)' }}>مدیریت وبلاگ</h2>
        <Button className='btn-aqualotus' size='sm' onClick={createHandler} disabled={loadingCreate}>
          <FaPlus className='ms-1' /> پست جدید
        </Button>
      </div>
      {isLoading ? <Loader /> : error ? <Message variant='danger'>خطا</Message> : (
        <>
          {/* دسکتاپ */}
          <div className='d-none d-md-block'>
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
                    <td>{post.isPublished ? <Badge bg='success'>منتشر شده</Badge> : <Badge bg='secondary'>پیش‌نویس</Badge>}</td>
                    <td>
                      <Button size='sm' variant='outline-primary' className='ms-1' onClick={() => navigate(`/admin/blog/${post._id}/edit`)}><FaEdit /></Button>
                      <Button size='sm' variant='outline-danger' onClick={() => deleteHandler(post._id)}><FaTrash /></Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>

          {/* موبایل */}
          <div className='d-md-none'>
            <Row className='g-3'>
              {posts?.map((post) => (
                <Col xs={12} key={post._id}>
                  <Card className='p-3'>
                    {post.image && <img src={post.image} alt='' loading='lazy' className='w-100 rounded mb-2' style={{ height: '140px', objectFit: 'cover' }} />}
                    <div className='d-flex justify-content-between align-items-start mb-1'>
                      <div style={{ fontWeight: '600', flex: 1, paddingLeft: '8px' }}>{post.title}</div>
                      {post.isPublished ? <Badge bg='success'>منتشر</Badge> : <Badge bg='secondary'>پیش‌نویس</Badge>}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#999', marginBottom: '10px' }}>
                      {post.user?.name} | {new Date(post.createdAt).toLocaleDateString('fa-IR')}
                    </div>
                    <div className='d-flex gap-2'>
                      <Button size='sm' variant='outline-primary' className='flex-grow-1' onClick={() => navigate(`/admin/blog/${post._id}/edit`)}>
                        <FaEdit className='ms-1' /> ویرایش
                      </Button>
                      <Button size='sm' variant='outline-danger' onClick={() => deleteHandler(post._id)}><FaTrash /></Button>
                    </div>
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

export default BlogListPage
