import { useState } from 'react'
import { Card, Button, Form, Row, Col } from 'react-bootstrap'
import { toast } from 'react-toastify'
import {
  useGetMyAddressesQuery,
  useAddAddressMutation,
  useUpdateAddressMutation,
  useDeleteAddressMutation,
} from '../../slices/addressesApiSlice'
import { iranProvinces } from '../../data/iranProvinces'
import Loader from './Loader'
import Message from './Message'

const emptyForm = { title: '', province: '', city: '', address: '', postalCode: '', phone: '' }

const CustomerAddressesList = () => {
  const { data: addresses, isLoading, error } = useGetMyAddressesQuery()
  const [addAddress, { isLoading: adding }] = useAddAddressMutation()
  const [updateAddress, { isLoading: updating }] = useUpdateAddressMutation()
  const [deleteAddress] = useDeleteAddressMutation()

  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [form, setForm] = useState(emptyForm)

  const selectedProvinceData = iranProvinces.find((p) => p.province === form.province)
  const availableCities = selectedProvinceData ? selectedProvinceData.cities : []

  const openAddForm = () => {
    setEditingId(null)
    setForm(emptyForm)
    setShowForm(true)
  }

  const openEditForm = (addr) => {
    setEditingId(addr._id)
    setForm({
      title: addr.title || '',
      province: addr.province || '',
      city: addr.city || '',
      address: addr.address || '',
      postalCode: addr.postalCode || '',
      phone: addr.phone || '',
    })
    setShowForm(true)
  }

  const closeForm = () => {
    setShowForm(false)
    setEditingId(null)
    setForm(emptyForm)
  }

  const handleProvinceChange = (e) => {
    setForm((f) => ({ ...f, province: e.target.value, city: '' }))
  }

  const submitHandler = async (e) => {
    e.preventDefault()
    try {
      if (editingId) {
        await updateAddress({ addressId: editingId, ...form }).unwrap()
        toast.success('آدرس ویرایش شد')
      } else {
        await addAddress(form).unwrap()
        toast.success('آدرس اضافه شد')
      }
      closeForm()
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ذخیره‌ی آدرس')
    }
  }

  const deleteHandler = async (addressId) => {
    if (!window.confirm('این آدرس حذف شود؟')) return
    try {
      await deleteAddress(addressId).unwrap()
      toast.success('آدرس حذف شد')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در حذف آدرس')
    }
  }

  return (
    <Card className='auth-card'>
      <Card.Body className='p-4'>
        <div className='d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2'>
          <h5 className='mb-0'>آدرس‌های من</h5>
          {!showForm && (
            <Button size='sm' className='btn-aqualotus' onClick={openAddForm}>
              + افزودن آدرس جدید
            </Button>
          )}
        </div>

        {showForm && (
          <Form
            onSubmit={submitHandler}
            className='mb-4 p-3'
            style={{ background: 'var(--bg-light, #f0f7f4)', borderRadius: '10px' }}
          >
            <Form.Group className='mb-3'>
              <Form.Label>عنوان آدرس (اختیاری)</Form.Label>
              <Form.Control
                type='text'
                placeholder='مثلاً: خانه، محل کار'
                value={form.title}
                onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
              />
            </Form.Group>
            <Row>
              <Col xs={12} md={6}>
                <Form.Group className='mb-3'>
                  <Form.Label>استان</Form.Label>
                  <Form.Select value={form.province} required onChange={handleProvinceChange}>
                    <option value=''>انتخاب استان</option>
                    {iranProvinces.map((p) => (
                      <option key={p.province} value={p.province}>
                        {p.province}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col xs={12} md={6}>
                <Form.Group className='mb-3'>
                  <Form.Label>شهر</Form.Label>
                  <Form.Select
                    value={form.city}
                    required
                    disabled={!form.province}
                    onChange={(e) => setForm((f) => ({ ...f, city: e.target.value }))}
                  >
                    <option value=''>{form.province ? 'انتخاب شهر' : 'ابتدا استان را انتخاب کنید'}</option>
                    {availableCities.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>
            <Form.Group className='mb-3'>
              <Form.Label>آدرس کامل</Form.Label>
              <Form.Control
                as='textarea'
                rows={2}
                required
                value={form.address}
                onChange={(e) => setForm((f) => ({ ...f, address: e.target.value }))}
              />
            </Form.Group>
            <Row>
              <Col xs={12} md={6}>
                <Form.Group className='mb-3'>
                  <Form.Label>کد پستی</Form.Label>
                  <Form.Control
                    type='text'
                    required
                    pattern='[0-9]{10}'
                    title='کد پستی باید ۱۰ رقم باشد'
                    value={form.postalCode}
                    onChange={(e) => setForm((f) => ({ ...f, postalCode: e.target.value }))}
                  />
                </Form.Group>
              </Col>
              <Col xs={12} md={6}>
                <Form.Group className='mb-3'>
                  <Form.Label>شماره تلفن</Form.Label>
                  <Form.Control
                    type='tel'
                    required
                    pattern='09[0-9]{9}'
                    title='شماره موبایل باید با 09 شروع شود و 11 رقم باشد'
                    value={form.phone}
                    onChange={(e) => setForm((f) => ({ ...f, phone: e.target.value }))}
                  />
                </Form.Group>
              </Col>
            </Row>
            <div className='d-flex gap-2'>
              <Button type='submit' className='btn-aqualotus' disabled={adding || updating}>
                {editingId ? 'ذخیره تغییرات' : 'افزودن آدرس'}
              </Button>
              <Button variant='outline-secondary' type='button' onClick={closeForm}>
                انصراف
              </Button>
            </div>
          </Form>
        )}

        {isLoading ? (
          <Loader />
        ) : error ? (
          <Message variant='danger'>{error?.data?.message}</Message>
        ) : !addresses || addresses.length === 0 ? (
          !showForm && <Message>هنوز آدرسی ذخیره نکرده‌اید</Message>
        ) : (
          addresses.map((addr) => (
            <Card key={addr._id} className='mb-2' style={{ border: '1px solid #eee' }}>
              <Card.Body className='p-3'>
                <div className='d-flex justify-content-between align-items-start flex-wrap gap-2'>
                  <div>
                    {addr.title && <strong className='d-block mb-1'>{addr.title}</strong>}
                    <div style={{ fontSize: '14px' }}>
                      {addr.province}، {addr.city} — {addr.address}
                    </div>
                    <div className='text-muted' style={{ fontSize: '13px' }}>
                      کد پستی: {addr.postalCode} | تلفن: {addr.phone}
                    </div>
                  </div>
                  <div className='d-flex gap-2'>
                    <Button size='sm' variant='outline-success' onClick={() => openEditForm(addr)}>
                      ویرایش
                    </Button>
                    <Button size='sm' variant='outline-danger' onClick={() => deleteHandler(addr._id)}>
                      حذف
                    </Button>
                  </div>
                </div>
              </Card.Body>
            </Card>
          ))
        )}
      </Card.Body>
    </Card>
  )
}

export default CustomerAddressesList
