import express from 'express'
import dotenv from 'dotenv'
import cookieParser from 'cookie-parser'
import path from 'path'
import { fileURLToPath } from 'url'
import helmet from 'helmet'
import rateLimit from 'express-rate-limit'
import mongoSanitize from 'express-mongo-sanitize'
import connectDB from './config/db.js'
import { notFound, errorHandler } from './middleware/errorMiddleware.js'
import userRoutes from './routes/userRoutes.js'
import activityLogRoutes from './routes/activityLogRoutes.js'
import productRoutes from './routes/productRoutes.js'
import orderRoutes from './routes/orderRoutes.js'
import uploadRoutes from './routes/uploadRoutes.js'
import familyRoutes from './routes/familyRoutes.js'
import settingsRoutes from './routes/settingsRoutes.js'
import sliderRoutes from './routes/sliderRoutes.js'
import blogRoutes from './routes/blogRoutes.js'
import notificationRoutes from './routes/notificationRoutes.js'
import linkPageRoutes from './routes/linkPageRoutes.js'
import { redirectShortLink } from './controllers/linkPageController.js'
import { generateSitemap } from './controllers/sitemapController.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
dotenv.config({ path: path.join(__dirname, '../.env') })
connectDB()

const app = express()

app.use(
  helmet({
    crossOriginResourcePolicy: { policy: 'cross-origin' },
  })
)

const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 300,
  standardHeaders: true,
  legacyHeaders: false,
  message: { message: 'تعداد درخواست‌های شما زیاد است، کمی بعد دوباره تلاش کنید' },
})

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 20,
  standardHeaders: true,
  legacyHeaders: false,
  message: { message: 'تعداد تلاش‌های ورود/ثبت‌نام زیاد است، ۱۵ دقیقه دیگر تلاش کنید' },
})

app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(cookieParser())
app.use(mongoSanitize())
app.use('/api', generalLimiter)

app.use('/api/users/login', authLimiter)
app.use('/api/users/register', authLimiter)
app.use('/api/users', userRoutes)
app.use('/api/activity-logs', activityLogRoutes)
app.use('/api/products', productRoutes)
app.use('/api/orders', orderRoutes)
app.use('/api/upload', uploadRoutes)
app.use('/api/families', familyRoutes)
app.use('/api/settings', settingsRoutes)
app.use('/api/sliders', sliderRoutes)
app.use('/api/blog', blogRoutes)
app.use('/api/notifications', notificationRoutes)
app.use('/api/linkpages', linkPageRoutes)
app.get('/go/:shortCode', redirectShortLink)
app.get('/sitemap.xml', generateSitemap)

app.use('/uploads', express.static(path.join(__dirname, '../uploads')))
app.use(notFound)
app.use(errorHandler)

const PORT = process.env.PORT || 5000
app.listen(PORT, () => {
  console.log(`سرور روی پورت ${PORT} اجرا شد`)
})
