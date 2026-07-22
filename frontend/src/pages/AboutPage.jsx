import { Container, Row, Col } from 'react-bootstrap'
import { useGetSettingsQuery } from '../slices/settingsApiSlice'

const AboutPage = () => {
  const { data: settings } = useGetSettingsQuery()
  return (
    <Container className='py-5'>
      <h2 className='mb-4 text-center aq-page-title'>درباره ما</h2>
      <Row className='justify-content-center'>
        <Col md={8}>
          <div className='aq-about-card'>
            <p className='mb-0'>{settings?.about_text || 'آکوالوتوس یک فروشگاه تخصصی گیاهان آکواریوم است.'}</p>
          </div>
        </Col>
      </Row>
    </Container>
  )
}
export default AboutPage
