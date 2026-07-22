#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_partial_index_operator.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/fix_partial_index_operator.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_partial_index_operator.py

مشکل: MongoDB تو partialFilterExpression از $ne پشتیبانی نمی‌کنه.
راه‌حل: $type + $ne رو با $gt: '' جایگزین می‌کنیم (هر رشته‌ی غیرخالی از '' بزرگ‌تره،
و مقایسه‌ی $gt فقط رو مقادیر هم‌نوع (string) انجام می‌شه، پس همون فیلتر قبلی رو می‌ده).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
BACKEND = ROOT / "backend"
model_path = BACKEND / "models" / "userModel.js"

if not model_path.exists():
    print(f"✗ فایل پیدا نشد: {model_path}")
    sys.exit(1)

content = model_path.read_text(encoding="utf-8")
backup_path = model_path.with_suffix(model_path.suffix + ".pre-indexfix-backup")
shutil.copy2(model_path, backup_path)

old = (
    "userSchema.index(\n"
    "  { phone: 1 },\n"
    "  { unique: true, partialFilterExpression: { phone: { $type: 'string', $ne: '' } } }\n"
    ")\n"
    "userSchema.index(\n"
    "  { email: 1 },\n"
    "  { unique: true, partialFilterExpression: { email: { $type: 'string', $ne: '' } } }\n"
    ")"
)
new = (
    "userSchema.index(\n"
    "  { phone: 1 },\n"
    "  { unique: true, partialFilterExpression: { phone: { $gt: '' } } }\n"
    ")\n"
    "userSchema.index(\n"
    "  { email: 1 },\n"
    "  { unique: true, partialFilterExpression: { email: { $gt: '' } } }\n"
    ")"
)

count = content.count(old)
if count != 1:
    print(f"✗ لنگر پیدا نشد یا تکراریه (تعداد: {count}) — هیچ تغییری اعمال نشد")
    sys.exit(1)

content = content.replace(old, new)
model_path.write_text(content, encoding="utf-8")
print(f"✓ userModel.js پچ شد — بک‌آپ: {backup_path.name}")
print("\nقدم بعدی:")
print("  node backend/sync_indexes.mjs   (از ریشه‌ی پروژه)")
