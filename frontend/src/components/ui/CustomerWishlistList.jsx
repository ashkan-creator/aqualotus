import { Row, Col } from 'react-bootstrap'
import { useGetMyWishlistQuery } from '../../slices/wishlistApiSlice'
import ProductCard from './ProductCard'
import Loader from './Loader'
import Message from './Message'

const CustomerWishlistList = () => {
  const { data: products, isLoading, error } = useGetMyWishlistQuery()

  if (isLoading) return <Loader />
  if (error) return <Message variant='danger'>{error?.data?.message}</Message>
  if (!products || products.length === 0) {
    return <Message>لیست علاقه‌مندی‌های شما خالی است</Message>
  }

  return (
    <Row>
      {products.map((product) => (
        <Col key={product._id} xs={6} md={4} lg={3} className='mb-4'>
          <ProductCard product={product} />
        </Col>
      ))}
    </Row>
  )
}

export default CustomerWishlistList
