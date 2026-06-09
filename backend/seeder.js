import mongoose from 'mongoose'
import dotenv from 'dotenv'
import path from 'path'
import { fileURLToPath } from 'url'
import users from './data/users.js'
import products from './data/products.js'
import User from './models/userModel.js'
import Product from './models/productModel.js'
import Order from './models/orderModel.js'
import Settings from './models/settingsModel.js'
import connectDB from './config/db.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
dotenv.config({ path: path.join(__dirname, '../.env') })

connectDB()

const defaultSettings = [
  { key: 'announcement', value: '🎉 ارسال رایگان برای خرید بالای ۵۰۰,۰۰۰ تومان' },
  { key: 'contact_phone', value: '۰۹۱۲-۰۰۰-۰۰۰۰' },
  { key: 'contact_email', value: 'info@aqualotus.ir' },
  { key: 'about_text', value: 'آکوالوتوس یک فروشگاه تخصصی گیاهان آکواریوم است.' },
]

const importData = async () => {
  try {
    await Order.deleteMany()
    await Product.deleteMany()
    await User.deleteMany()
    await Settings.deleteMany()

    const createdUsers = await User.insertMany(users)
    const adminUser = createdUsers[0]._id

    const sampleProducts = products.map((product) => ({
      ...product,
      user: adminUser,
    }))

    await Product.insertMany(sampleProducts)
    await Settings.insertMany(defaultSettings)

    console.log('داده‌ها با موفقیت وارد شدند!')
    process.exit()
  } catch (error) {
    console.error(`خطا: ${error.message}`)
    process.exit(1)
  }
}

const destroyData = async () => {
  try {
    await Order.deleteMany()
    await Product.deleteMany()
    await User.deleteMany()
    await Settings.deleteMany()
    console.log('داده‌ها پاک شدند!')
    process.exit()
  } catch (error) {
    console.error(`خطا: ${error.message}`)
    process.exit(1)
  }
}

if (process.argv[2] === '-d') {
  destroyData()
} else {
  importData()
}
