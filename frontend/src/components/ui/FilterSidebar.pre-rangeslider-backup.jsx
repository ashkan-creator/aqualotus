import { Form, Card, Button, Badge } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

const FilterSidebar = ({ filters, setFilters }) => {
  const navigate = useNavigate()

  const resetFilters = () => {
    setFilters({
      careLevel: '',
      position: '',
      cultivationType: '',
      needsSoil: '',
      minPrice: '',
      maxPrice: '',
    })
    navigate('/')
  }

  const activeCount = Object.values(filters).filter(Boolean).length

  return (
    <Card className='p-3'>
      <div className='d-flex justify-content-between align-items-center mb-3'>
        <h6 className='mb-0'>
          🔍 فیلتر
          {activeCount > 0 && <Badge bg='success' className='me-2'>{activeCount}</Badge>}
        </h6>
        {activeCount > 0 && (
          <Button variant='link' size='sm' className='text-danger p-0' onClick={resetFilters}>
            پاک کردن
          </Button>
        )}
      </div>

      <Form.Group className='mb-3'>
        <Form.Label>سختی نگهداری</Form.Label>
        <Form.Select value={filters.careLevel} onChange={(e) => setFilters({ ...filters, careLevel: e.target.value })}>
          <option value=''>همه</option>
          <option value='آسان'>🟢 آسان</option>
          <option value='متوسط'>🟡 متوسط</option>
          <option value='سخت'>🔴 سخت</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className='mb-3'>
        <Form.Label>محل کاشت</Form.Label>
        <Form.Select value={filters.position} onChange={(e) => setFilters({ ...filters, position: e.target.value })}>
          <option value=''>همه</option>
          <option value='جلو'>جلو آکواریوم</option>
          <option value='میانه'>میانه آکواریوم</option>
          <option value='پشت'>پشت آکواریوم</option>
          <option value='شناور'>شناور</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className='mb-3'>
        <Form.Label>نوع کشت</Form.Label>
        <Form.Select value={filters.cultivationType} onChange={(e) => setFilters({ ...filters, cultivationType: e.target.value })}>
          <option value=''>همه</option>
          <option value='آبزی'>آبزی</option>
          <option value='هیدروپونیک'>هیدروپونیک</option>
          <option value='هر دو'>هر دو</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className='mb-3'>
        <Form.Label>نیاز به بستر</Form.Label>
        <Form.Select value={filters.needsSoil} onChange={(e) => setFilters({ ...filters, needsSoil: e.target.value })}>
          <option value=''>همه</option>
          <option value='true'>دارد</option>
          <option value='false'>ندارد</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className='mb-2'>
        <Form.Label>قیمت (تومان)</Form.Label>
        <div className='d-flex gap-2'>
          <Form.Control
            type='number'
            placeholder='از'
            value={filters.minPrice}
            onChange={(e) => setFilters({ ...filters, minPrice: e.target.value })}
          />
          <Form.Control
            type='number'
            placeholder='تا'
            value={filters.maxPrice}
            onChange={(e) => setFilters({ ...filters, maxPrice: e.target.value })}
          />
        </div>
      </Form.Group>
    </Card>
  )
}

export default FilterSidebar
