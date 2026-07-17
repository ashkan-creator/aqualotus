// اسکریپت یک‌بار مصرف: محاسبه soldCount محصولات از روی سفارش‌های قبلاً پرداخت‌شده
// اجرا: از داخل پوشه‌ی backend بزن:
//   node backfillSoldCount.js
// این اسکریپت رو می‌تونی بعد از اجرا حذف کنی، دیگه لازم نیست.

import dotenv from 'dotenv'
import path from 'path'
import { fileURLToPath } from 'url'
import mongoose from 'mongoose'
import Order from './models/orderModel.js'
import Product from './models/productModel.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
dotenv.config({ path: path.join(__dirname, '../.env') })

const run = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI)
    console.log('به MongoDB وصل شد.')

    // مرحله ۱: soldCount همه‌ی محصولات رو صفر کن (تا محاسبه از نو و دقیق باشه)
    await Product.updateMany({}, { $set: { soldCount: 0 } })

    // مرحله ۲: از سفارش‌های پرداخت‌شده، مجموع تعداد هر محصول رو حساب کن
    const result = await Order.aggregate([
      { $match: { isPaid: true } },
      { $unwind: '$orderItems' },
      {
        $group: {
          _id: '$orderItems.product',
          totalQty: { $sum: '$orderItems.qty' },
        },
      },
    ])

    console.log(`تعداد محصولات دارای فروش قبلی: ${result.length}`)

    // مرحله ۳: هر محصول رو با مجموع واقعی‌اش آپدیت کن
    let updated = 0
    for (const row of result) {
      if (!row._id) continue
      await Product.updateOne({ _id: row._id }, { $set: { soldCount: row.totalQty } })
      updated++
    }

    console.log(`✓ SUCCESS — ${updated} محصول آپدیت شد.`)
    process.exit(0)
  } catch (err) {
    console.error('❌ خطا:', err.message)
    process.exit(1)
  }
}

run()
