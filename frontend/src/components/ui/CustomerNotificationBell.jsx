import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaBell } from 'react-icons/fa'
import {
  useGetMyNotificationsQuery,
  useGetMyUnreadCountQuery,
  useMarkMyNotificationReadMutation,
  useMarkAllMyNotificationsReadMutation,
} from '../../slices/notificationsApiSlice'

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

const CustomerNotificationBell = () => {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)
  const navigate = useNavigate()

  const { data: unreadData } = useGetMyUnreadCountQuery(undefined, {
    pollingInterval: 30000,
  })
  const { data: notifications, isLoading } = useGetMyNotificationsQuery(undefined, {
    skip: !open,
  })
  const [markRead] = useMarkMyNotificationReadMutation()
  const [markAllRead] = useMarkAllMyNotificationsReadMutation()

  const unreadCount = unreadData?.count || 0

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleItemClick = async (notif) => {
    if (!notif.isRead) {
      try { await markRead(notif._id).unwrap() } catch {}
    }
    setOpen(false)
    if (notif.link) navigate(notif.link)
  }

  const handleMarkAll = async (e) => {
    e.stopPropagation()
    try { await markAllRead().unwrap() } catch {}
  }

  return (
    <div ref={ref} style={{ position: 'relative', display: 'inline-block' }}>
      <button
        onClick={() => setOpen((o) => !o)}
        aria-label='نوتیفیکیشن‌ها'
        style={{
          background: 'none', border: 'none', position: 'relative',
          cursor: 'pointer', padding: '6px 8px', display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}
      >
        <FaBell style={{ color: 'rgba(255,255,255,0.9)', fontSize: '1.2rem' }} />
        {unreadCount > 0 && (
          <span style={{
            position: 'absolute', top: '2px', left: '2px',
            backgroundColor: '#e63946', color: '#fff',
            borderRadius: '50%', fontSize: '0.6rem',
            minWidth: '17px', height: '17px',
            display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '0 3px',
          }}>
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div 
          style={{
            position: 'absolute',
            top: '45px',
            left: window.innerWidth < 480 ? '-60px' : '0',
            width: window.innerWidth < 480 ? 'calc(100vw - 32px)' : '310px',
            maxWidth: '340px',
            maxHeight: '380px',
            overflowY: 'auto',
            backgroundColor: '#fff',
            color: '#212529',
            borderRadius: '8px',
            boxShadow: '0 4px 18px rgba(0,0,0,0.15)',
            zIndex: 2000,
            direction: 'rtl',
          }}
        >
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '10px 12px', borderBottom: '1px solid #eee',
            position: 'sticky', top: 0, background: '#fff', zIndex: 10
          }}>
            <strong style={{ fontSize: '0.9rem' }}>نوتیفیکیشن‌ها</strong>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              {unreadCount > 0 && (
                <button onClick={handleMarkAll} style={{
                  background: 'none', border: 'none',
                  color: '#2d6a4f', fontSize: '0.75rem', cursor: 'pointer',
                }}>
                  علامت‌گذاری همه
                </button>
              )}
              <button onClick={() => setOpen(false)} style={{
                background: 'none', border: 'none',
                color: '#999', fontSize: '0.9rem', cursor: 'pointer',
              }}>✕</button>
            </div>
          </div>

          {isLoading ? (
            <div style={{ textAlign: 'center', padding: '1rem', color: '#999', fontSize: '0.85rem' }}>در حال بارگذاری...</div>
          ) : !notifications || notifications.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '1rem', color: '#999', fontSize: '0.85rem' }}>نوتیفیکیشنی وجود ندارد</div>
          ) : (
            notifications.map((notif) => (
              <div
                key={notif._id}
                onClick={() => handleItemClick(notif)}
                style={{
                  padding: '10px 12px', borderBottom: '1px solid #f1f1f1',
                  cursor: 'pointer',
                  backgroundColor: notif.isRead ? '#fff' : '#f0f7f3',
                  display: 'flex', gap: '8px', alignItems: 'flex-start',
                }}
              >
                <span style={{ fontSize: '1rem' }}>{typeIcons[notif.type] || '🔔'}</span>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: notif.isRead ? 'normal' : 'bold', fontSize: '0.82rem', lineHeight: '1.4' }}>
                    {notif.title}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: '#555', marginTop: '2px' }}>{notif.message}</div>
                  <div style={{ fontSize: '0.7rem', color: '#999', marginTop: '4px' }}>
                    {timeAgo(notif.createdAt)}
                  </div>
                </div>
                {!notif.isRead && (
                  <span style={{
                    width: '6px', height: '6px', borderRadius: '50%',
                    backgroundColor: '#2d6a4f', marginTop: '5px', flexShrink: 0,
                  }} />
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}

export default CustomerNotificationBell
