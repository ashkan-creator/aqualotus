import { useState } from 'react'
import { Navbar, Nav, Container, NavDropdown, Badge } from 'react-bootstrap'
import { FaShoppingCart, FaUser } from 'react-icons/fa'
import { LinkContainer } from 'react-router-bootstrap'
import { useSelector, useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { useLogoutMutation } from '../../slices/usersApiSlice'
import { useGetSettingsQuery } from '../../slices/settingsApiSlice'
import { useGetFamiliesQuery } from '../../slices/familiesApiSlice'
import { logout } from '../../slices/authSlice'
import SearchBox from '../ui/SearchBox'

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

  // navigate با query params برای فیلترها
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
    <header>
      <Navbar expand='md' collapseOnSelect className='aqualotus-navbar' style={{ padding: '8px 0' }}>
        <Container>
          <LinkContainer to='/'>
            <Navbar.Brand className='brand-logo d-flex align-items-center' style={{ gap: '10px' }}>
              <img
                src='/logo.png'
                alt='AquaLotus'
                style={{ width: '52px', height: '52px', borderRadius: '50%', objectFit: 'cover' }}
              />
              <span style={{ fontWeight: '600', fontSize: '1.1rem' }}>AquaLotus</span>
            </Navbar.Brand>
          </LinkContainer>

          <div className='d-none d-md-flex mx-auto'>
            <SearchBox />
          </div>

          <div className='d-flex align-items-center gap-3'>
            {(!userInfo || !userInfo.isAdmin) && (
              <div style={{ position: 'relative', cursor: 'pointer' }} onClick={() => navigate('/cart')}>
                <FaShoppingCart style={{ color: 'rgba(255,255,255,0.9)', fontSize: '1.3rem' }} />
                {totalCartItems > 0 && (
                  <Badge pill bg='danger' style={{
                    position: 'absolute', top: '-8px', left: '-8px',
                    fontSize: '0.65rem', minWidth: '18px', height: '18px',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                  }}>
                    {totalCartItems}
                  </Badge>
                )}
              </div>
            )}

            {userInfo ? (
              <NavDropdown
                title={<span style={{ color: 'rgba(255,255,255,0.9)', fontSize: '0.9rem' }}>{userInfo.name}</span>}
                id='user-menu' align='end'
              >
                {!userInfo.isAdmin && (
                  <LinkContainer to='/profile'>
                    <NavDropdown.Item>پروفایل و سفارش‌هایم</NavDropdown.Item>
                  </LinkContainer>
                )}
                {userInfo.isAdmin && (
                  <>
                    <LinkContainer to='/profile'><NavDropdown.Item>پروفایل</NavDropdown.Item></LinkContainer>
                    <NavDropdown.Divider />
                    <LinkContainer to='/admin/dashboard'><NavDropdown.Item>📊 داشبورد</NavDropdown.Item></LinkContainer>
                    <LinkContainer to='/admin/productlist'><NavDropdown.Item>محصولات</NavDropdown.Item></LinkContainer>
                    <LinkContainer to='/admin/orderlist'><NavDropdown.Item>سفارش‌ها</NavDropdown.Item></LinkContainer>
                    <LinkContainer to='/admin/userlist'><NavDropdown.Item>کاربران</NavDropdown.Item></LinkContainer>
                    <LinkContainer to='/admin/familylist'><NavDropdown.Item>خانواده‌های گیاهی</NavDropdown.Item></LinkContainer>
                    <NavDropdown.Divider />
                    <LinkContainer to='/admin/sliders'><NavDropdown.Item>🖼️ اسلایدر</NavDropdown.Item></LinkContainer>
                    <LinkContainer to='/admin/blog'><NavDropdown.Item>📝 وبلاگ</NavDropdown.Item></LinkContainer>
                    <LinkContainer to='/admin/settings'><NavDropdown.Item>⚙️ تنظیمات</NavDropdown.Item></LinkContainer>
                  </>
                )}
                <NavDropdown.Divider />
                <NavDropdown.Item onClick={logoutHandler}>خروج</NavDropdown.Item>
              </NavDropdown>
            ) : (
              <div style={{ cursor: 'pointer' }} onClick={() => navigate('/login')}>
                <FaUser style={{ color: 'rgba(255,255,255,0.9)', fontSize: '1.2rem' }} />
              </div>
            )}

            <button
              onClick={() => setDrawerOpen(true)}
              style={{
                background: 'rgba(255,255,255,0.15)', border: 'none',
                borderRadius: '8px', padding: '7px 12px', color: 'white',
                fontSize: '0.85rem', cursor: 'pointer',
                display: 'flex', alignItems: 'center', gap: '6px',
              }}
            >
              <span style={{ fontSize: '1.1rem' }}>☰</span>
              دسته‌بندی
            </button>
          </div>
        </Container>

        <Container className='d-md-none mt-2'>
          <SearchBox />
        </Container>
      </Navbar>

      {settings?.announcement && (
        <div className='announcement-bar'>
          <Container className='d-flex justify-content-center py-2'>
            <span>{settings.announcement}</span>
          </Container>
        </div>
      )}

      {/* Sidebar Drawer */}
      {drawerOpen && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 9999, display: 'flex', flexDirection: 'row-reverse' }}>
          <div style={{
            width: '290px', background: '#fff', height: '100%',
            overflowY: 'auto', borderLeft: '1px solid #e0e0e0',
            display: 'flex', flexDirection: 'column', direction: 'rtl',
          }}>
            <div style={{ background: '#1b4332', padding: '14px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexShrink: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <img src='/logo.png' alt='logo' style={{ width: '38px', height: '38px', borderRadius: '50%' }} />
                <span style={{ color: 'white', fontSize: '15px', fontWeight: '500' }}>دسته‌بندی محصولات</span>
              </div>
              <button onClick={() => setDrawerOpen(false)} style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.3rem', cursor: 'pointer' }}>✕</button>
            </div>

            <div style={{ padding: '8px 0' }}>
              <SectionLabel>🌿 گیاهان زنده</SectionLabel>
              <DrawerItem icon='🌱' label='همه گیاهان' onClick={() => goToFilter({ category: 'گیاه زنده' })} />

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
                <SubItem label='✅ هر دو نوع کشت' onClick={() => goToFilter({ cultivationType: 'هر دو' })} />
              </DrawerSection>

              <DrawerSection icon='🪨' label='نیاز به بستر' color='#4e342e' isOpen={openSection === 'soil'} onToggle={() => toggleSection('soil')}>
                <SubItem label='🪨 نیاز به بستر دارد' onClick={() => goToFilter({ needsSoil: 'true' })} />
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
          <div onClick={() => setDrawerOpen(false)} style={{ flex: 1, background: 'rgba(0,0,0,0.5)' }} />
        </div>
      )}
    </header>
  )
}

