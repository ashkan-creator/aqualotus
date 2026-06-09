import { Container, Row, Col, Card } from 'react-bootstrap'
import { FaPhone, FaEnvelope, FaInstagram } from 'react-icons/fa'
import { useGetSettingsQuery } from '../slices/settingsApiSlice'

const ContactPage = () => {
  const { data: settings } = useGetSettingsQuery()
  return (
    <Container className='py-5'>
      <h2 className='mb-4 text-center'>تماس با ما</h2>
      <Row className='justify-content-center'>
        <Col md={8}>
          <Card className='p-4'>
            <div className='d-flex flex-column gap-3'>
              <div className='d-flex align-items-center gap-3'>
                <FaPhone size={24} color='#2d6a4f' />
                <div><strong>تلفن:</strong><p className='mb-0'>{settings?.contact_phone || '۰۹۱۲-۰۰۰-۰۰۰۰'}</p></div>
              </div>
              <div className='d-flex align-items-center gap-3'>
                <FaEnvelope size={24} color='#2d6a4f' />
                <div><strong>ایمیل:</strong><p className='mb-0'>{settings?.contact_email || 'info@aqualotus.ir'}</p></div>
              </div>
              <div className='d-flex align-items-center gap-3'>
                <FaInstagram size={24} color='#2d6a4f' />
                <div><strong>اینستاگرام:</strong><p className='mb-0'>@aqualotus.ir</p></div>
              </div>
            </div>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}
export default ContactPage
