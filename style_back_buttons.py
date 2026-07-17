#!/usr/bin/env python3
"""
اسکریپت پچ: تبدیل لینک «بازگشت به ورود» به دکمه با هاور و موشن
اجرا از ریشه پروژه: python3 style_back_buttons.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-backbtn-backup"

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
# 1) index.css — کلاس دکمه ثانویه برای «بازگشت»
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/index.css",
    ".otp-input {\n"
    "  letter-spacing: 10px;\n"
    "  font-size: 1.4rem;\n"
    "  font-weight: 700;\n"
    "  text-align: center;\n"
    "}",
    ".otp-input {\n"
    "  letter-spacing: 10px;\n"
    "  font-size: 1.4rem;\n"
    "  font-weight: 700;\n"
    "  text-align: center;\n"
    "}\n"
    ".btn-auth-secondary {\n"
    "  display: inline-block;\n"
    "  border: 2px solid var(--primary);\n"
    "  color: var(--primary);\n"
    "  font-weight: 600;\n"
    "  border-radius: 10px;\n"
    "  padding: 8px 22px;\n"
    "  transition: all 0.3s ease;\n"
    "  text-decoration: none;\n"
    "}\n"
    ".btn-auth-secondary:hover {\n"
    "  background: var(--primary);\n"
    "  color: #fff;\n"
    "  transform: translateY(-2px);\n"
    "  box-shadow: 0 4px 14px rgba(45, 106, 79, 0.35);\n"
    "  text-decoration: none;\n"
    "}\n"
    ".btn-auth-secondary:active {\n"
    "  transform: translateY(0);\n"
    "}",
    "index.css: افزودن کلاس btn-auth-secondary با هاور و موشن",
)

# ─────────────────────────────────────────────────────────
# 2) ForgotPasswordPage.jsx — «بازگشت به صفحه ورود» (حالت sent)
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/ForgotPasswordPage.jsx",
    "                    <Link to='/login' className='auth-link'>بازگشت به صفحه ورود</Link>",
    "                    <Link to='/login' className='btn-auth-secondary'>بازگشت به صفحه ورود</Link>",
    "ForgotPasswordPage.jsx: دکمه‌ای کردن «بازگشت به صفحه ورود»",
)

# ─────────────────────────────────────────────────────────
# 3) ForgotPasswordPage.jsx — «بازگشت به ورود» (پایین فرم)
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/ForgotPasswordPage.jsx",
    "                    <Link to='/login' className='auth-link'>بازگشت به ورود</Link>",
    "                    <Link to='/login' className='btn-auth-secondary'>بازگشت به ورود</Link>",
    "ForgotPasswordPage.jsx: دکمه‌ای کردن «بازگشت به ورود»",
)

# ─────────────────────────────────────────────────────────
# 4) ResetPasswordPage.jsx — «بازگشت به ورود»
# ─────────────────────────────────────────────────────────
patch_file(
    "frontend/src/pages/ResetPasswordPage.jsx",
    "                    <Link to='/login' className='auth-link'>بازگشت به ورود</Link>",
    "                    <Link to='/login' className='btn-auth-secondary'>بازگشت به ورود</Link>",
    "ResetPasswordPage.jsx: دکمه‌ای کردن «بازگشت به ورود»",
)

# ─────────────────────────────────────────────────────────
# گزارش نهایی
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("نتیجه اجرای پچ دکمه بازگشت به ورود")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)

fail_count = sum(1 for s, _ in results if s == "❌")
if fail_count:
    print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
else:
    print("\n✅ همه مراحل با موفقیت انجام شد.")
