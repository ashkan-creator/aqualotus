import { Form, Row, Col } from 'react-bootstrap'

// کامپوننت مشترک تنظیم استایل متن (رنگ/فونت/تراز/شدو/گلو/فید)
// value: آبجکت titleStyle | onChange: (newTitleStyle) => void
const FONT_OPTIONS = [
  { value: 'default', label: 'وزیرمتن (پیش‌فرض)' },
  { value: 'serif', label: 'سریف' },
  { value: 'mono', label: 'مونو' },
]

const TextStyleEditor = ({ value, onChange }) => {
  const style = value || {
    color: '#ffffff',
    fontFamily: 'default',
    textAlign: 'center',
    shadow: { enabled: false, color: '#000000', blur: 8, offsetX: 0, offsetY: 2, inset: false },
    glow: { enabled: false, color: '#52b788', intensity: 10 },
    fadeIn: { enabled: false },
  }

  const update = (patch) => onChange({ ...style, ...patch })
  const updateShadow = (patch) => onChange({ ...style, shadow: { ...style.shadow, ...patch } })
  const updateGlow = (patch) => onChange({ ...style, glow: { ...style.glow, ...patch } })

  return (
    <div className='border rounded-3 p-3 mb-3' style={{ background: '#f8f9fa' }}>
      <div className='fw-bold mb-3 small text-muted'>🎨 استایل متن</div>

      <Row className='mb-3'>
        <Col xs={6}>
          <Form.Label className='small'>رنگ فونت</Form.Label>
          <Form.Control
            type='color'
            value={style.color}
            onChange={(e) => update({ color: e.target.value })}
            title='رنگ فونت'
          />
        </Col>
        <Col xs={6}>
          <Form.Label className='small'>فونت</Form.Label>
          <Form.Select value={style.fontFamily} onChange={(e) => update({ fontFamily: e.target.value })}>
            {FONT_OPTIONS.map((f) => (
              <option key={f.value} value={f.value}>{f.label}</option>
            ))}
          </Form.Select>
        </Col>
      </Row>

      <div className='mb-3'>
        <Form.Label className='small d-block'>تراز متن</Form.Label>
        <div className='d-flex gap-2'>
          {[
            { value: 'right', label: 'راست' },
            { value: 'center', label: 'وسط' },
            { value: 'left', label: 'چپ' },
          ].map((a) => (
            <button
              key={a.value}
              type='button'
              className={`aq-align-btn ${style.textAlign === a.value ? 'active' : ''}`}
              onClick={() => update({ textAlign: a.value })}
            >
              {a.label}
            </button>
          ))}
        </div>
      </div>

      <Form.Check
        type='checkbox'
        id='titlestyle-shadow-enabled'
        label='سایه (شدو)'
        checked={style.shadow?.enabled || false}
        onChange={(e) => updateShadow({ enabled: e.target.checked })}
        className='mb-2'
      />
      {style.shadow?.enabled && (
        <Row className='mb-3 ps-3'>
          <Col xs={6} className='mb-2'>
            <Form.Label className='small'>رنگ سایه</Form.Label>
            <Form.Control type='color' value={style.shadow.color} onChange={(e) => updateShadow({ color: e.target.value })} />
          </Col>
          <Col xs={6} className='mb-2'>
            <Form.Check
              type='checkbox'
              id='titlestyle-shadow-inset'
              label='داخلی (inset)'
              checked={style.shadow.inset || false}
              onChange={(e) => updateShadow({ inset: e.target.checked })}
            />
          </Col>
          <Col xs={12} className='mb-2'>
            <Form.Label className='small'>میزان محو شدگی: {style.shadow.blur}px</Form.Label>
            <Form.Range min={0} max={40} value={style.shadow.blur} onChange={(e) => updateShadow({ blur: Number(e.target.value) })} />
          </Col>
          <Col xs={6}>
            <Form.Label className='small'>افست افقی: {style.shadow.offsetX}px</Form.Label>
            <Form.Range min={-20} max={20} value={style.shadow.offsetX} onChange={(e) => updateShadow({ offsetX: Number(e.target.value) })} />
          </Col>
          <Col xs={6}>
            <Form.Label className='small'>افست عمودی: {style.shadow.offsetY}px</Form.Label>
            <Form.Range min={-20} max={20} value={style.shadow.offsetY} onChange={(e) => updateShadow({ offsetY: Number(e.target.value) })} />
          </Col>
        </Row>
      )}

      <Form.Check
        type='checkbox'
        id='titlestyle-glow-enabled'
        label='درخشش (گلو)'
        checked={style.glow?.enabled || false}
        onChange={(e) => updateGlow({ enabled: e.target.checked })}
        className='mb-2'
      />
      {style.glow?.enabled && (
        <Row className='mb-3 ps-3'>
          <Col xs={6} className='mb-2'>
            <Form.Label className='small'>رنگ درخشش</Form.Label>
            <Form.Control type='color' value={style.glow.color} onChange={(e) => updateGlow({ color: e.target.value })} />
          </Col>
          <Col xs={6} className='mb-2'>
            <Form.Label className='small'>شدت: {style.glow.intensity}px</Form.Label>
            <Form.Range min={0} max={40} value={style.glow.intensity} onChange={(e) => updateGlow({ intensity: Number(e.target.value) })} />
          </Col>
        </Row>
      )}

      <Form.Check
        type='checkbox'
        id='titlestyle-fadein-enabled'
        label='انیمیشن ظاهرشدن (فید)'
        checked={style.fadeIn?.enabled || false}
        onChange={(e) => update({ fadeIn: { enabled: e.target.checked } })}
      />
    </div>
  )
}

export default TextStyleEditor
