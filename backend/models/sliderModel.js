import mongoose from 'mongoose'

const sliderSchema = new mongoose.Schema(
  {
    title: { type: String, default: '' },
    subtitle: { type: String, default: '' },
    location: { type: String, enum: ['home', 'blog'], default: 'home' },
    image: { type: String, required: true },
    link: { type: String, default: '/' },
    isActive: { type: Boolean, default: true },
    order: { type: Number, default: 0 },
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

const Slider = mongoose.model('Slider', sliderSchema)
export default Slider
