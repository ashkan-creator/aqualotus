import { Container, Row, Col } from 'react-bootstrap'
import { Link, useParams } from 'react-router-dom'
import { useGetPostByIdQuery } from '../slices/blogApiSlice'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'

const BlogPostPage = () => {
  const { id } = useParams()
  const { data: post, isLoading, error } = useGetPostByIdQuery(id)

  return (
    <Container className='py-5'>
      <Link to='/blog' className='btn btn-outline-secondary mb-4'>بازگشت به وبلاگ</Link>
      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>پست پیدا نشد</Message>
      ) : (
        <Row className='justify-content-center'>
          <Col md={8}>
            <h2 className='mb-3'>{post.title}</h2>
            <p className='text-muted mb-4'>
              نوشته: {post.user?.name} | {new Date(post.createdAt).toLocaleDateString('fa-IR')}
            </p>
            {post.image && (
              <img src={post.image} alt={post.title} className='w-100 rounded mb-4' style={{ maxHeight: '400px', objectFit: 'cover' }} />
            )}
            {post.video && (
              <video controls className='w-100 rounded mb-4'>
                <source src={post.video} />
              </video>
            )}
            <div style={{ lineHeight: '2', whiteSpace: 'pre-wrap' }}>{post.content}</div>
          </Col>
        </Row>
      )}
    </Container>
  )
}

export default BlogPostPage
