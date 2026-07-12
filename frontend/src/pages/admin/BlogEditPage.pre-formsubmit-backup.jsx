import { useState, useEffect } from 'react'
import { Container, Form, Button, Card, Badge, ListGroup } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router-dom'
import { toast } from 'react-toastify'
import { useGetPostByIdQuery, useUpdatePostMutation, useCreatePostMutation } from '../../slices/blogApiSlice'
import { useUploadProductImageMutation, useGetProductsQuery } from '../../slices/productsApiSlice'
import { useUploadVideoMutation } from '../../slices/uploadApiSlice'
import Loader from '../../components/ui/Loader'

const BlogEditPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { data: post, isLoading } = useGetPostByIdQuery(id)
  const [updatePost, { isLoading: loadingUpdate }] = useUpdatePostMutation()
  const [uploadImage, { isLoading: loadingImage }] = useUploadProductImageMutation()
  const [uploadVideo, { isLoading: loadingVideo }] = useUploadVideoMutation()
  const { data: allProductsData } = useGetProductsQuery({ admin: true })
  const allProducts = allProductsData?.products || []

  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [image, setImage] = useState('')
  const [video, setVideo] = useState('')
  const [isPublished, setIsPublished] = useState(false)
  const [relatedProducts, setRelatedProducts] = useState([])
  const [productSearch, setProductSearch] = useState('')

  useEffect(() => {
    if (post) {
      setTitle(post.title)
      setContent(post.content)
      setImage(post.image || '')
      setVideo(post.video || '')
      setIsPublished(post.isPublished)
      setRelatedProducts((post.relatedProducts || []).map((p) => (typeof p === 'string' ? p : p._id)))
    }
  }, [post])

  const selectedProducts = allProducts.filter((p) => relatedProducts.includes(p._id))

  const toggleProduct = (productId) => {
    setRelatedProducts((prev) =>
      prev.includes(productId) ? prev.filter((id) => id !== productId) : [...prev, productId]
    )
  }

  const filteredProducts = productSearch.trim()
    ? allProducts.filter((p) => p.name.includes(productSearch.trim())).slice(0, 15)
    : []

  const uploadImageHandler = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const formData = new FormData()
    formData.append('image', file)
    try {
      const res = await uploadImage(formData).unwrap()
      setImage(res.image)
      toast.success('تصویر آپلود شد')
    } catch {
      toast.error('خطا در آپلود تصویر')
    }
  }

  const uploadVideoHandler = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const formData = new FormData()
    formData.append('video', file)
    try {
      const res = await uploadVideo(formData).unwrap()
      setVideo(res.video)
      toast.success('ویدیو آپلود شد')
    } catch {
      toast.error('خطا در آپلود ویدیو')
    }
  }

  const submitHandler = async (e) => {
    e.preventDefault()
    try {
      await updatePost({ id, title, content, image, video, isPublished, relatedProducts }).unwrap()
      toast.success('پست ذخیره شد')
      navigate('/admin/blog')
    } catch {
      toast.error('خطا در ذخیره')
    }
  }

  if (isLoading) return <Loader />

  return (
    <Container className='py-4'>
      <Button variant='outline-secondary' className='mb-4' onClick={() => navigate('/admin/blog')}>
        بازگشت
      </Button>
      <Card className='p-4'>
        <h4 className='mb-4'>ویرایش پست وبلاگ</h4>
        <Form onSubmit={submitHandler}>
          <Form.Group className='mb-3'>
            <Form.Label>عنوان</Form.Label>
            <Form.Control value={title} onChange={(e) => setTitle(e.target.value)} required />
          </Form.Group>

          <Form.Group className='mb-3'>
            <Form.Label>تصویر پست</Form.Label>
            <Form.Control
              type='file'
              accept='image/jpg,image/jpeg,image/png,image/webp'
              onChange={uploadImageHandler}
              disabled={loadingImage}
            />
            {loadingImage && <small className='text-muted'>در حال آپلود تصویر...</small>}
            {image && (
              <div className='mt-2'>
                <img src={image} alt='' className='rounded' style={{ maxHeight: '150px', objectFit: 'cover' }} />
                <Button variant='link' className='text-danger p-0 me-2' onClick={() => setImage('')}>
                  حذف تصویر
                </Button>
              </div>
            )}
          </Form.Group>

          <Form.Group className='mb-3'>
            <Form.Label>ویدیو پست <small className='text-muted'>(mp4, webm, mov, avi - حداکثر ۵۰MB)</small></Form.Label>
            <Form.Control
              type='file'
              accept='video/mp4,video/webm,video/quicktime,video/avi'
              onChange={uploadVideoHandler}
              disabled={loadingVideo}
            />
            {loadingVideo && <small className='text-muted'>در حال آپلود ویدیو...</small>}
            {video && (
              <div className='mt-2'>
                <video controls style={{ maxWidth: '100%', maxHeight: '200px' }}>
                  <source src={video} />
                </video>
                <Button variant='link' className='text-danger p-0 me-2 d-block' onClick={() => setVideo('')}>
                  حذف ویدیو
                </Button>
              </div>
            )}
          </Form.Group>

          <Form.Group className='mb-3'>
            <Form.Label>متن پست</Form.Label>
            <Form.Control
              as='textarea'
              rows={12}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
            />
          </Form.Group>

          <Form.Group className='mb-4'>
            <Form.Label>🛒 محصولات مرتبط (اختیاری)</Form.Label>
            <p className='text-muted' style={{ fontSize: '0.82rem' }}>
              محصولاتی که انتخاب کنی، ته این پست به‌صورت کارت محصول نمایش داده می‌شن.
            </p>

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
                    active={relatedProducts.includes(p._id)}
                    onClick={() => toggleProduct(p._id)}
                    className='d-flex align-items-center gap-2'
                  >
                    <img src={p.image} alt='' style={{ width: '32px', height: '32px', objectFit: 'cover', borderRadius: '4px' }} />
                    <span>{p.name}</span>
                    <small className='text-muted ms-auto'>{p.price?.toLocaleString('fa-IR')} تومان</small>
                  </ListGroup.Item>
                ))}
              </ListGroup>
            )}
          </Form.Group>

          <Form.Group className='mb-4'>
            <Form.Check
              type='checkbox'
              label='منتشر شود'
              checked={isPublished}
              onChange={(e) => setIsPublished(e.target.checked)}
            />
          </Form.Group>

          <Button type='submit' className='btn-aqualotus' disabled={loadingUpdate || loadingImage || loadingVideo}>
            {loadingUpdate ? 'در حال ذخیره...' : 'ذخیره'}
          </Button>
        </Form>
      </Card>
    </Container>
  )
}

export default BlogEditPage
