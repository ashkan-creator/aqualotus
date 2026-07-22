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
          <div className='d-flex align-items-center justify-content-between w-100 aq-navbar-row' style={{ gap: '12px' }}>

            {/* بخش راست: لوگو (ماکزیمم سایز بدون افزایش ارتفاع هدر) و منوهای دسکتاپ */}
            <div className='d-flex align-items-center gap-3' style={{ minWidth: 0 }}>
              <LinkContainer to='/'>
                <Navbar.Brand className='brand-logo d-flex align-items-center m-0' style={{ flexShrink: 0 }}>
                  <img 
                    src='/logo.png' 
                    alt='AquaLotus' 
                    className='aq-brand-logo-img' 
                    style={{ height: '72px', width: '72px', objectFit: 'contain', marginTop: '-6px', marginBottom: '-6px' }} 
                  />
                </Navbar.Brand>
              </LinkContainer>

              <Nav className='d-none d-lg-flex aq-navbar-center-nav gap-3'>
                <LinkContainer to='/'><Nav.Link className='text-nowrap'>محصولات</Nav.Link></LinkContainer>
                <LinkContainer to='/blog'><Nav.Link className='text-nowrap'>مجله آکواریوم و گیاهان</Nav.Link></LinkContainer>
                <LinkContainer to='/about'><Nav.Link className='text-nowrap'>درباره ما</Nav.Link></LinkContainer>
                <LinkContainer to='/contact'><Nav.Link className='text-nowrap'>تماس با ما</Nav.Link></LinkContainer>
              </Nav>
            </div>

            {/* بخش چپ: دکمه‌ها، سرچ و آیکون‌ها */}
            <div className='d-flex align-items-center gap-2 gap-sm-3 ms-auto' style={{ minWidth: 0 }}>
              
              {/* آیکون کاربر ثابت بدون نمایش متن */}
              <div className='aq-user-dropdown-container text-nowrap'>
                {userInfo ? (
                  <NavDropdown
                    title={
                      <span style={{ color: 'rgba(255,255,255,0.92)' }} className='d-flex align-items-center p-1'>
                        <FaUser style={{ fontSize: '1.1rem' }} />
                      </span>
                    }
                    id='user-menu'
                    align='end'
                  >
                    {!userInfo.isAdmin && (
                      <LinkContainer to='/profile'>
                        <NavDropdown.Item>پنل کاربری</NavDropdown.Item>
                      </LinkContainer>
                    )}
                    {userInfo.isAdmin && (
                      <>
                        <LinkContainer to='/profile'><NavDropdown.Item>پنل کاربری</NavDropdown.Item></LinkContainer>
                        <NavDropdown.Divider />
                        <LinkContainer to='/admin/dashboard'><NavDropdown.Item>📊 داشبورد</NavDropdown.Item></LinkContainer>
                        <LinkContainer to='/admin/reports'><NavDropdown.Item>📈 گزارش‌گیری</NavDropdown.Item></LinkContainer>
                        <LinkContainer to='/admin/productlist'><NavDropdown.Item>محصولات</NavDropdown.Item></LinkContainer>
                        <LinkContainer to='/admin/orderlist'><NavDropdown.Item>سفارش‌ها</NavDropdown.Item></LinkContainer>
                        <LinkContainer to='/admin/reviews'><NavDropdown.Item>💬 نظرات و پاسخ‌ها</NavDropdown.Item></LinkContainer>
                        <LinkContainer to='/admin/userlist'><NavDropdown.Item>کاربران</NavDropdown.Item></LinkContainer>
                        <LinkContainer to='/admin/familylist'><NavDropdown.Item>خانواده‌های گیاهی</NavDropdown.Item></LinkContainer>
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
                  </NavDropdown>
                ) : (
                  <div className='aq-navbar-icon-btn p-1' onClick={() => navigate('/login')} style={{ cursor: 'pointer' }}>
                    <FaUser style={{ color: 'rgba(255,255,255,0.92)', fontSize: '1.05rem' }} />
                  </div>
                )}
              </div>

              {/* سرچ باکس مخصوص دسکتاپ */}
              <div className='d-none d-md-flex aq-header-search-desktop' style={{ maxWidth: '210px', flexShrink: 1, minWidth: '130px' }}>
                <SearchBox />
              </div>

              {/* کانتینر آیکون‌های اعلان و سبد خرید با استایل مهارکننده (relative) برای فیکس شدن پاپ‌آپ‌ها */}
              <div className='d-flex align-items-center gap-2' style={{ position: 'relative' }}>
                {userInfo && !userInfo.isAdmin && (
                  <div className='aq-navbar-icon-btn position-relative'><CustomerNotificationBell /></div>
                )}

                {userInfo?.isAdmin && (
                  <div className='aq-navbar-icon-btn position-relative' style={{ minWidth: '35px' }}>
                    <NotificationBell />
                  </div>
                )}

                {(!userInfo || !userInfo.isAdmin) && (
                  <div
                    id='cart-icon-target'
                    className='aq-navbar-icon-btn p-1'
                    style={{ position: 'relative', cursor: 'pointer' }}
                    onClick={() => navigate('/cart')}
                  >
                    <FaShoppingCart style={{ color: 'rgba(255,255,255,0.92)', fontSize: '1.1rem' }} />
                    {totalCartItems > 0 && (
                      <Badge pill bg='danger' style={{
                        position: 'absolute', top: '-6px', left: '-6px',
                        fontSize: '0.6rem', minWidth: '17px', height: '17px',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                      }}>
                        {totalCartItems}
                      </Badge>
                    )}
                  </div>
                )}
              </div>

              {/* دکمه همبرگری موبایل */}
              <button
                onClick={() => setDrawerOpen(true)}
                className='aq-navbar-icon-btn aq-navbar-hamburger'
                style={{ background: 'rgba(255,255,255,0.12)', border: 'none', cursor: 'pointer', borderRadius: '4px', padding: '6px' }}
              >
                <FiMenu style={{ fontSize: '1.2rem', color: 'white' }} />
              </button>

              {/* دکمه سرچ موبایل */}
              <button
                className='aq-navbar-icon-btn d-md-none'
                onClick={() => setMobileSearchOpen((o) => !o)}
                style={{ background: 'rgba(255,255,255,0.12)', border: 'none', cursor: 'pointer', borderRadius: '4px', padding: '6px' }}
              >
                <FiSearch style={{ fontSize: '1.2rem', color: 'white' }} />
              </button>

            </div>
          </div>

          {/* سرچ موبایل اصلاح شده به صورت تمام‌عرض و استاندارد زیر هدر */}
          {mobileSearchOpen && (
            <div className='d-md-none aq-mobile-search-row w-100' style={{ padding: '10px 4px', background: 'transparent' }}>
              <div style={{ width: '100%', maxWidth: '100%' }}>
                <SearchBox />
              </div>
            </div>
          )}
        </Container>
      </Navbar>

      <AnnouncementBar settings={settings} />

      {/* سایدبار کشویی */}
      <div
        style={{
          position: 'fixed', inset: 0, zIndex: 9999,
          display: 'flex', 
          pointerEvents: drawerOpen ? 'all' : 'none',
          visibility: drawerOpen ? 'visible' : 'hidden',
          transition: 'visibility 0.3s'
        }}
      >
        <div
          onClick={() => setDrawerOpen(false)}
          style={{
            flex: 1,
            background: drawerOpen ? 'rgba(0,0,0,0.5)' : 'rgba(0,0,0,0)',
            transition: 'background 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            pointerEvents: drawerOpen ? 'all' : 'none',
          }}
        />

        <div style={{
          width: '290px',
          background: '#fff',
          height: '100%',
          overflowY: 'auto',
          borderLeft: '1px solid #e0e0e0',
          display: 'flex',
          flexDirection: 'column',
          direction: 'rtl',
          boxShadow: drawerOpen ? '-5px 0 25px rgba(0,0,0,0.15)' : 'none',
          transform: drawerOpen ? 'translateX(0)' : 'translateX(-100%)',
          transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s',
        }}>
          <div style={{
            background: '#1b4332', padding: '14px 18px',
            display: 'flex', alignItems: 'center', justify-content: 'space-between', flexShrink: 0,
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <img src='/logo.png' alt='logo' style={{ width: '36px', height: '36px', borderRadius: '50%' }} />
              <span style={{ color: 'white', fontSize: '15px', fontWeight: '500' }}>دسته‌بندی محصولات</span>
            </div>
            <button
              onClick={() => setDrawerOpen(false)}
              style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.3rem', cursor: 'pointer', transition: 'transform 0.2s' }}
              onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.15)'}
              onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >✕</button>
          </div>

          <div style={{ padding: '8px 0' }}>
            <SectionLabel>🌿 گیاهان زنده</SectionLabel>
            <DrawerItem icon='🌱' label='همه گیاهان' onClick={() => goToFilter({ category: 'گیاهزنده' })} />

            <DrawerSection icon='📍' label='محل کاشت' color='#0d4f8b' isOpen={openSection === 'pos'} onToggle={() => toggleSection('pos')}>
              <SubItem label='جلو آکواریوم' onClick={() => goToFilter({ position: 'جلو' })} />
              <SubItem label='میانه آکواریوم' onClick={() => goToFilter({ position: 'میانه' })} />
              <SubItem label='پشت آکواریوم' onClick={() => goToFilter({ position: 'پشت' })} />
              <SubItem label='شناور' onClick={() => goToFilter({ position: 'شناور' })} />
            </DrawerSection>

            <DrawerSection icon='🌿' label='خانواده‌های گیاهی' color='#6a1b9a' isOpen={openSection === 'fam'} onToggle={() => toggleSection('fam')}>
              {families?.map((f) => (
                <SubItem key={f._id} label={f.name} onClick={() => goToFilter({ keyword: f.name })} />
              ))}
            </DrawerSection>

            <DrawerSection icon='💧' label='نوع کشت' color='#006064' isOpen={openSection === 'cult'} onToggle={() => toggleSection('cult')}>
              <SubItem label='💧 کشت آبزی' onClick={() => goToFilter({ cultivationType: 'آبزی' })} />
              <SubItem label='🌱 کشت هیدروپونیک' onClick={() => goToFilter({ cultivationType: 'هیدروپونیک' })} />
              <SubItem label='✅ هر دو نوع کشت' onClick={() => goToFilter({ cultivationType: 'هردو' })} />
            </DrawerSection>

            <DrawerSection icon='🪨' label='نیاز به بستر' color='#4e342e' isOpen={openSection ==='soil'} onToggle={() => toggleSection('soil')}>
              <SubItem label='🪨 نیاز به بستر دارد' onClick={() => goToFilter({ needsSoil: 'true'})} />
              <SubItem label='🚫 بدون نیاز به بستر' onClick={() => goToFilter({ needsSoil: 'false' })} />
            </DrawerSection>

            <Divider />
            <SectionLabel>🛒 لوازم و مکمل</SectionLabel>
            <DrawerItem icon='🧪' label='کود و مکمل' onClick={() => goToFilter({ category: 'کود و مکمل' })} />
            <DrawerItem icon='🪸' label='بستر آکواریوم' onClick={() => goToFilter({ category: 'بستر' })} />
            <DrawerItem icon='🔧' label='لوازم جانبی' onClick={() => goToFilter({ category: 'لوازم جانبی' })} />

            <Divider />
            <DrawerItem icon='📖' label='وبلاگ' onClick={() => goTo('/blog')} />
            <DrawerItem icon='📞' label='تماس با ما' onClick={() => goTo('/contact')} />
            <DrawerItem icon='ℹ️' label='درباره ما' onClick={() => goTo('/about')} />
          </div>
        </div>
      </div>
    </header>
  )
}

const SectionLabel = ({ children }) => (
  <div style={{ padding: '5px 18px 3px' }}>
    <span style={{ fontSize: '11px', color: '#888' }}>{children}</span>
  </div>
)

const Divider = () => <div style={{ height: '1px', background: '#e0e0e0', margin: '10px 18px' }}/>

const DrawerItem = ({ icon, label, onClick }) => (
  <div
    onClick={onClick}
    className='aq-drawer-item'
    style={{ padding: '10px 18px', display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer', transition: 'background 0.15s, transform 0.15s' }}
    onMouseOver={(e) => { e.currentTarget.style.background = '#f0f7f3'; e.currentTarget.style.transform = 'translateX(-4px)' }}
    onMouseOut={(e) => { e.currentTarget.style.background = ''; e.currentTarget.style.transform = '' }}
    onTouchStart={(e) => { e.currentTarget.style.background = '#f0f7f3' }}
    onTouchEnd={(e) => { e.currentTarget.style.background = '' }}
  >
    <span style={{ fontSize: '16px' }}>{icon}</span>
    <span style={{ fontSize: '14px', color: '#333' }}>{label}</span>
    <span style={{ marginRight: 'auto', color: '#aaa', fontSize: '12px' }}>‹</span>
  </div>
)

const DrawerSection = ({ icon, label, color, isOpen, onToggle, children }) => (
  <>
    <div
      onClick={onToggle}
      style={{ padding: '10px 18px', display: 'flex', alignItems: 'center', gap: '10px', cursor:'pointer', transition: 'background 0.15s, transform 0.15s' }}
      onMouseOver={(e) => { e.currentTarget.style.background = '#f0f7f3'; e.currentTarget.style.transform = 'translateX(-4px)' }}
      onMouseOut={(e) => { e.currentTarget.style.background = ''; e.currentTarget.style.transform = '' }}
    >
      <span style={{ fontSize: '16px' }}>{icon}</span>
      <span style={{ fontSize: '14px', color: '#333' }}>{label}</span>
      <span style={{ marginRight: 'auto', color: '#aaa', fontSize: '12px', transition: 'transform 0.2s', display: 'inline-block', transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)' }}>▼</span>
    </div>
    <div style={{
      overflow: 'hidden',
      maxHeight: isOpen ? '400px' : '0',
      transition: 'max-height 0.3s ease',
    }}>
      <div style={{ padding: '2px 18px 6px 18px' }}>
        <div style={{ borderRight: `2px solid ${color}`, paddingRight: '12px' }}>
          {children}
        </div>
      </div>
    </div>
  </>
)

const SubItem = ({ label, onClick }) => (
  <div
    onClick={onClick}
    style={{ padding: '7px 0', fontSize: '13px', color: '#666', cursor: 'pointer', transition: 'color 0.15s, padding-right 0.15s' }}
    onMouseOver={(e) => { e.currentTarget.style.color = '#1b4332'; e.currentTarget.style.paddingRight = '6px' }}
    onMouseOut={(e) => { e.currentTarget.style.color = '#666'; e.currentTarget.style.paddingRight = '0' }}
  >
    {label}
  </div>
)

export default Header
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_code)

print("فایل هدر با لوگوی بزرگ (72px) و اصلاح کامل سیستم ریسپانسیو و ناتیفیکیشن موبایل بازنویسی شد!")
