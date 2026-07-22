import { useState, useEffect, useRef } from 'react'
import { Form, Button, ListGroup } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router-dom'
import { FaSearch } from 'react-icons/fa'
import { useGetProductsQuery } from '../../slices/productsApiSlice'

const SearchBox = () => {
  const navigate = useNavigate()
  const { keyword: urlKeyword } = useParams()
  const [keyword, setKeyword] = useState(urlKeyword || '')
  const [debouncedKeyword, setDebouncedKeyword] = useState('')
  const [showSuggestions, setShowSuggestions] = useState(false)
  const wrapperRef = useRef(null)

  // debounce 300ms
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedKeyword(keyword)
    }, 300)
    return () => clearTimeout(timer)
  }, [keyword])

  const { data } = useGetProductsQuery(
    { keyword: debouncedKeyword },
    { skip: debouncedKeyword.length < 2 }
  )

  // بستن suggestions با کلیک بیرون
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowSuggestions(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const submitHandler = (e) => {
    e.preventDefault()
    setShowSuggestions(false)
    if (keyword.trim()) {
      navigate(`/search/${keyword}`)
    } else {
      navigate('/')
    }
  }

  const selectProduct = (productId) => {
    setShowSuggestions(false)
    setKeyword('')
    navigate(`/product/${productId}`)
  }

  return (
    <div ref={wrapperRef} style={{ position: 'relative', width: '100%' }}>
      <Form onSubmit={submitHandler} className='d-flex search-form'>
        <Form.Control
          type='text'
          value={keyword}
          onChange={(e) => {
            setKeyword(e.target.value)
            setShowSuggestions(true)
          }}
          onFocus={() => keyword.length >= 2 && setShowSuggestions(true)}
          placeholder='جستجو...'
          className='search-input'
        />
        <Button type='submit' className='search-btn'>
          <FaSearch />
        </Button>
      </Form>

      {/* نتایج live */}
      {showSuggestions && data?.products?.length > 0 && keyword.length >= 2 && (
        <ListGroup
          className='aq-search-results'
          style={{
            position: 'absolute',
            top: '100%',
            right: 0,
            left: 0,
            zIndex: 9999,
            maxHeight: '300px',
            overflowY: 'auto',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          }}
        >
          {data.products.slice(0, 6).map((product) => (
            <ListGroup.Item
              key={product._id}
              action
              onClick={() => selectProduct(product._id)}
              className='d-flex align-items-center gap-2 py-2'
              style={{ cursor: 'pointer' }}
            >
              <img
                src={product.image}
                alt={product.name}
                style={{ width: '40px', height: '40px', objectFit: 'cover', borderRadius: '4px' }}
              />
              <div>
                <div style={{ fontSize: '0.9rem' }}>{product.name}</div>
                <div style={{ fontSize: '0.8rem', color: '#2d6a4f', fontWeight: 'bold' }}>
                  {product.price.toLocaleString('fa-IR')} تومان
                </div>
              </div>
            </ListGroup.Item>
          ))}
          {data.products.length > 6 && (
            <ListGroup.Item
              action
              onClick={submitHandler}
              className='text-center text-muted'
              style={{ fontSize: '0.85rem' }}
            >
              مشاهده همه نتایج ({data.products.length} محصول)
            </ListGroup.Item>
          )}
        </ListGroup>
      )}
    </div>
  )
}

export default SearchBox
