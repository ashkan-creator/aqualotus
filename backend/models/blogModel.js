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
    titleStyle: {
      color: { type: String, default: '#ffffff' },
      fontFamily: { type: String, default: 'default' },
      textAlign: { type: String, enum: ['right', 'center', 'left'], default: 'center' },
      shadow: {
        enabled: { type: Boolean, default: false },
        color: { type: String, default: '#000000' },
        blur: { type: Number, default: 8 },
        offsetX: { type: Number, default: 0 },
        offsetY: { type: Number, default: 2 },
        inset: { type: Boolean, default: false },
      },
      glow: {
        enabled: { type: Boolean, default: false },
        color: { type: String, default: '#52b788' },
        intensity: { type: Number, default: 10 },
      },
      fadeIn: {
        enabled: { type: Boolean, default: false },
      },
    },
  },
  { timestamps: true }
)

const Blog = mongoose.model('Blog', blogSchema)
export default Blog
