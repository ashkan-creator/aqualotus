const ProductCardSkeleton = () => (
  <div
    style={{
      borderRadius: '20px',
      overflow: 'hidden',
      background: 'rgba(10,10,10,0.88)',
      border: '1px solid rgba(255,255,255,0.06)',
    }}
  >
    <div className='aq-skeleton-shimmer' style={{ height: '260px' }} />
    <div style={{ padding: '12px 14px' }}>
      <div className='aq-skeleton-shimmer' style={{ height: '16px', width: '55%', borderRadius: '6px', marginBottom: '10px' }} />
      <div className='aq-skeleton-shimmer' style={{ height: '12px', width: '35%', borderRadius: '6px', marginBottom: '10px' }} />
      <div className='aq-skeleton-shimmer' style={{ height: '16px', width: '45%', borderRadius: '6px' }} />
    </div>
  </div>
)

export default ProductCardSkeleton
