import { useState } from 'react'
import { Table, Button, Container, Modal, Form, Badge } from 'react-bootstrap'
import { FaEdit, FaTrash, FaPlus } from 'react-icons/fa'
import { toast } from 'react-toastify'
import {
  useGetFamiliesQuery,
  useCreateFamilyMutation,
  useUpdateFamilyMutation,
  useDeleteFamilyMutation,
} from '../../slices/familiesApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const FamilyListPage = () => {
  const [showModal, setShowModal] = useState(false)
  const [editId, setEditId] = useState(null)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [icon, setIcon] = useState('🌿')
  const [category, setCategory] = useState('گیاه زنده')

  const { data: families, isLoading, error, refetch } = useGetFamiliesQuery()
  const [createFamily, { isLoading: loadingCreate }] = useCreateFamilyMutation()
  const [updateFamily, { isLoading: loadingUpdate }] = useUpdateFamilyMutation()
  const [deleteFamily] = useDeleteFamilyMutation()

  const openModal = (family = null) => {
    if (family) {
      setEditId(family._id)
      setName(family.name)
      setDescription(family.description)
      setIcon(family.icon)
      setCategory(family.category)
    } else {
      setEditId(null)
      setName('')
      setDescription('')
      setIcon('🌿')
      setCategory('گیاه زنده')
    }
    setShowModal(true)
  }

  const submitHandler = async (e) => {
    e.preventDefault()
    try {
      if (editId) {
        await updateFamily({ id: editId, name, description, icon, category }).unwrap()
        toast.success('خانواده آپدیت شد')
      } else {
        await createFamily({ name, description, icon, category }).unwrap()
        toast.success('خانواده جدید اضافه شد')
      }
      setShowModal(false)
      refetch()
    } catch (err) {
      toast.error(err?.data?.message || 'خطا')
    }
  }

  const deleteHandler = async (id) => {
    if (window.confirm('آیا از حذف مطمئن هستید؟')) {
      try {
        await deleteFamily(id).unwrap()
        toast.success('خانواده حذف شد')
        refetch()
      } catch (err) {
        toast.error(err?.data?.message || 'خطا در حذف')
      }
    }
  }

  return (
    <Container className='py-4'>
      <div className='d-flex justify-content-between align-items-center mb-4'>
        <h2>مدیریت خانواده‌های گیاهی</h2>
        <Button className='btn-aqualotus' onClick={() => openModal()}>
          <FaPlus className='ms-1' /> خانواده جدید
        </Button>
      </div>

      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <Table striped hover responsive className='admin-table'>
          <thead>
            <tr>
              <th>آیکون</th>
              <th>نام خانواده</th>
              <th>دسته‌بندی</th>
              <th>توضیحات</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {families.map((family) => (
              <tr key={family._id}>
                <td>{family.icon}</td>
                <td><strong>{family.name}</strong></td>
                <td><Badge bg='success'>{family.category}</Badge></td>
                <td>{family.description || '-'}</td>
                <td>
                  <Button
                    size='sm'
                    variant='outline-primary'
                    className='ms-1'
                    onClick={() => openModal(family)}
                  >
                    <FaEdit />
                  </Button>
                  <Button
                    size='sm'
                    variant='outline-danger'
                    onClick={() => deleteHandler(family._id)}
                  >
                    <FaTrash />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      {/* Modal اضافه/ویرایش */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>
            {editId ? 'ویرایش خانواده' : 'خانواده جدید'}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={submitHandler}>
            <Form.Group className='mb-3'>
              <Form.Label>آیکون</Form.Label>
              <Form.Control
                type='text'
                value={icon}
                onChange={(e) => setIcon(e.target.value)}
                placeholder='🌿'
              />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>نام خانواده</Form.Label>
              <Form.Control
                type='text'
                value={name}
                required
                onChange={(e) => setName(e.target.value)}
                placeholder='مثلاً: آنوبیاس'
              />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>دسته‌بندی</Form.Label>
              <Form.Select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                <option value='گیاه زنده'>گیاه زنده</option>
                <option value='کود و مکمل'>کود و مکمل</option>
                <option value='بستر'>بستر</option>
                <option value='لوازم جانبی'>لوازم جانبی</option>
              </Form.Select>
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label>توضیحات</Form.Label>
              <Form.Control
                as='textarea'
                rows={2}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </Form.Group>
            <Button
              type='submit'
              className='w-100 btn-aqualotus'
              disabled={loadingCreate || loadingUpdate}
            >
              {editId ? 'ذخیره تغییرات' : 'اضافه کردن'}
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </Container>
  )
}

export default FamilyListPage