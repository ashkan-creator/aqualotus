const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/aqualotus';
const DATA_DIR = '/app/data_export';

async function importAll() {
  await mongoose.connect(MONGO_URI);
  const db = mongoose.connection.db;
  const files = fs.readdirSync(DATA_DIR).filter(f => f.endsWith('.json'));
  for (const file of files) {
    const col = file.replace('.json', '');
    const count = await db.collection(col).countDocuments();
    if (count === 0) {
      const docs = JSON.parse(fs.readFileSync(path.join(DATA_DIR, file), 'utf8'));
      if (docs.length > 0) await db.collection(col).insertMany(docs);
      console.log('Imported: ' + col + ' (' + docs.length + ' docs)');
    } else {
      console.log('Skipped: ' + col + ' (already has ' + count + ' docs)');
    }
  }
  await mongoose.disconnect();
}

importAll().catch(e => { console.error(e); process.exit(1); });
