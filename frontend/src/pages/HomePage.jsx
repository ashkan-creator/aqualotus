import { useState, useEffect } from 'react'
import { Row, Col, Container, Button } from 'react-bootstrap'
import { useParams, Link, useSearchParams } from 'react-router-dom'
import { useGetProductsQuery } from '../slices/productsApiSlice'
import ProductCard from '../components/ui/ProductCard'
import HeroSlider from '../components/ui/HeroSlider'
import FilterSidebar from '../components/ui/FilterSidebar'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'
import Paginate from '../components/ui/Paginate'

const HomePage = () => {
  const { keyword, pageNumber } = useParams()
  const [searchParams] = useSearchParams()
  const [showFilter, setShowFilter] = useState(false)

  const [filters, setFilters] = useState({
    careLevel: '',
    position: '',
    cultivationType: '',
    needsSoil: '',
    minPrice: '',
    maxPrice: '',
    category: '',
  })

  // هر بار که searchParams عوض شد فیلترها آپدیت بشن
  useEffect(() => {
    setFilters({
      careLevel: searchParams.get('careLevel') || '',
      position: searchParams.get('position') || '',
      cultivationType: searchParams.get('cultivationType') || '',
      needsSoil: searchParams.get('needsSoil') || '',
      minPrice: searchParams.get('minPrice') || '',
      maxPrice: searchParams.get('maxPrice') || '',
      category: searchParams.get('category') || '',
    })
  }, [searchParams.toString()])

  const queryParams = {
    keyword: keyword || searchParams.get('keyword') || '',
    pageNumber: pageNumber || 1,
    position: filters.position,
    cultivationType: filters.cultivationType,
    needsSoil: filters.needsSoil,
    careLevel: filters.careLevel,
    category: filters.category,
    minPrice: filters.minPrice,
    maxPrice: filters.maxPrice,
  }

  const { data, isLoading, error } = useGetProductsQuery(queryParams)

  const activeFilterCount = Object.values(filters).filter(Boolean).length

  const resetFilters = () => {
    setFilters({
      careLevel: '', position: '', cultivationType: '',
      needsSoil: '', minPrice: '', maxPrice: '', category: '',
    })
  }

  return (
    <>
      {!keyword && !activeFilterCount && <HeroSlider />}
      <Container className='py-4'>

        {keyword && (
          <div className='mb-3 d-flex align-items-center gap-2'>
            <h5 className='mb-0'>نتایج جستجو: {keyword}</h5>
            <Link to='/'><Button variant='outline-secondary' size='sm'>بازگشت</Button></Link>
          </div>
        )}

        {activeFilterCount > 0 && !keyword && (
          <div className='mb-3 d-flex align-items-center gap-2'>
            <h5 className='mb-0'>نتایج فیلتر</h5>
            <Button variant='outline-danger' size='sm' onClick={resetFilters}>
              پاک کردن فیلتر
            </Button>
          </div>
        )}

        {isLoading ? <Loader /> : error ? (
          <Message variant='danger'>{error?.data?.message || error.error}</Message>
        ) : (
          <Row>
            <Col xs={12} className='d-lg-none mb-3'>
              <Button variant='outline-success' size='sm' onClick={() => setShowFilter(!showFilter)}>
                🔍 فیلتر {activeFilterCount > 0 && `(${activeFilterCount})`}
              </Button>
            </Col>

            <Col lg={2} className={`${showFilter ? 'd-block' : 'd-none'} d-lg-block mb-4`}>
              <FilterSidebar filters={filters} setFilters={setFilters} />
            </Col>

            <Col lg={10}>
              {data?.products?.length === 0 ? (
                <Message>محصولی با این مشخصات پیدا نشد</Message>
              ) : (
                <>
                  <Row className='g-3'>
                    {data?.products?.map((product) => (
                      <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                        <ProductCard product={product} />
                      </Col>
                    ))}
                  </Row>
                  <Paginate pages={data?.pages} page={data?.page} keyword={keyword || ''} />
                </>
              )}
            </Col>
          </Row>
        )}
      </Container>
    </>
  )
}

export default HomePage
