#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ساخت فیچر کوییز انتخاب گیاه مناسب (AquaLotus)
از داخل پوشه ~/aqualotus اجرا کن:
    python3 build_quiz_feature.py

این اسکریپت:
- backend/controllers/quizController.js  (جدید)
- backend/routes/quizRoutes.js           (جدید)
- backend/server.js                      (پچ: import + mount)
- frontend/src/slices/quizApiSlice.js    (جدید)
- frontend/src/pages/QuizPage.jsx        (جدید)
- frontend/src/main.jsx                  (پچ: lazy import + route)
- frontend/src/pages/HomePage.jsx        (پچ: بنر کوییز زیر دو اسلایدر)
می‌سازه. قبل از هر تغییر، بک‌آپ با پسوند .pre-<tag>-backup می‌گیره.
"""

import os
import glob
import shutil

OK = "\u2713"
BAD = "\u2717"


def backup(path, tag):
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.pre-{tag}-backup")


def write_file(path, content, tag):
    exists = os.path.exists(path)
    if exists:
        backup(path, tag)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    label = "بازنویسی شد" if exists else "ساخته شد"
    print(f"{OK} {label}: {path}")


def patch_file(path, anchor, insertion, tag):
    if not os.path.exists(path):
        print(f"{BAD} فایل پیدا نشد: {path}")
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if insertion.strip() in content:
        print(f"(رد شد، قبلا اعمال شده) {path}")
        return True
    if anchor not in content:
        print(f"{BAD} anchor پیدا نشد در {path} -- دستی چک کن")
        return False
    backup(path, tag)
    new_content = content.replace(anchor, anchor + insertion, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"{OK} پچ شد: {path}")
    return True


def check_endpoint_collision(name):
    """طبق درس این پروژه: قبل از ساخت اندپوینت جدید تو RTK Query چک کن اسمش تو بقیه اسلایس‌ها نیست."""
    hits = []
    for fp in glob.glob("frontend/src/slices/*ApiSlice.js"):
        with open(fp, "r", encoding="utf-8") as f:
            if name in f.read():
                hits.append(fp)
    if hits:
        print(f"{BAD} هشدار تداخل اسم اندپوینت '{name}' در: {', '.join(hits)} -- قبل از ادامه دستی چک کن")
    else:
        print(f"{OK} اسم اندپوینت '{name}' تو بقیه اسلایس‌ها تکراری نیست")


print("=== شروع ساخت فیچر کوییز ===\n")

check_endpoint_collision("getQuizResults")

# ---------------------------------------------------------------------------
# 1) backend/controllers/quizController.js
# ---------------------------------------------------------------------------
quiz_controller = """import Product from '../models/productModel.js'

// @desc    گرفتن نتیجه کوییز انتخاب گیاه مناسب
// @route   POST /api/quiz/results
// @access  عمومی
const getQuizResults = async (req, res) => {
  try {
    const { careLevel, lightNeeds, co2Needs, position, growthRate, needsSoil } = req.body

    const products = await Product.find({ category: 'گیاه زنده' }).lean()

    const scored = products.map((p) => {
      let score = 0
      if (careLevel && p.careLevel === careLevel) score++
      if (lightNeeds && p.lightNeeds === lightNeeds) score++
      if (co2Needs && p.co2Needs === co2Needs) score++
      if (position && p.position === position) score++
      if (growthRate && p.growthRate === growthRate) score++
      if (typeof needsSoil === 'boolean' && p.needsSoil === needsSoil) score++
      return { ...p, quizScore: score }
    })

    scored.sort((a, b) => b.quizScore - a.quizScore)

    const RESULT_COUNT = 5
    const results = scored.slice(0, RESULT_COUNT)

    res.json({ results })
  } catch (error) {
    res.status(500).json({ message: error.message })
  }
}

export { getQuizResults }
"""
write_file("backend/controllers/quizController.js", quiz_controller, "quiz-controller")

# ---------------------------------------------------------------------------
# 2) backend/routes/quizRoutes.js
# ---------------------------------------------------------------------------
quiz_routes = """import express from 'express'
import { getQuizResults } from '../controllers/quizController.js'

const router = express.Router()

router.post('/results', getQuizResults)

