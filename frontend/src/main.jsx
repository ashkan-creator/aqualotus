import { StrictMode, lazy, Suspense } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { HelmetProvider } from 'react-helmet-async'
import store from './store'
import App from './App.jsx'
import ErrorBoundary from './components/ui/ErrorBoundary'
import Loader from './components/ui/Loader'
import 'bootstrap/dist/css/bootstrap.min.css'
import './index.css'
import './animations.css'
import './fonts.css'

// صفحات پرترافیک (بدون lazy — برای سرعت)
import HomePage from './pages/HomePage'
import LinkPagePublicPage from './pages/LinkPagePublicPage'
import NotFoundPage from './pages/NotFoundPage'
import CustomPagePublicPage from './pages/CustomPagePublicPage'
import ProductPage from './pages/ProductPage'
import LoginPage from './pages/LoginPage'

// بقیه صفحات — lazy load
const CartPage = lazy(() => import('./pages/CartPage'))
const RegisterPage = lazy(() => import('./pages/RegisterPage'))
const ForgotPasswordPage = lazy(() => import('./pages/ForgotPasswordPage'))
const ResetPasswordPage = lazy(() => import('./pages/ResetPasswordPage'))
const VerifyOtpPage = lazy(() => import('./pages/VerifyOtpPage'))
const ShippingPage = lazy(() => import('./pages/ShippingPage'))
const PaymentPage = lazy(() => import('./pages/PaymentPage'))
const PlaceOrderPage = lazy(() => import('./pages/PlaceOrderPage'))
const OrderPage = lazy(() => import('./pages/OrderPage'))
const ProfilePage = lazy(() => import('./pages/ProfilePage'))
const ContactPage = lazy(() => import('./pages/ContactPage'))
const QuizPage = lazy(() => import('./pages/QuizPage'))
const AboutPage = lazy(() => import('./pages/AboutPage'))
const BlogPage = lazy(() => import('./pages/BlogPage'))
const BlogPostPage = lazy(() => import('./pages/BlogPostPage'))

const AdminProductListPage = lazy(() => import('./pages/admin/ProductListPage'))
const AdminProductEditPage = lazy(() => import('./pages/admin/ProductEditPage'))
const AdminOrderListPage = lazy(() => import('./pages/admin/OrderListPage'))
const AdminUserListPage = lazy(() => import('./pages/admin/UserListPage'))
const AdminUserEditPage = lazy(() => import('./pages/admin/UserEditPage'))
const AdminFamilyListPage = lazy(() => import('./pages/admin/FamilyListPage'))
const AdminSettingsPage = lazy(() => import('./pages/admin/SettingsPage'))
const AdminDashboardPage = lazy(() => import('./pages/admin/DashboardPage'))
const AdminReportsPage = lazy(() => import('./pages/admin/ReportsPage'))
const AdminBlogListPage = lazy(() => import('./pages/admin/BlogListPage'))
const AdminSliderListPage = lazy(() => import('./pages/admin/SliderListPage'))
const AdminBlogEditPage = lazy(() => import('./pages/admin/BlogEditPage'))
const AdminReviewsPage = lazy(() => import('./pages/admin/AdminReviewsPage'))
const AdminActivityLogPage = lazy(() => import('./pages/admin/ActivityLogPage'))
const AdminLinkPageListPage = lazy(() => import('./pages/admin/LinkPageListPage'))
const AdminLinkPageEditPage = lazy(() => import('./pages/admin/LinkPageEditPage'))
const AdminCustomPageListPage = lazy(() => import('./pages/admin/CustomPageListPage'))
const AdminCustomPageEditPage = lazy(() => import('./pages/admin/CustomPageEditPage'))
const AdminPanelPage = lazy(() => import('./pages/admin/AdminPanelPage'))

import PrivateRoute from './components/PrivateRoute'
import AdminRoute from './components/AdminRoute'

// بستن هر lazy صفحه در Suspense
const withSuspense = (Component) => (
  <Suspense fallback={<Loader />}>
    <Component />
  </Suspense>
)

const router = createBrowserRouter([
  { path: 'links/:slug', element: <LinkPagePublicPage /> },
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'product/:id', element: <ProductPage /> },
      { path: 'cart', element: withSuspense(CartPage) },
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: withSuspense(RegisterPage) },
      { path: 'forgot-password', element: withSuspense(ForgotPasswordPage) },
      { path: 'reset-password/:token', element: withSuspense(ResetPasswordPage) },
      { path: 'verify-otp', element: withSuspense(VerifyOtpPage) },
      { path: 'search/:keyword', element: <HomePage /> },
      { path: 'page/:pageNumber', element: <HomePage /> },
      { path: 'filter', element: <HomePage /> },
      { path: 'search/:keyword/page/:pageNumber', element: <HomePage /> },
      { path: 'contact', element: withSuspense(ContactPage) },
      { path: 'quiz', element: withSuspense(QuizPage) },
      { path: 'about', element: withSuspense(AboutPage) },
      { path: 'blog', element: withSuspense(BlogPage) },
      { path: 'blog/:id', element: withSuspense(BlogPostPage) },
      { path: 'pages/:slug', element: <CustomPagePublicPage /> },
      {
        path: '',
        element: <PrivateRoute />,
        children: [
          { path: 'shipping', element: withSuspense(ShippingPage) },
          { path: 'payment', element: withSuspense(PaymentPage) },
          { path: 'placeorder', element: withSuspense(PlaceOrderPage) },
          { path: 'order/:id', element: withSuspense(OrderPage) },
          { path: 'profile', element: withSuspense(ProfilePage) },
        ],
      },
      {
        path: 'admin',
        element: <AdminRoute />,
        children: [
          { path: 'dashboard', element: withSuspense(AdminDashboardPage) },
          { path: 'reports', element: withSuspense(AdminReportsPage) },
          { path: 'productlist', element: withSuspense(AdminProductListPage) },
          { path: 'product/:id/edit', element: withSuspense(AdminProductEditPage) },
          { path: 'orderlist', element: withSuspense(AdminOrderListPage) },
          { path: 'userlist', element: withSuspense(AdminUserListPage) },
          { path: 'user/:id/edit', element: withSuspense(AdminUserEditPage) },
          { path: 'familylist', element: withSuspense(AdminFamilyListPage) },
          { path: 'settings', element: withSuspense(AdminSettingsPage) },
          { path: 'blog', element: withSuspense(AdminBlogListPage) },
          { path: 'sliders', element: withSuspense(AdminSliderListPage) },
          { path: 'blog/:id/edit', element: withSuspense(AdminBlogEditPage) },
          { path: 'reviews', element: withSuspense(AdminReviewsPage) },
          { path: 'activity-log', element: withSuspense(AdminActivityLogPage) },
          { path: 'linkpages', element: withSuspense(AdminLinkPageListPage) },
          { path: 'linkpages/:id/edit', element: withSuspense(AdminLinkPageEditPage) },
          { path: 'custompages', element: withSuspense(AdminCustomPageListPage) },
          { path: 'custompages/:id/edit', element: withSuspense(AdminCustomPageEditPage) },
          { path: 'panel', element: withSuspense(AdminPanelPage) },
        ],
      },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <HelmetProvider>
      <Provider store={store}>
        <ErrorBoundary>
          <RouterProvider router={router} />
        </ErrorBoundary>
      </Provider>
    </HelmetProvider>
  </StrictMode>
)
