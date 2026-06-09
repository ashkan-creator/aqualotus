import path from 'path'
import express from 'express'
import multer from 'multer'

const router = express.Router()

const storage = multer.diskStorage({
  destination(req, file, cb) {
    cb(null, 'uploads/')
  },
  filename(req, file, cb) {
    cb(null, `${file.fieldname}-${Date.now()}${path.extname(file.originalname)}`)
  },
})

function checkFileType(file, cb) {
  const imageTypes = /jpg|jpeg|png|webp/
  const videoTypes = /mp4|webm|mov|avi/
  const ext = path.extname(file.originalname).toLowerCase().replace('.', '')
  const isImage = imageTypes.test(ext) && imageTypes.test(file.mimetype)
  const isVideo = videoTypes.test(ext)

  if (isImage || isVideo) {
    return cb(null, true)
  } else {
    cb(new Error('فرمت مجاز نیست. عکس: jpg,jpeg,png,webp | ویدیو: mp4,webm,mov,avi'))
  }
}

const upload = multer({
  storage,
  fileFilter: (req, file, cb) => checkFileType(file, cb),
  limits: { fileSize: 50 * 1024 * 1024 }, // 50MB
})

// آپلود عکس
router.post('/', upload.single('image'), (req, res) => {
  res.json({
    message: 'فایل با موفقیت آپلود شد',
    image: `/${req.file.path}`,
  })
})

// آپلود ویدیو
router.post('/video', upload.single('video'), (req, res) => {
  res.json({
    message: 'ویدیو با موفقیت آپلود شد',
    video: `/${req.file.path}`,
  })
})

export default router
