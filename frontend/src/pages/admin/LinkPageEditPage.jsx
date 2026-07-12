import { useState, useEffect } from 'react'
import { Container, Form, Button, Card, ListGroup, Badge, InputGroup, Tabs, Tab } from 'react-bootstrap'
import { FaTrash, FaCopy, FaPlus } from 'react-icons/fa'
import { useNavigate, useParams } from 'react-router-dom'
import { toast } from 'react-toastify'
import {
  useGetLinkPageByIdQuery,
  useUpdateLinkPageMutation,
  useAddLinkMutation,
  useUpdateLinkMutation,
  useDeleteLinkMutation,
} from '../../slices/linkPageApiSlice'
import { useUploadProductImageMutation, useGetProductsQuery } from '../../slices/productsApiSlice'
import { useGetPostsQuery } from '../../slices/blogApiSlice'
import Loader from '../../components/ui/Loader'

const LinkPageEditPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: page, isLoading, refetch } = useGetLinkPageByIdQuery(id)
  const [updateLinkPage] = useUpdateLinkPageMutation()
  const [addLink] = useAddLinkMutation()
  const [updateLink] = useUpdateLinkMutation()
  const [deleteLink] = useDeleteLinkMutation()
  const [uploadImage, { isLoading: uploading }] = useUploadProductImageMutation()

  const { data: allProductsData } = useGetProductsQuery({ admin: true })
  const allProducts = allProductsData?.products || []
  const { data: allPosts } = useGetPostsQuery()

  const [meta, setMeta] = useState({ title: '', bio: '', avatar: '', isActive: true })
  const [linkMode, setLinkMode] = useState('product')
  const [search, setSearch] = useState('')
  const [selectedProductIds, setSelectedProductIds] = useState([])
  const [selectedPostIds, setSelectedPostIds] = useState([])
  const [externalLink, setExternalLink] = useState({ label: '', url: '', icon: '' })
  const [adding, setAdding] = useState(false)

  useEffect(() => {
    if (page) {
      setMeta({
        title: page.title || '',
        bio: page.bio || '',
        avatar: page.avatar || '',
        isActive: page.isActive,
      })
    }
  }, [page])

  const saveMeta = async () => {
    try {
      await updateLinkPage({ id, ...meta }).unwrap()
      toast.success('ذخیره شد')
    } catch {
      toast.error('خطا در ذخیره')
    }
  }

  const uploadAvatarHandler = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const fd = new FormData()
    fd.append('image', file)
    try {
      const res = await uploadImage(fd).unwrap()
      setMeta((m) => ({ ...m, avatar: res.image }))
      toast.success('آپلود شد')
    } catch {
      toast.error('خطا در آپلود')
    }
  }

  const toggleProductSelect = (productId) => {
    setSelectedProductIds((prev) =>
      prev.includes(productId) ? prev.filter((x) => x !== productId) : [...prev, productId]
    )
  }

  const togglePostSelect = (postId) => {
    setSelectedPostIds((prev) =>
      prev.includes(postId) ? prev.filter((x) => x !== postId) : [...prev, postId]
    )
  }

  const selectedProducts = allProducts.filter((p) => selectedProductIds.includes(p._id))
  const selectedPosts = (allPosts || []).filter((p) => selectedPostIds.includes(p._id))

  const filteredProducts = search.trim()
    ? allProducts.filter((p) => p.name.includes(search.trim())).slice(0, 15)
    : allProducts.slice(0, 15)

  const filteredPosts = search.trim()
    ? (allPosts || []).filter((p) => p.title.includes(search.trim())).slice(0, 15)
    : (allPosts || []).slice(0, 15)

  const addSelectedProducts = async () => {
    if (selectedProducts.length === 0) {
      toast.error('حداقل یه محصول انتخاب کن')
      return
    }
    setAdding(true)
    try {
      for (const p of selectedProducts) {
        // eslint-disable-next-line no-await-in-loop
        await addLink({ id, label: p.name, url: `/product/${p.slug || p._id}`, icon: '🪴', type: 'product', productId: p._id }).unwrap()
      }
      toast.success(`${selectedProducts.length} لینک محصول اضافه شد`)
      setSelectedProductIds([])
      setSearch('')
      refetch()
    } catch {
      toast.error('خطا در افزودن یکی از لینک‌ها')
    } finally {
      setAdding(false)
    }
  }

  const addSelectedPosts = async () => {
    if (selectedPosts.length === 0) {
      toast.error('حداقل یه پست انتخاب کن')
      return
    }
    setAdding(true)
    try {
      for (const post of selectedPosts) {
        // eslint-disable-next-line no-await-in-loop
        await addLink({ id, label: post.title, url: `/blog/${post._id}`, icon: '📝', type: 'blog' }).unwrap()
      }
      toast.success(`${selectedPosts.length} لینک پست اضافه شد`)
      setSelectedPostIds([])
      setSearch('')
      refetch()
    } catch {
      toast.error('خطا در افزودن یکی از لینک‌ها')
    } finally {
      setAdding(false)
    }
  }

  const addExternalHandler = async (e) => {
    e.preventDefault()
    if (!externalLink.label.trim() || !externalLink.url.trim()) {
      toast.error('برچسب و آدرس الزامی است')
      return
    }
    try {
      await addLink({ id, ...externalLink }).unwrap()
      setExternalLink({ label: '', url: '', icon: '' })
      toast.success('لینک اضافه شد')
      refetch()
    } catch {
      toast.error('خطا در افزودن لینک')
    }
  }

  const toggleLinkActive = async (link) => {
    try {
      await updateLink({ id, linkId: link._id, isActive: !link.isActive }).unwrap()
      refetch()
    } catch {
      toast.error('خطا')
    }
  }

  const deleteLinkHandler = async (linkId) => {
    if (!window.confirm('این لینک حذف شود؟')) return
    try {
      await deleteLink({ id, linkId }).unwrap()
      toast.success('حذف شد')
      refetch()
    } catch {
      toast.error('خطا در حذف')
    }
  }

  const copyShortUrl = (shortCode) => {
    const url = `${window.location.origin}/go/${shortCode}`
    navigator.clipboard.writeText(url)
    toast.success('لینک کوتاه کپی شد')
  }

  if (isLoading) return <Loader />

  return (
    <Container className='py-4'>
      <Button variant='outline-secondary' className='mb-4' onClick={() => navigate('/admin/linkpages')}>
        بازگشت
      </Button>

      <Card className='p-4 mb-4'>
        <h5 className='mb-3'>اطلاعات صفحه — <code>/links/{page?.slug}</code></h5>
        <Form.Group className='mb-3'>
          <Form.Label>آواتار (اختیاری)</Form.Label>
          <Form.Control type='file' accept='image/*' onChange={uploadAvatarHandler} disabled={uploading} />
          {meta.avatar && (
            <img src={meta.avatar} alt='' className='mt-2 rounded-circle' style={{ width: '80px', height: '80px', objectFit: 'cover' }} />
          )}
        </Form.Group>
        <Form.Group className='mb-3'>
          <Form.Label>عنوان</Form.Label>
          <Form.Control value={meta.title} onChange={(e) => setMeta({ ...meta, title: e.target.value })} />
        </Form.Group>
        <Form.Group className='mb-3'>
          <Form.Label>بیو</Form.Label>
          <Form.Control as='textarea' rows={2} value={meta.bio} onChange={(e) => setMeta({ ...meta, bio: e.target.value })} />
        </Form.Group>
        <Form.Check
          type='switch'
          className='mb-3'
          label='صفحه فعال باشد'
          checked={meta.isActive}
          onChange={(e) => setMeta({ ...meta, isActive: e.target.checked })}
        />
        <Button className='btn-aqualotus' size='sm' onClick={saveMeta} disabled={uploading}>
          ذخیره اطلاعات
        </Button>
      </Card>

      <Card className='p-4'>
        <h5 className='mb-3'>لینک‌ها</h5>

        {page?.links?.length > 0 && (
          <ListGroup className='mb-4'>
            {page.links.map((link) => (
              <ListGroup.Item key={link._id} className='d-flex align-items-center gap-2 flex-wrap'>
                <span style={{ fontSize: '1.1rem' }}>{link.icon || '🔗'}</span>
                <div style={{ flex: 1, minWidth: '140px' }}>
                  <div style={{ fontWeight: '600' }}>{link.label}</div>
                  <small className='text-muted'>{link.url}</small>
                </div>
                <Badge bg='secondary'>{link.clicks || 0} کلیک</Badge>
                <Button size='sm' variant='outline-secondary' type='button' onClick={() => copyShortUrl(link.shortCode)}>
                  <FaCopy /> کپی لینک کوتاه
                </Button>
                <Form.Check
                  type='switch'
                  checked={link.isActive}
                  onChange={() => toggleLinkActive(link)}
                  label={link.isActive ? 'فعال' : 'غیرفعال'}
                />
                <Button size='sm' variant='outline-danger' type='button' onClick={() => deleteLinkHandler(link._id)}>
                  <FaTrash />
                </Button>
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}

        <h6 className='mb-2'>+ افزودن لینک جدید</h6>

        <Tabs activeKey={linkMode} onSelect={(k) => { setLinkMode(k); setSearch('') }} className='mb-3'>
          <Tab eventKey='product' title={`🪴 محصول${selectedProducts.length ? ` (${selectedProducts.length})` : ''}`}>
            {selectedProducts.length > 0 && (
              <div className='d-flex flex-wrap gap-2 my-2'>
                {selectedProducts.map((p) => (
                  <Badge key={p._id} bg='success' style={{ cursor: 'pointer' }} onClick={() => toggleProductSelect(p._id)}>
                    {p.name} ✕
                  </Badge>
                ))}
              </div>
            )}
            <Form.Control
              className='mt-2'
              placeholder='جستجوی نام محصول... (یا خالی بگذار برای دیدن همه)'
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <ListGroup className='mt-1' style={{ maxHeight: '240px', overflowY: 'auto' }}>
              {filteredProducts.map((p) => (
                <ListGroup.Item
                  key={p._id}
                  action
                  type='button'
                  active={selectedProductIds.includes(p._id)}
                  onClick={(e) => { e.preventDefault(); toggleProductSelect(p._id) }}
                  className='d-flex align-items-center gap-2'
                >
                  <Form.Check type='checkbox' checked={selectedProductIds.includes(p._id)} onChange={() => {}} />
                  <img src={p.image} alt='' style={{ width: '28px', height: '28px', objectFit: 'cover', borderRadius: '4px' }} />
                  {p.name}
                </ListGroup.Item>
              ))}
              {filteredProducts.length === 0 && (
                <ListGroup.Item className='text-muted text-center'>محصولی پیدا نشد</ListGroup.Item>
              )}
            </ListGroup>
            <Button className='btn-aqualotus mt-3' onClick={addSelectedProducts} disabled={adding || selectedProducts.length === 0}>
              <FaPlus className='ms-1' /> افزودن {selectedProducts.length > 0 ? `${selectedProducts.length} محصول انتخاب‌شده` : 'محصولات انتخاب‌شده'}
            </Button>
          </Tab>

          <Tab eventKey='blog' title={`📝 پست وبلاگ${selectedPosts.length ? ` (${selectedPosts.length})` : ''}`}>
            {selectedPosts.length > 0 && (
              <div className='d-flex flex-wrap gap-2 my-2'>
                {selectedPosts.map((post) => (
                  <Badge key={post._id} bg='success' style={{ cursor: 'pointer' }} onClick={() => togglePostSelect(post._id)}>
                    {post.title} ✕
                  </Badge>
                ))}
              </div>
            )}
            <Form.Control
              className='mt-2'
              placeholder='جستجوی عنوان پست... (یا خالی بگذار برای دیدن همه)'
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <ListGroup className='mt-1' style={{ maxHeight: '240px', overflowY: 'auto' }}>
              {filteredPosts.map((post) => (
                <ListGroup.Item
                  key={post._id}
                  action
                  type='button'
                  active={selectedPostIds.includes(post._id)}
                  onClick={(e) => { e.preventDefault(); togglePostSelect(post._id) }}
                  className='d-flex align-items-center gap-2'
                >
                  <Form.Check type='checkbox' checked={selectedPostIds.includes(post._id)} onChange={() => {}} />
                  {post.title}
                </ListGroup.Item>
              ))}
              {filteredPosts.length === 0 && (
                <ListGroup.Item className='text-muted text-center'>پستی پیدا نشد</ListGroup.Item>
              )}
            </ListGroup>
            <Button className='btn-aqualotus mt-3' onClick={addSelectedPosts} disabled={adding || selectedPosts.length === 0}>
              <FaPlus className='ms-1' /> افزودن {selectedPosts.length > 0 ? `${selectedPosts.length} پست انتخاب‌شده` : 'پست‌های انتخاب‌شده'}
            </Button>
          </Tab>

          <Tab eventKey='external' title='🌐 لینک خارجی'>
            <Form onSubmit={addExternalHandler} className='mt-2'>
              <InputGroup className='mb-2'>
                <Form.Control
                  placeholder='آیکون (اختیاری، مثلاً 📷)'
                  style={{ maxWidth: '120px' }}
                  value={externalLink.icon}
                  onChange={(e) => setExternalLink({ ...externalLink, icon: e.target.value })}
                />
                <Form.Control
                  placeholder='برچسب لینک (مثلاً اینستاگرام ما)'
                  value={externalLink.label}
                  onChange={(e) => setExternalLink({ ...externalLink, label: e.target.value })}
                />
              </InputGroup>
              <InputGroup className='mb-2'>
                <Form.Control
                  placeholder='https://instagram.com/...'
                  value={externalLink.url}
                  onChange={(e) => setExternalLink({ ...externalLink, url: e.target.value })}
                />
                <Button type='submit' className='btn-aqualotus'>
                  <FaPlus className='ms-1' /> افزودن
                </Button>
              </InputGroup>
            </Form>
          </Tab>
        </Tabs>
      </Card>
    </Container>
  )
}

export default LinkPageEditPage
