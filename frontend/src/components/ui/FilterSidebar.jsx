import { Card, Button, Badge, Accordion } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

const MAX_PRICE = 5000000

const CHIP_GROUPS = [
  {
    key: 'category',
    label: 'نوع جنس',
    icon: '🪴',
    options: [
      { value: 'گیاه زنده', label: 'گیاه زنده' },
      { value: 'کود و مکمل', label: 'کود و مکمل' },
      { value: 'بستر', label: 'بستر' },
      { value: 'لوازم جانبی', label: 'لوازم جانبی' },
      { value: 'سنگ', label: 'سنگ' },
      { value: 'چوب', label: 'چوب' },
    ],
  },
  {
    key: 'careLevel',
    label: 'سختی نگهداری',
    icon: '🌿',
    options: [
      { value: 'آسان', label: '🟢 آسان' },
      { value: 'متوسط', label: '🟡 متوسط' },
      { value: 'سخت', label: '🔴 سخت' },
    ],
  },
  {
    key: 'position',
    label: 'محل کاشت',
    icon: '📍',
    options: [
      { value: 'جلو', label: 'جلو آکواریوم' },
      { value: 'میانه', label: 'میانه آکواریوم' },
      { value: 'پشت', label: 'پشت آکواریوم' },
      { value: 'شناور', label: 'شناور' },
    ],
  },
  {
    key: 'cultivationType',
    label: 'نوع کشت',
    icon: '💧',
    options: [
      { value: 'آبزی', label: 'آبزی' },
      { value: 'هیدروپونیک', label: 'هیدروپونیک' },
      { value: 'هر دو', label: 'هر دو' },
    ],
  },
  {
    key: 'needsSoil',
    label: 'نیاز به بستر',
    icon: '🪨',
    options: [
      { value: 'true', label: 'دارد' },
      { value: 'false', label: 'ندارد' },
    ],
  },
]

const chipLabelFor = (key, value) => {
  if (key === 'minPrice') return `از ${Number(value).toLocaleString('fa-IR')} ت`
  if (key === 'maxPrice') return `تا ${Number(value).toLocaleString('fa-IR')} ت`
  if (key === 'needsSoil') return `بستر: ${value === 'true' ? 'دارد' : 'ندارد'}`
  const group = CHIP_GROUPS.find((g) => g.key === key)
  const opt = group?.options.find((o) => o.value === value)
  return opt?.label || value
}

const FilterSidebar = ({ filters, setFilters }) => {
  const navigate = useNavigate()

  const resetFilters = () => {
    setFilters({
      careLevel: '', position: '', cultivationType: '',
      needsSoil: '', minPrice: '', maxPrice: '', category: '',
    })
    navigate('/')
  }

  const clearOne = (key) => setFilters({ ...filters, [key]: '' })

  const toggleOption = (key, value) => {
    setFilters({ ...filters, [key]: filters[key] === value ? '' : value })
  }

  const activeChips = Object.entries(filters)
    .filter(([, v]) => Boolean(v))
    .map(([key, value]) => ({ key, label: chipLabelFor(key, value) }))

  const minPct = (Number(filters.minPrice || 0) / MAX_PRICE) * 100
  const maxPct = (Number(filters.maxPrice || MAX_PRICE) / MAX_PRICE) * 100

  return (
    <Card className='p-3 aq-filter-card'>
      <div className='d-flex justify-content-between align-items-center mb-3 aq-filter-header'>
        <h6 className='mb-0 d-flex align-items-center'>
          <span className='aq-filter-title-badge'>🔍</span>
          فیلتر
          {activeChips.length > 0 && <Badge bg='success' className='me-2 aq-filter-count-total'>{activeChips.length}</Badge>}
        </h6>
        {activeChips.length > 0 && (
          <Button variant='link' size='sm' className='text-danger p-0 aq-filter-clear-all' onClick={resetFilters}>
            پاک کردن همه
          </Button>
        )}
      </div>

      {activeChips.length > 0 && (
        <div className='d-flex flex-wrap gap-2 mb-3'>
          {activeChips.map((chip) => (
            <span
              key={chip.key}
              className='aq-filter-chip'
              onClick={() => clearOne(chip.key)}
              role='button'
            >
              {chip.label} <span className='aq-filter-chip-x'>✕</span>
            </span>
          ))}
        </div>
      )}

      <Accordion defaultActiveKey='0' alwaysOpen>
        {CHIP_GROUPS.map((group, idx) => (
          <Accordion.Item eventKey={String(idx)} key={group.key} className='aq-filter-accordion-item'>
            <Accordion.Header>
              <span className='aq-filter-section-icon'>{group.icon}</span>
              <span>{group.label}</span>
              {filters[group.key] && <Badge bg='success' className='ms-2 aq-filter-count-badge'>1</Badge>}
            </Accordion.Header>
            <Accordion.Body>
              <div className='d-flex flex-wrap gap-2'>
                {group.options.map((opt) => (
                  <button
                    key={opt.value}
                    type='button'
                    className={`aq-filter-pill ${filters[group.key] === opt.value ? 'active' : ''}`}
                    onClick={() => toggleOption(group.key, opt.value)}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </Accordion.Body>
          </Accordion.Item>
        ))}

        <Accordion.Item eventKey='price' className='aq-filter-accordion-item'>
          <Accordion.Header>
            <span className='aq-filter-section-icon'>💰</span>
            <span>قیمت (تومان)</span>
            {(filters.minPrice || filters.maxPrice) && (
              <Badge bg='success' className='ms-2 aq-filter-count-badge'>1</Badge>
            )}
          </Accordion.Header>
          <Accordion.Body>
            <div className='aq-price-box'>
              <div className='d-flex justify-content-between mb-1'>
                <small className='text-muted'>{Number(filters.minPrice || 0).toLocaleString('fa-IR')}</small>
                <small className='text-muted'>{Number(filters.maxPrice || MAX_PRICE).toLocaleString('fa-IR')}</small>
              </div>
              <div className='aq-price-range-slider' style={{ position: 'relative', height: '44px' }}>
                <span
                  className='aq-price-bubble'
                  style={{ left: `${minPct}%` }}
                >
                  {Number(filters.minPrice || 0).toLocaleString('fa-IR')}
                </span>
                <span
                  className='aq-price-bubble'
                  style={{ left: `${maxPct}%` }}
                >
                  {Number(filters.maxPrice || MAX_PRICE).toLocaleString('fa-IR')}
                </span>
                <div className='aq-price-track' />
                <div
                  className='aq-price-track-fill'
                  style={{
                    right: `${100 - maxPct}%`,
                    left: `${minPct}%`,
                  }}
                />
                <input
                  type='range'
                  min={0}
                  max={MAX_PRICE}
                  step={10000}
                  value={filters.minPrice || 0}
                  onChange={(e) => {
                    const val = Math.min(Number(e.target.value), Number(filters.maxPrice || MAX_PRICE))
                    setFilters({ ...filters, minPrice: val })
                  }}
                  className='aq-range-thumb'
                />
                <input
                  type='range'
                  min={0}
                  max={MAX_PRICE}
                  step={10000}
                  value={filters.maxPrice || MAX_PRICE}
                  onChange={(e) => {
                    const val = Math.max(Number(e.target.value), Number(filters.minPrice || 0))
                    setFilters({ ...filters, maxPrice: val })
                  }}
                  className='aq-range-thumb'
                />
              </div>
            </div>
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </Card>
  )
}

export default FilterSidebar
