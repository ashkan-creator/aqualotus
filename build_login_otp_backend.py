#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_login_otp_backend.py
اجرا از داخل ~/aqualotus (نه backend/):
    cp ~/Downloads/build_login_otp_backend.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_login_otp_backend.py

کارهایی که انجام می‌ده:
  1. backend/models/userModel.js
     - email دیگه اجباری نیست (فقط برای حساب‌های غیر phone-only)
     - phone و email هر دو یکتا می‌شن، ولی با partial index
       (یعنی مقدار '' یا نبودن فیلد باعث تداخل نمی‌شه - داده‌ی فعلی دست‌نخورده می‌مونه)
     - فیلد جدید isPhoneOnly + فیلدهای loginOtpCode/loginOtpExpire/loginOtpAttempts
  2. backend/controllers/userController.js
     - دو تابع جدید: requestLoginOtp و verifyLoginOtp (دقیقاً هم‌الگو با forgotPassword/verifyOtpAndReset)
  3. backend/routes/userRoutes.js
     - دو روت جدید: POST /login-otp/request و POST /login-otp/verify
  4. backend/server.js
     - همون authLimiter که رو /login و /register هست، رو /login-otp هم اعمال می‌شه

هر فایل قبل از تغییر بک‌آپ می‌گیره (پسوند .pre-loginotp-backup).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
BACKEND = ROOT / "backend"

results = []


def backup_and_patch(path: Path, patches, label):
    """patches: list of (old, new) tuples. Each old must appear exactly once."""
    if not path.exists():
        results.append((label, False, f"فایل پیدا نشد: {path}"))
        return

    content = path.read_text(encoding="utf-8")
    backup_path = path.with_suffix(path.suffix + ".pre-loginotp-backup")
    shutil.copy2(path, backup_path)

    for i, (old, new) in enumerate(patches):
        count = content.count(old)
        if count != 1:
            results.append((
                label, False,
                f"لنگر شماره {i+1} پیدا نشد یا تکراریه (تعداد یافت‌شده: {count}) — هیچ تغییری اعمال نشد، فایل اصلی دست‌نخورده"
            ))
            return
        content = content.replace(old, new)

    path.write_text(content, encoding="utf-8")
    results.append((label, True, f"بک‌آپ: {backup_path.name}"))


# ---------------------------------------------------------------------------
# 1. userModel.js
# ---------------------------------------------------------------------------
model_path = BACKEND / "models" / "userModel.js"

model_patches = [
    (
        "      email: { type: String, required: true, unique: true },\n"
        "      password: { type: String, required: function () { return !this.googleId } },\n"
        "      googleId: { type: String, default: null },\n"
        "      phone: { type: String, default: '' },",

        "      email: { type: String, required: function () { return !this.isPhoneOnly } },\n"
        "      password: { type: String, required: function () { return !this.googleId && !this.isPhoneOnly } },\n"
        "      googleId: { type: String, default: null },\n"
        "      isPhoneOnly: { type: Boolean, default: false },\n"
        "      phone: { type: String, default: '' },",
    ),
    (
        "      resetOtpAttempts: { type: Number, default: 0 },\n"
        "      isAdmin: { type: Boolean, required: true, default: false },",

        "      resetOtpAttempts: { type: Number, default: 0 },\n"
        "      loginOtpCode: { type: String, default: null },\n"
        "      loginOtpExpire: { type: Date, default: null },\n"
        "      loginOtpAttempts: { type: Number, default: 0 },\n"
        "      isAdmin: { type: Boolean, required: true, default: false },",
    ),
    (
        "const User = mongoose.model('User', userSchema)\n"
        "export default User",

        "userSchema.index(\n"
        "  { phone: 1 },\n"
        "  { unique: true, partialFilterExpression: { phone: { $type: 'string', $ne: '' } } }\n"
        ")\n"
        "userSchema.index(\n"
        "  { email: 1 },\n"
        "  { unique: true, partialFilterExpression: { email: { $type: 'string', $ne: '' } } }\n"
        ")\n\n"
        "const User = mongoose.model('User', userSchema)\n"
        "export default User",
    ),
]
backup_and_patch(model_path, model_patches, "userModel.js")

# ---------------------------------------------------------------------------
# 2. userController.js
# ---------------------------------------------------------------------------
controller_path = BACKEND / "controllers" / "userController.js"

