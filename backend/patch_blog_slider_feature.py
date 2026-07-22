#!/usr/bin/env python3
"""
Feature build: real blog-post-driven slider.
Run this from the project ROOT (the folder containing both `backend/` and
`frontend/`) — it locates each file by relative path from there.

What changes:
- backend/models/blogModel.js: adds `featuredInSlider` boolean field
- backend/controllers/blogController.js: adds `getFeaturedPosts` (public,
  isPublished + featuredInSlider), and `updatePost` now also accepts
  `featuredInSlider`
- backend/routes/blogRoutes.js: adds `GET /api/blog/featured` (before the
  `/:id` catch-all, like `/all` already is)
- frontend/src/slices/blogApiSlice.js: adds `useGetFeaturedPostsQuery`
- frontend/src/components/ui/HeroSlider.jsx: when `location === 'blog'`,
  pulls from featured blog posts instead of the generic Slider collection
  (home behavior is untouched)
- frontend/src/pages/admin/SliderListPage.jsx: full rewrite — the "وبلاگ"
  tab now lists real blog posts with a فعال/غیرفعال toggle
  (`featuredInSlider`) and a "پست جدید" button, instead of the generic
  slide-creation form (which stays for the "صفحه اصلی" tab, unchanged)

Backs up every file before touching it. Safe to inspect diffs via the
`.pre-blogsliderfeature-backup` files afterward.
"""
import shutil
import sys
from pathlib import Path

BACKEND = Path("backend")
FRONTEND = Path("frontend/src")

FILES = {
    "model": BACKEND / "models/blogModel.js",
    "controller": BACKEND / "controllers/blogController.js",
    "routes": BACKEND / "routes/blogRoutes.js",
    "slice": FRONTEND / "slices/blogApiSlice.js",
    "hero": FRONTEND / "components/ui/HeroSlider.jsx",
    "sliderpage": FRONTEND / "pages/admin/SliderListPage.jsx",
}

