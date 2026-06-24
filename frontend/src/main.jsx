import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { HelmetProvider } from 'react-helmet-async'
import store from './store'
import App from './App.jsx'
import 'bootstrap/dist/css/bootstrap.min.css'
import './index.css'
import './animations.css'
import HomePage from './pages/HomePage'
import ProductPage from './pages/ProductPage'
import CartPage from './pages/CartPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ShippingPage from './pages/ShippingPage'
import PaymentPage from './pages/PaymentPage'
import PlaceOrderPage from './pages/PlaceOrderPage'
import OrderPage from './pages/OrderPage'
import ProfilePage from './pages/ProfilePage'
import ContactPage from './pages/ContactPage'
import AboutPage from './pages/AboutPage'
import BlogPage from './pages/BlogPage'
import BlogPostPage from './pages/BlogPostPage'
import AdminProductListPage from './pages/admin/ProductListPage'
import AdminProductEditPage from './pages/admin/ProductEditPage'
import AdminOrderListPage from './pages/admin/OrderListPage'
import AdminUserListPage from './pages/admin/UserListPage'
import AdminUserEditPage from './pages/admin/UserEditPage'
import AdminFamilyListPage from './pages/admin/FamilyListPage'
import AdminSettingsPage from './pages/admin/SettingsPage'
import AdminDashboardPage from './pages/admin/DashboardPage'
import AdminBlogListPage from './pages/admin/BlogListPage'
import AdminSliderListPage from './pages/admin/SliderListPage'
import AdminBlogEditPage from './pages/admin/BlogEditPage'
import AdminReviewsPage from './pages/admin/AdminReviewsPage'
import PrivateRoute from './components/PrivateRoute'
import AdminRoute from './components/AdminRoute'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'product/:id', element: <ProductPage /> },
      { path: 'cart', element: <CartPage /> },
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: <RegisterPage /> },
      { path: 'search/:keyword', element: <HomePage /> },
      { path: 'page/:pageNumber', element: <HomePage /> },
      { path: 'filter', element: <HomePage /> },
      { path: 'search/:keyword/page/:pageNumber', element: <HomePage /> },
      { path: 'contact', element: <ContactPage /> },
      { path: 'about', element: <AboutPage /> },
      { path: 'blog', element: <BlogPage /> },
      { path: 'blog/:id', element: <BlogPostPage /> },
      {
        path: '',
        element: <PrivateRoute />,
        children: [
          { path: 'shipping', element: <ShippingPage /> },
          { path: 'payment', element: <PaymentPage /> },
          { path: 'placeorder', element: <PlaceOrderPage /> },
          { path: 'order/:id', element: <OrderPage /> },
          { path: 'profile', element: <ProfilePage /> },
        ],
      },
      {
        path: 'admin',
        element: <AdminRoute />,
        children: [
          { path: 'dashboard', element: <AdminDashboardPage /> },
          { path: 'productlist', element: <AdminProductListPage /> },
          { path: 'product/:id/edit', element: <AdminProductEditPage /> },
          { path: 'orderlist', element: <AdminOrderListPage /> },
          { path: 'userlist', element: <AdminUserListPage /> },
          { path: 'user/:id/edit', element: <AdminUserEditPage /> },
          { path: 'familylist', element: <AdminFamilyListPage /> },
          { path: 'settings', element: <AdminSettingsPage /> },
          { path: 'blog', element: <AdminBlogListPage /> },
          { path: 'sliders', element: <AdminSliderListPage /> },
          { path: 'blog/:id/edit', element: <AdminBlogEditPage /> },
          { path: 'reviews', element: <AdminReviewsPage /> },
        ],
      },
    ],
  },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <HelmetProvider>
      <Provider store={store}>
        <RouterProvider router={router} />
      </Provider>
    </HelmetProvider>
  </StrictMode>
)
