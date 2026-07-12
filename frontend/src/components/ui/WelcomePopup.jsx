import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { useGetSettingsQuery } from '../../slices/settingsApiSlice'

const WelcomePopup = () => {
  const [visible, setVisible] = useState(false)
  const navigate = useNavigate()
  const { userInfo } = useSelector((state) => state.auth)
  const { data: settings, isSuccess } = useGetSettingsQuery()

  useEffect(() => {
    if (!isSuccess || !settings) return
    if (settings.popup_active !== 'true') return
    if (userInfo?.isAdmin) return

    const now = new Date()
    if (settings.popup_start && settings.popup_start !== '' && now < new Date(settings.popup_start)) return
    if (settings.popup_end && settings.popup_end !== '' && now > new Date(settings.popup_end)) return

    const today = new Date().toISOString().slice(0, 10)
    const lastShown = localStorage.getItem('aq_welcome_popup_last_shown')
    if (lastShown === today) return

    const t = setTimeout(() => {
      setVisible(true)
      localStorage.setItem('aq_welcome_popup_last_shown', today)
    }, 800)
    return () => clearTimeout(t)
  }, [isSuccess, settings, userInfo])

  const handleClose = () => setVisible(false)

  const handleBtn = () => {
    handleClose()
    if (settings?.popup_link) navigate(settings.popup_link)
  }

  const textAlign = settings?.popup_align || 'right'

  if (!visible) return null

  return (
    <>
      <style>{`
        .aq-welcome-popup {
          width: min(92vw, 820px);
          max-height: 90vh;
        }
        .aq-welcome-popup-img {
          height: 340px;
        }
        .aq-welcome-popup-content {
          padding: 32px;
        }
        .aq-welcome-popup-title {
          font-size: 1.5rem;
          margin-bottom: 14px;
        }
        .aq-welcome-popup-text {
          font-size: 1.05rem;
          margin-bottom: 28px;
        }
        .aq-welcome-popup-actions {
          display: flex;
          gap: 12px;
        }
        .aq-welcome-popup-btn {
          flex: 0 0 auto;
        }
        @media (max-width: 576px) {
          .aq-welcome-popup {
            width: 94vw;
            max-height: 85vh;
            border-radius: 16px;
          }
          .aq-welcome-popup-img {
            height: 150px;
          }
          .aq-welcome-popup-content {
            padding: 18px 16px;
          }
          .aq-welcome-popup-title {
            font-size: 1.1rem;
            margin-bottom: 8px;
          }
          .aq-welcome-popup-text {
            font-size: 0.88rem;
            line-height: 1.7;
            margin-bottom: 16px;
          }
          .aq-welcome-popup-actions {
            flex-direction: column;
          }
          .aq-welcome-popup-btn {
            width: 100%;
            text-align: center;
          }
        }
      `}</style>

      <div onClick={handleClose} style={{
        position: 'fixed', inset: 0, zIndex: 99990,
        background: 'rgba(0,0,0,0.65)',
        backdropFilter: 'blur(3px)',
      }} />

      <div className='aq-welcome-popup' style={{
        position: 'fixed',
        top: '50%', left: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 99991,
        overflowY: 'auto',
        background: '#fff',
        borderRadius: '20px',
        overflow: 'hidden',
        boxShadow: '0 25px 60px rgba(0,0,0,0.35)',
        animation: 'aq-popup-in 0.4s cubic-bezier(0.34,1.56,0.64,1)',
        direction: 'rtl',
      }}>
        <button onClick={handleClose} style={{
          position: 'absolute', top: '14px', left: '14px',
          width: '36px', height: '36px',
          background: 'rgba(0,0,0,0.5)', color: 'white',
          border: 'none', borderRadius: '50%',
          cursor: 'pointer', fontSize: '1.1rem',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          zIndex: 3,
        }}>✕</button>

        {settings?.popup_image && (
          <img src={settings.popup_image} alt='' className='aq-welcome-popup-img'
            style={{ width: '100%', objectFit: 'cover', display: 'block' }} />
        )}

        <div className='aq-welcome-popup-content' style={{ textAlign }}>
          {settings?.popup_title && (
            <h3 className='aq-welcome-popup-title' style={{ color: '#2d6a4f' }}>
              {settings.popup_title}
            </h3>
          )}
          {settings?.popup_text && (
            <p className='aq-welcome-popup-text' style={{ color: '#555', lineHeight: '2' }}>
              {settings.popup_text}
            </p>
          )}
          <div className='aq-welcome-popup-actions' style={{ justifyContent: textAlign === 'center' ? 'center' : textAlign === 'left' ? 'flex-end' : 'flex-start' }}>
            {settings?.popup_btn && (
              <button onClick={handleBtn} className='aq-welcome-popup-btn' style={{
                padding: '13px 28px',
                background: '#2d6a4f', color: 'white',
                border: 'none', borderRadius: '12px',
                cursor: 'pointer', fontFamily: 'inherit',
                fontSize: '1rem', fontWeight: '600',
              }}>
                {settings.popup_btn}
              </button>
            )}
            <button onClick={handleClose} className='aq-welcome-popup-btn' style={{
              padding: '13px 22px',
              background: '#f0f0f0', color: '#666',
              border: 'none', borderRadius: '12px',
              cursor: 'pointer', fontFamily: 'inherit',
              fontSize: '0.95rem',
            }}>
              بعداً
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

export default WelcomePopup
