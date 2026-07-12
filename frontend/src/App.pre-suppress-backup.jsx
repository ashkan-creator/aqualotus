import { Outlet, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import Header from './components/layout/Header'
import Footer from './components/layout/Footer'
import CustomCursor from './components/ui/CustomCursor'
import PageTransition from './components/ui/PageTransition'
import ErrorBoundary from './components/ui/ErrorBoundary'

const App = () => {
  const location = useLocation()
  // صفحه‌ی محصول از انیمیشن Framer مستثناست چون مورف عکس بومی مرورگر
  // (View Transitions API) جایگزینش شده؛ ترکیب هر دو باعث تداخل می‌شد.
  const isProductRoute = location.pathname.startsWith('/product/')

  return (
    <ErrorBoundary>
      <CustomCursor />
      <ToastContainer position='top-right' rtl={true} />
      <Header />
      <main className='py-3'>
        <AnimatePresence mode='sync'>
          {isProductRoute ? (
            <div key={location.pathname}>
              <ErrorBoundary>
                <Outlet />
              </ErrorBoundary>
            </div>
          ) : (
            <PageTransition key={location.pathname}>
              <ErrorBoundary>
                <Outlet />
              </ErrorBoundary>
            </PageTransition>
          )}
        </AnimatePresence>
      </main>
      <Footer />
    </ErrorBoundary>
  )
}
export default App
