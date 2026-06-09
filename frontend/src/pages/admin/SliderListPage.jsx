import { useState } from 'react'
import { Container, Table, Button, Form, Modal } from 'react-bootstrap'
import { FaEdit, FaTrash, FaPlus, FaEye, FaEyeSlash, FaUpload } from 'react-icons/fa'
import { toast } from 'react-toastify'
import {
  useGetAllSlidersQuery,
  useCreateSliderMutation,
  useUpdateSliderMutation,
  useDeleteSliderMutation,
} from '../../slices/sliderApiSlice'
import { useUploadProductImageMutation } from '../../slices/productsApiSlice'
import Loader from '../../components/ui/Loader'

const SliderListPage = () => {
  const { data: sliders, isLoading, refetch } = useGetAllSlidersQuery()
  const [createSlider] = useCreateSliderMutation()
  const [updateSlider] = useUpdateSliderMutation()
  const [deleteSlider] = useDeleteSliderMutation()
  const [uploadImage, { isLoading: loadingUpload }] = useUploadProductImageMutation()

  const [showModal, setShowModal] = useState(false)
  const [editingSlider, setEditingSlider] = useState(null)
  const [form, setForm] = useState({ title: '', subtitle: '', image: '', link: '/', order: 0 })

  const openCreate = () => {
    setEditingSlider(null)
    setForm({ title: '', subtitle: '', image: '', link: '/', order: sliders?.length || 0 })
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
    } catch {
      toast.error('خطا در آپلود تصویر')
    }
  }

  const submitHandler = async () => {
    if (!form.image) {
      toast.error('تصویر الزامی است')
      return
    }
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
    } catch {
      toast.error('خطا در ذخیره')
    }
  }

  const deleteHandler = async (id) => {
    if (window.confirm('حذف شود؟')) {
      try {
        await deleteSlider(id).unwrap()
        refetch()
        toast.success('اسلاید حذف شد')
      } catch {
        toast.error('خطا در حذف')
      }
    }
  }

  const toggleActive = async (slider) => {
    try {
      await updateSlider({ id: slider._id, isActive: !slider.isActive }).unwrap()
      refetch()
      toast.success(slider.isActive ? 'غیرفعال شد' : 'فعال شد')
    } catch {
      toast.error('خطا')
    }
  }

  return (
    <Container className='py-4'>
      <div className='d-flex justify-content-between align-items-center mb-4'>
        <h2>مدیریت اسلایدر</h2>
        <Button className='btn-aqualotus' onClick={openCreate}>
          <FaPlus className='ms-1' /> اسلاید جدید
        </Button>
      </div>

      {isLoading ? <Loader /> : (
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
                <td>
                  {slider.image && (
                    <img src={slider.image} alt='' style={{ width: '80px', height: '45px', objectFit: 'cover', borderRadius: '4px' }} />
                  )}
                </td>
                <td>{slider.title || '-'}</td>
                <td><small>{slider.link}</small></td>
                <td>
                  <Button size='sm' variant={slider.isActive ? 'success' : 'secondary'} onClick={() => toggleActive(slider)}>
                    {slider.isActive ? <><FaEye className='ms-1' /> فعال</> : <><FaEyeSlash className='ms-1' /> غیرفعال</>}
                  </Button>
                </td>
                <td>
                  <Button size='sm' variant='outline-primary' className='ms-1' onClick={() => openEdit(slider)}>
                    <FaEdit />
                  </Button>
                  <Button size='sm' variant='outline-danger' onClick={() => deleteHandler(slider._id)}>
                    <FaTrash />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>{editingSlider ? 'ویرایش اسلاید' : 'اسلاید جدید'}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className='mb-3'>
              <Form.Label>عنوان (اختیاری)</Form.Label>
              <Form.Control
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                placeholder='عنوان اسلاید'
              />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>زیرعنوان (اختیاری)</Form.Label>
              <Form.Control
                value={form.subtitle}
                onChange={(e) => setForm({ ...form, subtitle: e.target.value })}
                placeholder='توضیح کوتاه'
              />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>تصویر <span className='text-danger'>*</span></Form.Label>
              <div className='d-flex gap-2 align-items-center'>
                <Form.Control
                  type='file'
                  accept='image/*'
                  onChange={uploadHandler}
                  disabled={loadingUpload}
                />
                {loadingUpload && <span>در حال آپلود...</span>}
              </div>
              {form.image && (
                <img src={form.image} alt='' className='mt-2 w-100 rounded' style={{ maxHeight: '150px', objectFit: 'cover' }} />
              )}
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>لینک (کاربر کجا بره؟)</Form.Label>
              <Form.Control
                value={form.link}
                onChange={(e) => setForm({ ...form, link: e.target.value })}
                placeholder='مثلاً: /search/گیاه زنده یا /product/123'
              />
              <Form.Text className='text-muted'>
                مثال‌ها: /search/آسان | /product/ID | /
              </Form.Text>
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>ترتیب نمایش</Form.Label>
              <Form.Control
                type='number'
                value={form.order}
                onChange={(e) => setForm({ ...form, order: Number(e.target.value) })}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant='secondary' onClick={() => setShowModal(false)}>انصراف</Button>
          <Button className='btn-aqualotus' onClick={submitHandler} disabled={loadingUpload}>
            {loadingUpload ? 'در حال آپلود...' : 'ذخیره'}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  )
}

export default SliderListPage
