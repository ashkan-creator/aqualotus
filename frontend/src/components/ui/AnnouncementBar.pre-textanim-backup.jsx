import { useEffect, useState } from 'react'
import { Container } from 'react-bootstrap'

/**
 * AnnouncementBar
 * ----------------
 * نوار اطلاع‌رسانی با پشتیبانی از:
 * - چند پیام که با تایمر و فید بین‌شون می‌چرخه
 * - افکت RGB متغیر (مثل نور کارت گرافیک) یا رنگ دلخواه ادمین
 *
 * تنظیمات از طریق Settings (key-value) خونده می‌شه:
 * - announcement_messages: JSON string آرایه‌ی پیام‌ها
 * - announcement_interval: فاصله‌ی تعویض به ثانیه
 * - announcement_rgb: 'true' | 'false'
 * - announcement_color: کد رنگ وقتی RGB خاموشه
 * - announcement: (قدیمی) رشته‌ی تکی، برای سازگاری با عقب
 */
const AnnouncementBar = ({ settings }) => {
  const [index, setIndex] = useState(0)
  const [visible, setVisible] = useState(true)

  let messages = []
  try {
    messages = JSON.parse(settings?.announcement_messages || '[]').filter((m) => m && m.trim())
  } catch {
    messages = []
  }
  if (messages.length === 0 && settings?.announcement) {
    messages = [settings.announcement]
  }

  const intervalSec = Math.max(Number(settings?.announcement_interval) || 4, 2)
  const rgbActive = settings?.announcement_rgb === 'true'
  const customColor = settings?.announcement_color || '#1b4332'

  useEffect(() => {
    if (messages.length <= 1) return
    const timer = setInterval(() => {
      setVisible(false)
      setTimeout(() => {
        setIndex((i) => (i + 1) % messages.length)
        setVisible(true)
      }, 300)
    }, intervalSec * 1000)
    return () => clearInterval(timer)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messages.length, intervalSec])

  if (messages.length === 0) return null

  return (
    <div
      className={rgbActive ? 'announcement-bar aq-announcement-rgb' : 'announcement-bar'}
      style={!rgbActive ? { background: customColor } : undefined}
    >
      <Container className='d-flex justify-content-center py-2'>
        <span className='aq-announcement-text' style={{ opacity: visible ? 1 : 0 }}>
          {messages[index % messages.length]}
        </span>
      </Container>
    </div>
  )
}

export default AnnouncementBar
