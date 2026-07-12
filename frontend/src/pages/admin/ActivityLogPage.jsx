import { Container, Table, Card, Row, Col, Badge } from 'react-bootstrap'
import { useGetActivityLogsQuery } from '../../slices/activityLogApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const actionColors = {
  'حذف محصول': 'danger',
  'ساخت محصول': 'success',
  'ویرایش محصول': 'info',
  'حذف کاربر': 'danger',
  'تأیید پرداخت': 'success',
  'ثبت ارسال': 'success',
  'ویرایش تنظیمات': 'warning',
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

const ActivityLogPage = () => {
  const { data: logs, isLoading, error } = useGetActivityLogsQuery(undefined, {
    pollingInterval: 30000,
  })

  return (
    <Container className='py-4'>
      <h2 className='mb-4' style={{ fontSize: 'clamp(1rem, 4vw, 1.5rem)' }}>
        📋 لاگ فعالیت ادمین
      </h2>

      {isLoading ? <Loader /> : error ? (
        <Message variant='danger'>{error?.data?.message || 'خطا در دریافت لاگ‌ها'}</Message>
      ) : logs?.length === 0 ? (
        <Message>هنوز فعالیتی ثبت نشده</Message>
      ) : (
        <>
          {/* دسکتاپ */}
          <div className='d-none d-md-block'>
            <Table striped hover responsive className='admin-table'>
              <thead>
                <tr>
                  <th>عملیات</th>
                  <th>ادمین</th>
                  <th>جزئیات</th>
                  <th>زمان</th>
                </tr>
              </thead>
              <tbody>
                {logs?.map((log) => (
                  <tr key={log._id}>
                    <td><Badge bg={actionColors[log.action] || 'secondary'}>{log.action}</Badge></td>
                    <td>{log.adminName}</td>
                    <td>
                      <small className='text-muted'>
                        {log.targetType && `${log.targetType}: `}{log.details}
                      </small>
                    </td>
                    <td><small>{timeAgo(log.createdAt)}</small></td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>

          {/* موبایل */}
          <div className='d-md-none'>
            <Row className='g-2'>
              {logs?.map((log) => (
                <Col xs={12} key={log._id}>
                  <Card className='p-3'>
                    <div className='d-flex justify-content-between align-items-start mb-1'>
                      <Badge bg={actionColors[log.action] || 'secondary'}>{log.action}</Badge>
                      <small className='text-muted'>{timeAgo(log.createdAt)}</small>
                    </div>
                    <div style={{ fontSize: '0.85rem', fontWeight: '600' }}>{log.adminName}</div>
                    {log.details && (
                      <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '4px' }}>
                        {log.targetType && `${log.targetType}: `}{log.details}
                      </div>
                    )}
                  </Card>
                </Col>
              ))}
            </Row>
          </div>
        </>
      )}
    </Container>
  )
}

export default ActivityLogPage
