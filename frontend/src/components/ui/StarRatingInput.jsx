import { useState } from 'react'

const StarRatingInput = ({ value, onChange }) => {
  const [hoverValue, setHoverValue] = useState(0)

  const displayValue = hoverValue || value

  return (
    <div className='star-rating-input' style={{ display: 'flex', gap: '6px', fontSize: '1.8rem', cursor: 'pointer' }}>
      {[1, 2, 3, 4, 5].map((star) => (
        <i
          key={star}
          className={displayValue >= star ? 'fas fa-star' : 'far fa-star'}
          style={{ color: displayValue >= star ? '#2d6a4f' : '#ccc', transition: 'color 0.15s' }}
          onMouseEnter={() => setHoverValue(star)}
          onMouseLeave={() => setHoverValue(0)}
          onClick={() => onChange(star)}
        />
      ))}
    </div>
  )
}

export default StarRatingInput