export default router
"""
write_file("backend/routes/quizRoutes.js", quiz_routes, "quiz-routes")

# ---------------------------------------------------------------------------
# 3) backend/server.js -- patch import + mount
# ---------------------------------------------------------------------------
patch_file(
    "backend/server.js",
    "import reportRoutes from './routes/reportRoutes.js'",
    "\nimport quizRoutes from './routes/quizRoutes.js'",
    "quiz-server-import",
)
patch_file(
    "backend/server.js",
    "app.use('/api/reports', reportRoutes)",
    "\napp.use('/api/quiz', quizRoutes)",
    "quiz-server-mount",
)

# ---------------------------------------------------------------------------
# 4) frontend/src/slices/quizApiSlice.js
# ---------------------------------------------------------------------------
quiz_api_slice = """import { apiSlice } from './apiSlice'

const QUIZ_URL = '/api/quiz'

export const quizApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getQuizResults: builder.mutation({
      query: (answers) => ({
        url: `${QUIZ_URL}/results`,
        method: 'POST',
        body: answers,
      }),
    }),
  }),
})

export const { useGetQuizResultsMutation } = quizApiSlice
"""
write_file("frontend/src/slices/quizApiSlice.js", quiz_api_slice, "quiz-apislice")

# ---------------------------------------------------------------------------
# 5) frontend/src/pages/QuizPage.jsx
# ---------------------------------------------------------------------------
quiz_page = """import { useState } from 'react'
import { Container, Row, Col, Button, ProgressBar, Card } from 'react-bootstrap'
import { Helmet } from 'react-helmet-async'
import { Link } from 'react-router-dom'
import { useGetQuizResultsMutation } from '../slices/quizApiSlice'
import ProductCard from '../components/ui/ProductCard'
import Loader from '../components/ui/Loader'
import Message from '../components/ui/Message'

const QUESTIONS = [
  {
    key: 'careLevel',
    title: 'تجربه‌ت تو نگهداری گیاه آکواریوم چقدره؟',
    options: [
      { label: 'تازه‌کارم 🌱', value: 'آسان' },
      { label: 'یه‌کم تجربه دارم', value: 'متوسط' },
      { label: 'حرفه‌ای‌ام 🌳', value: 'سخت' },
    ],
  },
  {
    key: 'lightNeeds',
    title: 'نورت معمولی/شرکتیه یا تخصصی و طیف‌داره؟',
    options: [
      { label: 'معمولی/شرکتی', value: 'متوسط' },
      { label: 'تخصصی/طیف‌دار', value: 'زیاد' },
      { label: 'نمی‌دونم 🤷', value: '' },
    ],
  },
  {
    key: 'co2Needs',
    title: 'برای CO2 چیکار می‌کنی؟',
    options: [
      { label: 'اصلاً ندارم', value: 'بدون CO2' },
      { label: 'گاهی وصل می‌کنم', value: 'اختیاری' },
      { label: 'همیشه دارم', value: 'ضروری' },
    ],
  },
  {
    key: 'position',
    title: 'کجای تانک می‌خوای بشونیش؟',
    options: [
      { label: 'جلو', value: 'جلو' },
      { label: 'میانه', value: 'میانه' },
      { label: 'پشت', value: 'پشت' },
      { label: 'شناور', value: 'شناور' },
    ],
  },
  {
    key: 'growthRate',
    title: 'چقدر عجول تشریف داری؟ 😄',
    options: [
      { label: 'آروم آروم خوبه', value: 'کند' },
      { label: 'یه سرعت معمولی', value: 'متوسط' },
      { label: 'زود می‌خوامش پرپشت!', value: 'سریع' },
    ],
  },
  {
    key: 'needsSoil',
    title: 'بستر آکواریومت خاک مخصوصه یا فقط شن/سنگریزه؟',
    options: [
      { label: 'خاک مخصوص دارم', value: true },
      { label: 'فقط شن/سنگریزه', value: false },
    ],
  },
  {
    key: 'vibe',
    title: 'چه حسی از آکواریومت می‌خوای؟ 🌿',
    options: [
      { label: 'آرامش و سادگی 🧘', value: 'calm' },
      { label: 'رنگارنگی و چشم‌نوازی 🎨', value: 'colorful' },
      { label: 'جنگل انبوه و پرپشت 🌳', value: 'jungle' },
    ],
  },
]

