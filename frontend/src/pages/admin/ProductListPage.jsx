import { useNavigate } from 'react-router-dom'
import { Table, Button, Container, Badge } from 'react-bootstrap'
import { FaEdit, FaTrash, FaPlus } from 'react-icons/fa'
import { toast } from 'react-toastify'
import {
  useGetProductsQuery,
  useCreateProductMutation,
  useDeleteProductMutation,
} from '../../slices/productsApiSlice'
import Loader from '../../components/ui/Loader'
import Message from '../../components/ui/Message'

const ProductListPage = () => {
  const navigate = useNavigate()
  const { data, isLoading, error, refetch } = useGetProductsQuery({})
  const [createProduct, { isLoading: loadingCreate }] = useCreateProductMutation()
  const [deleteProduct, { isLoading: loadingDelete }] = useDeleteProductMutation()

  const createProductHandler = async () => {
    if (window.confirm('یک محصول جدید ساخته می‌شود. ادامه می‌دهید؟')) {
      try {
        await createProduct().unwrap()
        refetch()
        toast.success('محصول جدید ساخته شد')
      } catch (err) {
        toast.error(err?.data?.message || 'خطا در ساخت محصول')
      }
    }
  }

  const deleteProductHandler = async (id) => {
    if (window.confirm('آیا از حذف این محصول مطمئن هستید؟')) {
      try {
        await deleteProduct(id).unwrap()
        refetch()
        toast.success('محصول حذف شد')
      } catch (err) {
        toast.error(err?.data?.message || 'خطا در حذف محصول')
      }
    }
  }

  return (
    <Container className='py-4'>
      <div className='d-flex justify-content-between align-items-center mb-4'>
        <h2>مدیریت محصولات</h2>
        <Button className='btn-aqualotus' onClick={createProductHandler}>
          <FaPlus className='ms-1' /> محصول جدید
        </Button>
      </div>

      {loadingCreate && <Loader />}
      {loadingDelete && <Loader />}

      {isLoading ? (
        <Loader />
      ) : error ? (
        <Message variant='danger'>{error?.data?.message}</Message>
      ) : (
        <Table striped hover responsive className='admin-table'>
          <thead>
            <tr>
              <th>شناسه</th>
              <th>نام</th>
              <th>قیمت</th>
              <th>دسته‌بندی</th>
              <th>موجودی</th>
              <th>تخفیف</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {data?.products.map((product) => (
              <tr key={product._id}>
                <td>#{product._id.slice(-6)}</td>
                <td>{product.name}</td>
                <td>{product.price.toLocaleString('fa-IR')} تومان</td>
                <td>{product.category}</td>
                <td>
                  {product.countInStock > 0 ? (
                    <Badge bg='success'>{product.countInStock}</Badge>
                  ) : (
                    <Badge bg='danger'>ناموجود</Badge>
                  )}
                </td>
                <td>
                  {product.discount > 0 ? (
                    <Badge bg='danger'>{product.discount}%</Badge>
                  ) : (
                    '-'
                  )}
                </td>
                <td>
                  <Button
                    size='sm'
                    variant='outline-primary'
                    className='ms-1'
                    onClick={() => navigate(`/admin/product/${product._id}/edit`)}
                  >
                    <FaEdit />
                  </Button>
                  <Button
                    size='sm'
                    variant='outline-danger'
                    onClick={() => deleteProductHandler(product._id)}
                  >
                    <FaTrash />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  )
}

export default ProductListPage