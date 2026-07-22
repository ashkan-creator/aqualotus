import { Container, Row, Col, Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import './AdminPanelPage.css'

const SECTIONS = [
  {
    title: 'مدیریت اصلی',
    items: [
      { to: '/admin/dashboard', label: 'داشبورد', icon: 'fa-gauge-high' },
      { to: '/admin/reports', label: 'گزارش\u200cگیری', icon: 'fa-chart-line' },
      { to: '/admin/productlist', label: 'محصولات', icon: 'fa-boxes-stacked' },
      { to: '/admin/orderlist', label: 'سفارش\u200cها', icon: 'fa-cart-shopping' },
      { to: '/admin/reviews', label: 'نظرات و پاسخ\u200cها', icon: 'fa-comments' },
      { to: '/admin/userlist', label: 'کاربران', icon: 'fa-users' },
      { to: '/admin/familylist', label: 'خانواده\u200cهای گیاهی', icon: 'fa-seedling' },
    ],
  },
  {
    title: 'محتوا و تنظیمات',
    items: [
      { to: '/admin/sliders', label: 'اسلایدر', icon: 'fa-images' },
      { to: '/admin/blog', label: 'وبلاگ', icon: 'fa-newspaper' },
      { to: '/admin/settings', label: 'تنظیمات', icon: 'fa-gear' },
      { to: '/admin/activity-log', label: 'لاگ فعالیت', icon: 'fa-list-check' },
      { to: '/admin/linkpages', label: 'لینک\u200cساز', icon: 'fa-link' },
      { to: '/admin/custompages', label: 'صفحه\u200cساز', icon: 'fa-layer-group' },
    ],
  },
]

const AdminPanelPage = () => {
  return (
    <>
      <Helmet><title>پنل مدیریت | AquaLotus</title></Helmet>
      <Container className='py-4'>
        <h4 className='mb-4'>پنل مدیریت</h4>

        {SECTIONS.map((section) => (
          <div key={section.title} className='mb-4'>
            <h6 className='text-muted mb-3'>{section.title}</h6>
            <Row className='g-3'>
              {section.items.map((item) => (
                <Col key={item.to} xs={6} md={4} lg={3}>
                  <Link to={item.to} className='admin-panel-card-link'>
                    <Card className='admin-panel-card'>
                      <Card.Body className='text-center p-3'>
                        <i className={`fa-solid ${item.icon} admin-panel-card-icon`}></i>
                        <div className='admin-panel-card-label'>{item.label}</div>
                      </Card.Body>
                    </Card>
                  </Link>
                </Col>
              ))}
            </Row>
          </div>
        ))}
      </Container>
    </>
  )
}

export default AdminPanelPage
