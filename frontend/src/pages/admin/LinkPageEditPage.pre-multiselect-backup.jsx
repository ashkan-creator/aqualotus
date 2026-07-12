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
  const [newLink, setNewLink] = useState({ label: '', url: '', icon: '' })
  const [linkMode, setLinkMode] = useState('product')
  const [search, setSearch] = useState('')

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

  const pickProduct = (p) => {
    setNewLink({ ...newLink, label: p.name, url: `/product/${p.slug || p._id}` })
    setSearch('')
  }

  const pickPost = (post) => {
    setNewLink({ ...newLink, label: post.title, url: `/blog/${post._id}` })
    setSearch('')
  }

  const filteredProducts = search.trim() && linkMode === 'product'
    ? allProducts.filter((p) => p.name.includes(search.trim())).slice(0, 10)
    : []

  const filteredPosts = search.trim() && linkMode === 'blog'
    ? (allPosts || []).filter((p) => p.title.includes(search.trim())).slice(0, 10)
    : []

  const addLinkHandler = async (e) => {
    e.preventDefault()
    if (!newLink.label.trim() || !newLink.url.trim()) {
      toast.error('برچسب و آدرس الزامی است — از جستجو بالا انتخاب کن یا دستی تایپ کن')
      return
    }
    try {
      await addLink({ id, ...newLink }).unwrap()
      setNewLink({ label: '', url: '', icon: '' })
      setSearch('')
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
    const url = `${window.location.origin}/l/${shortCode}`
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

        <Tabs activeKey={linkMode} onSelect={(k) => { setLinkMode(k); setSearch(''); setNewLink({ label: '', url: '', icon: '' }) }} className='mb-3'>
          <Tab eventKey='product' title='🪴 محصول'>
            <Form.Control
              className='mt-2'
              placeholder='جستجوی نام محصول...'
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            {filteredProducts.length > 0 && (
              <ListGroup className='mt-1' style={{ maxHeight: '200px', overflowY: 'auto' }}>
                {filteredProducts.map((p) => (
                  <ListGroup.Item key={p._id} action type='button' onClick={(e) => { e.preventDefault(); pickProduct(p) }} className='d-flex align-items-center gap-2'>
                    <img src={p.image} alt='' style={{ width: '28px', height: '28px', objectFit: 'cover', borderRadius: '4px' }} />
                    {p.name}
                  </ListGroup.Item>
                ))}
              </ListGroup>
            )}
          </Tab>
          <Tab eventKey='blog' title='📝 پست وبلاگ'>
            <Form.Control
              className='mt-2'
              placeholder='جستجوی عنوان پست...'
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            {filteredPosts.length > 0 && (
              <ListGroup className='mt-1' style={{ maxHeight: '200px', overflowY: 'auto' }}>
                {filteredPosts.map((post) => (
                  <ListGroup.Item key={post._id} action type='button' onClick={(e) => { e.preventDefault(); pickPost(post) }}>
                    {post.title}
                  </ListGroup.Item>
                ))}
              </ListGroup>
            )}
          </Tab>
          <Tab eventKey='external' title='🌐 لینک خارجی'>
            <Form.Control
              className='mt-2'
              placeholder='https://instagram.com/...'
              value={linkMode === 'external' ? newLink.url : ''}
              onChange={(e) => setNewLink({ ...newLink, url: e.target.value })}
            />
          </Tab>
        </Tabs>

        {newLink.url && (
          <div className='mb-2 p-2' style={{ background: '#f0f7f3', borderRadius: '8px', fontSize: '0.85rem' }}>
            انتخاب‌شده: <strong>{newLink.label || '(بدون برچسب)'}</strong> → <code>{newLink.url}</code>
          </div>
        )}

        <Form onSubmit={addLinkHandler}>
          <InputGroup className='mb-2'>
            <Form.Control
              placeholder='آیکون (اختیاری، مثلاً 🌿)'
              style={{ maxWidth: '120px' }}
              value={newLink.icon}
              onChange={(e) => setNewLink({ ...newLink, icon: e.target.value })}
            />
            <Form.Control
              placeholder='برچسب لینک (اسم دکمه)'
              value={newLink.label}
              onChange={(e) => setNewLink({ ...newLink, label: e.target.value })}
            />
            <Button type='submit' className='btn-aqualotus'>
              <FaPlus className='ms-1' /> افزودن
            </Button>
          </InputGroup>
        </Form>
      </Card>
    </Container>
  )
}

export default LinkPageEditPage
