import { useParams } from 'react-router-dom'
import { Container, Row, Col } from 'react-bootstrap'
import { useGetLinkPageBySlugQuery } from '../slices/linkPageApiSlice'
import ProductCard from '../components/ui/ProductCard'
import Loader from '../components/ui/Loader'

const LinkPagePublicPage = () => {
  const { slug } = useParams()
  const { data: page, isLoading, error } = useGetLinkPageBySlugQuery(slug)

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(160deg, #1b4332 0%, #2d6a4f 50%, #52b788 100%)',
        padding: '32px 16px',
        direction: 'rtl',
      }}
    >
      <Container style={{ maxWidth: '480px' }}>
        {isLoading ? (
          <Loader />
        ) : error || !page ? (
          <div style={{ background: '#fff', borderRadius: '20px', padding: '32px', textAlign: 'center' }}>
            صفحه پیدا نشد
          </div>
        ) : (
          <>
            <div className='text-center mb-4'>
              <img
                src={page.avatar || '/logo.png'}
                alt=''
                style={{ width: '96px', height: '96px', borderRadius: '50%', objectFit: 'cover', border: '3px solid #fff' }}
              />
              {page.title && (
                <h4 style={{ color: '#fff', marginTop: '14px', fontWeight: '700' }}>{page.title}</h4>
              )}
              {page.bio && (
                <p style={{ color: 'rgba(255,255,255,0.85)', fontSize: '0.9rem', marginTop: '4px' }}>{page.bio}</p>
              )}
            </div>

            <div className='d-flex flex-column gap-3 mb-4'>
              {page.links.filter((l) => l.type !== 'product').map((link) => (
                <a
                  key={link._id}
                  href={link.shortUrl}
                  target='_blank'
                  rel='noreferrer'
                  style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
                    background: 'rgba(255,255,255,0.95)', color: '#1b4332',
                    borderRadius: '14px', padding: '14px 18px', fontWeight: '600',
                    textDecoration: 'none', boxShadow: '0 4px 14px rgba(0,0,0,0.15)',
                  }}
                >
                  {link.icon && <span>{link.icon}</span>}
                  {link.label}
                </a>
              ))}
            </div>

            {page.links.some((l) => l.type === 'product' && l.product) && (
              <Row className='g-3'>
                {page.links
                  .filter((l) => l.type === 'product' && l.product)
                  .map((link) => (
                    <Col key={link._id} xs={3}>
                      <ProductCard product={link.product} />
                    </Col>
                  ))}
              </Row>
            )}

            <p className='text-center mt-4' style={{ color: 'rgba(255,255,255,0.6)', fontSize: '0.75rem' }}>
              AquaLotus 🌿
            </p>
          </>
        )}
      </Container>
    </div>
  )
}

export default LinkPagePublicPage