new_functions = '''
const requestLoginOtp = asyncHandler(async (req, res) => {
  const { phone } = req.body
  if (!phone) {
    res.status(400)
    throw new Error('شماره موبایل ارسال نشده')
  }

  let user = await User.findOne({ phone })
  if (!user) {
    user = await User.create({
      name: 'کاربر آکوالوتوس',
      phone,
      isPhoneOnly: true,
    })
  }

  const otpCode = Math.floor(100000 + Math.random() * 900000).toString()
  user.loginOtpCode = otpCode
  user.loginOtpExpire = Date.now() + 10 * 60 * 1000
  user.loginOtpAttempts = 0
  await user.save()

  try {
    await sendSms({
      to: phone,
      message: `کد ورود شما به آکوالوتوس: ${otpCode}\\nاین کد تا ۱۰ دقیقه معتبراست.`,
    })
  } catch (err) {
    user.loginOtpCode = null
    user.loginOtpExpire = null
    await user.save()
    res.status(500)
    throw new Error('ارسال پیامک با خطا مواجه شد')
  }

  res.json({ message: 'کد تایید ارسال شد' })
})

const verifyLoginOtp = asyncHandler(async (req, res) => {
  const { phone, otp } = req.body
  if (!phone || !otp) {
    res.status(400)
    throw new Error('شماره موبایل و کد تایید الزامی است')
  }

  const user = await User.findOne({ phone })
  if (!user || !user.loginOtpCode || !user.loginOtpExpire) {
    res.status(400)
    throw new Error('درخواستی برای این شماره ثبت نشده')
  }

  if (user.loginOtpExpire < Date.now()) {
    user.loginOtpCode = null
    user.loginOtpExpire = null
    await user.save()
    res.status(400)
    throw new Error('کد تایید منقضی شده است')
  }

  if (user.loginOtpAttempts >= 5) {
    user.loginOtpCode = null
    user.loginOtpExpire = null
    await user.save()
    res.status(400)
    throw new Error('تعداد تلاش‌های شما بیش از حد مجاز است')
  }

  if (user.loginOtpCode !== otp) {
    user.loginOtpAttempts += 1
    await user.save()
    res.status(400)
    throw new Error('کد تایید نادرست است')
  }

  user.loginOtpCode = null
  user.loginOtpExpire = null
  user.loginOtpAttempts = 0
  await user.save()

  setTokenCookies(res, user._id, user.isAdmin)
  res.json({
    _id: user._id,
    name: user.name,
    email: user.email,
    phone: user.phone,
    address: user.address,
    isAdmin: user.isAdmin,
  })
})

'''

controller_patches = [
    (
        "const registerUser = asyncHandler(async (req, res) => {",
        new_functions + "const registerUser = asyncHandler(async (req, res) => {",
    ),
    (
        "  forgotPassword,\n  resetPassword,\n  verifyOtpAndReset,\n}",
        "  forgotPassword,\n  resetPassword,\n  verifyOtpAndReset,\n  requestLoginOtp,\n  verifyLoginOtp,\n}",
    ),
]
backup_and_patch(controller_path, controller_patches, "userController.js")

# ---------------------------------------------------------------------------
# 3. userRoutes.js
# ---------------------------------------------------------------------------
routes_path = BACKEND / "routes" / "userRoutes.js"

routes_patches = [
    (
        "  forgotPassword,\n  resetPassword,\n  verifyOtpAndReset,\n} from '../controllers/userController.js'",
        "  forgotPassword,\n  resetPassword,\n  verifyOtpAndReset,\n  requestLoginOtp,\n  verifyLoginOtp,\n} from '../controllers/userController.js'",
    ),
    (
        "router.post('/verify-otp', verifyOtpAndReset)",
        "router.post('/verify-otp', verifyOtpAndReset)\n"
        "router.post('/login-otp/request', requestLoginOtp)\n"
        "router.post('/login-otp/verify', verifyLoginOtp)",
    ),
]
backup_and_patch(routes_path, routes_patches, "userRoutes.js")

# ---------------------------------------------------------------------------
# 4. server.js
# ---------------------------------------------------------------------------
server_path = BACKEND / "server.js"

server_patches = [
    (
        "app.use('/api/users/login', authLimiter)\napp.use('/api/users/register', authLimiter)",
        "app.use('/api/users/login', authLimiter)\napp.use('/api/users/register', authLimiter)\napp.use('/api/users/login-otp', authLimiter)",
    ),
]
backup_and_patch(server_path, server_patches, "server.js")

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("گزارش نهایی:")
print("=" * 60)
ok_count = 0
for label, ok, note in results:
    mark = "✓" if ok else "✗"
    print(f"{mark} {label} — {note}")
    if ok:
        ok_count += 1

print("=" * 60)
if ok_count == len(results):
    print("همه‌چیز با موفقیت اعمال شد.")
    print("\nقدم بعدی: چون index ایمیل عوض شده، این دستور رو یه‌بار بزن تا ایندکس‌ها sync بشن:")
    print("  cd ~/aqualotus/backend && node sync_indexes.mjs")
    print("(اسکریپت sync_indexes.mjs جدا ارسال میشه)")
else:
    print(f"⚠️  {len(results) - ok_count} مورد ناموفق بود. فایل‌های مربوطه دست‌نخورده موندن.")
    sys.exit(1)