NEW_SLIDER_PAGE = '''// BLOG_SLIDER_FEATURE_v1
import { useState } from 'react'
import { Container, Table, Button, Form, Modal, Card, Row, Col, Badge, Nav } from 'react-bootstrap'
import { FaEdit, FaTrash, FaPlus, FaEye, FaEyeSlash } from 'react-icons/fa'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import {
  useGetAllSlidersQuery,
  useCreateSliderMutation,
  useUpdateSliderMutation,
  useDeleteSliderMutation,
} from '../../slices/sliderApiSlice'
import { useUploadProductImageMutation } from '../../slices/productsApiSlice'
import {
  useGetAllPostsQuery,
  useCreatePostMutation,
  useUpdatePostMutation,
} from '../../slices/blogApiSlice'
import Loader from '../../components/ui/Loader'

const SliderListPage = () => {
  const navigate = useNavigate()
  const [activeLocation, setActiveLocation] = useState('home')

  // --- اسلایدر صفحه اصلی (بدون تغییر نسبت به قبل) ---
  const { data: sliders, isLoading, refetch } = useGetAllSlidersQuery(activeLocation, { skip: activeLocation !== 'home' })
  const [createSlider] = useCreateSliderMutation()
  const [updateSlider] = useUpdateSliderMutation()
  const [deleteSlider] = useDeleteSliderMutation()
  const [uploadImage, { isLoading: loadingUpload }] = useUploadProductImageMutation()

  const [showModal, setShowModal] = useState(false)
  const [editingSlider, setEditingSlider] = useState(null)
  const [form, setForm] = useState({ title: '', subtitle: '', image: '', link: '/', order: 0, location: 'home' })

  const openCreate = () => {
    setEditingSlider(null)
    setForm({ title: '', subtitle: '', image: '', link: '/', order: sliders?.length || 0, location: activeLocation })
    setShowModal(true)
  }

  const openEdit = (slider) => {
    setEditingSlider(slider)
    setForm({
      title: slider.title || '',
      subtitle: slider.subtitle || '',
      image: slider.image || '',
      link: slider.link || '/',
      order: slider.order || 0,
      location: slider.location || 'home',
    })
    setShowModal(true)
  }

  const uploadHandler = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const formData = new FormData()
    formData.append('image', file)
    try {
      const res = await uploadImage(formData).unwrap()
      setForm((prev) => ({ ...prev, image: res.image }))
      toast.success('تصویر آپلود شد')
    } catch { toast.error('خطا در آپلود') }
  }

  const submitHandler = async () => {
    if (!form.image) { toast.error('تصویر الزامی است'); return }
    try {
      if (editingSlider) {
        await updateSlider({ id: editingSlider._id, ...form }).unwrap()
        toast.success('اسلاید آپدیت شد')
      } else {
        await createSlider(form).unwrap()
        toast.success('اسلاید جدید ساخته شد')
      }
      setShowModal(false)
      refetch()
    } catch { toast.error('خطا در ذخیره') }
  }

  const deleteHandler = async (id) => {
    if (window.confirm('حذف شود؟')) {
      try {
        await deleteSlider(id).unwrap()
        refetch()
        toast.success('اسلاید حذف شد')
      } catch { toast.error('خطا در حذف') }
    }
  }

  const toggleActive = async (slider) => {
    try {
      await updateSlider({ id: slider._id, isActive: !slider.isActive }).unwrap()
      refetch()
      toast.success(slider.isActive ? 'غیرفعال شد' : 'فعال شد')
    } catch { toast.error('خطا') }
  }

  // --- تب وبلاگ: پست‌های واقعی بلاگ با فعال/غیرفعال برای اسلایدر ---
  const { data: posts, isLoading: postsLoading, refetch: refetchPosts } = useGetAllPostsQuery(undefined, { skip: activeLocation !== 'blog' })
  const [createPost, { isLoading: loadingCreatePost }] = useCreatePostMutation()
  const [updatePost] = useUpdatePostMutation()

  const createPostHandler = async () => {
    try {
      const post = await createPost({ title: 'عنوان پست جدید', content: 'محتوای پست...', isPublished: false }).unwrap()
      navigate(`/admin/blog/${post._id}/edit`)
    } catch { toast.error('خطا در ساخت پست') }
  }

  const toggleFeatured = async (post) => {
    try {
      await updatePost({ id: post._id, featuredInSlider: !post.featuredInSlider }).unwrap()
      refetchPosts()
      toast.success(post.featuredInSlider ? 'از اسلایدر وبلاگ برداشته شد' : 'به اسلایدر وبلاگ اضافه شد')
    } catch { toast.error('خطا') }
  }

  return (
    <Container className='py-4'>
      <div className='d-flex justify-content-between align-items-center mb-3'>
        <h2 style={{ fontSize: 'clamp(1rem, 4vw, 1.5rem)' }}>مدیریت اسلایدر</h2>
        {activeLocation === 'home' ? (
          <Button className='btn-aqualotus' size='sm' onClick={openCreate}>
            <FaPlus className='ms-1' /> اسلاید جدید
          </Button>
        ) : (
          <Button className='btn-aqualotus' size='sm' onClick={createPostHandler} disabled={loadingCreatePost}>
            <FaPlus className='ms-1' /> پست جدید
          </Button>
        )}
      </div>

      <Nav variant='tabs' activeKey={activeLocation} onSelect={(k) => setActiveLocation(k)} className='mb-4'>
        <Nav.Item>
          <Nav.Link eventKey='home'>🏠 صفحه اصلی</Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link eventKey='blog'>📝 وبلاگ</Nav.Link>
        </Nav.Item>
      </Nav>

      {activeLocation === 'home' ? (
        isLoading ? <Loader /> : (
          <>
            {/* دسکتاپ */}
            <div className='d-none d-md-block'>
              <Table striped hover responsive>
                <thead>
                  <tr>
                    <th>ترتیب</th>
                    <th>تصویر</th>
                    <th>عنوان</th>
                    <th>لینک</th>
                    <th>وضعیت</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {sliders?.map((slider) => (
                    <tr key={slider._id}>
                      <td>{slider.order}</td>
                      <td>{slider.image && <img src={slider.image} alt='' loading='lazy' style={{ width: '80px', height: '45px', objectFit: 'cover', borderRadius: '4px' }} />}</td>
                      <td>{slider.title || '-'}</td>
                      <td><small>{slider.link}</small></td>
                      <td>
                        <Button size='sm' variant={slider.isActive ? 'success' : 'secondary'} onClick={() => toggleActive(slider)}>
                          {slider.isActive ? <><FaEye className='ms-1' /> فعال</> : <><FaEyeSlash className='ms-1' /> غیرفعال</>}
                        </Button>
                      </td>
                      <td>
                        <Button size='sm' variant='outline-primary' className='ms-1' onClick={() => openEdit(slider)}><FaEdit /></Button>
                        <Button size='sm' variant='outline-danger' onClick={() => deleteHandler(slider._id)}><FaTrash /></Button>
                      </td>
                    </tr>
                  ))}
                  {sliders?.length === 0 && (
                    <tr><td colSpan={6} className='text-center text-muted py-3'>اسلایدی برای این بخش ثبت نشده</td></tr>
                  )}
                </tbody>
              </Table>
            </div>

            {/* موبایل */}
            <div className='d-md-none'>
              <Row className='g-3'>
                {sliders?.map((slider) => (
                  <Col xs={12} key={slider._id}>
                    <Card className='p-3'>
                      {slider.image && (
                        <img src={slider.image} alt='' loading='lazy' className='w-100 rounded mb-2'
                          style={{ height: '120px', objectFit: 'cover' }} />
                      )}
                      <div className='d-flex justify-content-between align-items-start'>
                        <div>
                          <div style={{ fontWeight: '600' }}>{slider.title || 'بدون عنوان'}</div>
                          <small style={{ color: '#666' }}>{slider.link}</small>
                        </div>
                        <Badge bg={slider.isActive ? 'success' : 'secondary'}>
                          {slider.isActive ? 'فعال' : 'غیرفعال'}
                        </Badge>
                      </div>
                      <div className='d-flex gap-2 mt-2'>
                        <Button size='sm' variant={slider.isActive ? 'outline-secondary' :'outline-success'}
                          className='flex-grow-1' onClick={() => toggleActive(slider)}>
                          {slider.isActive ? 'غیرفعال کن' : 'فعال کن'}
                        </Button>
                        <Button size='sm' variant='outline-primary' onClick={() => openEdit(slider)}><FaEdit /></Button>
                        <Button size='sm' variant='outline-danger' onClick={() => deleteHandler(slider._id)}><FaTrash /></Button>
                      </div>
                    </Card>
                  </Col>
                ))}
                {sliders?.length === 0 && (
                  <Col xs={12}><p className='text-center text-muted py-3'>اسلایدی برای اینبخش ثبت نشده</p></Col>
                )}
              </Row>
            </div>
          </>
        )
      ) : (
        postsLoading ? <Loader /> : (
          <>
            {/* دسکتاپ */}
            <div className='d-none d-md-block'>
              <Table striped hover responsive>
                <thead>
                  <tr>
                    <th>تصویر</th>
                    <th>عنوان</th>
                    <th>وضعیت انتشار</th>
                    <th>نمایش در اسلایدر</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {posts?.map((post) => (
                    <tr key={post._id}>
                      <td>{post.image && <img src={post.image} alt='' loading='lazy' style={{ width: '80px', height: '45px', objectFit: 'cover', borderRadius: '4px' }} />}</td>
                      <td>{post.title}</td>
                      <td>{post.isPublished ? <Badge bg='success'>منتشر شده</Badge> : <Badge bg='secondary'>پیش‌نویس</Badge>}</td>
                      <td>
                        <Button size='sm' variant={post.featuredInSlider ? 'success' : 'secondary'} onClick={() => toggleFeatured(post)}>
                          {post.featuredInSlider ? <><FaEye className='ms-1' /> فعال</> : <><FaEyeSlash className='ms-1' /> غیرفعال</>}
                        </Button>
                      </td>
                      <td>
                        <Button size='sm' variant='outline-primary' onClick={() => navigate(`/admin/blog/${post._id}/edit`)}><FaEdit /></Button>
                      </td>
                    </tr>
                  ))}
                  {posts?.length === 0 && (
                    <tr><td colSpan={5} className='text-center text-muted py-3'>پستی برای وبلاگ ثبت نشده</td></tr>
                  )}
                </tbody>
              </Table>
            </div>

            {/* موبایل */}
            <div className='d-md-none'>
              <Row className='g-3'>
                {posts?.map((post) => (
                  <Col xs={12} key={post._id}>
                    <Card className='p-3'>
                      {post.image && (
                        <img src={post.image} alt='' loading='lazy' className='w-100 rounded mb-2'
                          style={{ height: '120px', objectFit: 'cover' }} />
                      )}
                      <div className='d-flex justify-content-between align-items-start'>
                        <div style={{ fontWeight: '600' }}>{post.title}</div>
                        {post.isPublished ? <Badge bg='success'>منتشر</Badge> : <Badge bg='secondary'>پیش‌نویس</Badge>}
                      </div>
                      <div className='d-flex gap-2 mt-2'>
                        <Button size='sm' variant={post.featuredInSlider ? 'outline-secondary' : 'outline-success'}
                          className='flex-grow-1' onClick={() => toggleFeatured(post)}>
                          {post.featuredInSlider ? 'حذف از اسلایدر' : 'افزودن به اسلایدر'}
                        </Button>
                        <Button size='sm' variant='outline-primary' onClick={() => navigate(`/admin/blog/${post._id}/edit`)}><FaEdit /></Button>
                      </div>
                    </Card>
                  </Col>
                ))}
                {posts?.length === 0 && (
                  <Col xs={12}><p className='text-center text-muted py-3'>پستی برای وبلاگ ثبت نشده</p></Col>
                )}
              </Row>
            </div>
          </>
        )
      )}

      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>{editingSlider ? 'ویرایش اسلاید' : 'اسلاید جدید'}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className='mb-3'>
              <Form.Label>محل نمایش</Form.Label>
              <Form.Select value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })}>
                <option value='home'>🏠 صفحه اصلی</option>
                <option value='blog'>📝 وبلاگ</option>
              </Form.Select>
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>عنوان (اختیاری)</Form.Label>
              <Form.Control value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder='عنوان اسلاید' />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>زیرعنوان (اختیاری)</Form.Label>
              <Form.Control value={form.subtitle} onChange={(e) => setForm({ ...form, subtitle: e.target.value })} placeholder='توضیح کوتاه' />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>تصویر <span className='text-danger'>*</span></Form.Label>
              <Form.Control type='file' accept='image/*' onChange={uploadHandler} disabled={loadingUpload} />
              {loadingUpload && <small className='text-muted'>در حال آپلود...</small>}
              {form.image && <img src={form.image} alt='' className='mt-2 w-100 rounded'style={{ maxHeight: '120px', objectFit: 'cover' }} />}
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>لینک</Form.Label>
              <Form.Control value={form.link} onChange={(e) => setForm({ ...form, link: e.target.value })} placeholder='/search/گیاه زنده' />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>ترتیب نمایش</Form.Label>
              <Form.Control type='number' value={form.order} onChange={(e) => setForm({ ...form, order: Number(e.target.value) })} />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className='flex-wrap gap-2'>
          <Button variant='secondary' onClick={() => setShowModal(false)} style={{ minWidth: '90px' }}>انصراف</Button>
          <Button className='btn-aqualotus' onClick={submitHandler} disabled={loadingUpload} style={{ minWidth: '90px' }}>
            {loadingUpload ? 'آپلود...' : 'ذخیره'}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  )
}

export default SliderListPage
'''

