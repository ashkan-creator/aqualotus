import { Container, Row, Col } from 'react-bootstrap'
import { FaLeaf, FaInstagram, FaTelegram, FaWhatsapp } from 'react-icons/fa'
import { LinkContainer } from 'react-router-bootstrap'

const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className='aqualotus-footer'>
      <Container>
        <Row className='py-4'>
          <Col md={4} className='mb-3'>
            <div className='footer-brand'>
              <FaLeaf className='footer-icon' />
              <span>AquaLotus</span>
            </div>
            <p className='footer-desc'>
              فروشگاه تخصصی گیاهان زنده آکواریوم و لوازم جانبی
            </p>
            <div className='social-links'>
              <a href='#' className='social-link'>
                <FaInstagram />
              </a>
              <a href='#' className='social-link'>
                <FaTelegram />
              </a>
              <a href='#' className='social-link'>
                <FaWhatsapp />
              </a>
            </div>
          </Col>

          <Col md={4} className='mb-3'>
            <h6 className='footer-title'>دسته‌بندی‌ها</h6>
            <ul className='footer-links'>
              <li><LinkContainer to='/search/گیاه زنده'><a>گیاهان زنده</a></LinkContainer></li>
              <li><LinkContainer to='/search/کود و مکمل'><a>کود و مکمل</a></LinkContainer></li>
              <li><LinkContainer to='/search/بستر'><a>بستر آکواریوم</a></LinkContainer></li>
              <li><LinkContainer to='/search/لوازم جانبی'><a>لوازم جانبی</a></LinkContainer></li>
            </ul>
          </Col>

          <Col md={4} className='mb-3'>
            <h6 className='footer-title'>راهنما</h6>
            <ul className='footer-links'>
              <li><LinkContainer to='/blog'><a>وبلاگ و آموزش</a></LinkContainer></li>
              <li><LinkContainer to='/about'><a>درباره ما</a></LinkContainer></li>
              <li><LinkContainer to='/contact'><a>تماس با ما</a></LinkContainer></li>
            </ul>
          </Col>
        </Row>

        <Row>
          <Col className='text-center footer-bottom py-2'>
            <p>© {currentYear} AquaLotus - تمامی حقوق محفوظ است</p>
          </Col>
        </Row>
      </Container>
    </footer>
  )
}

export default Footer