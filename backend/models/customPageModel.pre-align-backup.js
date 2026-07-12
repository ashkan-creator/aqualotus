import mongoose from 'mongoose'

const sectionSchema = new mongoose.Schema({
  heading: { type: String, default: '' },
  body: { type: String, default: '' },
  image: { type: String, default: '' },
})

const customPageSchema = new mongoose.Schema(
  {
    slug: { type: String, required: true, unique: true, index: true },
    heroImage: { type: String, default: '' },
    heroTitle: { type: String, default: '' },
    heroSubtitle: { type: String, default: '' },
    heroButtonText: { type: String, default: '' },
    heroButtonLink: { type: String, default: '' },
    sections: [sectionSchema],
    relatedProducts: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Product' }],
    showInHomeSlider: { type: Boolean, default: false },
    linkedSliderId: { type: mongoose.Schema.Types.ObjectId, ref: 'Slider', default: null },
    isPublished: { type: Boolean, default: true },
  },
  { timestamps: true }
)

const CustomPage = mongoose.model('CustomPage', customPageSchema)
export default CustomPage