const SectionLabel = ({ children }) => (
  <div style={{ padding: '5px 18px 3px' }}>
    <span style={{ fontSize: '11px', color: '#888' }}>{children}</span>
  </div>
)

const Divider = () => <div style={{ height: '1px', background: '#e0e0e0', margin: '10px 18px' }} />

const DrawerItem = ({ icon, label, onClick }) => (
  <div onClick={onClick} style={{ padding: '10px 18px', display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}
    onMouseOver={(e) => e.currentTarget.style.background = '#f5f5f5'}
    onMouseOut={(e) => e.currentTarget.style.background = ''}>
    <span style={{ fontSize: '16px' }}>{icon}</span>
    <span style={{ fontSize: '14px', color: '#333' }}>{label}</span>
    <span style={{ marginRight: 'auto', color: '#aaa', fontSize: '12px' }}>‹</span>
  </div>
)

const DrawerSection = ({ icon, label, color, isOpen, onToggle, children }) => (
  <>
    <div onClick={onToggle} style={{ padding: '10px 18px', display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}
      onMouseOver={(e) => e.currentTarget.style.background = '#f5f5f5'}
      onMouseOut={(e) => e.currentTarget.style.background = ''}>
      <span style={{ fontSize: '16px' }}>{icon}</span>
      <span style={{ fontSize: '14px', color: '#333' }}>{label}</span>
      <span style={{ marginRight: 'auto', color: '#aaa', fontSize: '12px' }}>{isOpen ? '▲' : '▼'}</span>
    </div>
    {isOpen && (
      <div style={{ padding: '2px 18px 6px 18px' }}>
        <div style={{ borderRight: `2px solid ${color}`, paddingRight: '12px' }}>
          {children}
        </div>
      </div>
    )}
  </>
)

const SubItem = ({ label, onClick }) => (
  <div onClick={onClick} style={{ padding: '7px 0', fontSize: '13px', color: '#666', cursor: 'pointer' }}
    onMouseOver={(e) => e.currentTarget.style.color = '#333'}
    onMouseOut={(e) => e.currentTarget.style.color = '#666'}>
    {label}
  </div>
)

export default Header
