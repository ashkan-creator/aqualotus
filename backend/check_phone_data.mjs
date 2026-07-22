// check_phone_data.mjs
// فقط می‌خونه — هیچ تغییری تو دیتابیس نمی‌ده
// اجرا: node check_phone_data.mjs  (از داخل پوشه‌ی backend، تا .env و مسیرها درست پیدا بشن)

import mongoose from 'mongoose'
import dotenv from 'dotenv'
dotenv.config()

const run = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI)
    console.log('✓ اتصال به دیتابیس برقرار شد:', mongoose.connection.name)

    const User = mongoose.connection.collection('users')

    const totalUsers = await User.countDocuments({})
    const noPhone = await User.countDocuments({
      $or: [{ phone: '' }, { phone: null }, { phone: { $exists: false } }],
    })

    console.log(`\nکل کاربرها: ${totalUsers}`)
    console.log(`کاربرای بدون شماره: ${noPhone}`)

    console.log('\n--- شماره‌های تکراری ---')
    const dupes = await User.aggregate([
      { $match: { phone: { $nin: ['', null] } } },
      { $group: { _id: '$phone', count: { $sum: 1 }, emails: { $push: '$email' } } },
      { $match: { count: { $gt: 1 } } },
    ]).toArray()

    if (dupes.length === 0) {
      console.log('هیچ شماره‌ی تکراری‌ای پیدا نشد ✓')
    } else {
      dupes.forEach((d) => console.log(`شماره: ${d._id} | تعداد: ${d.count} | ایمیل‌ها: ${d.emails.join(', ')}`))
    }

    process.exit(0)
  } catch (err) {
    console.error('✗ خطا:', err.message)
    process.exit(1)
  }
}

run()
