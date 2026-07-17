import { Card, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import {
  useGetMyNotificationsQuery,
  useMarkMyNotificationReadMutation,
  useMarkAllMyNotificationsReadMutation,
} from '../../slices/notificationsApiSlice'
import Loader from './Loader'
import Message from './Message'

const typeIcons = {
  new_review: '⭐',
  new_reply: '💬',
  new_order: '🛒',
  low_stock: '📦',
  new_message: '✉️',
  order_confirmed: '✅',
  order_delivered: '🚚',
}

const timeAgo = (dateString) => {
  const now = new Date()
  const date = new Date(dateString)
  const diffMinutes = Math.floor((now - date) / 60000)
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)
  if (diffMinutes < 1) return 'همین الان'
  if (diffMinutes < 60) return `${diffMinutes} دقیقه پیش`
  if (diffHours < 24) return `${diffHours} ساعت پیش`
  if (diffDays < 30) return `${diffDays} روز پیش`
  return date.toLocaleDateString('fa-IR')
}

const CustomerNotificationsList = () => {
  const navigate = useNavigate()
  const { data: notifications, isLoading, error } = useGetMyNotificationsQuery()
  const [markRead] = useMarkMyNotificationReadMutation()
  const [markAllRead] = useMarkAllMyNotificationsReadMutation()

  const unreadCount = notifications?.filter((n) => !n.isRead).length || 0

  const handleItemClick = async (notif) => {
    if (!notif.isRead) {
      try {
        await markRead(notif._id).unwrap()
      } catch {
        // خطای بی‌اهمیت — بی‌صدا رد می‌شود
      }
    }
    if (notif.link) navigate(notif.link)
  }

  const handleMarkAll = async () => {
    try {
      await markAllRead().unwrap()
    } catch {
      // خطای بی‌اهمیت — بی‌صدا رد می‌شود
    }
  }

  return (
    <Card className='auth-card'>
      <Card.Body className='p-4'>
        <div className='d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2'>
          <h5 className='mb-0'>نوتیفیکیشن‌ها</h5>
          {unreadCount > 0 && (
            <Button
              variant='link'
              size='sm'
              className='p-0'
              style={{ color: 'var(--primary, #2d6a4f)', textDecoration: 'none', fontSize: '13px' }}
              onClick={handleMarkAll}
            >
              علامت‌گذاری همه به‌عنوان خوانده‌شده
            </Button>
          )}
        </div>

        {isLoading ? (
          <Loader />
        ) : error ? (
          <Message variant='danger'>{error?.data?.message}</Message>
        ) : !notifications || notifications.length === 0 ? (
          <Message>نوتیفیکیشنی وجود ندارد</Message>
        ) : (
          <div>
            {notifications.map((notif) => (
              <div
                key={notif._id}
                onClick={() => handleItemClick(notif)}
                style={{
                  padding: '12px 10px',
                  borderBottom: '1px solid #f1f1f1',
                  cursor: notif.link ? 'pointer' : 'default',
                  backgroundColor: notif.isRead ? 'transparent' : '#f0f7f3',
                  display: 'flex',
                  gap: '12px',
                  alignItems: 'flex-start',
                  borderRadius: '8px',
                  transition: 'background 0.2s',
                }}
              >
                <span style={{ fontSize: '1.2rem', flexShrink: 0 }}>
                  {typeIcons[notif.type] || '🔔'}
                </span>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: notif.isRead ? 'normal' : 'bold', fontSize: '0.9rem' }}>
                    {notif.title}
                  </div>
                  <div style={{ fontSize: '0.82rem', color: '#555', marginTop: '2px' }}>
                    {notif.message}
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#999', marginTop: '4px' }}>
                    {timeAgo(notif.createdAt)}
                  </div>
                </div>
                {!notif.isRead && (
                  <span
                    style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      backgroundColor: 'var(--primary, #2d6a4f)',
                      marginTop: '4px',
                      flexShrink: 0,
                    }}
                  />
                )}
              </div>
            ))}
          </div>
        )}
      </Card.Body>
    </Card>
  )
}

export default CustomerNotificationsList
