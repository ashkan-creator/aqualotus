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

    const t = setTimeout(() => setVisible(true), 800)
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
      <div onClick={handleClose} style={{
        position: 'fixed', inset: 0, zIndex: 99990,
        background: 'rgba(0,0,0,0.65)',
        backdropFilter: 'blur(3px)',
      }} />

      <div style={{
        position: 'fixed',
        top: '50%', left: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 99991,
        width: 'min(92vw, 820px)',
        maxHeight: '90vh',
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
          <img src={settings.popup_image} alt=''
            style={{ width: '100%', height: '340px', objectFit: 'cover', display: 'block' }} />
        )}

        <div style={{ padding: '32px', textAlign }}>
          {settings?.popup_title && (
            <h3 style={{ color: '#2d6a4f', marginBottom: '14px', fontSize: '1.5rem' }}>
              {settings.popup_title}
            </h3>
          )}
          {settings?.popup_text && (
            <p style={{ color: '#555', lineHeight: '2', marginBottom: '28px', fontSize: '1.05rem' }}>
              {settings.popup_text}
            </p>
          )}
          <div style={{ display: 'flex', gap: '12px', justifyContent: textAlign === 'center' ? 'center' : textAlign === 'left' ? 'flex-end' : 'flex-start' }}>
            {settings?.popup_btn && (
              <button onClick={handleBtn} style={{
                padding: '13px 28px',
                background: '#2d6a4f', color: 'white',
                border: 'none', borderRadius: '12px',
                cursor: 'pointer', fontFamily: 'inherit',
                fontSize: '1rem', fontWeight: '600',
              }}>
                {settings.popup_btn}
              </button>
            )}
            <button onClick={handleClose} style={{
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
