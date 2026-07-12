import { useState, useEffect } from 'react'
import { Container, Card, Form, Button, Row, Col, InputGroup } from 'react-bootstrap'
import { toast } from 'react-toastify'
import { useGetSettingsQuery, useUpdateSettingMutation } from '../../slices/settingsApiSlice'
import { useUploadProductImageMutation } from '../../slices/productsApiSlice'
import Loader from '../../components/ui/Loader'

const SettingsPage = () => {
  const { data: settings, isLoading } = useGetSettingsQuery()
  const [updateSetting] = useUpdateSettingMutation()
  const [uploadImage, { isLoading: uploading }] = useUploadProductImageMutation()

  const [form, setForm] = useState({
    announcement: '',
    contact_phone: '',
    contact_email: '',
    about_text: '',
  })

  const [announcementCfg, setAnnouncementCfg] = useState({
    messages: [''],
    interval: 4,
    rgb: false,
    color: '#1b4332',
    animation: 'fade',
    rgbSpeed: 6,
  })

  const [popup, setPopup] = useState({
    popup_active: false,
    popup_title: '',
    popup_text: '',
    popup_image: '',
    popup_link: '',
    popup_btn: '',
    popup_start: '',
    popup_end: '',
  })

  useEffect(() => {
    if (!settings) return
    setForm({
      announcement: settings.announcement || '',
      contact_phone: settings.contact_phone || '',
      contact_email: settings.contact_email || '',
      about_text: settings.about_text || '',
    })

    let parsedMessages = []
    try {
      parsedMessages = JSON.parse(settings.announcement_messages || '[]')
    } catch {
      parsedMessages = []
    }
    if (parsedMessages.length === 0 && settings.announcement) {
      parsedMessages = [settings.announcement]
    }
    if (parsedMessages.length === 0) parsedMessages = ['']

    setAnnouncementCfg({
      messages: parsedMessages,
      interval: Number(settings.announcement_interval) || 4,
      rgb: settings.announcement_rgb === 'true',
      color: settings.announcement_color || '#1b4332',
      animation: settings.announcement_animation || 'fade',
      rgbSpeed: Number(settings.announcement_rgb_speed) || 6,
    })
    setPopup({
      popup_active: settings.popup_active === 'true',
      popup_title: settings.popup_title || '',
      popup_text: settings.popup_text || '',
      popup_image: settings.popup_image || '',
      popup_link: settings.popup_link || '',
      popup_btn: settings.popup_btn || '',
      popup_start: settings.popup_start || '',
      popup_end: settings.popup_end || '',
      popup_align: settings.popup_align || 'right',
    })
  }, [settings])

  const saveSection = async (data) => {
    try {
      await Promise.all(
        Object.entries(data).map(([key, value]) =>
          updateSetting({ key, value: String(value) }).unwrap()
        )
      )
      toast.success('ذخیره شد')
    } catch { toast.error('خطا در ذخیره') }
  }

  const uploadPopupImage = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const fd = new FormData()
    fd.append('image', file)
    try {
      const res = await uploadImage(fd).unwrap()
      setPopup((p) => ({ ...p, popup_image: res.image }))
      await updateSetting({ key: 'popup_image', value: res.image }).unwrap()
      toast.success('تصویر آپلود شد')
    } catch { toast.error('خطا در آپلود') }
  }

  if (isLoading) return <Loader />

  return (
    <Container className='py-4'>
      <h2 className='mb-4' style={{ fontSize: 'clamp(1rem, 4vw, 1.5rem)' }}>تنظیمات سایت</h2>
      <Row className='g-4'>

        {/* نوار اطلاع‌رسانی */}
        <Col xs={12}>
          <Card className='p-3 p-md-4'>
            <h5 className='mb-3'>📢 نوار اطلاع‌رسانی</h5>

            <Form.Group className='mb-3'>
              <Form.Label>پیام‌ها (به نوبت نمایش داده می‌شن)</Form.Label>
              {announcementCfg.messages.map((msg, i) => (
                <InputGroup className='mb-2' key={i}>
                  <Form.Control
                    value={msg}
                    onChange={(e) => {
                      const updated = [...announcementCfg.messages]
                      updated[i] = e.target.value
                      setAnnouncementCfg({ ...announcementCfg, messages: updated })
                    }}
                    placeholder='مثلاً: ارسال رایگان بالای ۵۰۰ هزار تومان 🎉'
                  />
                  {announcementCfg.messages.length > 1 && (
                    <Button
                      variant='outline-danger'
                      onClick={() => {
                        const updated = announcementCfg.messages.filter((_, idx) => idx !== i)
                        setAnnouncementCfg({ ...announcementCfg, messages: updated })
                      }}
                    >
                      ✕
                    </Button>
                  )}
                </InputGroup>
              ))}
              <Button
                variant='outline-secondary'
                size='sm'
                onClick={() => setAnnouncementCfg({ ...announcementCfg, messages: [...announcementCfg.messages, ''] })}
              >
                + افزودن پیام
              </Button>
            </Form.Group>

            <Form.Group className='mb-3' style={{ maxWidth: '220px' }}>
              <Form.Label>فاصله‌ی تعویض پیام‌ها (ثانیه)</Form.Label>
              <Form.Control
                type='number'
                min='2'
                value={announcementCfg.interval}
                onChange={(e) => setAnnouncementCfg({ ...announcementCfg, interval: e.target.value })}
              />
            </Form.Group>

            <Form.Check
              type='switch'
              id='announcement-rgb'
              className='mb-3'
              label='🌈 افکت رنگارنگ RGB (مثل نور کارت گرافیک)'
              checked={announcementCfg.rgb}
              onChange={(e) => setAnnouncementCfg({ ...announcementCfg, rgb: e.target.checked })}
            />

            {announcementCfg.rgb && (
              <Form.Group className='mb-3' style={{ maxWidth: '260px' }}>
                <Form.Label>سرعت افکت RGB (ثانیه)</Form.Label>
                <Form.Control
                  type='number'
                  min='1'
                  step='0.5'
                  value={announcementCfg.rgbSpeed}
                  onChange={(e) => setAnnouncementCfg({ ...announcementCfg, rgbSpeed: e.target.value })}
                />
              </Form.Group>
            )}

            <Form.Group className='mb-3' style={{ maxWidth: '260px' }}>
              <Form.Label>نوع انیمیشن متن</Form.Label>
              <Form.Select
                value={announcementCfg.animation}
                onChange={(e) => setAnnouncementCfg({ ...announcementCfg, animation: e.target.value })}
              >
                <option value='fade'>محو شدن (Fade)</option>
                <option value='slide'>لغزشی (Slide)</option>
                <option value='bounce'>پرشی (Bounce)</option>
                <option value='glow'>درخشش (Glow)</option>
                <option value='typewriter'>تایپ‌رایتر (Typewriter)</option>
              </Form.Select>
            </Form.Group>

            {!announcementCfg.rgb && (
              <Form.Group className='mb-3'>
                <Form.Label>رنگ دلخواه نوار</Form.Label>
                <Form.Control
                  type='color'
                  value={announcementCfg.color}
                  onChange={(e) => setAnnouncementCfg({ ...announcementCfg, color: e.target.value })}
                  style={{ width: '80px', height: '40px', padding: '4px' }}
                />
              </Form.Group>
            )}

            <Button
              className='btn-aqualotus'
              size='sm'
              onClick={() =>
                saveSection({
                  announcement_messages: JSON.stringify(announcementCfg.messages.filter((m) => m.trim())),
                  announcement_interval: String(announcementCfg.interval),
                  announcement_rgb: String(announcementCfg.rgb),
                  announcement_color: announcementCfg.color,
                  announcement_animation: announcementCfg.animation,
                  announcement_rgb_speed: String(announcementCfg.rgbSpeed),
                })
              }
            >
              ذخیره
            </Button>
          </Card>
        </Col>

        {/* تماس */}
        <Col xs={12} md={6}>
          <Card className='p-3 p-md-4'>
            <h5 className='mb-3'>📞 تماس با ما</h5>
            <Form.Group className='mb-3'>
              <Form.Label>تلفن</Form.Label>
              <Form.Control value={form.contact_phone} onChange={(e) => setForm({ ...form, contact_phone: e.target.value })} />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>ایمیل</Form.Label>
              <Form.Control value={form.contact_email} onChange={(e) => setForm({ ...form, contact_email: e.target.value })} />
            </Form.Group>
            <Button className='btn-aqualotus' size='sm'
              onClick={() => saveSection({ contact_phone: form.contact_phone, contact_email: form.contact_email })}>
              ذخیره
            </Button>
          </Card>
        </Col>

        {/* درباره ما */}
        <Col xs={12} md={6}>
          <Card className='p-3 p-md-4'>
            <h5 className='mb-3'>ℹ️ درباره ما</h5>
            <Form.Group className='mb-3'>
              <Form.Label>متن</Form.Label>
              <Form.Control as='textarea' rows={5} value={form.about_text}
                onChange={(e) => setForm({ ...form, about_text: e.target.value })} />
            </Form.Group>
            <Button className='btn-aqualotus' size='sm' onClick={() => saveSection({ about_text: form.about_text })}>
              ذخیره
            </Button>
          </Card>
        </Col>

        {/* پوپاپ */}
        <Col xs={12}>
          <Card className='p-3 p-md-4'>
            <h5 className='mb-3'>🎉 پوپاپ خوش‌آمدگویی</h5>
            <p className='text-muted mb-3' style={{ fontSize: '0.85rem' }}>
              پوپاپ برای کاربران غیرادمین یک بار در روز نمایش داده می‌شود.
            </p>

            <Row className='g-3'>
              <Col xs={12}>
                <Form.Check type='switch' id='popup-active' label='فعال باشد'
                  checked={popup.popup_active}
                  onChange={(e) => setPopup({ ...popup, popup_active: e.target.checked })} />
              </Col>
              <Col xs={12} md={6}>
                <Form.Group>
                  <Form.Label>عنوان</Form.Label>
                  <Form.Control value={popup.popup_title}
                    onChange={(e) => setPopup({ ...popup, popup_title: e.target.value })}
                    placeholder='مثلاً: تخفیف ویژه 🎉' />
                </Form.Group>
              </Col>
              <Col xs={12} md={6}>
                <Form.Group>
                  <Form.Label>متن دکمه (اختیاری)</Form.Label>
                  <Form.Control value={popup.popup_btn}
                    onChange={(e) => setPopup({ ...popup, popup_btn: e.target.value })}
                    placeholder='مشاهده تخفیف‌ها' />
                </Form.Group>
              </Col>
              <Col xs={12}>
                <Form.Group>
                  <Form.Label>متن پوپاپ</Form.Label>
                  <Form.Control as='textarea' rows={3} value={popup.popup_text}
                    onChange={(e) => setPopup({ ...popup, popup_text: e.target.value })}
                    placeholder='متن تبلیغاتی...' />
                </Form.Group>
              </Col>
              <Col xs={12} md={6}>
                <Form.Group>
                  <Form.Label>لینک دکمه (اختیاری)</Form.Label>
                  <Form.Control value={popup.popup_link}
                    onChange={(e) => setPopup({ ...popup, popup_link: e.target.value })}
                    placeholder='/search/گیاه زنده' />
                </Form.Group>
              </Col>
              <Col xs={12} md={6}>
                <Form.Group>
                  <Form.Label>ترازبندی متن</Form.Label>
                  <Form.Select value={popup.popup_align}
                    onChange={(e) => setPopup({ ...popup, popup_align: e.target.value })}>
                    <option value='right'>راست‌چین</option>
                    <option value='center'>وسط‌چین</option>
                    <option value='left'>چپ‌چین</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col xs={12} md={3}>
                <Form.Group>
                  <Form.Label>تاریخ شروع</Form.Label>
                  <Form.Control type='date' value={popup.popup_start}
                    onChange={(e) => setPopup({ ...popup, popup_start: e.target.value })} />
                </Form.Group>
              </Col>
              <Col xs={12} md={3}>
                <Form.Group>
                  <Form.Label>تاریخ پایان</Form.Label>
                  <Form.Control type='date' value={popup.popup_end}
                    onChange={(e) => setPopup({ ...popup, popup_end: e.target.value })} />
                </Form.Group>
              </Col>
              <Col xs={12}>
                <Form.Group>
                  <Form.Label>تصویر (اختیاری)</Form.Label>
                  <Form.Control type='file' accept='image/*'
                    onChange={uploadPopupImage} disabled={uploading} />
                  {uploading && <small className='text-muted'>در حال آپلود...</small>}
                  {popup.popup_image && (
                    <div className='mt-2' style={{ position: 'relative', display: 'inline-block', width: '100%' }}>
                      <img src={popup.popup_image} alt=''
                        style={{ width: '100%', maxHeight: '160px', objectFit: 'cover', borderRadius: '8px' }} />
                      <button
                        onClick={() => setPopup({ ...popup, popup_image: '' })}
                        style={{
                          position: 'absolute', top: '8px', left: '8px',
                          background: 'rgba(0,0,0,0.6)', color: 'white',
                          border: 'none', borderRadius: '50%',
                          width: '28px', height: '28px', cursor: 'pointer',
                        }}
                      >✕</button>
                    </div>
                  )}
                </Form.Group>
              </Col>
              <Col xs={12}>
                <Button className='btn-aqualotus' onClick={() => saveSection({
                  popup_active: String(popup.popup_active),
                  popup_title: popup.popup_title,
                  popup_text: popup.popup_text,
                  popup_image: popup.popup_image,
                  popup_link: popup.popup_link,
                  popup_btn: popup.popup_btn,
                  popup_start: popup.popup_start,
                  popup_end: popup.popup_end,
                  popup_align: popup.popup_align,
                })}>
                  ذخیره تنظیمات پوپاپ
                </Button>
              </Col>
            </Row>
          </Card>
        </Col>

      </Row>
    </Container>
  )
}

export default SettingsPage
