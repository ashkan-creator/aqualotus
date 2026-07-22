#!/usr/bin/env python3
"""
اسکریپت پچ اصلاحی: وسط‌چین کردن هدر جدول‌های محصولات/مشتریان (با regex منعطف نسبت به فاصله‌گذاری)
اجرا از ریشه پروژه: python3 fix_center_headers.py
"""

import os
import re
import shutil

ROOT = os.path.expanduser("~/aqualotus")
BACKUP_SUFFIX = ".pre-centerheaders-backup"

path = os.path.join(ROOT, "frontend/src/pages/admin/ReportsPage.jsx")
results = []

if not os.path.exists(path):
    print(f"❌ فایل پیدا نشد: {path}")
else:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    backup_path = path + BACKUP_SUFFIX
    if not os.path.exists(backup_path):
        shutil.copy2(path, backup_path)

    # هدر جدول محصولات
    pattern1 = re.compile(r"(<th>محصول</th>)(\s*)<th>تعداد فروش</th>(\s*)<th>درآمد</th>")
    if pattern1.search(content):
        content, n1 = pattern1.subn(
            lambda m: f"{m.group(1)}{m.group(2)}<th className='text-center'>تعداد فروش</th>{m.group(3)}<th className='text-center'>درآمد</th>",
            content,
        )
        results.append(("✓", f"هدر جدول محصولات وسط‌چین شد ({n1} مورد)"))
    else:
        if "text-center'>تعداد فروش" in content:
            results.append(("✓", "هدر جدول محصولات (قبلاً اعمال شده بود)"))
        else:
            results.append(("❌", "هدر جدول محصولات — الگو پیدا نشد"))

    # هدر جدول مشتریان
    pattern2 = re.compile(r"(<th>مشتری</th>)(\s*)<th>تعداد سفارش</th>(\s*)<th>مجموع خرید</th>")
    if pattern2.search(content):
        content, n2 = pattern2.subn(
            lambda m: f"{m.group(1)}{m.group(2)}<th className='text-center'>تعداد سفارش</th>{m.group(3)}<th className='text-center'>مجموع خرید</th>",
            content,
        )
        results.append(("✓", f"هدر جدول مشتریان وسط‌چین شد ({n2} مورد)"))
    else:
        if "text-center'>تعداد سفارش" in content:
            results.append(("✓", "هدر جدول مشتریان (قبلاً اعمال شده بود)"))
        else:
            results.append(("❌", "هدر جدول مشتریان — الگو پیدا نشد"))

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print("\n" + "=" * 60)
    print("نتیجه اجرای پچ اصلاحی وسط‌چین هدرها")
    print("=" * 60)
    for status, msg in results:
        print(f"{status} {msg}")
    print("=" * 60)

    fail_count = sum(1 for s, _ in results if s == "❌")
    if fail_count:
        print(f"\n⚠️  {fail_count} مورد با خطا مواجه شد — لطفاً خروجی بالا رو کامل بفرست.")
    else:
        print("\n✅ همه مراحل با موفقیت انجام شد.")
