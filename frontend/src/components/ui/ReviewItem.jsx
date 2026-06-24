import { useState } from 'react'
import { Button, Form } from 'react-bootstrap'
import { toast } from 'react-toastify'
import Rating from './Rating'
import { useAddReviewReplyMutation } from '../../slices/productsApiSlice'

const timeAgo = (dateString) => {
  const now = new Date()
  const date = new Date(dateString)
  const diffMs = now - date
  const diffMinutes = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffMinutes < 1) return 'همین الان'
  if (diffMinutes < 60) return `${diffMinutes} دقیقه پیش`
  if (diffHours < 24) return `${diffHours} ساعت پیش`
  if (diffDays < 30) return `${diffDays} روز پیش`
  return date.toLocaleDateString('fa-IR')
}

const Avatar = ({ name, isAdmin }) => {
  const letter = name?.charAt(0) || '?'
  return (
    <div
      style={{
        width: '38px',
        height: '38px',
        borderRadius: '50%',
        backgroundColor: isAdmin ? '#2d6a4f' : '#e9ecef',
        color: isAdmin ? '#fff' : '#495057',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 'bold',
        flexShrink: 0,
        fontSize: '1rem',
      }}
    >
      {letter}
    </div>
  )
}

const ReviewItem = ({ review, productId, userInfo }) => {
  const [showReplyForm, setShowReplyForm] = useState(false)
  const [replyText, setReplyText] = useState('')
  const [addReviewReply, { isLoading: loadingReply }] = useAddReviewReplyMutation()

  const approvedReplies = (review.replies || []).filter((r) => r.isApproved)

  const submitReply = async (e) => {
    e.preventDefault()
    if (!replyText.trim()) {
      toast.error('لطفاً متن پاسخ را وارد کنید')
      return
    }
    try {
      const res = await addReviewReply({
        productId,
        reviewId: review._id,
        comment: replyText,
      }).unwrap()
      toast.success(res.message)
      setReplyText('')
      setShowReplyForm(false)
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ثبت پاسخ')
    }
  }

  return (
    <div
      style={{
        border: '1px solid #e0e0e0',
        borderRadius: '12px',
        padding: '16px',
        marginBottom: '14px',
        backgroundColor: '#fff',
      }}
    >
      <div className='d-flex align-items-start gap-2'>
        <Avatar name={review.name} />
        <div className='flex-grow-1'>
          <div className='d-flex justify-content-between align-items-center flex-wrap'>
            <strong>{review.name}</strong>
            <small className='text-muted'>{timeAgo(review.createdAt)}</small>
          </div>
          <Rating value={review.rating} />
          <p className='mt-2 mb-1' style={{ color: '#212529' }}>{review.comment}</p>

          {userInfo && (
            <Button
              variant='link'
              size='sm'
              className='p-0'
              onClick={() => setShowReplyForm((s) => !s)}
            >
              {showReplyForm ? 'انصراف' : 'پاسخ دادن'}
            </Button>
          )}

          {showReplyForm && (
            <Form onSubmit={submitReply} className='mt-2'>
              <Form.Control
                as='textarea'
                rows={2}
                value={replyText}
                onChange={(e) => setReplyText(e.target.value)}
                placeholder='پاسخ خود را بنویسید...'
              />
              <Button
                type='submit'
                size='sm'
                className='btn-aqualotus mt-2'
                disabled={loadingReply}
              >
                ارسال پاسخ
              </Button>
            </Form>
          )}

          {approvedReplies.length > 0 && (
            <div className='mt-3' style={{ borderRight: '3px solid #e9ecef', paddingRight: '14px' }}>
              {approvedReplies.map((reply) => (
                <div key={reply._id} className='d-flex align-items-start gap-2 mb-2'>
                  <Avatar name={reply.name} isAdmin={reply.isAdmin} />
                  <div>
                    <div className='d-flex align-items-center gap-2'>
                      <strong style={{ fontSize: '0.9rem' }}>{reply.name}</strong>
                      {reply.isAdmin && (
                        <span
                          className='badge'
                          style={{ backgroundColor: '#2d6a4f', fontSize: '0.7rem' }}
                        >
                          پاسخ فروشگاه
                        </span>
                      )}
                      <small className='text-muted'>{timeAgo(reply.createdAt)}</small>
                    </div>
                    <p className='mb-0' style={{ fontSize: '0.9rem', color: '#212529' }}>{reply.comment}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ReviewItem
