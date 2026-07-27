#!/usr/bin/env python3
"""
فیکس نهایی باگ فیلتر خانواده («همه‌چیز با هم قاطی میاد»)

مشکل واقعی: productsApiSlice.js's getProducts یه آبجکت params دستی
می‌سازه که هرکدوم از فیلترها رو تک‌تک لیست کرده (keyword, position,
cultivationType, ...) — ولی 'family' اصلاً تو این لیست نبود. یعنی حتی
با اینکه HomePage.jsx مقدار family رو درست پاس می‌داد، خود این تابع
query داشت یه آبجکت محدودتر می‌ساخت که family توش نبود، پس هیچ‌وقت
واقعاً به سرور فرستاده نمی‌شد.

فیکس: اضافه‌کردن family به لیست پارامترهای ارسالی.

نحوه‌ی اجرا:
    cp fix_products_apislice_family_param.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_products_apislice_family_param.py
"""

import sys
from pathlib import Path

TARGET = Path("frontend/src/slices/productsApiSlice.js")

OLD = (
    "          minPrice: params.minPrice || '',\n"
    "          maxPrice: params.maxPrice || '',\n"
    "          sortBy: params.sortBy || 'newest',\n"
)
NEW = (
    "          minPrice: params.minPrice || '',\n"
    "          maxPrice: params.maxPrice || '',\n"
    "          family: params.family || '',\n"
    "          sortBy: params.sortBy || 'newest',\n"
)


def main():
    if not TARGET.exists():
        print(f"❌ فایل پیدا نشد: {TARGET.resolve()}")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    if "family: params.family" in content:
        print("⚠️ به‌نظر می‌رسه قبلاً فیکس شده.")
        sys.exit(0)

    count = content.count(OLD)
    if count == 0:
        print("❌ انکر پیدا نشد. فایل رو دستی چک کن.")
        sys.exit(1)
    if count > 1:
        print(f"⚠️ {count} مورد پیدا شد (انتظار ۱ مورد). فقط اولی رو عوض می‌کنم.")

    backup_path = TARGET.with_suffix(TARGET.suffix + ".pre-family-param-fix-backup")
    backup_path.write_text(content, encoding="utf-8")

    new_content = content.replace(OLD, NEW, 1)
    TARGET.write_text(new_content, encoding="utf-8")

    print(f"✅ {TARGET}: 'family' به پارامترهای ارسالی اضافه شد.")
    print(f"بک‌آپ: {backup_path}")
    print("حالا git diff بزن تا تغییر رو ببینی.")


if __name__ == "__main__":
    main()
