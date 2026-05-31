const Rating = ({ value, text }) => {
  return (
    <div className='rating'>
      {[1, 2, 3, 4, 5].map((star) => (
        <span key={star}>
          <i
            style={{ color: '#2d6a4f' }}
            className={
              value >= star
                ? 'fas fa-star'
                : value >= star - 0.5
                ? 'fas fa-star-half-alt'
                : 'far fa-star'
            }
          />
        </span>
      ))}
      {text && <span className='rating-text me-1'>{text}</span>}
    </div>
  )
}

export default Rating