import os

file_path = os.path.expanduser("~/aqualotus/frontend/src/components/layout/Header.jsx")

new_code = """import { useState } from 'react'
import { Navbar, Nav, Container, NavDropdown, Badge } from 'react-bootstrap'
import { FaShoppingCart, FaUser } from 'react-icons/fa'
import { FiMenu, FiSearch } from 'react-icons/fi'
import { LinkContainer } from 'react-router-bootstrap'
import { useSelector, useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { useLogoutMutation } from '../../slices/usersApiSlice'
import { useGetSettingsQuery } from '../../slices/settingsApiSlice'
import { useGetFamiliesQuery } from '../../slices/familiesApiSlice'
import { logout } from '../../slices/authSlice'
import SearchBox from '../ui/SearchBox'
import NotificationBell from '../ui/NotificationBell'
import CustomerNotificationBell from '../ui/CustomerNotificationBell'
import AnnouncementBar from '../ui/AnnouncementBar'

const Header = () => {
  const { cartItems } = useSelector((state) => state.cart)
  const { userInfo } = useSelector((state) => state.auth)
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const [logoutApiCall] = useLogoutMutation()
  const { data: settings } = useGetSettingsQuery()
  const { data: families } = useGetFamiliesQuery()
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [openSection, setOpenSection] = useState(null)
  const [mobileSearchOpen, setMobileSearchOpen] = useState(false)

  const logoutHandler = async () => {
    try {
      await logoutApiCall().unwrap()
      dispatch(logout())
      navigate('/login')
    } catch (err) {
      console.error(err)
    }
  }

  const toggleSection = (section) => {
    setOpenSection(openSection === section ? null : section)
  }

  const goToFilter = (params) => {
    setDrawerOpen(false)
    setOpenSection(null)
    const query = new URLSearchParams(params).toString()
    navigate(`/filter?${query}`)
  }

  const goTo = (path) => {
    setDrawerOpen(false)
    setOpenSection(null)
    navigate(path)
  }

  const totalCartItems = cartItems.reduce((a, c) => a + c.qty, 0)

  return (
    <header className='aq-sticky-header' style={{ zIndex: 1050, position: 'relative' }}>
      <Navbar className='aqualotus-navbar py-1' style={{ direction: 'rtl', minHeight: '65px' }}>
        <Container fluid='md'>
          <div className='d-flex align-items-center justify-content-between w-100' style={{ gap: '6px' }}>

            {/* بخش راست: لوگو */}
            <div className='d-flex align-items-center' style={{ gap: '10px', flexShrink: 0 }}>
              <LinkContainer to='/'>
                <Navbar.Brand className='brand-logo d-flex align-items-center m-0'>
                  <img 
                    src='/logo.png' 
                    alt='AquaLotus' 
                    style={{ height: '70px', width: '70px', objectFit: 'contain' }} 
                  />
                </Navbar.Brand>
              </LinkContainer>

              <Nav className='d-none d-lg-flex gap-3 aq-navbar-center-nav'>
                <LinkContainer to='/'><Nav.Link className='text-nowrap'>محصولات</Nav.Link></LinkContainer>
                <LinkContainer to='/blog'><Nav.Link className='text-nowrap'>مجله آکواریوم و گیاهان</Nav.Link></LinkContainer>
                <LinkContainer to='/about'><Nav.Link className='text-nowrap'>درباره ما</Nav.Link></LinkContainer>
                <LinkContainer to='/contact'><Nav.Link className='text-nowrap'>تماس با ما</Nav.Link></LinkContainer>
              </Nav>
            </div>

            {/* بخش چپ: کنترلها */}
            <div className='d-flex align-items-center justify-content-end' style={{ gap: '10px' }}>
              
              <div className='d-none d-md-flex' style={{ maxWidth: '200px' }}>
                <SearchBox />
              </div>

              <button
                className='d-md-none'
                onClick={() => setMobileSearchOpen(true)}
                style={{ background: 'rgba(255,255,255,0.12)', border: 'none', cursor: 'pointer', borderRadius: '6px', padding: '7px 9px', display: 'flex', alignItems: 'center' }}
              >
                <FiSearch style={{ fontSize: '1.2rem', color: 'white' }} />
              </button>

              {/* دراپ‌داون کاربر / ادمین اصلاح‌شده */}
              <div className='aq-user-dropdown-container'>
                {userInfo ? (
                  <NavDropdown
                    title={<span style={{ color: 'rgba(255,255,255,0.92)' }} className='d-flex align-items-center p-1'><FaUser style={{ fontSize: '1.1rem' }} /></span>}
                    id='user-menu'
                    align='end'
                  >
                    <div style={{ 
                      maxHeight: window.innerWidth < 768 ? '260px' : 'none', 
                      overflowY: window.innerWidth < 768 ? 'auto' : 'visible',
                      minWidth: '200px'
                    }}>
                      <LinkContainer to='/profile'><NavDropdown.Item>پنل کاربری</NavDropdown.Item></LinkContainer>
                      
                      {userInfo.isAdmin && (
                        <>
                          <NavDropdown.Divider />
                          <LinkContainer to='/admin/dashboard'><NavDropdown.Item>📊 داشبورد</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/reports'><NavDropdown.Item>📈 گزارش‌گیری</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/productlist'><NavDropdown.Item>📦 محصولات</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/orderlist'><NavDropdown.Item>🛒 سفارش‌ها</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/reviews'><NavDropdown.Item>💬 نظرات و پاسخ‌ها</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/userlist'><NavDropdown.Item>👥 کاربران</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/familylist'><NavDropdown.Item>🌱 خانواده‌ها</NavDropdown.Item></LinkContainer>
                          <NavDropdown.Divider />
                          <LinkContainer to='/admin/sliders'><NavDropdown.Item>🖼️ اسلایدر</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/blog'><NavDropdown.Item>📝 وبلاگ</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/settings'><NavDropdown.Item>⚙️ تنظیمات</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/activity-log'><NavDropdown.Item>📋 لاگ فعالیت</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/linkpages'><NavDropdown.Item>🔗 لینک‌ساز</NavDropdown.Item></LinkContainer>
                          <LinkContainer to='/admin/custompages'><NavDropdown.Item>🏗️ صفحه‌ساز</NavDropdown.Item></LinkContainer>
                        </>
                      )}
                      
                      <NavDropdown.Divider />
                      <NavDropdown.Item onClick={logoutHandler}>خروج</NavDropdown.Item>
                    </div>
                  </NavDropdown>
                ) : (
                  <div className='p-1' onClick={() => navigate('/login')} style={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
                    <FaUser style={{ color: 'rgba(255,255,255,0.92)', fontSize: '1.05rem' }} />
                  </div>
                )}
              </div>

              {/* اعلان‌ها */}
              {userInfo && !userInfo.isAdmin && <CustomerNotificationBell />}
              {userInfo?.isAdmin && <NotificationBell />}

              {/* سبد خرید */}
              {(!userInfo || !userInfo.isAdmin) && (
                <div className='p-1' style={{ position: 'relative', cursor: 'pointer', display: 'flex', alignItems: 'center' }} onClick={() => navigate('/cart')}>
                  <FaShoppingCart style={{ color: 'rgba(255,255,255,0.92)', fontSize: '1.1rem' }} />
                  {totalCartItems > 0 && (
                    <Badge pill bg='danger' style={{ position: 'absolute', top: '-6px', left: '-6px', fontSize: '0.6rem', minWidth: '17px', height: '17px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      {totalCartItems}
                    </Badge>
                  )}
                </div>
              )}

              {/* منوی همبرگر */}
              <button
                onClick={() => setDrawerOpen(true)}
                style={{ background: 'rgba(255,255,255,0.12)', border: 'none', cursor: 'pointer', borderRadius: '6px', padding: '7px 9px', display: 'flex', alignItems: 'center' }}
              >
                <FiMenu style={{ fontSize: '1.2rem', color: 'white' }} />
              </button>

            </div>
          </div>
        </Container>
      </Navbar>

      {/* سرچ‌بار تمام‌صفحه متحرک برای موبایل */}
      <div 
        style={{
          position: 'absolute', top: '0', left: '0', width: '100%', backgroundColor: '#1b4332', padding: '14px 16px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)', zIndex: 1100, display: 'flex', alignItems: 'center', gap: '10px',
          transition: 'transform 0.3s cubic-bezier(0.1, 0.76, 0.55, 0.94), opacity 0.2s',
          transform: mobileSearchOpen ? 'translateY(0)' : 'translateY(-100%)',
          opacity: mobileSearchOpen ? 1 : 0, pointerEvents: mobileSearchOpen ? 'all' : 'none', direction: 'rtl'
        }}
      >
        <div style={{ flex: 1 }}><SearchBox /></div>
        <button onClick={() => setMobileSearchOpen(false)} style={{ background: 'rgba(255,255,255,0.15)', border: 'none', color: 'white', fontSize: '1rem', padding: '8px 14px', borderRadius: '6px', cursor: 'pointer' }}>✕</button>
      </div>

      <AnnouncementBar settings={settings} />

      {/* سایدبار کشویی (دراور موبایل) */}
      <div
        style={{
          position: 'fixed', inset: 0, zIndex: 9999, display: 'flex', 
          pointerEvents: drawerOpen ? 'all' : 'none', visibility: drawerOpen ? 'visible' : 'hidden', transition: 'visibility 0.3s'
        }}
      >
        <div onClick={() => setDrawerOpen(false)} style={{ flex: 1, background: drawerOpen ? 'rgba(0,0,0,0.5)' : 'rgba(0,0,0,0)', transition: 'background 0.3s' }} />
        <div style={{
          width: '290px', background: '#fff', height: '100%', overflowY: 'auto',
          display: 'flex', flexDirection: 'column', direction: 'rtl',
          transform: drawerOpen ? 'translateX(0)' : 'translateX(-100%)',
          transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        }}>
          <div style={{ background: '#1b4332', padding: '14px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexShrink: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <img src='/logo.png' alt='logo' style={{ width: '36px', height: '36px', borderRadius: '50%' }} />
              <span style={{ color: 'white', fontSize: '14px', fontWeight: '500' }}>دسته‌بندی محصولات</span>
            </div>
            <button onClick={() => setDrawerOpen(false)} style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.3rem', cursor: 'pointer' }}>✕</button>
          </div>
          <div style={{ padding: '8px 0' }}>
            <SectionLabel>🌿 گیاهان زنده</SectionLabel>
            <DrawerItem icon='🌱' label='همه گیاهان' onClick={() => goToFilter({ category: 'گیاهزنده' })} />
            <DrawerSection icon='📍' label='محل کاشت' color='#0d4f8b' isOpen={openSection === 'pos'} onToggle={() => toggleSection('pos')}>
              <SubItem label='جلو آکواریوم' onClick={() => goToFilter({ position: 'جلو' })} />
              <SubItem label='میانه آکواریوم' onClick={() => goToFilter({ position: 'میانه' })} />
              <SubItem label='پشت آکواریوم' onClick={() => goToFilter({ position: 'پشت' })} />
            </DrawerSection>
            <Divider />
            <DrawerItem icon='📖' label='وبلاگ' onClick={() => goTo('/blog')} />
            <DrawerItem icon='📞' label='تماس با ما' onClick={() => goTo('/contact')} />
          </div>
        </div>
      </div>
    </header>
  )
}

const SectionLabel = ({ children }) => <div style={{ padding: '5px 18px 3px' }}><span style={{ fontSize: '11px', color: '#888' }}>{children}</span></div>
const Divider = () => <div style={{ height: '1px', background: '#e0e0e0', margin: '10px 18px' }}/>
const DrawerItem = ({ icon, label, onClick }) => (
  <div onClick={onClick} style={{ padding: '10px 18px', display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
    <span style={{ fontSize: '15px' }}>{icon}</span>
    <span style={{ fontSize: '13.5px', color: '#333' }}>{label}</span>
  </div>
)
const DrawerSection = ({ icon, label, color, isOpen, onToggle, children }) => (
  <>
    <div onClick={onToggle} style={{ padding: '10px 18px', display: 'flex', alignItems: 'center', gap: '10px', cursor:'pointer' }}>
      <span style={{ fontSize: '15px' }}>{icon}</span>
      <span style={{ fontSize: '13.5px', color: '#333' }}>{label}</span>
      <span style={{ marginRight: 'auto', color: '#aaa', fontSize: '11px', transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)' }}>▼</span>
    </div>
    <div style={{ overflow: 'hidden', maxHeight: isOpen ? '200px' : '0', transition: 'max-height 0.3s' }}>
      <div style={{ padding: '2px 18px 6px 18px' }}><div style={{ borderRight: `2px solid ${color}`, paddingRight: '12px' }}>{children}</div></div>
    </div>
  </>
)
const SubItem = ({ label, onClick }) => <div onClick={onClick} style={{ padding: '7px 0', fontSize: '12.5px', color: '#666', cursor: 'pointer' }}>{label}</div>

export default Header
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_code)

print("منوی ادمین با قابلیت اسکرول اختصاصی موبایل اصلاح شد!")
