#!/usr/bin/env python3
"""
اسکریپت پچ: راست‌چین کردن فیلد شماره موبایل در ForgotPasswordPage
اجرا از ریشه پروژه: python3 fix_phone_rtl.py
"""

import os
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-phonertl-backup"

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


patch_file(
    "frontend/src/pages/ForgotPasswordPage.jsx",
    "                        <Form.Control\n"
    "                          type='tel'\n"
    "                          placeholder='شماره موبایل خود را وارد کنید'\n"
    "                          value={phone}\n"
    "                          onChange={(e) => setPhone(e.target.value)}\n"
    "                          required\n"
    "                        />",
    "                        <Form.Control\n"
    "                          type='tel'\n"
    "                          dir='rtl'\n"
    "                          style={{ textAlign: 'right' }}\n"
    "                          placeholder='شماره موبایل خود را وارد کنید'\n"
    "                          value={phone}\n"
    "                          onChange={(e) => setPhone(e.target.value)}\n"
    "                          required\n"
    "                        />",
    "ForgotPasswordPage.jsx: راست‌چین کردن فیلد شماره موبایل",
)

print("\n" + "=" * 60)
print("نتیجه اجرای پچ راست‌چین شماره موبایل")
print("=" * 60)
for status, msg in results:
    print(f"{status} {msg}")
print("=" * 60)
