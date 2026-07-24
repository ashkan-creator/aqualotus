import mongoose from 'mongoose'
import fs from 'fs'
import path from 'path'

const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/aqualotus'
const DATA_DIR = '/app/data_export'

function revive(value) {
  if (value === null || value === undefined) return value
  if (Array.isArray(value)) return value.map(revive)
  if (typeof value === 'object') {
    const keys = Object.keys(value)
    if (keys.length === 1 && typeof value.$oid === 'string') {
      return new mongoose.Types.ObjectId(value.$oid)
    }
    if (keys.length === 1 && typeof value.$date === 'string') {
      return new Date(value.$date)
    }
    if (keys.length === 1 && typeof value.$buffer === 'string') {
      return Buffer.from(value.$buffer, 'base64')
    }
    const out = {}
    for (const k of keys) out[k] = revive(value[k])
    return out
  }
  return value
}

async function importAll() {
  await mongoose.connect(MONGO_URI)
  const db = mongoose.connection.db
  const files = fs.readdirSync(DATA_DIR).filter((f) => f.endsWith('.json'))
  for (const file of files) {
    const col = file.replace('.json', '')
    const count = await db.collection(col).countDocuments()
    if (count === 0) {
      const raw = JSON.parse(fs.readFileSync(path.join(DATA_DIR, file), 'utf8'))
      const docs = raw.map(revive)
      if (docs.length > 0) await db.collection(col).insertMany(docs)
      console.log('Imported: ' + col + ' (' + docs.length + ' docs)')
    } else {
      console.log('Skipped: ' + col + ' (already has ' + count + ' docs)')
    }
  }
  await mongoose.disconnect()
}

importAll().catch((e) => {
  console.error(e)
  process.exit(1)
})
