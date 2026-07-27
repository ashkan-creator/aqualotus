import mongoose from 'mongoose'

const blogSchema = new mongoose.Schema(
  {
    user: { type: mongoose.Schema.Types.ObjectId, required: true, ref: 'User' },
    title: { type: String, required: true },
    content: { type: String, required: true },
    image: { type: String, default: '' },
    video: { type: String, default: '' },
    isPublished: { type: Boolean, default: false },
    featuredInSlider: { type: Boolean, default: false },
    relatedProducts: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Product' }],
  },
  { timestamps: true }
)

const Blog = mongoose.model('Blog', blogSchema)
export default Blog
