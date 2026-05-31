import { Spinner } from 'react-bootstrap'

const Loader = () => {
  return (
    <div className='d-flex justify-content-center align-items-center py-5'>
      <Spinner
        animation='border'
        role='status'
        style={{ width: '50px', height: '50px', color: '#2d6a4f' }}
      >
        <span className='visually-hidden'>در حال بارگذاری...</span>
      </Spinner>
    </div>
  )
}

export default Loader