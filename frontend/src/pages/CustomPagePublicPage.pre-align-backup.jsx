import { useParams, Link } from 'react-router-dom'
import { Container, Row, Col } from 'react-bootstrap'
import { Helmet } from 'react-helmet-async'
import { useGetCustomPageBySlugQuery } from '../slices/customPageApiSlice'
import ProductCard from '../components/ui/ProductCard'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'

const CustomPagePublicPage = () => {
  const { slug } = useParams()
  const { data: page, isLoading, error } = useGetCustomPageBySlugQuery(slug)

  if (isLoading) return <Container className='py-5'><Loader /></Container>
  if (error || !page) return <Container className='py-5'><Message variant='danger'>صفحه پیدا نشد</Message></Container>

  return (
    <>
      <Helmet>
        <title>{page.heroTitle ? `${page.heroTitle} | AquaLotus` : 'AquaLotus'}</title>
      </Helmet>

      {page.heroImage && (
        <div
          style={{
            backgroundImage: `url(${page.heroImage})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            minHeight: '360px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            position: 'relative',
          }}
        >
          <div style={{ position: 'absolute', inset: 0, background: 'rgba(27,67,50,0.45)' }} />
          <div className='text-center' style={{ position: 'relative', zIndex: 1, color: '#fff', padding: '24px' }}>
            {page.heroTitle && (
              <h1 style={{ fontSize: 'clamp(1.6rem, 5vw, 2.8rem)', fontWeight: '800' }}>{page.heroTitle}</h1>
            )}
            {page.heroSubtitle && (
              <p style={{ fontSize: 'clamp(0.95rem, 2.5vw, 1.2rem)' }}>{page.heroSubtitle}</p>
            )}
            {page.heroButtonText && page.heroButtonLink && (
              <Link to={page.heroButtonLink} className='btn btn-aqualotus px-4 mt-2'>
                {page.heroButtonText}
              </Link>
            )}
          </div>
        </div>
      )}

      <Container className='py-5'>
        {page.sections?.map((section, idx) => (
          <div key={idx} className='mb-5'>
            {section.heading && <h3 className='mb-3'>{section.heading}</h3>}
            {section.image && (
              <img src={section.image} alt='' className='w-100 rounded mb-3' style={{ maxHeight: '360px', objectFit: 'cover' }} />
            )}
            {section.body && (
              <p style={{ lineHeight: '2', whiteSpace: 'pre-wrap' }}>{section.body}</p>
            )}
          </div>
        ))}

        {page.relatedProducts?.length > 0 && (
          <div className='mt-5'>
            <h4 className='mb-3'>🛒 محصولات مرتبط</h4>
            <Row className='g-3'>
              {page.relatedProducts.map((product) => (
                <Col key={product._id} xs={6} md={3}>
                  <ProductCard product={product} />
                </Col>
              ))}
            </Row>
          </div>
        )}
      </Container>
    </>
  )
}

export default CustomPagePublicPage
