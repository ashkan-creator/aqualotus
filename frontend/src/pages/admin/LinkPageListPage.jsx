import { useState } from 'react'
import { Container, Table, Button, Form, Modal, Card, Row, Col, Badge } from 'react-bootstrap'
import { FaEdit, FaTrash, FaPlus, FaExternalLinkAlt } from 'react-icons/fa'
import { toast } from 'react-toastify'
import { Link } from 'react-router-dom'
import {
  useGetAllLinkPagesQuery,
  useCreateLinkPageMutation,
  useDeleteLinkPageMutation,
} from '../../slices/linkPageApiSlice'
import Loader from '../../components/ui/Loader'

const LinkPageListPage = () => {
  const { data: pages, isLoading, refetch } = useGetAllLinkPagesQuery()
  const [createLinkPage] = useCreateLinkPageMutation()
  const [deleteLinkPage] = useDeleteLinkPageMutation()

  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ slug: '', title: '', bio: '' })

  const submitHandler = async () => {
    if (!form.slug.trim()) { toast.error('اسلاگ الزامی است'); return }
    try {
      const created = await createLinkPage(form).unwrap()
      toast.success('صفحه ساخته شد')
      setShowModal(false)
      setForm({ slug: '', title: '', bio: '' })
      refetch()
      window.location.href = `/admin/linkpages/${created._id}/edit`
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ساخت صفحه')
    }
  }

  const deleteHandler = async (id) => {
    if (!window.confirm('این صفحه حذف شود؟')) return
    try {
      await deleteLinkPage(id).unwrap()
      toast.success('صفحه حذف شد')
      refetch()
    } catch {
      toast.error('خطا در حذف')
    }
  }

  return (
    <Container className='py-4'>
      <div className='d-flex justify-content-between align-items-center mb-4'>
        <h2 style={{ fontSize: 'clamp(1rem, 4vw, 1.5rem)' }}>🔗 لینک‌ساز (لینک‌های بایو)</h2>
        <Button className='btn-aqualotus' size='sm' onClick={() => setShowModal(true)}>
          <FaPlus className='ms-1' /> صفحه جدید
        </Button>
      </div>

      {isLoading ? <Loader /> : (
        <>
          <div className='d-none d-md-block'>
            <Table striped hover responsive>
              <thead>
                <tr>
                  <th>اسلاگ</th>
                  <th>عنوان</th>
                  <th>تعداد لینک</th>
                  <th>وضعیت</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {pages?.map((page) => (
                  <tr key={page._id}>
                    <td><code>/links/{page.slug}</code></td>
                    <td>{page.title || '-'}</td>
                    <td>{page.links?.length || 0}</td>
                    <td>
                      <Badge bg={page.isActive ? 'success' : 'secondary'}>
                        {page.isActive ? 'فعال' : 'غیرفعال'}
                      </Badge>
                    </td>
                    <td>
                      <a href={`/links/${page.slug}`} target='_blank' rel='noreferrer' className='btn btn-sm btn-outline-secondary ms-1'>
                        <FaExternalLinkAlt />
                      </a>
                      <Link to={`/admin/linkpages/${page._id}/edit`} className='btn btn-sm btn-outline-primary ms-1'>
                        <FaEdit />
                      </Link>
                      <Button size='sm' variant='outline-danger' onClick={() => deleteHandler(page._id)}>
                        <FaTrash />
                      </Button>
                    </td>
                  </tr>
                ))}
                {pages?.length === 0 && (
                  <tr><td colSpan={5} className='text-center text-muted py-3'>هنوز صفحه‌ای نساختی</td></tr>
                )}
              </tbody>
            </Table>
          </div>

          <div className='d-md-none'>
            <Row className='g-3'>
              {pages?.map((page) => (
                <Col xs={12} key={page._id}>
                  <Card className='p-3'>
                    <div className='d-flex justify-content-between align-items-start mb-2'>
                      <div>
                        <div style={{ fontWeight: '600' }}>{page.title || 'بدون عنوان'}</div>
                        <code style={{ fontSize: '0.8rem' }}>/links/{page.slug}</code>
                      </div>
                      <Badge bg={page.isActive ? 'success' : 'secondary'}>
                        {page.isActive ? 'فعال' : 'غیرفعال'}
                      </Badge>
                    </div>
                    <small className='text-muted mb-2'>{page.links?.length || 0} لینک</small>
                    <div className='d-flex gap-2 mt-2'>
                      <a href={`/links/${page.slug}`} target='_blank' rel='noreferrer' className='btn btn-sm btn-outline-secondary flex-grow-1'>
                        مشاهده
                      </a>
                      <Link to={`/admin/linkpages/${page._id}/edit`} className='btn btn-sm btn-outline-primary'>
                        <FaEdit />
                      </Link>
                      <Button size='sm' variant='outline-danger' onClick={() => deleteHandler(page._id)}>
                        <FaTrash />
                      </Button>
                    </div>
                  </Card>
                </Col>
              ))}
            </Row>
          </div>
        </>
      )}

      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>صفحه‌ی لینک جدید</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group className='mb-3'>
            <Form.Label>اسلاگ (فقط انگلیسی/خط‌تیره، تو آدرس استفاده می‌شه)</Form.Label>
            <Form.Control
              value={form.slug}
              onChange={(e) => setForm({ ...form, slug: e.target.value.trim() })}
              placeholder='main یا spring-sale'
            />
            <Form.Text className='text-muted'>آدرس نهایی: /links/{form.slug || '...'}</Form.Text>
          </Form.Group>
          <Form.Group className='mb-3'>
            <Form.Label>عنوان</Form.Label>
            <Form.Control value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder='AquaLotus 🌿' />
          </Form.Group>
          <Form.Group className='mb-3'>
            <Form.Label>بیو (توضیح کوتاه)</Form.Label>
            <Form.Control as='textarea' rows={2} value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })} />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant='secondary' onClick={() => setShowModal(false)}>انصراف</Button>
          <Button className='btn-aqualotus' onClick={submitHandler}>ساخت و ویرایش</Button>
        </Modal.Footer>
      </Modal>
    </Container>
  )
}

export default LinkPageListPage
