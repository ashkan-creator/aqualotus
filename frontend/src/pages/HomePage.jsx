import { Row, Col, Container, Button, Badge } from 'react-bootstrap'
import { useParams, Link } from 'react-router-dom'
import { useGetProductsQuery } from '../slices/productsApiSlice'
import ProductCard from '../components/ui/ProductCard'
import HeroSlider from '../components/ui/HeroSlider'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'
import Paginate from '../components/ui/Paginate'

const HomePage = () => {
  const { keyword, pageNumber } = useParams()

  const { data, isLoading, error } = useGetProductsQuery({
    keyword: keyword || '',
    pageNumber: pageNumber || 1,
  })

  // فیلتر سختی نگهداری
  const careLevels = ['آسان', 'متوسط', 'سخت']
  const careLevelColors = {
    'آسان': 'success',
    'متوسط': 'warning',
    'سخت': 'danger',
  }

  return (
    <>
      {/* Hero Slider - فقط صفحه اصلی */}
      {!keyword && <HeroSlider />}

      <Container className='py-4'>
        {/* فیلتر سختی نگهداری */}
        {!keyword && (
          <div className='care-filter mb-4'>
            <h5 className='filter-title'>🌿 فیلتر بر اساس سختی نگهداری</h5>
            <div className='d-flex gap-2 flex-wrap'>
              <Link to='/'>
                <Button variant='outline-secondary' size='sm'>
                  همه گیاهان
                </Button>
              </Link>
              {careLevels.map((level) => (
                <Link key={level} to={`/search/${level}`}>
                  <Button
                    variant={`outline-${careLevelColors[level]}`}
                    size='sm'
                  >
                    {level === 'آسان' && '🟢'}
                    {level === 'متوسط' && '🟡'}
                    {level === 'سخت' && '🔴'}
                    {' '}{level}
                  </Button>
                </Link>
              ))}
            </div>
          </div>
        )}

        {keyword && (
          <div className='mb-3 d-flex align-items-center gap-2'>
            <h5 className='mb-0'>نتایج جستجو: {keyword}</h5>
            <Link to='/'>
              <Button variant='outline-secondary' size='sm'>
                بازگشت
              </Button>
            </Link>
          </div>
        )}

        {isLoading ? (
          <Loader />
        ) : error ? (
          <Message variant='danger'>
            {error?.data?.message || error.error}
          </Message>
        ) : (
          <>
            <Row>
              {data.products.map((product) => (
                <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                  <ProductCard product={product} />
                </Col>
              ))}
            </Row>
            <Paginate
              pages={data.pages}
              page={data.page}
              keyword={keyword ? keyword : ''}
            />
          </>
        )}
      </Container>
    </>
  )
}

export default HomePage