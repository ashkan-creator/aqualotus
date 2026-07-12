/**
 * backfillSlugs.js
 * -------------------
 * اسکریپت یک‌باره: به محصولاتی که از قبل تو دیتابیس هستن و اسلاگ ندارن،
 * یه اسلاگ یکتا (بر اساس نام فارسی‌شون) اختصاص می‌ده.
 *
 * اجرا:
 *   cd ~/aqualotus/backend
 *   node backfillSlugs.js
 */
import dotenv from 'dotenv'
import path from 'path'
import { fileURLToPath } from 'url'
import mongoose from 'mongoose'
import Product from './models/productModel.js'
import { generateUniqueSlug } from './utils/slugify.js'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
dotenv.config({ path: path.resolve(__dirname, '../.env') })

const run = async () => {
  console.log('در حال اتصال به MongoDB...')
  await mongoose.connect(process.env.MONGO_URI)
  console.log('وصل شد.')

  const products = await Product.find({
    $or: [{ slug: { $exists: false } }, { slug: null }, { slug: '' }],
  })

  console.log(`${products.length} محصول بدون اسلاگ پیدا شد.`)

  let count = 0
  for (const product of products) {
    product.slug = await generateUniqueSlug(Product, product.name, product._id)
    await product.save()
    count += 1
    console.log(`✓ [${count}/${products.length}] ${product.name} -> ${product.slug}`)
  }

  console.log(`\nتمام شد. ${count} محصول به‌روزرسانی شد.`)
  await mongoose.disconnect()
  process.exit(0)
}

run().catch((err) => {
  console.error('خطا:', err)
  process.exit(1)
})
