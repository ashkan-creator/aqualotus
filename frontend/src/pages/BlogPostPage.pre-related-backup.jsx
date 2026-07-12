import { Container, Row, Col } from 'react-bootstrap'
import { Link, useParams } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import { useGetPostByIdQuery } from '../slices/blogApiSlice'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'

const SITE = 'https://aqualotus.ir'

const BlogPostPage = () => {
  const { id } = useParams()
  const { data: post, isLoading, error } = useGetPostByIdQuery(id)

  return (
    <Container className='py-4'>
      <Link to='/blog' className='btn btn-outline-secondary mb-4'>
        بازگشت به وبلاگ
      </Link>

      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>پست پیدا نشد</Message>
      ) : (
        <Row className='justify-content-center'>
          <Col xs={12} md={10} lg={8}>
            <Helmet>
              <title>{post?.title ? `${post.title} | وبلاگ AquaLotus` : 'AquaLotus'}</title>
              <meta name='description' content={post?.content?.slice(0, 155)} />
              <meta name='robots' content='index, follow' />
              <meta property='og:title' content={post?.title} />
              <meta property='og:description' content={post?.content?.slice(0, 155)} />
              <meta property='og:image' content={post?.image || `${SITE}/logo.png`} />
              <meta property='og:url' content={`${SITE}/blog/${post?._id}`} />
              <meta property='og:type' content='article' />
              <meta property='og:site_name' content='AquaLotus' />
              <meta name='twitter:card' content='summary_large_image' />
              <meta name='twitter:title' content={post?.title} />
              <meta name='twitter:image' content={post?.image || `${SITE}/logo.png`} />
              <link rel='canonical' href={`${SITE}/blog/${post?._id}`} />
              <script type='application/ld+json'>{JSON.stringify({
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": post?.title,
                "image": post?.image,
                "author": { "@type": "Person", "name": post?.user?.name },
                "publisher": {
                  "@type": "Organization",
                  "name": "AquaLotus",
                  "logo": { "@type": "ImageObject", "url": `${SITE}/logo.png` }
                },
                "datePublished": post?.createdAt,
                "dateModified": post?.updatedAt,
                "description": post?.content?.slice(0, 200)
              })}</script>
            </Helmet>

            <h2 style={{ fontSize: 'clamp(1.2rem, 4vw, 1.8rem)', marginBottom: '0.5rem' }}>
              {post?.title}
            </h2>
            <p className='text-muted mb-4' style={{ fontSize: '0.88rem' }}>
              نوشته: {post?.user?.name} | {new Date(post?.createdAt).toLocaleDateString('fa-IR')}
            </p>
            {post?.image && (
              <img src={post.image} alt={post.title} loading='lazy' className='w-100 rounded mb-4'
                style={{ maxHeight: '360px', objectFit: 'cover' }} />
            )}
            {post?.video && (
              <video controls className='w-100 rounded mb-4'>
                <source src={post.video} />
              </video>
            )}
            <div style={{ lineHeight: '2.2', whiteSpace: 'pre-wrap', fontSize: 'clamp(0.9rem, 2.5vw, 1rem)' }}>
              {post?.content}
            </div>
          </Col>
        </Row>
      )}
    </Container>
  )
}

export default BlogPostPage
