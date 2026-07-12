import { useState, useEffect } from 'react'
import { Container, Form, Button, Card, Row, Col, ListGroup, Badge } from 'react-bootstrap'
import { FaTrash, FaPlus } from 'react-icons/fa'
import { useNavigate, useParams } from 'react-router-dom'
import { toast } from 'react-toastify'
import {
  useGetCustomPageByIdQuery,
  useUpdateCustomPageMutation,
} from '../../slices/customPageApiSlice'
import { useUploadProductImageMutation, useGetProductsQuery } from '../../slices/productsApiSlice'
import Loader from '../../components/ui/Loader'

const CustomPageEditPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: page, isLoading } = useGetCustomPageByIdQuery(id)
  const [updateCustomPage, { isLoading: saving }] = useUpdateCustomPageMutation()
  const [uploadImage, { isLoading: uploading }] = useUploadProductImageMutation()
  const { data: allProductsData } = useGetProductsQuery({ admin: true })
  const allProducts = allProductsData?.products || []

  const [form, setForm] = useState({
    heroImage: '', heroTitle: '', heroSubtitle: '', heroButtonText: '', heroButtonLink: '',
    sections: [], relatedProducts: [], showInHomeSlider: false, isPublished: true,
  })
  const [productSearch, setProductSearch] = useState('')

  useEffect(() => {
    if (page) {
      setForm({
        heroImage: page.heroImage || '',
        heroTitle: page.heroTitle || '',
        heroSubtitle: page.heroSubtitle || '',
        heroButtonText: page.heroButtonText || '',
        heroButtonLink: page.heroButtonLink || '',
        sections: page.sections || [],
        relatedProducts: (page.relatedProducts || []).map((p) => (typeof p === 'string' ? p : p._id)),
        showInHomeSlider: page.showInHomeSlider || false,
        isPublished: page.isPublished !== undefined ? page.isPublished : true,
      })
    }
  }, [page])

  const uploadHeroImage = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const fd = new FormData()
    fd.append('image', file)
    try {
      const res = await uploadImage(fd).unwrap()
      setForm((f) => ({ ...f, heroImage: res.image }))
      toast.success('آپلود شد')
    } catch {
      toast.error('خطا در آپلود')
    }
  }

  const addSection = () => {
    setForm((f) => ({ ...f, sections: [...f.sections, { heading: '', body: '', image: '' }] }))
  }

  const updateSection = (idx, field, value) => {
    setForm((f) => {
      const sections = [...f.sections]
      sections[idx] = { ...sections[idx], [field]: value }
      return { ...f, sections }
    })
  }

  const removeSection = (idx) => {
    setForm((f) => ({ ...f, sections: f.sections.filter((_, i) => i !== idx) }))
  }

  const selectedProducts = allProducts.filter((p) => form.relatedProducts.includes(p._id))
  const filteredProducts = productSearch.trim()
    ? allProducts.filter((p) => p.name.includes(productSearch.trim())).slice(0, 15)
    : []

  const toggleProduct = (productId) => {
    setForm((f) => ({
      ...f,
      relatedProducts: f.relatedProducts.includes(productId)
        ? f.relatedProducts.filter((id2) => id2 !== productId)
        : [...f.relatedProducts, productId],
    }))
  }

  const saveHandler = async () => {
    try {
      await updateCustomPage({ id, ...form }).unwrap()
      toast.success('ذخیره شد')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ذخیره')
    }
  }

  if (isLoading) return <Loader />

  return (
    <Container className='py-4'>
      <Button variant='outline-secondary' className='mb-4' onClick={() => navigate('/admin/custompages')}>
        بازگشت
      </Button>

      <Card className='p-4 mb-4'>
        <h5 className='mb-3'>🖼️ هیرو — <code>/pages/{page?.slug}</code></h5>
        <Form.Group className='mb-3'>
          <Form.Label>عکس هیرو</Form.Label>
          <Form.Control type='file' accept='image/*' onChange={uploadHeroImage} disabled={uploading} />
          {form.heroImage && (
            <img src={form.heroImage} alt='' className='mt-2 rounded w-100' style={{ maxHeight: '220px', objectFit: 'cover' }} />
          )}
        </Form.Group>
        <Form.Group className='mb-3'>
          <Form.Label>عنوان</Form.Label>
          <Form.Control value={form.heroTitle} onChange={(e) => setForm({ ...form, heroTitle: e.target.value })} />
        </Form.Group>
        <Form.Group className='mb-3'>
          <Form.Label>زیرعنوان</Form.Label>
          <Form.Control value={form.heroSubtitle} onChange={(e) => setForm({ ...form, heroSubtitle: e.target.value })} />
        </Form.Group>
        <Row>
          <Col md={6}>
            <Form.Group className='mb-3'>
              <Form.Label>متن دکمه</Form.Label>
              <Form.Control value={form.heroButtonText} onChange={(e) => setForm({ ...form, heroButtonText: e.target.value })} placeholder='مشاهده محصولات' />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group className='mb-3'>
              <Form.Label>لینک دکمه</Form.Label>
              <Form.Control value={form.heroButtonLink} onChange={(e) => setForm({ ...form, heroButtonLink: e.target.value })} placeholder='/search/گیاه زنده' />
            </Form.Group>
          </Col>
        </Row>
      </Card>

      <Card className='p-4 mb-4'>
        <div className='d-flex justify-content-between align-items-center mb-3'>
          <h5 className='mb-0'>📄 بخش‌های متنی آزاد</h5>
          <Button size='sm' variant='outline-success' onClick={addSection}>
            <FaPlus className='ms-1' /> بخش جدید
          </Button>
        </div>
        {form.sections.map((section, idx) => (
          <Card key={idx} className='p-3 mb-3 bg-light'>
            <div className='d-flex justify-content-between mb-2'>
              <strong>بخش {idx + 1}</strong>
              <Button size='sm' variant='outline-danger' onClick={() => removeSection(idx)}>
                <FaTrash />
              </Button>
            </div>
            <Form.Group className='mb-2'>
              <Form.Control placeholder='عنوان بخش' value={section.heading} onChange={(e) => updateSection(idx, 'heading', e.target.value)} />
            </Form.Group>
            <Form.Group>
              <Form.Control as='textarea' rows={3} placeholder='متن بخش' value={section.body} onChange={(e) => updateSection(idx, 'body', e.target.value)} />
            </Form.Group>
          </Card>
        ))}
        {form.sections.length === 0 && <p className='text-muted'>هنوز بخشی اضافه نکردی.</p>}
      </Card>

      <Card className='p-4 mb-4'>
        <h5 className='mb-3'>🛒 محصولات مرتبط</h5>
        {selectedProducts.length > 0 && (
          <div className='d-flex flex-wrap gap-2 mb-2'>
            {selectedProducts.map((p) => (
              <Badge key={p._id} bg='success' style={{ cursor: 'pointer' }} onClick={() => toggleProduct(p._id)}>
                {p.name} ✕
              </Badge>
            ))}
          </div>
        )}
        <Form.Control
          placeholder='جستجوی نام محصول برای افزودن...'
          value={productSearch}
          onChange={(e) => setProductSearch(e.target.value)}
        />
        {filteredProducts.length > 0 && (
          <ListGroup className='mt-1' style={{ maxHeight: '220px', overflowY: 'auto' }}>
            {filteredProducts.map((p) => (
              <ListGroup.Item
                key={p._id}
                action
                type='button'
                active={form.relatedProducts.includes(p._id)}
                onClick={(e) => { e.preventDefault(); toggleProduct(p._id) }}
                className='d-flex align-items-center gap-2'
              >
                <img src={p.image} alt='' style={{ width: '32px', height: '32px', objectFit: 'cover', borderRadius: '4px' }} />
                {p.name}
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </Card>

      <Card className='p-4 mb-4'>
        <Form.Check
          type='switch'
          className='mb-2'
          label='نمایش هم تو اسلایدر اصلی صفحه‌ی خانه'
          checked={form.showInHomeSlider}
          onChange={(e) => setForm({ ...form, showInHomeSlider: e.target.checked })}
        />
        <Form.Check
          type='switch'
          label='منتشر شود (در دسترس عمومی)'
          checked={form.isPublished}
          onChange={(e) => setForm({ ...form, isPublished: e.target.checked })}
        />
      </Card>

      <Button className='btn-aqualotus' onClick={saveHandler} disabled={saving || uploading}>
        {saving ? 'در حال ذخیره...' : 'ذخیره صفحه'}
      </Button>
    </Container>
  )
}

export default CustomPageEditPage
