import { Container, Card, Button, Badge, Row, Col } from 'react-bootstrap'
import { FaCheck, FaTimes } from 'react-icons/fa'
import { toast } from 'react-toastify'
import { Link } from 'react-router-dom'
import {
  useGetPendingReviewsQuery,
  useApproveReviewMutation,
  useRejectReviewMutation,
  useApproveReplyMutation,
  useRejectReplyMutation,
} from '../../slices/productsApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'
import Rating from '../../components/ui/Rating'

const AdminReviewsPage = () => {
  const { data, isLoading, error, refetch } = useGetPendingReviewsQuery()
  const [approveReview, { isLoading: loadingApprove }] = useApproveReviewMutation()
  const [rejectReview, { isLoading: loadingReject }] = useRejectReviewMutation()
  const [approveReply, { isLoading: loadingApproveReply }] = useApproveReplyMutation()
  const [rejectReply, { isLoading: loadingRejectReply }] = useRejectReplyMutation()

  const busy = loadingApprove || loadingReject || loadingApproveReply || loadingRejectReply

  const handleApproveReview = async (productId, reviewId) => {
    try {
      await approveReview({ productId, reviewId }).unwrap()
      toast.success('نظر تایید شد')
      refetch()
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در تایید نظر')
    }
  }

  const handleRejectReview = async (productId, reviewId) => {
    if (!window.confirm('آیا از رد و حذف این نظر مطمئن هستید؟')) return
    try {
      await rejectReview({ productId, reviewId }).unwrap()
      toast.success('نظر رد و حذف شد')
      refetch()
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در رد نظر')
    }
  }

  const handleApproveReply = async (productId, reviewId, replyId) => {
    try {
      await approveReply({ productId, reviewId, replyId }).unwrap()
      toast.success('پاسخ تایید شد')
      refetch()
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در تایید پاسخ')
    }
  }

  const handleRejectReply = async (productId, reviewId, replyId) => {
    if (!window.confirm('آیا از رد و حذف این پاسخ مطمئن هستید؟')) return
    try {
      await rejectReply({ productId, reviewId, replyId }).unwrap()
      toast.success('پاسخ رد و حذف شد')
      refetch()
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در رد پاسخ')
    }
  }

  return (
    <Container className='py-4'>
      <h2 className='mb-4'>
        مدیریت نظرات و پاسخ‌ها
        {data && (
          <Badge bg='secondary' className='ms-2' style={{ fontSize: '0.9rem' }}>
            {(data.pendingReviews?.length || 0) + (data.pendingReplies?.length || 0)} در انتظار
          </Badge>
        )}
      </h2>

      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <>
          <h4 className='mt-4 mb-3'>نظرات در انتظار تایید ({data.pendingReviews.length})</h4>
          {data.pendingReviews.length === 0 ? (
            <Message>نظر در انتظار تایید وجود ندارد</Message>
          ) : (
            data.pendingReviews.map((item) => (
              <Card key={item.reviewId} className='mb-3'>
                <Card.Body>
                  <Row className='align-items-center'>
                    <Col md={1}>
                      <img
                        src={item.productImage}
                        alt={item.productName}
                        style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '8px' }}
                      />
                    </Col>
                    <Col md={8}>
                      <div className='d-flex align-items-center gap-2 mb-1'>
                        <Link to={`/product/${item.productId}`} target='_blank' style={{ fontWeight: 'bold' }}>
                          {item.productName}
                        </Link>
                        <small className='text-muted'>توسط {item.name}</small>
                      </div>
                      <Rating value={item.rating} />
                      <p className='mb-0 mt-1'>{item.comment}</p>
                    </Col>
                    <Col md={3} className='text-end'>
                      <Button
                        size='sm'
                        variant='success'
                        className='me-2'
                        disabled={busy}
                        onClick={() => handleApproveReview(item.productId, item.reviewId)}
                      >
                        <FaCheck /> تایید
                      </Button>
                      <Button
                        size='sm'
                        variant='outline-danger'
                        disabled={busy}
                        onClick={() => handleRejectReview(item.productId, item.reviewId)}
                      >
                        <FaTimes /> رد
                      </Button>
                    </Col>
                  </Row>
                </Card.Body>
              </Card>
            ))
          )}

          <h4 className='mt-5 mb-3'>پاسخ‌ها در انتظار تایید ({data.pendingReplies.length})</h4>
          {data.pendingReplies.length === 0 ? (
            <Message>پاسخ در انتظار تایید وجود ندارد</Message>
          ) : (
            data.pendingReplies.map((item) => (
              <Card key={item.replyId} className='mb-3'>
                <Card.Body>
                  <Row className='align-items-center'>
                    <Col md={1}>
                      <img
                        src={item.productImage}
                        alt={item.productName}
                        style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '8px' }}
                      />
                    </Col>
                    <Col md={8}>
                      <div className='d-flex align-items-center gap-2 mb-1'>
                        <Link to={`/product/${item.productId}`} target='_blank' style={{ fontWeight: 'bold' }}>
                          {item.productName}
                        </Link>
                        <small className='text-muted'>پاسخ {item.name} به نظر:</small>
                      </div>
                      <p className='mb-1 text-muted' style={{ fontSize: '0.85rem', borderRight: '2px solid #ccc', paddingRight: '8px' }}>
                        {item.originalComment}
                      </p>
                      <p className='mb-0'>{item.comment}</p>
                    </Col>
                    <Col md={3} className='text-end'>
                      <Button
                        size='sm'
                        variant='success'
                        className='me-2'
                        disabled={busy}
                        onClick={() => handleApproveReply(item.productId, item.reviewId, item.replyId)}
                      >
                        <FaCheck /> تایید
                      </Button>
                      <Button
                        size='sm'
                        variant='outline-danger'
                        disabled={busy}
                        onClick={() => handleRejectReply(item.productId, item.reviewId, item.replyId)}
                      >
                        <FaTimes /> رد
                      </Button>
                    </Col>
                  </Row>
                </Card.Body>
              </Card>
            ))
          )}
        </>
      )}
    </Container>
  )
}

export default AdminReviewsPage
