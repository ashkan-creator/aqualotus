import { useState, useEffect } from 'react'
import { Container, Card, Form, Button, Row, Col } from 'react-bootstrap'
import { toast } from 'react-toastify'
import { useGetSettingsQuery, useUpdateSettingMutation } from '../../slices/settingsApiSlice'
import Loader from '../../components/ui/Loader'

const SettingsPage = () => {
  const { data: settings, isLoading } = useGetSettingsQuery()
  const [updateSetting] = useUpdateSettingMutation()

  const [announcement, setAnnouncement] = useState('')
  const [contactPhone, setContactPhone] = useState('')
  const [contactEmail, setContactEmail] = useState('')
  const [aboutText, setAboutText] = useState('')

  useEffect(() => {
    if (settings) {
      setAnnouncement(settings.announcement || '')
      setContactPhone(settings.contact_phone || '')
      setContactEmail(settings.contact_email || '')
      setAboutText(settings.about_text || '')
    }
  }, [settings])

  const saveHandler = async (key, value) => {
    try {
      await updateSetting({ key, value }).unwrap()
      toast.success('ذخیره شد')
    } catch {
      toast.error('خطا در ذخیره')
    }
  }

  if (isLoading) return <Loader />

  return (
    <Container className='py-4'>
      <h2 className='mb-4'>تنظیمات سایت</h2>
      <Row className='g-4'>
        <Col md={12}>
          <Card className='p-4'>
            <h5 className='mb-3'>📢 نوار اطلاع‌رسانی</h5>
            <div className='d-flex gap-2'>
              <Form.Control
                value={announcement}
                onChange={(e) => setAnnouncement(e.target.value)}
                placeholder='مثلاً: ارسال رایگان بالای ۵۰۰ هزار تومان 🎉'
              />
              <Button className='btn-aqualotus' onClick={() => saveHandler('announcement', announcement)}>
                ذخیره
              </Button>
            </div>
          </Card>
        </Col>
        <Col md={6}>
          <Card className='p-4'>
            <h5 className='mb-3'>📞 تماس با ما</h5>
            <Form.Group className='mb-2'>
              <Form.Label>تلفن</Form.Label>
              <div className='d-flex gap-2'>
                <Form.Control value={contactPhone} onChange={(e) => setContactPhone(e.target.value)} />
                <Button className='btn-aqualotus' onClick={() => saveHandler('contact_phone', contactPhone)}>ذخیره</Button>
              </div>
            </Form.Group>
            <Form.Group>
              <Form.Label>ایمیل</Form.Label>
              <div className='d-flex gap-2'>
                <Form.Control value={contactEmail} onChange={(e) => setContactEmail(e.target.value)} />
                <Button className='btn-aqualotus' onClick={() => saveHandler('contact_email', contactEmail)}>ذخیره</Button>
              </div>
            </Form.Group>
          </Card>
        </Col>
        <Col md={6}>
          <Card className='p-4'>
            <h5 className='mb-3'>ℹ️ درباره ما</h5>
            <Form.Group>
              <div className='d-flex gap-2 align-items-start'>
                <Form.Control
                  as='textarea'
                  rows={4}
                  value={aboutText}
                  onChange={(e) => setAboutText(e.target.value)}
                />
                <Button className='btn-aqualotus' onClick={() => saveHandler('about_text', aboutText)}>ذخیره</Button>
              </div>
            </Form.Group>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default SettingsPage
