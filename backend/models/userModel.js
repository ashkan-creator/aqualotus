import mongoose from 'mongoose'
import bcrypt from 'bcryptjs'

const userSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    email: { type: String, required: function () { return !this.isPhoneOnly } },
    password: { type: String, required: function () { return !this.googleId && !this.isPhoneOnly } },
    googleId: { type: String, default: null },
    isPhoneOnly: { type: Boolean, default: false },
    phone: { type: String, default: '' },
    address: { type: String, default: '' },
    addresses: [
      {
        title: { type: String, default: '' },
        province: { type: String, required: true },
        city: { type: String, required: true },
        address: { type: String, required: true },
        postalCode: { type: String, required: true },
        phone: { type: String, required: true },
      },
    ],
    resetPasswordToken: { type: String, default: null },
    resetPasswordExpire: { type: Date, default: null },
    resetOtpCode: { type: String, default: null },
    resetOtpExpire: { type: Date, default: null },
    resetOtpAttempts: { type: Number, default: 0 },
    loginOtpCode: { type: String, default: null },
    loginOtpExpire: { type: Date, default: null },
    loginOtpAttempts: { type: Number, default: 0 },
    isAdmin: { type: Boolean, required: true, default: false },
  },
  { timestamps: true }
)

userSchema.pre('save', async function (next) {
  if (!this.isModified('password') || !this.password) { return next() }
  const salt = await bcrypt.genSalt(10)
  this.password = await bcrypt.hash(this.password, salt)
  next()
})

userSchema.methods.matchPassword = async function (enteredPassword) {
  return await bcrypt.compare(enteredPassword, this.password)
}

userSchema.index(
  { phone: 1 },
  { unique: true, partialFilterExpression: { phone: { $gt: '' } } }
)
userSchema.index(
  { email: 1 },
  { unique: true, partialFilterExpression: { email: { $gt: '' } } }
)

const User = mongoose.model('User', userSchema)
export default User