results = []


def backup(path: Path):
    bak = path.with_suffix(path.suffix + ".pre-blogsliderfeature-backup")
    shutil.copy2(path, bak)
    return bak


def patch_model():
    p = FILES["model"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد")); return
    content = p.read_text(encoding="utf-8")
    old = "    isPublished: { type: Boolean, default: false },\n    relatedProducts:"
    new = "    isPublished: { type: Boolean, default: false },\n    featuredInSlider: { type: Boolean, default: false },\n    relatedProducts:"
    if content.count(old) != 1:
        results.append((str(p), False, f"لنگر یافت‌شده: {content.count(old)} بار")); return
    backup(p)
    p.write_text(content.replace(old, new), encoding="utf-8")
    results.append((str(p), True, "فیلد featuredInSlider اضافه شد"))


def patch_controller():
    p = FILES["controller"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد")); return
    content = p.read_text(encoding="utf-8")

    old_getposts = (
        "const getPosts = asyncHandler(async (req, res) => {\n"
        "  const posts = await Blog.find({ isPublished: true })\n"
        "    .sort({ createdAt: -1 })\n"
        "    .populate('user', 'name')\n"
        "  res.json(posts)\n"
        "})\n\n"
        "// @desc    دریافت همه پست‌ها برای ادمین"
    )
    new_getposts = (
        "const getPosts = asyncHandler(async (req, res) => {\n"
        "  const posts = await Blog.find({ isPublished: true })\n"
        "    .sort({ createdAt: -1 })\n"
        "    .populate('user', 'name')\n"
        "  res.json(posts)\n"
        "})\n\n"
        "// @desc    دریافت پست‌های فعال‌شده برای اسلایدر وبلاگ\n"
        "// @route   GET /api/blog/featured\n"
        "// @access  Public\n"
        "const getFeaturedPosts = asyncHandler(async (req, res) => {\n"
        "  const posts = await Blog.find({ isPublished: true, featuredInSlider: true })\n"
        "    .sort({ createdAt: -1 })\n"
        "    .populate('user', 'name')\n"
        "  res.json(posts)\n"
        "})\n\n"
        "// @desc    دریافت همه پست‌ها برای ادمین"
    )

    old_update = (
        "    post.isPublished = req.body.isPublished ?? post.isPublished\n"
        "    post.relatedProducts = req.body.relatedProducts ?? post.relatedProducts"
    )
    new_update = (
        "    post.isPublished = req.body.isPublished ?? post.isPublished\n"
        "    post.featuredInSlider = req.body.featuredInSlider ?? post.featuredInSlider\n"
        "    post.relatedProducts = req.body.relatedProducts ?? post.relatedProducts"
    )

    old_export = "export { getPosts, getAllPosts, getPostById, createPost, updatePost, deletePost }"
    new_export = "export { getPosts, getFeaturedPosts, getAllPosts, getPostById, createPost, updatePost, deletePost }"

    checks = [("getPosts block", old_getposts), ("updatePost fields", old_update), ("export", old_export)]
    for label, anchor in checks:
        if content.count(anchor) != 1:
            results.append((str(p), False, f"لنگر «{label}» یافت‌شده: {content.count(anchor)} بار")); return

    backup(p)
    content = content.replace(old_getposts, new_getposts)
    content = content.replace(old_update, new_update)
    content = content.replace(old_export, new_export)
    p.write_text(content, encoding="utf-8")
    results.append((str(p), True, "getFeaturedPosts اضافه شد + updatePost فیلد جدید رو قبول می‌کنه"))


def patch_routes():
    p = FILES["routes"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد")); return
    content = p.read_text(encoding="utf-8")

    old_import = (
        "import {\n"
        "  getPosts,\n"
        "  getAllPosts,\n"
        "  getPostById,\n"
        "  createPost,\n"
        "  updatePost,\n"
        "  deletePost,\n"
        "} from '../controllers/blogController.js'"
    )
    new_import = (
        "import {\n"
        "  getPosts,\n"
        "  getFeaturedPosts,\n"
        "  getAllPosts,\n"
        "  getPostById,\n"
        "  createPost,\n"
        "  updatePost,\n"
        "  deletePost,\n"
        "} from '../controllers/blogController.js'"
    )

    old_route = "router.get('/all', protect, admin, getAllPosts)"
    new_route = "router.get('/featured', getFeaturedPosts)\nrouter.get('/all', protect, admin, getAllPosts)"

    if content.count(old_import) != 1:
        results.append((str(p), False, f"لنگر ایمپورت یافت‌شده: {content.count(old_import)} بار")); return
    if content.count(old_route) != 1:
        results.append((str(p), False, f"لنگر روت یافت‌شده: {content.count(old_route)} بار")); return

    backup(p)
    content = content.replace(old_import, new_import)
    content = content.replace(old_route, new_route)
    p.write_text(content, encoding="utf-8")
    results.append((str(p), True, "روت GET /api/blog/featured اضافه شد"))


def patch_slice():
    p = FILES["slice"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد")); return
    content = p.read_text(encoding="utf-8")

    old_query = (
        "    getPosts: builder.query({\n"
        "      query: () => '/api/blog',\n"
        "      providesTags: ['Blog'],\n"
        "      keepUnusedDataFor: 30,\n"
        "    }),\n"
        "    getAllPosts: builder.query({"
    )
    new_query = (
        "    getPosts: builder.query({\n"
        "      query: () => '/api/blog',\n"
        "      providesTags: ['Blog'],\n"
        "      keepUnusedDataFor: 30,\n"
        "    }),\n"
        "    getFeaturedPosts: builder.query({\n"
        "      query: () => '/api/blog/featured',\n"
        "      providesTags: ['Blog'],\n"
        "      keepUnusedDataFor: 30,\n"
        "    }),\n"
        "    getAllPosts: builder.query({"
    )

    old_export = (
        "export const {\n"
        "  useGetPostsQuery,\n"
        "  useGetAllPostsQuery,"
    )
    new_export = (
        "export const {\n"
        "  useGetPostsQuery,\n"
        "  useGetFeaturedPostsQuery,\n"
        "  useGetAllPostsQuery,"
    )

    if content.count(old_query) != 1:
        results.append((str(p), False, f"لنگر کوئری یافت‌شده: {content.count(old_query)} بار")); return
    if content.count(old_export) != 1:
        results.append((str(p), False, f"لنگر اکسپورت یافت‌شده: {content.count(old_export)} بار")); return

    backup(p)
    content = content.replace(old_query, new_query)
    content = content.replace(old_export, new_export)
    p.write_text(content, encoding="utf-8")
    results.append((str(p), True, "useGetFeaturedPostsQuery اضافه شد"))


def patch_hero():
    p = FILES["hero"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد")); return
    content = p.read_text(encoding="utf-8")

    old_import = "import { useGetSlidersQuery } from '../../slices/sliderApiSlice'"
    new_import = (
        "import { useGetSlidersQuery } from '../../slices/sliderApiSlice'\n"
        "import { useGetFeaturedPostsQuery } from '../../slices/blogApiSlice'"
    )

    old_data = (
        "  const { data: dbSliders } = useGetSlidersQuery(location)\n\n"
        "  const slides = dbSliders && dbSliders.length > 0 ? dbSliders : staticSlides"
    )
    new_data = (
        "  const { data: dbSliders } = useGetSlidersQuery(location, { skip: location === 'blog' })\n"
        "  const { data: featuredPosts } = useGetFeaturedPostsQuery(undefined, { skip: location !== 'blog' })\n\n"
        "  const blogSlides = (featuredPosts || []).map((post) => ({\n"
        "    _id: post._id,\n"
        "    title: post.title,\n"
        "    image: post.image,\n"
        "    link: `/blog/${post._id}`,\n"
        "    buttonText: 'مطالعه مطلب',\n"
        "  }))\n\n"
        "  const slides =\n"
        "    location === 'blog'\n"
        "      ? (blogSlides.length > 0 ? blogSlides : staticSlides)\n"
        "      : (dbSliders && dbSliders.length > 0 ? dbSliders : staticSlides)"
    )

    if content.count(old_import) != 1:
        results.append((str(p), False, f"لنگر ایمپورت یافت‌شده: {content.count(old_import)} بار")); return
    if content.count(old_data) != 1:
        results.append((str(p), False, f"لنگر دیتا یافت‌شده: {content.count(old_data)} بار")); return

    backup(p)
    content = content.replace(old_import, new_import)
    content = content.replace(old_data, new_data)
    p.write_text(content, encoding="utf-8")
    results.append((str(p), True, "location='blog' الان از پست‌های فعال‌شده استفاده می‌کنه، home دست‌نخورده موند"))


def patch_slider_page():
    p = FILES["sliderpage"]
    if not p.exists():
        results.append((str(p), False, "فایل پیدا نشد")); return
    content = p.read_text(encoding="utf-8")

    if "BLOG_SLIDER_FEATURE_v1" in content:
        results.append((str(p), False, "این فایل قبلاً بازسازی شده (مارکر پیدا شد) — دوباره اجرا نشد")); return

    backup(p)
    p.write_text(NEW_SLIDER_PAGE, encoding="utf-8")
    results.append((str(p), True, "کل فایل بازسازی شد — تب وبلاگ الان لیست پست‌های واقعیه"))


def main():
    if not FILES["model"].parent.parent.exists() or not FILES["hero"].parent.parent.parent.exists():
        print("✗ به نظر می‌رسه این اسکریپت از ریشه‌ی پروژه (پوشه‌ای که هم backend هم frontend توشه) اجرا نشده")
        sys.exit(1)

    patch_model()
    patch_controller()
    patch_routes()
    patch_slice()
    patch_hero()
    patch_slider_page()

    print("\n=== گزارش نهایی ===")
    all_ok = True
    for path, ok, msg in results:
        mark = "✓" if ok else "✗"
        print(f"{mark} {path} — {msg}")
        if not ok:
            all_ok = False

    if all_ok:
        print("\n✓ همه چیز موفق")
        print("  ۱) بک‌اند رو کامل ری‌استارت کن")
        print("  ۲) فرانت رو کامل ری‌استارت کن (npm run dev)")
        print("  ۳) پنل ادمین → اسلایدرها → تب «وبلاگ» رو ببین — باید لیست پست‌های بلاگ باشه، نه فرم اسلاید دلخواه")
        print("  ۴) یکی از پست‌ها رو «فعال» کن، برو /blog، رفرش کن — باید بالای صفحه بیاد")
    else:
        print("\n✗ حداقل یکی از پچ‌ها اعمال نشد — فایل‌های موفق قبلی همچنان اعمال شدن، بک‌آپ‌ها رو چک کن")
        sys.exit(1)


if __name__ == "__main__":
    main()
