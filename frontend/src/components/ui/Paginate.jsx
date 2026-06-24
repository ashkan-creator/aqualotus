import { Link } from 'react-router-dom'

const Paginate = ({ pages, page, isAdmin = false, keyword = '' }) => {
  if (pages <= 1) return null

  const getLink = (pageNumber) => {
    if (isAdmin) return `/admin/productlist/${pageNumber}`
    return keyword ? `/search/${keyword}/page/${pageNumber}` : `/page/${pageNumber}`
  }

  return (
    <div
      className='d-flex justify-content-center align-items-center mt-4'
      style={{ gap: '8px', flexWrap: 'wrap', direction: 'ltr' }}
    >
      {[...Array(pages).keys()].map((x) => {
        const pageNumber = x + 1
        const isActive = pageNumber === page
        return (
          <Link
            key={pageNumber}
            to={getLink(pageNumber)}
            style={{
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 600,
              fontSize: '0.9rem',
              textDecoration: 'none',
              transition: 'all var(--dur-base, 0.3s) var(--ease-soft, ease)',
              backgroundColor: isActive ? 'var(--primary)' : 'var(--white)',
              color: isActive ? '#fff' : 'var(--primary)',
              border: `1.5px solid ${isActive ? 'var(--primary)' : 'var(--primary-light)'}`,
              boxShadow: isActive ? '0 4px 10px rgba(45,106,79,0.3)' : 'none',
            }}
            onMouseEnter={(e) => {
              if (!isActive) {
                e.currentTarget.style.backgroundColor = 'var(--bg-light)'
                e.currentTarget.style.transform = 'translateY(-2px)'
              }
            }}
            onMouseLeave={(e) => {
              if (!isActive) {
                e.currentTarget.style.backgroundColor = 'var(--white)'
                e.currentTarget.style.transform = 'translateY(0)'
              }
            }}
          >
            {pageNumber}
          </Link>
        )
      })}
    </div>
  )
}

export default Paginate
