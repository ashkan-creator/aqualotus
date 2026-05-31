import { Navbar, Nav, Container, NavDropdown, Badge } from 'react-bootstrap'
import { FaShoppingCart, FaUser, FaLeaf, FaBars } from 'react-icons/fa'
import { LinkContainer } from 'react-router-bootstrap'
import { useSelector, useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { useLogoutMutation } from '../../slices/usersApiSlice'
import { logout } from '../../slices/authSlice'
import SearchBox from '../ui/SearchBox'

const Header = () => {
  const { cartItems } = useSelector((state) => state.cart)
  const { userInfo } = useSelector((state) => state.auth)
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const [logoutApiCall] = useLogoutMutation()

  const logoutHandler = async () => {
    try {
      await logoutApiCall().unwrap()
      dispatch(logout())
      navigate('/login')
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <header>
      <Navbar expand='md' collapseOnSelect className='aqualotus-navbar'>
        <Container>
          {/* راست: لوگو */}
          <LinkContainer to='/'>
            <Navbar.Brand className='brand-logo'>
              <FaLeaf className='brand-icon' />
              <span>AquaLotus</span>
            </Navbar.Brand>
          </LinkContainer>

          {/* ورود - کنار لوگو سمت راست */}
          {userInfo ? (
            <NavDropdown
              title={userInfo.name}
              id='username'
              className='nav-user d-md-none'
            >
              <LinkContainer to='/profile'>
                <NavDropdown.Item>پروفایل</NavDropdown.Item>
              </LinkContainer>
              <NavDropdown.Item onClick={logoutHandler}>خروج</NavDropdown.Item>
            </NavDropdown>
          ) : (
            <LinkContainer to='/login' className='d-md-none'>
              <Nav.Link className='nav-login-mobile'>
                <FaUser />
              </Nav.Link>
            </LinkContainer>
          )}

          <Navbar.Toggle aria-controls='basic-navbar-nav' />

          <Navbar.Collapse id='basic-navbar-nav'>
            <Nav className='w-100 align-items-center'>

              {/* منوی دسته‌بندی - سمت راست بعد از لوگو */}
              <NavDropdown
                title={<span><FaBars className='ms-1' /> دسته‌بندی</span>}
                id='categories-menu'
                className='nav-categories'
              >
                {/* گیاهان زنده با زیرمنو */}
                <NavDropdown.Header>🌿 گیاهان زنده</NavDropdown.Header>
                <LinkContainer to='/search/گیاه زنده'>
                  <NavDropdown.Item>همه گیاهان</NavDropdown.Item>
                </LinkContainer>

                <NavDropdown.Divider />
                <NavDropdown.Header>📍 بر اساس محل کاشت</NavDropdown.Header>
                <LinkContainer to='/search/جلو'>
                  <NavDropdown.Item>گیاهان جلو آکواریوم</NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to='/search/میانه'>
                  <NavDropdown.Item>گیاهان میانه آکواریوم</NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to='/search/پشت'>
                  <NavDropdown.Item>گیاهان پشت آکواریوم</NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to='/search/شناور'>
                  <NavDropdown.Item>گیاهان شناور</NavDropdown.Item>
                </LinkContainer>

                <NavDropdown.Divider />
                <NavDropdown.Header>🌱 بر اساس خانواده</NavDropdown.Header>
                <LinkContainer to='/search/آنوبیاس'>
                  <NavDropdown.Item>خانواده آنوبیاس</NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to='/search/بوسفالاندرا'>
                  <NavDropdown.Item>خانواده بوسفالاندرا</NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to='/search/کریپتوکورین'>
                  <NavDropdown.Item>خانواده کریپتوکورین</NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to='/search/هیگروفیلا'>
                  <NavDropdown.Item>خانواده هیگروفیلا</NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to='/search/موس'>
                  <NavDropdown.Item>خانواده موس‌ها</NavDropdown.Item>
                </LinkContainer>

                <NavDropdown.Divider />
                <NavDropdown.Header>🛒 لوازم و مکمل</NavDropdown.Header>
                <LinkContainer to='/search/کود و مکمل'>
                  <NavDropdown.Item>کود و مکمل</NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to='/search/بستر'>
                  <NavDropdown.Item>بستر آکواریوم</NavDropdown.Item>
                </LinkContainer>
                <LinkContainer to='/search/لوازم جانبی'>
                  <NavDropdown.Item>لوازم جانبی</NavDropdown.Item>
                </LinkContainer>
              </NavDropdown>

              {/* سرچ - وسط */}
              <div className='mx-auto'>
                <SearchBox />
              </div>

              {/* چپ: سبد خرید */}
              <LinkContainer to='/cart'>
                <Nav.Link className='nav-cart ms-2'>
                  <FaShoppingCart />
                  <span className='me-1'>سبد خرید</span>
                  {cartItems.length > 0 && (
                    <Badge pill bg='success' className='cart-badge'>
                      {cartItems.reduce((a, c) => a + c.qty, 0)}
                    </Badge>
                  )}
                </Nav.Link>
              </LinkContainer>

              {/* ورود/پروفایل - دسکتاپ */}
              {userInfo ? (
                <NavDropdown
                  title={userInfo.name}
                  id='username-desktop'
                  className='nav-user d-none d-md-block'
                >
                  <LinkContainer to='/profile'>
                    <NavDropdown.Item>پروفایل</NavDropdown.Item>
                  </LinkContainer>
                  <NavDropdown.Item onClick={logoutHandler}>خروج</NavDropdown.Item>
                </NavDropdown>
              ) : (
                <LinkContainer to='/login' className='d-none d-md-flex'>
                  <Nav.Link className='nav-login'>
                    <FaUser />
                    <span className='me-1'>ورود</span>
                  </Nav.Link>
                </LinkContainer>
              )}

              {/* ادمین */}
              {userInfo && userInfo.isAdmin && (
                <NavDropdown title='مدیریت' id='adminmenu' className='nav-admin'>
  <LinkContainer to='/admin/productlist'>
    <NavDropdown.Item>محصولات</NavDropdown.Item>
  </LinkContainer>
  <LinkContainer to='/admin/orderlist'>
    <NavDropdown.Item>سفارش‌ها</NavDropdown.Item>
  </LinkContainer>
  <LinkContainer to='/admin/userlist'>
    <NavDropdown.Item>کاربران</NavDropdown.Item>
  </LinkContainer>
  <LinkContainer to='/admin/familylist'>
    <NavDropdown.Item>خانواده‌های گیاهی</NavDropdown.Item>
  </LinkContainer>
</NavDropdown>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* نوار سختی نگهداری */}
      <div className='care-level-bar'>
        <Container className='d-flex gap-3 justify-content-center py-2'>
          <LinkContainer to='/search/آسان'>
            <span className='care-badge easy'>🟢 نگهداری آسان</span>
          </LinkContainer>
          <LinkContainer to='/search/متوسط'>
            <span className='care-badge medium'>🟡 نگهداری متوسط</span>
          </LinkContainer>
          <LinkContainer to='/search/سخت'>
            <span className='care-badge hard'>🔴 نگهداری سخت</span>
          </LinkContainer>
        </Container>
      </div>
    </header>
  )
}

export default Header