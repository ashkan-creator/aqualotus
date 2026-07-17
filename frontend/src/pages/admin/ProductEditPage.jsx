import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Form, Button, Container, Card, Row, Col, Image, Table, Badge } from 'react-bootstrap'
import { toast } from 'react-toastify'
import { FaTrash, FaPlus } from 'react-icons/fa'
import {
  useGetProductDetailsQuery,
  useUpdateProductMutation,
  useUploadProductImageMutation,
} from '../../slices/productsApiSlice'
import { useUploadVideoMutation } from '../../slices/uploadApiSlice'
import { useGetFamiliesQuery } from '../../slices/familiesApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const ProductEditPage = () => {
  const { id: productId } = useParams()
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [price, setPrice] = useState(0)
  const [image, setImage] = useState('')
  const [images, setImages] = useState([])
  const [video, setVideo] = useState('')
  const [brand, setBrand] = useState('')
  const [category, setCategory] = useState('گیاه زنده')
  const [description, setDescription] = useState('')
  const [countInStock, setCountInStock] = useState(0)
  const [discount, setDiscount] = useState(0)
  const [discountMinQty, setDiscountMinQty] = useState(0)
  const [discountQtyPercent, setDiscountQtyPercent] = useState(0)
  const [careLevel, setCareLevel] = useState('آسان')
  const [lightNeeds, setLightNeeds] = useState('متوسط')
  const [co2Needs, setCo2Needs] = useState('اختیاری')
  const [growthRate, setGrowthRate] = useState('متوسط')
  const [family, setFamily] = useState('')
  const [position, setPosition] = useState('نامشخص')
  const [cultivationType, setCultivationType] = useState('آبزی')
  const [needsSoil, setNeedsSoil] = useState(false)
  const [variants, setVariants] = useState([])
  const [newVariant, setNewVariant] = useState({ size: '', price: '', countInStock: '' })

  const { data: product, isLoading, error } = useGetProductDetailsQuery(productId)
  const [updateProduct, { isLoading: loadingUpdate }] = useUpdateProductMutation()
  const [uploadImage, { isLoading: loadingUpload }] = useUploadProductImageMutation()
  const [uploadVideo, { isLoading: loadingVideo }] = useUploadVideoMutation()
  const { data: families } = useGetFamiliesQuery()

  useEffect(() => {
    if (product) {
      setName(product.name)
      setPrice(product.price)
      setImage(product.image)
      setImages(product.images || [])
      setVideo(product.video || '')
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
      setFamily(product.family || '')
      setPosition(product.position || 'نامشخص')
      setCultivationType(product.cultivationType || 'آبزی')
      setNeedsSoil(product.needsSoil || false)
      setVariants(product.variants || [])
    }
  }, [product])

  const uploadMainImageHandler = async (e) => {
    const formData = new FormData()
    formData.append('image', e.target.files[0])
    try {
      const res = await uploadImage(formData).unwrap()
      setImage(res.image)
      toast.success('تصویر اصلی آپلود شد')
    } catch { toast.error('خطا در آپلود') }
  }

  const uploadExtraImageHandler = async (e) => {
    if (images.length >= 5) { toast.error('حداکثر ۵ تصویر'); return }
    const formData = new FormData()
    formData.append('image', e.target.files[0])
    try {
      const res = await uploadImage(formData).unwrap()
      setImages((prev) => [...prev, res.image])
      toast.success('تصویر اضافه شد')
    } catch { toast.error('خطا در آپلود') }
  }

  const uploadVideoHandler = async (e) => {
    const formData = new FormData()
    formData.append('video', e.target.files[0])
    try {
      const res = await uploadVideo(formData).unwrap()
      setVideo(res.video)
      toast.success('ویدیو آپلود شد')
    } catch { toast.error('خطا در آپلود ویدیو') }
  }

  const addVariantHandler = () => {
    if (!newVariant.size || !newVariant.price) {
      toast.error('سایز و قیمت الزامی است')
      return
    }
    setVariants((prev) => [...prev, {
      size: newVariant.size,
      price: Number(newVariant.price),
      countInStock: Number(newVariant.countInStock) || 0,
    }])
    setNewVariant({ size: '', price: '', countInStock: '' })
  }

  const removeVariantHandler = (idx) => {
    setVariants((prev) => prev.filter((_, i) => i !== idx))
  }

  const submitHandler = async (e) => {
    e.preventDefault()
    try {
      await updateProduct({
        productId, name, price, image, images, video,
        brand, category, description, countInStock,
        discount, discountMinQty, discountQtyPercent,
        careLevel, lightNeeds, co2Needs, growthRate,
        family, position, cultivationType, needsSoil,
        variants,
      }).unwrap()
      toast.success('محصول آپدیت شد')
      navigate('/admin/productlist')
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در آپدیت')
    }
  }

  return (
    <Container className='py-4'>
      <div className='d-flex justify-content-between align-items-center mb-4'>
        <h2>ویرایش محصول</h2>
        <Button variant='outline-secondary' onClick={() => navigate('/admin/productlist')}>بازگشت</Button>
      </div>

      {isLoading ? <Loader /> : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <Form onSubmit={submitHandler}>
          <Row className='g-4'>
            <Col md={6}>
              <Card className='p-3 mb-3'>
                <h5 className='mb-3'>📦 اطلاعات اصلی</h5>
                <Form.Group className='mb-3'>
                  <Form.Label>نام محصول</Form.Label>
                  <Form.Control value={name} onChange={(e) => setName(e.target.value)} required />
                </Form.Group>
                <Form.Group className='mb-3'>
                  <Form.Label>
                    قیمت پایه (تومان)
                    {variants.length > 0 && <small className='text-muted me-2'>(اگر سایز دارد، قیمت پایه برای نمایش در لیست)</small>}
                  </Form.Label>
                  <Form.Control type='number' value={price} onChange={(e) => setPrice(e.target.value)} required />
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
                    <option value='سنگ'>سنگ</option>
                    <option value='چوب'>چوب</option>
                  </Form.Select>
                </Form.Group>
                <Form.Group className='mb-3'>
                  <Form.Label>
                    موجودی کل
                    {variants.length > 0 && <small className='text-muted me-2'>(موجودی هر سایز جداگانه تعریف شده)</small>}
                  </Form.Label>
                  <Form.Control type='number' value={countInStock} onChange={(e) => setCountInStock(e.target.value)} />
                </Form.Group>
                <Form.Group className='mb-3'>
                  <Form.Label>توضیحات</Form.Label>
                  <Form.Control as='textarea' rows={4} value={description} onChange={(e) => setDescription(e.target.value)} />
                </Form.Group>
              </Card>

              {/* سایزبندی */}
              <Card className='p-3 mb-3'>
                <h5 className='mb-3'>📐 سایزبندی و قیمت‌گذاری</h5>
                <small className='text-muted d-block mb-3'>
                  اگر محصول سایزهای مختلف دارد اینجا تعریف کنید. در غیر اینصورت خالی بگذارید.
                </small>

                {variants.length > 0 && (
                  <Table size='sm' bordered className='mb-3'>
                    <thead>
                      <tr>
                        <th>سایز</th>
                        <th>قیمت (تومان)</th>
                        <th>موجودی</th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      {variants.map((v, idx) => (
                        <tr key={idx}>
                          <td><Badge bg='success'>{v.size}</Badge></td>
                          <td>{Number(v.price).toLocaleString('fa-IR')}</td>
                          <td>{v.countInStock}</td>
                          <td>
                            <Button size='sm' variant='outline-danger' onClick={() => removeVariantHandler(idx)}>
                              <FaTrash size={10} />
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                )}

                <Row className='g-2 align-items-end'>
                  <Col xs={4}>
                    <Form.Label>سایز</Form.Label>
                    <Form.Control
                      size='sm'
                      placeholder='مثلاً: کوچک'
                      value={newVariant.size}
                      onChange={(e) => setNewVariant({ ...newVariant, size: e.target.value })}
                    />
                  </Col>
                  <Col xs={4}>
                    <Form.Label>قیمت</Form.Label>
                    <Form.Control
                      size='sm'
                      type='number'
                      placeholder='تومان'
                      value={newVariant.price}
                      onChange={(e) => setNewVariant({ ...newVariant, price: e.target.value })}
                    />
                  </Col>
                  <Col xs={3}>
                    <Form.Label>موجودی</Form.Label>
                    <Form.Control
                      size='sm'
                      type='number'
                      placeholder='تعداد'
                      value={newVariant.countInStock}
                      onChange={(e) => setNewVariant({ ...newVariant, countInStock: e.target.value })}
                    />
                  </Col>
                  <Col xs={1}>
                    <Button size='sm' className='btn-aqualotus' onClick={addVariantHandler}>
                      <FaPlus />
                    </Button>
                  </Col>
                </Row>
              </Card>

              <Card className='p-3'>
                <h5 className='mb-3'>🏷️ تخفیف</h5>
                <Form.Group className='mb-3'>
                  <Form.Label>درصد تخفیف مستقیم (%)</Form.Label>
                  <Form.Control type='number' min='0' max='100' value={discount} onChange={(e) => setDiscount(e.target.value)} />
                </Form.Group>
                <Form.Group className='mb-3'>
                  <Form.Label>حداقل تعداد برای تخفیف</Form.Label>
                  <Form.Control type='number' min='0' value={discountMinQty} onChange={(e) => setDiscountMinQty(e.target.value)} />
                </Form.Group>
                <Form.Group className='mb-3'>
                  <Form.Label>درصد تخفیف تعداد (%)</Form.Label>
                  <Form.Control type='number' min='0' max='100' value={discountQtyPercent} onChange={(e) => setDiscountQtyPercent(e.target.value)} />
                </Form.Group>
              </Card>
            </Col>

            <Col md={6}>
              <Card className='p-3 mb-3'>
                <h5 className='mb-3'>🖼️ تصویر اصلی</h5>
                {image && (
                  <Image src={image} fluid rounded className='mb-2' style={{ maxHeight: '200px', objectFit: 'cover' }} />
                )}
                <Form.Control type='file' accept='image/*' onChange={uploadMainImageHandler} disabled={loadingUpload} />
                {loadingUpload && <small className='text-muted'>در حال آپلود...</small>}
              </Card>

              <Card className='p-3 mb-3'>
                <h5 className='mb-3'>🖼️ تصاویر اضافه <small className='text-muted'>({images.length}/5)</small></h5>
                <div className='d-flex flex-wrap gap-2 mb-2'>
                  {images.map((img, idx) => (
                    <div key={idx} style={{ position: 'relative' }}>
                      <Image src={img} style={{ width: '80px', height: '80px', objectFit: 'cover', borderRadius: '8px' }} />
                      <Button
                        size='sm' variant='danger'
                        style={{ position: 'absolute', top: '-8px', left: '-8px', borderRadius: '50%', padding: '0 5px' }}
                        onClick={() => setImages((prev) => prev.filter((_, i) => i !== idx))}
                      >
                        <FaTrash size={10} />
                      </Button>
                    </div>
                  ))}
                </div>
                {images.length < 5 && (
                  <Form.Control type='file' accept='image/*' onChange={uploadExtraImageHandler} disabled={loadingUpload} />
                )}
              </Card>

              <Card className='p-3 mb-3'>
                <h5 className='mb-3'>🎥 ویدیو محصول</h5>
                {video && (
                  <div className='mb-2'>
                    <video controls style={{ width: '100%', maxHeight: '150px', borderRadius: '8px' }}>
                      <source src={video} />
                    </video>
                    <Button variant='link' className='text-danger p-0' onClick={() => setVideo('')}>حذف ویدیو</Button>
                  </div>
                )}
                <Form.Control type='file' accept='video/mp4,video/webm,video/quicktime,video/avi' onChange={uploadVideoHandler} disabled={loadingVideo} />
                {loadingVideo && <small className='text-muted'>در حال آپلود ویدیو...</small>}
              </Card>

              <Card className='p-3'>
                <h5 className='mb-3'>🌿 مشخصات گیاه</h5>
                <Form.Group className='mb-3'>
                  <Form.Label>خانواده گیاهی</Form.Label>
                  <Form.Select value={family} onChange={(e) => setFamily(e.target.value)}>
                    <option value=''>-- انتخاب خانواده --</option>
                    {families?.map((f) => (
                      <option key={f._id} value={f.name}>{f.name}</option>
                    ))}
                  </Form.Select>
                </Form.Group>
                <Form.Group className='mb-3'>
                  <Form.Label>محل کاشت</Form.Label>
                  <Form.Select value={position} onChange={(e) => setPosition(e.target.value)}>
                    <option value='جلو'>جلو</option>
                    <option value='میانه'>میانه</option>
                    <option value='پشت'>پشت</option>
                    <option value='شناور'>شناور</option>
                    <option value='نامشخص'>نامشخص</option>
                  </Form.Select>
                </Form.Group>
                <Form.Group className='mb-3'>
                  <Form.Label>نوع کشت</Form.Label>
                  <Form.Select value={cultivationType} onChange={(e) => setCultivationType(e.target.value)}>
                    <option value='آبزی'>آبزی</option>
                    <option value='هیدروپونیک'>هیدروپونیک</option>
                    <option value='هر دو'>هر دو</option>
                  </Form.Select>
                </Form.Group>
                <Form.Group className='mb-3'>
                  <Form.Check type='checkbox' label='نیاز به بستر دارد' checked={needsSoil} onChange={(e) => setNeedsSoil(e.target.checked)} />
                </Form.Group>
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
                    <option value='اختیاری'>غیر ضروری ولی تاثیر گذار در رشد و کیفیت</option>
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
              </Card>
            </Col>
          </Row>

          <Button type='submit' className='btn-aqualotus mt-4 w-100' disabled={loadingUpdate}>
            {loadingUpdate ? 'در حال ذخیره...' : '✅ ذخیره تغییرات'}
          </Button>
        </Form>
      )}
    </Container>
  )
}

export default ProductEditPage
