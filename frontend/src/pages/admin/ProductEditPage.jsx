import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Form, Button, Container, Card, Row, Col } from 'react-bootstrap'
import { toast } from 'react-toastify'
import {
  useGetProductDetailsQuery,
  useUpdateProductMutation,
  useUploadProductImageMutation,
} from '../../slices/productsApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const ProductEditPage = () => {
  const { id: productId } = useParams()
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [price, setPrice] = useState(0)
  const [image, setImage] = useState('')
  const [brand, setBrand] = useState('')
  const [category, setCategory] = useState('')
  const [description, setDescription] = useState('')
  const [countInStock, setCountInStock] = useState(0)
  const [discount, setDiscount] = useState(0)
  const [discountMinQty, setDiscountMinQty] = useState(0)
  const [discountQtyPercent, setDiscountQtyPercent] = useState(0)
  const [careLevel, setCareLevel] = useState('آسان')
  const [lightNeeds, setLightNeeds] = useState('متوسط')
  const [co2Needs, setCo2Needs] = useState('اختیاری')
  const [growthRate, setGrowthRate] = useState('متوسط')

  const { data: product, isLoading, error } = useGetProductDetailsQuery(productId)
  const [updateProduct, { isLoading: loadingUpdate }] = useUpdateProductMutation()
  const [uploadImage, { isLoading: loadingUpload }] = useUploadProductImageMutation()

  useEffect(() => {
    if (product) {
      setName(product.name)
      setPrice(product.price)
      setImage(product.image)
      setBrand(product.brand)
      setCategory(product.category)
      setDescription(product.description)
      setCountInStock(product.countInStock)
      setDiscount(product.discount || 0)
      setDiscountMinQty(product.discountMinQty || 0)
      setDiscountQtyPercent(product.discountQtyPercent || 0)
      setCareLevel(product.careLevel || 'آسان')
      setLightNeeds(product.lightNeeds || 'متوسط')
      setCo2Needs(product.co2Needs || 'اختیاری')
      setGrowthRate(product.growthRate || 'متوسط')
    }
  }, [product])

  const uploadImageHandler = async (e) => {
    const formData = new FormData()
    formData.append('image', e.target.files[0])
    try {
      const res = await uploadImage(formData).unwrap()
      toast.success('تصویر آپلود شد')
      setImage(res.image)
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در آپلود تصویر')
    }
  }

  const submitHandler = async (e) => {
    e.preventDefault()
    try {
      await updateProduct({
        productId,
        name, price, image, brand, category,
        description, countInStock, discount,
        discountMinQty, discountQtyPercent,
        careLevel, lightNeeds, co2Needs, growthRate,
      }).unwrap()
      toast.success('محصول آپدیت شد')
      navigate('/admin/productlist')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در آپدیت محصول')
    }
  }

  return (
    <Container className='py-4'>
      <h2 className='mb-4'>ویرایش محصول</h2>

      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <Card className='auth-card'>
          <Card.Body className='p-4'>
            <Form onSubmit={submitHandler}>
              <Row>
                <Col md={6}>
                  <Form.Group className='mb-3'>
                    <Form.Label>نام محصول</Form.Label>
                    <Form.Control value={name} onChange={(e) => setName(e.target.value)} />
                  </Form.Group>

                  <Form.Group className='mb-3'>
                    <Form.Label>قیمت (تومان)</Form.Label>
                    <Form.Control type='number' value={price} onChange={(e) => setPrice(e.target.value)} />
                  </Form.Group>

                  <Form.Group className='mb-3'>
                    <Form.Label>تصویر</Form.Label>
                    <Form.Control value={image} onChange={(e) => setImage(e.target.value)} />
                    <Form.Control type='file' className='mt-1' onChange={uploadImageHandler} />
                    {loadingUpload && <Loader />}
                  </Form.Group>

                  <Form.Group className='mb-3'>
                    <Form.Label>برند / منشأ</Form.Label>
                    <Form.Control value={brand} onChange={(e) => setBrand(e.target.value)} />
                  </Form.Group>

                  <Form.Group className='mb-3'>
                    <Form.Label>دسته‌بندی</Form.Label>
                    <Form.Select value={category} onChange={(e) => setCategory(e.target.value)}>
                      <option value='گیاه زنده'>گیاه زنده</option>
                      <option value='کود و مکمل'>کود و مکمل</option>
                      <option value='بستر'>بستر</option>
                      <option value='لوازم جانبی'>لوازم جانبی</option>
                    </Form.Select>
                  </Form.Group>

                  <Form.Group className='mb-3'>
                    <Form.Label>موجودی</Form.Label>
                    <Form.Control type='number' value={countInStock} onChange={(e) => setCountInStock(e.target.value)} />
                  </Form.Group>

                  <Form.Group className='mb-3'>
                    <Form.Label>توضیحات</Form.Label>
                    <Form.Control as='textarea' rows={4} value={description} onChange={(e) => setDescription(e.target.value)} />
                  </Form.Group>
                </Col>

                <Col md={6}>
                  <h5 className='mb-3'>🏷️ تخفیف</h5>
                  <Form.Group className='mb-3'>
                    <Form.Label>درصد تخفیف مستقیم</Form.Label>
                    <Form.Control type='number' min='0' max='100' value={discount} onChange={(e) => setDiscount(e.target.value)} />
                  </Form.Group>
                  <Form.Group className='mb-3'>
                    <Form.Label>حداقل تعداد برای تخفیف</Form.Label>
                    <Form.Control type='number' min='0' value={discountMinQty} onChange={(e) => setDiscountMinQty(e.target.value)} />
                  </Form.Group>
                  <Form.Group className='mb-3'>
                    <Form.Label>درصد تخفیف تعداد</Form.Label>
                    <Form.Control type='number' min='0' max='100' value={discountQtyPercent} onChange={(e) => setDiscountQtyPercent(e.target.value)} />
                  </Form.Group>

                  <h5 className='mb-3 mt-4'>🌿 مشخصات گیاه</h5>
                  <Form.Group className='mb-3'>
                    <Form.Label>سختی نگهداری</Form.Label>
                    <Form.Select value={careLevel} onChange={(e) => setCareLevel(e.target.value)}>
                      <option value='آسان'>🟢 آسان</option>
                      <option value='متوسط'>🟡 متوسط</option>
                      <option value='سخت'>🔴 سخت</option>
                    </Form.Select>
                  </Form.Group>
                  <Form.Group className='mb-3'>
                    <Form.Label>نیاز نوری</Form.Label>
                    <Form.Select value={lightNeeds} onChange={(e) => setLightNeeds(e.target.value)}>
                      <option value='کم'>کم</option>
                      <option value='متوسط'>متوسط</option>
                      <option value='زیاد'>زیاد</option>
                    </Form.Select>
                  </Form.Group>
                  <Form.Group className='mb-3'>
                    <Form.Label>نیاز CO2</Form.Label>
                    <Form.Select value={co2Needs} onChange={(e) => setCo2Needs(e.target.value)}>
                      <option value='بدون CO2'>بدون CO2</option>
                      <option value='اختیاری'>اختیاری</option>
                      <option value='ضروری'>ضروری</option>
                    </Form.Select>
                  </Form.Group>
                  <Form.Group className='mb-3'>
                    <Form.Label>سرعت رشد</Form.Label>
                    <Form.Select value={growthRate} onChange={(e) => setGrowthRate(e.target.value)}>
                      <option value='کند'>کند</option>
                      <option value='متوسط'>متوسط</option>
                      <option value='سریع'>سریع</option>
                    </Form.Select>
                  </Form.Group>
                </Col>
              </Row>

              <Button
                type='submit'
                className='btn-aqualotus mt-3'
                disabled={loadingUpdate}
              >
                {loadingUpdate ? 'در حال ذخیره...' : 'ذخیره تغییرات'}
              </Button>
            </Form>
          </Card.Body>
        </Card>
      )}
    </Container>
  )
}

export default ProductEditPage