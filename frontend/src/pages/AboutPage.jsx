import { Container, Row, Col } from 'react-bootstrap'
import { useGetSettingsQuery } from '../slices/settingsApiSlice'

const AboutPage = () => {
  const { data: settings } = useGetSettingsQuery()
  return (
    <Container className='py-5'>
      <h2 className='mb-4 text-center'>درباره ما</h2>
      <Row className='justify-content-center'>
        <Col md={8}>
          <p>{settings?.about_text || 'آکوالوتوس یک فروشگاه تخصصی گیاهان آکواریوم است.'}</p>
        </Col>
      </Row>
    </Container>
  )
}
export default AboutPage
