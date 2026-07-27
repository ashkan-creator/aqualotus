#!/usr/bin/env python3
"""
فیکس لینک breadcrumb تو ProductPage.jsx
مشکل: <Link to="/products"> به یه روت ناموجود اشاره می‌کرد (چون تو main.jsx
هیچ روت جدایی به اسم /products تعریف نشده) و به NotFoundPage (404) می‌خورد.
فیکس: چون صفحه‌ی "همه‌ی محصولات" همون HomePage رو مسیر ریشه‌ست، لینک باید
به "/" اشاره کنه.

نحوه‌ی اجرا:
    cp fix_breadcrumb_link.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_breadcrumb_link.py
"""

import re
import sys
from pathlib import Path

TARGET = Path("frontend/src/pages/ProductPage.jsx")

OLD = 'to="/products"'
NEW = 'to="/"'


def main():
    if not TARGET.exists():
        print(f"❌ فایل پیدا نشد: {TARGET.resolve()}")
        print("مطمئن شو این اسکریپت رو از ریشه‌ی ~/aqualotus/ اجرا می‌کنی.")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    count = content.count(OLD)

    if count == 0:
        print("⚠️ هیچ موردی از 'to=\"/products\"' پیدا نشد. شاید قبلاً فیکس شده.")
        sys.exit(0)

    if count > 1:
        print(f"⚠️ {count} مورد پیدا شد (انتظار داشتیم فقط ۱ مورد باشه).")
        print("برای امنیت، همه‌شون رو عوض می‌کنم، ولی بعدش دستی چک کن.")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")

    print(f"✅ {count} مورد تو {TARGET} از '{OLD}' به '{NEW}' تغییر کرد.")
    print("حالا git diff بزن تا تغییر رو ببینی، بعد کامیت/پوش کن.")


if __name__ == "__main__":
    main()
