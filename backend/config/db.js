import mongoose from 'mongoose'

const connectDB = async () => {
  try {
    console.log('در حال اتصال به MongoDB...')
    console.log('URI:', process.env.MONGO_URI)
    const conn = await mongoose.connect(process.env.MONGO_URI)
    console.log(`MongoDB وصل شد: ${conn.connection.host}`)
  } catch (error) {
    console.error(`خطای MongoDB: ${error.message}`)
    process.exit(1)
  }
}

export default connectDB