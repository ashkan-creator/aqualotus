import { Navbar, Nav, Container, NavDropdown, Badge } from 'react-bootstrap'
import { FaShoppingCart, FaUser } from 'react-icons/fa'
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

  const totalCartItems = cartItems.reduce((acc, item) => acc + item.qty, 0)

  return (
    <header>
      <Navbar expand='lg' className='navbar-aqualotus' variant='dark'>
        <Container>
          <LinkContainer to='/'>
            <Navbar.Brand className='brand-logo'>
              🌿 AquaLotus
            </Navbar.Brand>
          </LinkContainer>

          <Navbar.Toggle aria-controls='basic-navbar-nav' />
          <Navbar.Collapse id='basic-navbar-nav'>
            <Nav className='ms-auto align-items-center'>
              <SearchBox />

              {/* سبد خرید - فقط برای کاربران غیرادمین */}
              {(!userInfo || !userInfo.isAdmin) && (
                <LinkContainer to='/cart'>
                  <Nav.Link className='nav-cart'>
                    <FaShoppingCart />
                    {totalCartItems > 0 && (
                      <Badge pill bg='danger' className='cart-badge'>
                        {totalCartItems}
                      </Badge>
                    )}
                  </Nav.Link>
                </LinkContainer>
              )}

              {/* منوی کاربر لاگین شده */}
              {userInfo ? (
                <NavDropdown title={userInfo.name} id='username' className='nav-user'>
                  {/* باگ ۶ fix: ادمین "سفارش‌های من" نمی‌بینه */}
                  {!userInfo.isAdmin && (
                    <LinkContainer to='/profile'>
                      <NavDropdown.Item>پروفایل و سفارش‌هایم</NavDropdown.Item>
                    </LinkContainer>
                  )}
                  {userInfo.isAdmin && (
                    <LinkContainer to='/profile'>
                      <NavDropdown.Item>پروفایل</NavDropdown.Item>
                    </LinkContainer>
                  )}
                  <NavDropdown.Divider />
                  <NavDropdown.Item onClick={logoutHandler}>
                    خروج
                  </NavDropdown.Item>
                </NavDropdown>
              ) : (
                <LinkContainer to='/login'>
                  <Nav.Link>
                    <FaUser />
                    <span className='me-1'>ورود</span>
                  </Nav.Link>
                </LinkContainer>
              )}

              {/* منوی ادمین */}
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

      {/* باگ ۸ آماده‌سازی: نوار پیام ادمین (فعلاً ثابت) */}
      <div className='announcement-bar'>
        <Container className='d-flex justify-content-center py-2'>
          <span>🎉 ارسال رایگان برای خرید بالای ۵۰۰,۰۰۰ تومان</span>
        </Container>
      </div>
    </header>
  )
}

export default Header
