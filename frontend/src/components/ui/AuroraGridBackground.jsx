import { useState, useEffect } from 'react'

const BEAM_COUNT = 60

const AuroraGridBackground = ({ beamCount = BEAM_COUNT }) => {
  const [beams, setBeams] = useState([])

  useEffect(() => {
    const generated = Array.from({ length: beamCount }).map((_, i) => {
      const riseDur = Math.random() * 2 + 4
      const dropDur = Math.random() * 3 + 3
      return {
        id: i,
        style: {
          left: `${Math.random() * 100}%`,
          width: `${Math.floor(Math.random() * 3) + 1}px`,
          animationDelay: `${Math.random() * 5}s`,
          animationDuration: `${riseDur}s, ${riseDur}s, ${dropDur}s`,
        },
      }
    })
    setBeams(generated)
  }, [beamCount])

  return (
    <div className='aq-aurora-scene' aria-hidden='true'>
      <div className='aq-aurora-floor' />
      <div className='aq-aurora-main-column' />
      <div className='aq-aurora-beam-container'>
        {beams.map((beam) => (
          <div key={beam.id} className='aq-aurora-beam' style={beam.style} />
        ))}
      </div>
    </div>
  )
}

export default AuroraGridBackground