const QuizPage = () => {
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState({})
  const [submitted, setSubmitted] = useState(false)
  const [getQuizResults, { data, isLoading, error }] = useGetQuizResultsMutation()

  const question = QUESTIONS[step]
  const progress = Math.round((step / QUESTIONS.length) * 100)

  const handleAnswer = (value) => {
    const nextAnswers = { ...answers, [question.key]: value }
    setAnswers(nextAnswers)

    if (step + 1 < QUESTIONS.length) {
      setStep(step + 1)
    } else {
      // vibe فقط تزئینیه و تو امتیازدهی سرور استفاده نمی‌شه
      const { vibe, ...scoringAnswers } = nextAnswers
      getQuizResults(scoringAnswers)
      setSubmitted(true)
    }
  }

  const restart = () => {
    setStep(0)
    setAnswers({})
    setSubmitted(false)
  }

  return (
    <Container className='py-4'>
      <Helmet>
        <title>کوییز پیدا کردن گیاه مناسب | AquaLotus</title>
      </Helmet>

      {!submitted ? (
        <Row className='justify-content-center'>
          <Col xs={12} md={8} lg={6}>
            <ProgressBar now={progress} className='mb-4' style={{ height: '8px' }} />
            <Card className='text-center p-4 border-0 shadow-sm rounded-4'>
              <Card.Body>
                <Card.Title as='h4' className='mb-4'>
                  {question.title}
                </Card.Title>
                <div className='d-flex flex-column gap-2'>
                  {question.options.map((opt, i) => (
                    <Button key={i} className='btn-aqualotus py-2' onClick={() => handleAnswer(opt.value)}>
                      {opt.label}
                    </Button>
                  ))}
                </div>
              </Card.Body>
            </Card>
            <p className='text-center text-muted mt-3'>
              سوال {step + 1} از {QUESTIONS.length}
            </p>
          </Col>
        </Row>
      ) : (
        <>
          <h3 className='text-center mb-4'>گیاه‌های پیشنهادی برات 🌿</h3>
          {isLoading ? (
            <Loader />
          ) : error ? (
            <Message variant='danger'>{error?.data?.message || error.error}</Message>
          ) : data?.results?.length === 0 ? (
            <div className='text-center'>
              <p className='text-muted'>چیزی دقیقاً مچ نشد، ولی می‌تونی همه محصولات رو ببینی.</p>
              <Link to='/' className='btn btn-aqualotus px-4'>
                🌿 همه محصولات
              </Link>
            </div>
          ) : (
            <Row className='g-3 justify-content-center'>
              {data?.results?.map((product) => (
                <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                  <ProductCard product={product} />
                </Col>
              ))}
            </Row>
          )}
          <div className='text-center mt-4'>
            <Button variant='outline-secondary' onClick={restart}>
              دوباره از اول
            </Button>
          </div>
        </>
      )}
    </Container>
  )
}

export default QuizPage
"""
write_file("frontend/src/pages/QuizPage.jsx", quiz_page, "quiz-page")

# ---------------------------------------------------------------------------
# 6) frontend/src/main.jsx -- patch lazy import + route
# ---------------------------------------------------------------------------
patch_file(
    "frontend/src/main.jsx",
    "const ContactPage = lazy(() => import('./pages/ContactPage'))",
    "\nconst QuizPage = lazy(() => import('./pages/QuizPage'))",
    "quiz-mainjsx-import",
)
patch_file(
    "frontend/src/main.jsx",
    "{ path: 'contact', element: withSuspense(ContactPage) },",
    "\n      { path: 'quiz', element: withSuspense(QuizPage) },",
    "quiz-mainjsx-route",
)

# ---------------------------------------------------------------------------
# 7) frontend/src/pages/HomePage.jsx -- patch banner under the two sliders
# ---------------------------------------------------------------------------
quiz_banner = """
          <Link to='/quiz' className='d-block text-decoration-none mb-3'>
            <div
              className='d-flex flex-column align-items-center justify-content-center text-center rounded-4 p-4'
              style={{
                background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))',
                minHeight: '180px',
                color: '#fff',
              }}
            >
              <div style={{ fontSize: '2rem' }}>🌿</div>
              <h4 className='mt-2 mb-1' style={{ color: '#fff' }}>
                گیاه مناسب آکواریومت رو پیدا کن!
              </h4>
              <p className='mb-0' style={{ color: '#fff', opacity: 0.9 }}>
                با چند سوال ساده، بهترین گیاه‌ها رو برات پیشنهاد می‌دیم
              </p>
            </div>
          </Link>"""
patch_file(
    "frontend/src/pages/HomePage.jsx",
    "          <BlogHighlightsSlider />",
    quiz_banner,
    "quiz-homepage-banner",
)

print("\n=== تمام شد ===")
print("سرور بک‌اند رو ری‌استارت کن، فرانت رو رفرش کن، برو به /quiz تست کن.")
print("بنر روی صفحه اصلی فعلاً استایل موقته (بدون عکس) -- بعداً عکس رو جایگزین کن.")
