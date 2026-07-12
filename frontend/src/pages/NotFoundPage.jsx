import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { Container, Button } from 'react-bootstrap'
import { NazarIcon, HorizonBanner } from '../components/ui/SurrealAssets'

const FUNNY_MESSAGES = [
  'این صفحه هم مثل کوی‌فیش همسایه رفته یه جای دیگه زندگی کنه.',
  'گیاهت رو پیدا کردیم، ولی این صفحه رو نه. عجیبه، نه؟',
  'به احتمال ۹۹٪ این لینک تو یه بعد موازی از آکواریوم گم شده.',
  'نظرِ محافظ ما هم این صفحه رو ندیده — پس واقعاً نیست!',
  'شاید این صفحه رفته زیر بستر قایم شده. بگرد ولی پیدا نمی‌شه.',
  'ماهی‌های ما هم گشتن، این صفحه رو پیدا نکردن.',
]

const NotFoundPage = () => {
  const message = useMemo(
    () => FUNNY_MESSAGES[Math.floor(Math.random() * FUNNY_MESSAGES.length)],
    []
  )

  return (
    <div style={{ position: 'relative', overflow: 'hidden', minHeight: '70vh' }}>
      <Container className='py-5 text-center d-flex flex-column align-items-center justify-content-center' style={{ minHeight: '70vh' }}>
        <div style={{ position: 'relative', width: '300px', height: '300px', marginBottom: '18px' }}>
          <NazarIcon size={300} />
        </div>

        <h1 style={{
          fontSize: 'clamp(3rem, 10vw, 6rem)',
          fontWeight: '800',
          background: 'linear-gradient(135deg, #1b4332, #52b788)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          lineHeight: 1,
          marginBottom: '8px',
        }}>
          ۴۰۴
        </h1>

        <h4 style={{ color: '#1b4332', marginBottom: '12px' }}>
          این صفحه پیدا نشد!
        </h4>

        <p className='text-muted mb-4' style={{ maxWidth: '460px', lineHeight: '1.9' }}>
          {message}
        </p>

        <Link to='/'>
          <Button className='btn-aqualotus px-4'>
            🌿 برگرد به خونه (صفحه اصلی)
          </Button>
        </Link>
      </Container>

      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, opacity: 0.25, pointerEvents: 'none' }}>
        <HorizonBanner />
      </div>
    </div>
  )
}

export default NotFoundPage
