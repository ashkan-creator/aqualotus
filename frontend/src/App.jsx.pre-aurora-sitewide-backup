import { Outlet, useLocation } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { AnimatePresence } from 'framer-motion'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import Header from './components/layout/Header'
import Footer from './components/layout/Footer'
import ScrollToTop from './components/ScrollToTop'
import CustomCursor from './components/ui/CustomCursor'
import PageTransition from './components/ui/PageTransition'
import ErrorBoundary from './components/ui/ErrorBoundary'

const App = () => {
  const location = useLocation()
  const suppressPageTransition = useSelector((state) => state.ui.suppressPageTransition)

  return (
    <ErrorBoundary>
      <CustomCursor />
      <ToastContainer position='top-right' rtl={true} />
      <ScrollToTop />
      <Header />
      <main className='py-3'>
        {suppressPageTransition ? (
          // در طول یه ناوبری View-Transition، بدون هیچ افکت Framer —
          // تا صفحه‌ی قدیم/جدید هم‌پوشانی نداشته باشن و مورف کار کنه
          <div key={location.pathname}>
            <ErrorBoundary>
              <Outlet />
            </ErrorBoundary>
          </div>
        ) : (
          <AnimatePresence mode='wait'>
            <PageTransition key={location.pathname}>
              <ErrorBoundary>
                <Outlet />
              </ErrorBoundary>
            </PageTransition>
          </AnimatePresence>
        )}
      </main>
      <Footer />
    </ErrorBoundary>
  )
}
export default App
