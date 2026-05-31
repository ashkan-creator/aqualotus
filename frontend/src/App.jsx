import { Outlet } from 'react-router-dom'
import Header from './components/layout/Header'
import Footer from './components/layout/Footer'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

const App = () => {
  return (
    <>
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