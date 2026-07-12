import path from 'path'
import fs from 'fs'
import express from 'express'
import multer from 'multer'
import sharp from 'sharp'

const router = express.Router()

// عکس‌ها تو حافظه نگه داشته می‌شن تا با sharp پردازش و به WebP تبدیل بشن
const imageStorage = multer.memoryStorage()

// ویدیوها مستقیم روی دیسک ذخیره می‌شن (بدون پردازش)
const videoStorage = multer.diskStorage({
  destination(req, file, cb) {
    cb(null, 'uploads/')
  },
  filename(req, file, cb) {
    cb(null, `${file.fieldname}-${Date.now()}${path.extname(file.originalname)}`)
  },
})

function checkImageType(file, cb) {
  const imageTypes = /jpg|jpeg|png|webp/
  const ext = path.extname(file.originalname).toLowerCase().replace('.', '')
  const isImage = imageTypes.test(ext) && imageTypes.test(file.mimetype)
  if (isImage) return cb(null, true)
  cb(new Error('فرمت مجاز نیست. عکس: jpg,jpeg,png,webp'))
}

function checkVideoType(file, cb) {
  const videoTypes = /mp4|webm|mov|avi/
  const ext = path.extname(file.originalname).toLowerCase().replace('.', '')
  if (videoTypes.test(ext)) return cb(null, true)
  cb(new Error('فرمت مجاز نیست. ویدیو: mp4,webm,mov,avi'))
}

const uploadImage = multer({
  storage: imageStorage,
  fileFilter: (req, file, cb) => checkImageType(file, cb),
  limits: { fileSize: 50 * 1024 * 1024 }, // 50MB
})

const uploadVideo = multer({
  storage: videoStorage,
  fileFilter: (req, file, cb) => checkVideoType(file, cb),
  limits: { fileSize: 50 * 1024 * 1024 }, // 50MB
})

if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads', { recursive: true })
}

// آپلود عکس — تبدیل خودکار به WebP
router.post('/', uploadImage.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      res.status(400)
      throw new Error('فایلی ارسال نشده')
    }

    const filename = `image-${Date.now()}.webp`
    const filepath = path.join('uploads', filename)

    await sharp(req.file.buffer)
      .resize({ width: 1600, withoutEnlargement: true })
      .webp({ quality: 82 })
      .toFile(filepath)

    res.json({
      message: 'فایل با موفقیت آپلود و به WebP تبدیل شد',
      image: `/${filepath}`,
    })
  } catch (err) {
    res.status(500)
    throw new Error(err.message || 'خطا در پردازش تصویر')
  }
})

// آپلود ویدیو
router.post('/video', uploadVideo.single('video'), (req, res) => {
  res.json({
    message: 'ویدیو با موفقیت آپلود شد',
    video: `/${req.file.path}`,
  })
})

export default router
