import express from 'express'
import dotenv from 'dotenv'
import cookieParser from 'cookie-parser'
import path from 'path'
import { fileURLToPath } from 'url'
import connectDB from './config/db.js'
import { notFound, errorHandler } from './middleware/errorMiddleware.js'
import userRoutes from './routes/userRoutes.js'
import productRoutes from './routes/productRoutes.js'
import orderRoutes from './routes/orderRoutes.js'
import uploadRoutes from './routes/uploadRoutes.js'
import familyRoutes from './routes/familyRoutes.js'
import settingsRoutes from './routes/settingsRoutes.js'
import sliderRoutes from './routes/sliderRoutes.js'
import blogRoutes from './routes/blogRoutes.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
dotenv.config({ path: path.join(__dirname, '../.env') })
connectDB()

const app = express()
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(cookieParser())

app.use('/api/users', userRoutes)
app.use('/api/products', productRoutes)
app.use('/api/orders', orderRoutes)
app.use('/api/upload', uploadRoutes)
app.use('/api/families', familyRoutes)
app.use('/api/settings', settingsRoutes)
app.use('/api/sliders', sliderRoutes)
app.use('/api/blog', blogRoutes)

app.use('/uploads', express.static(path.join(__dirname, '../uploads')))
app.use(notFound)
app.use(errorHandler)

const PORT = process.env.PORT || 5000
app.listen(PORT, () => {
  console.log(`سرور روی پورت ${PORT} اجرا شد`)
})
