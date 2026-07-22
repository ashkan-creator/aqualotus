// sync_indexes.mjs
// یه‌بار اجرا میشه بعد از پچ مدل، تا ایندکس قدیمی email با ایندکس partial جدید جایگزین بشه.
// اجرا از ریشه‌ی پروژه (تا .env پیدا بشه):
//   cd ~/aqualotus
//   node backend/sync_indexes.mjs

import mongoose from 'mongoose'
import dotenv from 'dotenv'
import User from './models/userModel.js'
dotenv.config()

const run = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI)
    console.log('✓ وصل شد:', mongoose.connection.name)

    console.log('ایندکس‌های قبلی:')
    console.log(await User.collection.indexes())

    const result = await User.syncIndexes()
    console.log('\n✓ sync انجام شد. تغییرات:', result)

    console.log('\nایندکس‌های فعلی:')
    console.log(await User.collection.indexes())

    process.exit(0)
  } catch (err) {
    console.error('✗ خطا:', err.message)
    process.exit(1)
  }
}

run()
