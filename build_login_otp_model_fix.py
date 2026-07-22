#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_login_otp_model_fix.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_login_otp_model_fix.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_login_otp_model_fix.py

فقط backend/models/userModel.js رو پچ می‌کنه (نسخه‌ی قبلی این فایل رو ناموفق بود،
بقیه‌ی فایل‌ها -- controller/routes/server -- از اجرای قبلی درست پچ شدن و اینجا لمس نمی‌شن).
تورفتگی این نسخه بر اساس خروجی واقعی cat -A تنظیم شده (۴ فاصله، نه ۶).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
BACKEND = ROOT / "backend"

results = []


def backup_and_patch(path: Path, patches, label):
    if not path.exists():
        results.append((label, False, f"فایل پیدا نشد: {path}"))
        return

    content = path.read_text(encoding="utf-8")
    backup_path = path.with_suffix(path.suffix + ".pre-loginotp-model-backup")
    shutil.copy2(path, backup_path)

    for i, (old, new) in enumerate(patches):
        count = content.count(old)
        if count != 1:
            results.append((
                label, False,
                f"لنگر شماره {i+1} پیدا نشد یا تکراریه (تعداد یافت‌شده: {count}) — هیچ تغییری اعمال نشد"
            ))
            return
        content = content.replace(old, new)

    path.write_text(content, encoding="utf-8")
    results.append((label, True, f"بک‌آپ: {backup_path.name}"))


model_path = BACKEND / "models" / "userModel.js"

model_patches = [
    (
        "    email: { type: String, required: true, unique: true },\n"
        "    password: { type: String, required: function () { return !this.googleId } },\n"
        "    googleId: { type: String, default: null },\n"
        "    phone: { type: String, default: '' },",

        "    email: { type: String, required: function () { return !this.isPhoneOnly } },\n"
        "    password: { type: String, required: function () { return !this.googleId && !this.isPhoneOnly } },\n"
        "    googleId: { type: String, default: null },\n"
        "    isPhoneOnly: { type: Boolean, default: false },\n"
        "    phone: { type: String, default: '' },",
    ),
    (
        "    resetOtpAttempts: { type: Number, default: 0 },\n"
        "    isAdmin: { type: Boolean, required: true, default: false },",

        "    resetOtpAttempts: { type: Number, default: 0 },\n"
        "    loginOtpCode: { type: String, default: null },\n"
        "    loginOtpExpire: { type: Date, default: null },\n"
        "    loginOtpAttempts: { type: Number, default: 0 },\n"
        "    isAdmin: { type: Boolean, required: true, default: false },",
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
    print("موفق. حالا این رو بزن تا ایندکس‌ها sync بشن:")
    print("  node backend/sync_indexes.mjs   (از ریشه‌ی پروژه)")
else:
    sys.exit(1)
