import { Container, Row, Col, Card, Badge } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useGetPostsQuery } from '../slices/blogApiSlice'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'

const BlogPage = () => {
  const { data: posts, isLoading, error } = useGetPostsQuery()

  return (
    <Container className='py-5'>
      <h2 className='mb-4'>وبلاگ</h2>
      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>خطا در دریافت پست‌ها</Message>
      ) : posts?.length === 0 ? (
        <Message>هنوز پستی منتشر نشده</Message>
      ) : (
        <Row className='g-4'>
          {posts?.map((post) => (
            <Col key={post._id} md={6} lg={4}>
              <Card className='h-100'>
                {post.image && (
                  <Card.Img variant='top' src={post.image} style={{ height: '200px', objectFit: 'cover' }} />
                )}
                <Card.Body>
                  <Card.Title>{post.title}</Card.Title>
                  <Card.Text className='text-muted' style={{ fontSize: '0.9rem' }}>
                    {post.content.slice(0, 120)}...
                  </Card.Text>
                </Card.Body>
                <Card.Footer className='d-flex justify-content-between align-items-center'>
                  <small className='text-muted'>
                    {new Date(post.createdAt).toLocaleDateString('fa-IR')}
                  </small>
                  <Link to={`/blog/${post._id}`} className='btn btn-sm btn-outline-success'>
                    ادامه مطلب
                  </Link>
                </Card.Footer>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </Container>
  )
}

export default BlogPage
