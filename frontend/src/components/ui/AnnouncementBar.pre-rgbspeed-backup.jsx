import { useEffect, useState } from 'react'
import { Container } from 'react-bootstrap'

/**
 * AnnouncementBar
 * ----------------
 * نوار اطلاع‌رسانی با پشتیبانی از:
 * - چند پیام که با تایمر بین‌شون می‌چرخه
 * - افکت RGB متغیر یا رنگ دلخواه ادمین
 * - نوع انیمیشن متن: fade | slide | bounce | glow | typewriter
 *
 * تنظیمات از Settings (key-value):
 * - announcement_messages, announcement_interval
 * - announcement_rgb, announcement_color
 * - announcement_animation: 'fade' | 'slide' | 'bounce' | 'glow' | 'typewriter'
 */
const ANIM_CLASS = {
  fade: 'aq-anim-fade',
  slide: 'aq-anim-slide',
  bounce: 'aq-anim-bounce',
  glow: 'aq-anim-glow',
}

const TYPEWRITER_SPEED_MS = 45

const AnnouncementBar = ({ settings }) => {
  const [index, setIndex] = useState(0)
  const [renderKey, setRenderKey] = useState(0)
  const [typedText, setTypedText] = useState('')

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
  const animation = settings?.announcement_animation || 'fade'
  const currentMessage = messages[index % messages.length] || ''

  // چرخش بین پیام‌ها
  useEffect(() => {
    if (messages.length <= 1) return
    const timer = setInterval(() => {
      setIndex((i) => (i + 1) % messages.length)
      setRenderKey((k) => k + 1)
    }, intervalSec * 1000)
    return () => clearInterval(timer)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messages.length, intervalSec])

  // افکت تایپ‌رایتر (جدا از بقیه‌ی انیمیشن‌ها چون نیاز به منطق JS داره)
  useEffect(() => {
    if (animation !== 'typewriter') return
    setTypedText('')
    let i = 0
    const typing = setInterval(() => {
      i += 1
      setTypedText(currentMessage.slice(0, i))
      if (i >= currentMessage.length) clearInterval(typing)
    }, TYPEWRITER_SPEED_MS)
    return () => clearInterval(typing)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [renderKey, animation, currentMessage])

  if (messages.length === 0) return null

  return (
    <div
      className={rgbActive ? 'announcement-bar aq-announcement-rgb' : 'announcement-bar'}
      style={!rgbActive ? { background: customColor } : undefined}
    >
      <Container className='d-flex justify-content-center py-2'>
        {animation === 'typewriter' ? (
          <span className='aq-announcement-text aq-anim-typewriter' key={renderKey}>
            {typedText}
            <span className='aq-typewriter-cursor'>|</span>
          </span>
        ) : (
          <span
            className={`aq-announcement-text ${ANIM_CLASS[animation] || ANIM_CLASS.fade}`}
            key={renderKey}
          >
            {currentMessage}
          </span>
        )}
      </Container>
    </div>
  )
}

export default AnnouncementBar
