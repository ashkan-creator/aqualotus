import mongoose from 'mongoose'

const linkItemSchema = new mongoose.Schema({
  label: { type: String, required: true },
  url: { type: String, required: true },
  icon: { type: String, default: '' },
  order: { type: Number, default: 0 },
  isActive: { type: Boolean, default: true },
  shortCode: { type: String, unique: true, sparse: true, index: true },
  clicks: { type: Number, default: 0 },
  type: { type: String, enum: ['external', 'blog', 'product'], default: 'external' },
  productId: { type: mongoose.Schema.Types.ObjectId, ref: 'Product', default: null },
})

const linkPageSchema = new mongoose.Schema(
  {
    slug: { type: String, required: true, unique: true, index: true },
    title: { type: String, default: '' },
    bio: { type: String, default: '' },
    avatar: { type: String, default: '' },
    isActive: { type: Boolean, default: true },
    links: [linkItemSchema],
  },
  { timestamps: true }
)

const LinkPage = mongoose.model('LinkPage', linkPageSchema)
export default LinkPage
