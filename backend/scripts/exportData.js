import mongoose from 'mongoose'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import dotenv from 'dotenv'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
dotenv.config({ path: path.join(__dirname, '../../.env') })

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/aqualotus'
const OUT_DIR = path.join(__dirname, '../../data_export')

function serialize(value) {
  if (value === null || value === undefined) return value
  if (value && typeof value === 'object' && value._bsontype && /objectid/i.test(value._bsontype)) {
    return { $oid: value.toString() }
  }
  if (value instanceof Date) return { $date: value.toISOString() }
  if (Buffer.isBuffer(value)) return { $buffer: value.toString('base64') }
  if (Array.isArray(value)) return value.map(serialize)
  if (typeof value === 'object') {
    const out = {}
    for (const k of Object.keys(value)) out[k] = serialize(value[k])
    return out
  }
  return value
}

async function main() {
  console.log('در حال اتصال به:', MONGO_URI)
  await mongoose.connect(MONGO_URI)
  console.log('متصل شد.')

  fs.mkdirSync(OUT_DIR, { recursive: true })

  const collections = await mongoose.connection.db.listCollections().toArray()
  let total = 0
  for (const c of collections) {
    const docs = await mongoose.connection.db.collection(c.name).find({}).toArray()
    const serialized = docs.map(serialize)
    fs.writeFileSync(path.join(OUT_DIR, `${c.name}.json`), JSON.stringify(serialized))
    console.log(`✓ ${c.name}: ${docs.length} سند`)
    total += docs.length
  }

  console.log(`\nتمام شد. مجموع اسناد: ${total}`)
  console.log(`خروجی در پوشه: ${OUT_DIR}`)
  await mongoose.disconnect()
}

main().catch((e) => {
  console.error('❌ خطا:', e)
  process.exit(1)
})
