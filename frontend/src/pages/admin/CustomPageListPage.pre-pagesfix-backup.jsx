import { useState } from 'react'
import { Container, Table, Button, Form, Modal, Card, Row, Col, Badge } from 'react-bootstrap'
import { FaEdit, FaTrash, FaPlus, FaExternalLinkAlt } from 'react-icons/fa'
import { toast } from 'react-toastify'
import { Link } from 'react-router-dom'
import {
  useGetAllCustomPagesQuery,
  useCreateCustomPageMutation,
  useDeleteCustomPageMutation,
} from '../../slices/customPageApiSlice'
import Loader from '../../components/ui/Loader'

const CustomPageListPage = () => {
  const { data: pages, isLoading, refetch } = useGetAllCustomPagesQuery()
  const [createCustomPage] = useCreateCustomPageMutation()
  const [deleteCustomPage] = useDeleteCustomPageMutation()

  const [showModal, setShowModal] = useState(false)
  const [slug, setSlug] = useState('')

  const submitHandler = async () => {
    if (!slug.trim()) { toast.error('اسلاگ الزامی است'); return }
    try {
      const created = await createCustomPage({ slug: slug.trim() }).unwrap()
      toast.success('صفحه ساخته شد')
      setShowModal(false)
      setSlug('')
      refetch()
      window.location.href = `/admin/custompages/${created._id}/edit`
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ساخت صفحه')
    }
  }

  const deleteHandler = async (id) => {
    if (!window.confirm('این صفحه حذف شود؟ (اگه تو اسلایدر اصلی هم بود، اونم حذف می‌شه)')) return
    try {
      await deleteCustomPage(id).unwrap()
      toast.success('صفحه حذف شد')
      refetch()
    } catch {
      toast.error('خطا در حذف')
    }
  }

  return (
    <Container className='py-4'>
      <div className='d-flex justify-content-between align-items-center mb-4'>
        <h2 style={{ fontSize: 'clamp(1rem, 4vw, 1.5rem)' }}>🏗️ صفحه‌ساز</h2>
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
                  <th>عنوان هیرو</th>
                  <th>تو اسلایدر اصلی؟</th>
                  <th>وضعیت</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {pages?.map((page) => (
                  <tr key={page._id}>
                    <td><code>/page/{page.slug}</code></td>
                    <td>{page.heroTitle || '-'}</td>
                    <td>
                      <Badge bg={page.showInHomeSlider ? 'success' : 'secondary'}>
                        {page.showInHomeSlider ? 'بله' : 'خیر'}
                      </Badge>
                    </td>
                    <td>
                      <Badge bg={page.isPublished ? 'success' : 'secondary'}>
                        {page.isPublished ? 'منتشرشده' : 'پیش‌نویس'}
                      </Badge>
                    </td>
                    <td>
                      <a href={`/page/${page.slug}`} target='_blank' rel='noreferrer' className='btn btn-sm btn-outline-secondary ms-1'>
                        <FaExternalLinkAlt />
                      </a>
                      <Link to={`/admin/custompages/${page._id}/edit`} className='btn btn-sm btn-outline-primary ms-1'>
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
                        <div style={{ fontWeight: '600' }}>{page.heroTitle || 'بدون عنوان'}</div>
                        <code style={{ fontSize: '0.8rem' }}>/page/{page.slug}</code>
                      </div>
                      <Badge bg={page.isPublished ? 'success' : 'secondary'}>
                        {page.isPublished ? 'منتشرشده' : 'پیش‌نویس'}
                      </Badge>
                    </div>
                    {page.showInHomeSlider && <Badge bg='info' className='mb-2'>تو اسلایدر اصلی هم هست</Badge>}
                    <div className='d-flex gap-2 mt-2'>
                      <a href={`/page/${page.slug}`} target='_blank' rel='noreferrer' className='btn btn-sm btn-outline-secondary flex-grow-1'>
                        مشاهده
                      </a>
                      <Link to={`/admin/custompages/${page._id}/edit`} className='btn btn-sm btn-outline-primary'>
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
          <Modal.Title>صفحه‌ی سفارشی جدید</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group>
            <Form.Label>اسلاگ (فقط انگلیسی/خط‌تیره)</Form.Label>
            <Form.Control value={slug} onChange={(e) => setSlug(e.target.value.trim())} placeholder='summer-sale' />
            <Form.Text className='text-muted'>آدرس نهایی: /page/{slug || '...'}</Form.Text>
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

export default CustomPageListPage
