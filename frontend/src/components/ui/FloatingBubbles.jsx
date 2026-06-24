const FloatingBubbles = ({ count = 14 }) => {
  const bubbles = Array.from({ length: count }, (_, i) => {
    const size = 10 + Math.random() * 26
    const left = Math.random() * 100
    const duration = 7 + Math.random() * 8
    const delay = Math.random() * 8
    const drift = (Math.random() * 60 - 30).toFixed(0)
    return { id: i, size, left, duration, delay, drift }
  })

  return (
    <div className='aq-bubbles' aria-hidden='true'>
      {bubbles.map((b) => (
        <span
          key={b.id}
          className='aq-bubble'
          style={{
            width: `${b.size}px`,
            height: `${b.size}px`,
            left: `${b.left}%`,
            animationDuration: `${b.duration}s`,
            animationDelay: `${b.delay}s`,
            '--drift': `${b.drift}px`,
          }}
        />
      ))}
    </div>
  )
}

export default FloatingBubbles
