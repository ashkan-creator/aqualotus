#!/usr/bin/env python3
"""
اسکریپت پچ: استایل صفحات بازیابی رمز عبور (تب‌ها، OTP، ریسپانسیو، موشن)
اجرا از ریشه پروژه: python3 apply_forgot_password_style.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-forgotpw-style-backup"

results = []


def backup(path):
    if os.path.exists(path + BACKUP_SUFFIX):
        return
    shutil.copy2(path, path + BACKUP_SUFFIX)


def patch_file(rel_path, old, new, label):
    path = os.path.join(ROOT, rel_path)
    if not os.path.exists(path):
        results.append(("❌", f"{label} — فایل پیدا نشد: {rel_path}"))
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if old not in content:
        if new in content:
            results.append(("✓", f"{label} (قبلاً اعمال شده بود)"))
            return
        results.append(("❌", f"{label} — anchor پیدا نشد در {rel_path}"))
        return
    backup(path)
    content = content.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    results.append(("✓", label))


# ─────────────────────────────────────────────────────────
# 1) index.css — استایل تب‌ها، لینک‌ها، OTP، فید-این، ریسپانسیو
# ─────────────────────────────────────────────────────────
NEW_CSS = """.auth-title {
  color: var(--primary-dark);
  font-weight: 700;
}
/* ===== بازیابی رمز عبور - تب‌ها، لینک، OTP ===== */
.auth-card {
  animation: authFadeIn 0.4s ease;
}
@keyframes authFadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
.auth-tabs.nav-pills .nav-link {
  color: var(--primary-dark);
  font-weight: 600;
  border-radius: 30px;
  padding: 8px 22px;
  margin: 0 4px;
  background: rgba(45, 106, 79, 0.06);
  transition: all 0.25s ease;
  cursor: pointer;
}
.auth-tabs.nav-pills .nav-link:hover {
  background: rgba(45, 106, 79, 0.14);
  transform: translateY(-1px);
}
.auth-tabs.nav-pills .nav-link.active {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: #fff;
  box-shadow: 0 4px 12px rgba(45, 106, 79, 0.3);
}
.auth-link {
  color: var(--primary);
  font-weight: 500;
  transition: color 0.2s ease;
}
.auth-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}
.otp-input {
  letter-spacing: 10px;
  font-size: 1.4rem;
  font-weight: 700;
  text-align: center;
}
@media (max-width: 576px) {
  .auth-card .card-body {
    padding: 1.5rem !important;
  }
  .auth-tabs.nav-pills .nav-link {
    padding: 8px 16px;
    font-size: 0.85rem;
    margin: 0 2px;
  }
  .otp-input {
    letter-spacing: 6px;
    font-size: 1.2rem;
  }
}"""

patch_file(
    "frontend/src/index.css",
    ".auth-title {\n  color: var(--primary-dark);\n  font-weight: 700;\n}",
    NEW_CSS,
    "index.css: افزودن استایل تب‌ها / OTP / فید-این / ریسپانسیو",
)

# ─────────────────────────────────────────────────────────
# 2) ForgotPasswordPage.jsx — اعمال کلاس‌های جدید
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/ForgotPasswordPage.jsx",
    "                <Nav variant='pills' className='justify-content-center mb-4'>",
    "                <Nav variant='pills' className='auth-tabs justify-content-center mb-4'>",
    "ForgotPasswordPage.jsx: کلاس auth-tabs روی Nav",
)

patch_file(
    "frontend/src/pages/ForgotPasswordPage.jsx",
    "                    <Link to='/login'>بازگشت به صفحه ورود</Link>",
    "                    <Link to='/login' className='auth-link'>بازگشت به صفحه ورود</Link>",
    "ForgotPasswordPage.jsx: کلاس auth-link روی لینک بازگشت (حالت sent)",
)

patch_file(
    "frontend/src/pages/ForgotPasswordPage.jsx",
    "                    <Link to='/login'>بازگشت به ورود</Link>",
    "                    <Link to='/login' className='auth-link'>بازگشت به ورود</Link>",
    "ForgotPasswordPage.jsx: کلاس auth-link روی لینک پایین فرم",
)

# ─────────────────────────────────────────────────────────
# 3) ResetPasswordPage.jsx — اعمال کلاس‌های جدید
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/ResetPasswordPage.jsx",
    "                    <Link to='/login'>بازگشت به ورود</Link>",
    "                    <Link to='/login' className='auth-link'>بازگشت به ورود</Link>",
    "ResetPasswordPage.jsx: کلاس auth-link روی لینک بازگشت",
)

# ─────────────────────────────────────────────────────────
# 4) VerifyOtpPage.jsx — کلاس otp-input و auth-link
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/VerifyOtpPage.jsx",
    "                    <Form.Control\n"
    "                      type='text'\n"
    "                      inputMode='numeric'\n"
    "                      maxLength={6}\n"
    "                      value={otp}\n"
    "                      onChange={(e) => setOtp(e.target.value)}\n"
    "                      required\n"
    "                    />",
    "                    <Form.Control\n"
    "                      type='text'\n"
    "                      inputMode='numeric'\n"
    "                      maxLength={6}\n"
    "                      className='otp-input'\n"
    "                      value={otp}\n"
    "                      onChange={(e) => setOtp(e.target.value)}\n"
    "                      required\n"
    "                    />",
    "VerifyOtpPage.jsx: کلاس otp-input روی فیلد کد",
)

patch_file(
    "frontend/src/pages/VerifyOtpPage.jsx",
    "                    <Link to='/forgot-password'>ارسال مجدد کد</Link>",
    "                    <Link to='/forgot-password' className='auth-link'>ارسال مجدد کد</Link>",
    "VerifyOtpPage.jsx: کلاس auth-link روی لینک ارسال مجدد",
)

patch_file(
    "frontend/src/pages/VerifyOtpPage.jsx",
    "            <Link to='/forgot-password'>بازگشت به بازیابی رمز عبور</Link>",
    "            <Link to='/forgot-password' className='auth-link'>بازگشت به بازیابی رمز عبور</Link>",
    "VerifyOtpPage.jsx: کلاس auth-link روی لینک صفحه خطا",
)

# ─────────────────────────────────────────────────────────
# 5) LoginPage.jsx — کلاس auth-link روی لینک فراموشی رمز
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/LoginPage.jsx",
    "                  <Link to='/forgot-password' style={{ fontSize: '0.9rem' }}>",
    "                  <Link to='/forgot-password' className='auth-link' style={{ fontSize: '0.9rem' }}>",
    "LoginPage.jsx: کلاس auth-link روی لینک فراموشی رمز عبور",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ استایل بازیابی رمز عبور")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
    print("سرور فرانت رو ری‌استارت کن (اگه با npm run dev بازه، خودکار hot-reload میشه)")
    print("و صفحات /login → «رمز عبور را فراموش کرده‌اید؟» → /forgot-password رو تست کن.")
