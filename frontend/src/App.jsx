import { Outlet } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import Header from './components/layout/Header'
import Footer from './components/layout/Footer'
import CustomCursor from './components/ui/CustomCursor'

const App = () => {
  return (
    <>
      <CustomCursor />
      <ToastContainer position='top-right' rtl={true} />
      <Header />
      <main className='py-3'>
        <Outlet />
      </main>
      <Footer />
    </>
  )
}

export default App
