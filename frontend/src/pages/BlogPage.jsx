import { Container, Row, Col, Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import { useGetPostsQuery } from '../slices/blogApiSlice'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'
import HeroSlider from '../components/ui/HeroSlider'

const SITE = 'https://aqualotus.ir'

const BlogPage = () => {
  const { data: posts, isLoading, error } = useGetPostsQuery()

  return (
    <>
      <Helmet>
        <title>وبلاگ | AquaLotus</title>
        <meta name='description' content='مطالب آموزشی گیاهان آکواریوم، نگهداری و راهنمای خرید' />
        <meta name='robots' content='index, follow' />
        <meta property='og:title' content='وبلاگ | AquaLotus' />
        <meta property='og:description' content='مطالب آموزشی گیاهان آکواریوم' />
        <meta property='og:image' content={`${SITE}/logo.png`} />
        <meta property='og:url' content={`${SITE}/blog`} />
        <meta property='og:type' content='website' />
        <meta property='og:site_name' content='AquaLotus' />
        <meta name='twitter:card' content='summary_large_image' />
        <meta name='twitter:title' content='وبلاگ | AquaLotus' />
        <meta name='twitter:image' content={`${SITE}/logo.png`} />
        <link rel='canonical' href={`${SITE}/blog`} />
        <script type='application/ld+json'>{JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Blog",
          "name": "AquaLotus Blog",
          "url": `${SITE}/blog`,
          "description": "مطالب آموزشی گیاهان آکواریوم",
          "publisher": {
            "@type": "Organization",
            "name": "AquaLotus",
            "logo": { "@type": "ImageObject", "url": `${SITE}/logo.png` }
          }
        })}</script>
      </Helmet>

      <HeroSlider location='blog' />

      <Container className='py-4 py-md-5'>
        <h2 className='mb-4 aq-page-title'>وبلاگ</h2>
        {isLoading ? (
          <Loader />
        ) : error ? (
          <Message variant='danger'>خطا در دریافت پست‌ها</Message>
        ) : posts?.length === 0 ? (
          <Message>هنوز پستی منتشر نشده</Message>
        ) : (
          <Row className='g-3 g-md-4'>
            {posts?.map((post) => (
              <Col key={post._id} xs={12} sm={6} lg={4}>
                <Card className='h-100 aq-blog-card' style={{ borderRadius: '12px', overflow: 'hidden' }}>
                  {post.image && (
                    <Card.Img variant='top' src={post.image} loading='lazy'
                      style={{ height: '180px', objectFit: 'cover' }} />
                  )}
                  <Card.Body className='d-flex flex-column'>
                    <Card.Title style={{ fontSize: 'clamp(0.95rem, 2.5vw, 1.1rem)', fontWeight: '600' }}>
                      {post.title}
                    </Card.Title>
                    <Card.Text className='text-muted' style={{ fontSize: '0.88rem', flex: 1 }}>
                      {post.content.slice(0, 100)}...
                    </Card.Text>
                    <div className='d-flex justify-content-between align-items-center mt-2'>
                      <small className='text-muted'>
                        {new Date(post.createdAt).toLocaleDateString('fa-IR')}
                      </small>
                      <Link to={`/blog/${post._id}`} className='btn btn-sm btn-outline-success'>
                        ادامه مطلب
                      </Link>
                    </div>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        )}
      </Container>
    </>
  )
}

export default BlogPage
