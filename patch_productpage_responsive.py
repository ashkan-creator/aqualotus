import os

file_path = os.path.expanduser('~/aqualotus/frontend/src/pages/ProductPage.jsx')
os.makedirs(os.path.dirname(file_path), exist_ok=True)

jsx_code = """import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Card, Button, Badge, Spinner, Alert } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { 
  FaCartPlus, 
  FaHeart, 
  FaRegHeart, 
  FaTruckFast, 
  FaShieldHalved, 
  FaRotateLeft, 
  FaShareNodes,
  FaMinus,
  FaPlus,
  FaStar,
  FaChevronLeft
} from 'react-icons/fa6';
import { toast } from 'react-toastify';

const ProductPage = () => {
  const { id: productId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [qty, setQty] = useState(1);
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const [isWishlisted, setIsWishlisted] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const res = await fetch(`/api/products/${productId}`);
        if (!res.ok) throw new Error('محصول مورد نظر یافت نشد.');
        const data = await res.json();
        setProduct(data);
        setLoading(false);
      } catch (err) {
        setError(err.message || 'خطا در ارتباط با سرور');
        setLoading(false);
      }
    };

    if (productId) fetchProduct();
  }, [productId]);

  const handleQtyChange = (delta) => {
    const newQty = qty + delta;
    if (newQty >= 1 && newQty <= (product?.countInStock || 10)) {
      setQty(newQty);
    }
  };

  const handleAddToCart = () => {
    toast.success(`${qty} عدد ${product?.name || 'محصول'} به سبد خرید افزوده شد`, {
      position: "bottom-right",
      autoClose: 3000,
    });
  };

  const handleToggleWishlist = () => {
    setIsWishlisted(!isWishlisted);
    toast(isWishlisted ? 'از لیست علاقه‌مندی‌ها حذف شد' : 'به لیست علاقه‌مندی‌ها اضافه شد', {
      type: isWishlisted ? 'warning' : 'info',
      position: "bottom-right",
      autoClose: 2000,
    });
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({ title: product?.name, url: window.location.href });
    } else {
      navigator.clipboard.writeText(window.location.href);
      toast.success('لینک صفحه در کلیپ‌بورد کپی شد');
    }
  };

  if (loading) {
    return (
      <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '70vh' }}>
        <Spinner animation="grow" variant="success" />
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="py-5">
        <Alert variant="danger" className="text-center rounded-4 shadow-sm border-0">
          <h5 className="fw-bold mb-3">مشکلی پیش آمد!</h5>
          <p>{error}</p>
          <Button variant="danger" className="px-4 rounded-pill" onClick={() => navigate('/products')}>
            بازگشت به محصولات
          </Button>
        </Alert>
      </Container>
    );
  }

  const images = product?.images?.length > 0 ? product.images : [product?.image || '/placeholder.webp'];

  return (
    <Container className="py-4 py-lg-5 text-end" style={{ direction: 'rtl' }}>
      
      <nav aria-label="breadcrumb" className="mb-4 overflow-x-auto pb-2">
        <div className="d-flex align-items-center gap-2 text-muted small text-nowrap">
          <Link to="/" className="text-decoration-none text-muted">خانه</Link>
          <FaChevronLeft style={{ fontSize: '0.65rem', marginTop: '2px' }} />
          <Link to="/products" className="text-decoration-none text-muted">محصولات</Link>
          <FaChevronLeft style={{ fontSize: '0.65rem', marginTop: '2px' }} />
          <span className="text-dark fw-bold text-truncate" style={{ maxWidth: '200px' }}>
            {product?.name}
          </span>
        </div>
      </nav>

      <Row className="g-4 g-lg-5 mb-5">
        
        <Col xs={12} lg={6}>
          <div className="position-relative rounded-4 overflow-hidden mb-3 border border-light-subtle shadow-sm bg-white d-flex align-items-center justify-content-center" style={{ aspectRatio: '1 / 1', maxHeight: '500px' }}>
            <img
              src={images[selectedImageIndex]}
              alt={product?.name}
              className="w-100 h-100 object-fit-contain p-2 p-md-4"
              style={{ transition: 'opacity 0.3s ease-in-out' }}
            />
            
            <div className="position-absolute top-0 start-0 m-3 d-flex flex-column gap-2 z-2">
              <Button 
                variant="light" 
                className="rounded-circle shadow-sm p-0 d-flex align-items-center justify-content-center border-0"
                onClick={handleToggleWishlist}
                style={{ width: '42px', height: '42px', backgroundColor: 'rgba(255,255,255,0.9)' }}
              >
                {isWishlisted ? <FaHeart className="text-danger fs-5" /> : <FaRegHeart className="text-secondary fs-5" />}
              </Button>
              <Button 
                variant="light" 
                className="rounded-circle shadow-sm p-0 d-flex align-items-center justify-content-center border-0"
                onClick={handleShare}
                style={{ width: '42px', height: '42px', backgroundColor: 'rgba(255,255,255,0.9)' }}
              >
                <FaShareNodes className="text-secondary fs-5" />
              </Button>
            </div>

            {product?.countInStock === 0 && (
              <div className="position-absolute top-0 end-0 m-3 z-2">
                <Badge bg="danger" className="px-3 py-2 fs-6 rounded-pill shadow-sm">ناموجود</Badge>
              </div>
            )}
          </div>

          {images.length > 1 && (
            <div className="d-flex gap-2 overflow-x-auto pb-2 scrollbar-hide" style={{ scrollSnapType: 'x mandatory' }}>
              {images.map((img, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedImageIndex(idx)}
                  className={`btn p-0 border rounded-3 overflow-hidden bg-white ${
                    selectedImageIndex === idx ? 'border-success border-2 shadow-sm' : 'border-light-subtle opacity-75 hover-opacity-100'
                  }`}
                  style={{ width: '80px', height: '80px', flexShrink: 0, scrollSnapAlign: 'start' }}
                >
                  <img src={img} alt={`تصویر ${idx + 1}`} className="w-100 h-100 object-fit-cover" />
                </button>
              ))}
            </div>
          )}
        </Col>

        <Col xs={12} lg={6}>
          <div className="d-flex flex-column h-100">
            <div className="mb-auto">
              {product?.category && (
                <Badge bg="success" bg-opacity="10" className="text-success bg-success-subtle px-3 py-2 rounded-pill fw-normal mb-3">
                  {product.category}
                </Badge>
              )}

              <h1 className="fw-bolder mb-3 fs-4 fs-lg-3 text-dark lh-base">{product?.name}</h1>

              <div className="d-flex flex-wrap align-items-center gap-3 mb-4">
                <div className="d-flex align-items-center gap-1 text-warning bg-light px-2 py-1 rounded-pill">
                  <FaStar className="mb-1" />
                  <span className="fw-bold text-dark pt-1">{product?.rating || '5.0'}</span>
                </div>
                <span className="text-muted small">({product?.numReviews || 0} دیدگاه ثبت شده)</span>
              </div>

              <div className="p-3 p-md-4 bg-light bg-opacity-50 rounded-4 mb-4 border border-light-subtle d-flex flex-column flex-sm-row align-items-sm-center justify-content-between gap-2">
                <span className="text-secondary fw-medium">قیمت نهایی:</span>
                <div className="d-flex align-items-baseline gap-1">
                  <span className="fs-2 fw-black text-success" style={{ fontWeight: 900 }}>
                    {product?.price ? Number(product.price).toLocaleString('fa-IR') : '۰'}
                  </span>
                  <span className="text-muted small fw-bold">تومان</span>
                </div>
              </div>

              <p className="text-secondary lh-lg mb-4 text-justify" style={{ textAlign: 'justify' }}>
                {product?.description || 'توضیحات کوتاه این محصول در حال آماده‌سازی است.'}
              </p>
            </div>

            <div className="mt-4 pt-4 border-top border-light-subtle">
              {product?.countInStock > 0 ? (
                <Row className="g-2 g-sm-3 align-items-center">
                  <Col xs={5} sm={4} md={3} lg={4} xl={3}>
                    <div className="d-flex align-items-center justify-content-between border rounded-pill p-1 bg-white shadow-sm h-100">
                      <Button
                        variant="link"
                        className="text-dark p-2 p-sm-3 border-0 text-decoration-none focus-ring-0"
                        onClick={() => handleQtyChange(-1)}
                        disabled={qty <= 1}
                      >
                        <FaMinus size={14} />
                      </Button>
                      <span className="fw-bold fs-5 px-1">{qty.toLocaleString('fa-IR')}</span>
                      <Button
                        variant="link"
                        className="text-dark p-2 p-sm-3 border-0 text-decoration-none focus-ring-0"
                        onClick={() => handleQtyChange(1)}
                        disabled={qty >= (product?.countInStock || 10)}
                      >
                        <FaPlus size={14} />
                      </Button>
                    </div>
                  </Col>

                  <Col xs={7} sm={8} md={9} lg={8} xl={9}>
                    <Button
                      variant="success"
                      size="lg"
                      className="w-100 rounded-pill py-3 shadow-sm d-flex align-items-center justify-content-center gap-2 fw-bold transition-all hover-shadow"
                      onClick={handleAddToCart}
                    >
                      <FaCartPlus className="fs-5" />
                      <span className="d-none d-sm-inline">افزودن به سبد خرید</span>
                      <span className="d-inline d-sm-none">افزودن به سبد</span>
                    </Button>
                  </Col>
                </Row>
              ) : (
                <Button variant="secondary" size="lg" className="w-100 rounded-pill disabled py-3 text-white opacity-75">
                  متاسفانه موجود نیست
                </Button>
              )}

              <Row className="g-2 g-md-3 mt-4 text-center">
                <Col xs={4}>
                  <div className="p-2 py-3 border border-light-subtle rounded-4 bg-white shadow-sm h-100 d-flex flex-column align-items-center justify-content-center transition-all hover-bg-light">
                    <FaTruckFast className="text-success fs-4 mb-2 opacity-75" />
                    <span className="small text-secondary fw-medium" style={{ fontSize: '0.8rem' }}>ارسال سریع</span>
                  </div>
                </Col>
                <Col xs={4}>
                  <div className="p-2 py-3 border border-light-subtle rounded-4 bg-white shadow-sm h-100 d-flex flex-column align-items-center justify-content-center transition-all hover-bg-light">
                    <FaShieldHalved className="text-success fs-4 mb-2 opacity-75" />
                    <span className="small text-secondary fw-medium" style={{ fontSize: '0.8rem' }}>ضمانت اصالت</span>
                  </div>
                </Col>
                <Col xs={4}>
                  <div className="p-2 py-3 border border-light-subtle rounded-4 bg-white shadow-sm h-100 d-flex flex-column align-items-center justify-content-center transition-all hover-bg-light">
                    <FaRotateLeft className="text-success fs-4 mb-2 opacity-75" />
                    <span className="small text-secondary fw-medium" style={{ fontSize: '0.8rem' }}>۷ روز بازگشت</span>
                  </div>
                </Col>
              </Row>
            </div>
          </div>
        </Col>
      </Row>

      <Card className="border-light-subtle shadow-sm rounded-4 mb-5">
        <Card.Header className="bg-light bg-opacity-50 border-bottom-0 p-3 p-md-4">
          <h5 className="fw-bold mb-0 text-dark fs-5">توضیحات تکمیلی و مشخصات</h5>
        </Card.Header>
        <Card.Body className="p-3 p-md-4 pt-md-2">
          <p className="text-secondary lh-lg mb-0 text-justify" style={{ textAlign: 'justify' }}>
            {product?.fullDescription || product?.description || 'مشخصات کامل این محصول به زودی اضافه خواهد شد.'}
          </p>
        </Card.Body>
      </Card>

    </Container>
  );
};

export default ProductPage;
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(jsx_code)

print("✅ فایل ProductPage.jsx با تنظیمات فوق‌پیشرفته ریسپانسیو و راست‌چین با موفقیت جایگزین شد!")
