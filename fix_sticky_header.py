#!/usr/bin/env python3
"""
فیکس هدر قفل‌شده (sticky) که از کار افتاده بود

مشکل: خود تگ <header> یه inline style داره: { zIndex: 1050, position: 'relative' }.
کلاس CSS .aq-sticky-header می‌گه position: sticky، ولی inline style همیشه
(صرف‌نظر از specificity) روی CSS خارجی اولویت داره — پس این position:'relative'
داشت sticky رو بی‌اثر می‌کرد.

فیکس: فقط 'position: relative' رو از اون inline style حذف می‌کنیم (zIndex
رو نگه می‌داریم چون خودش دلیل جدا داره: بالاتر از z-index:1030 کلاس CSS).
بعدش position:sticky از کلاس CSS دوباره خودش رو نشون میده.

نحوه‌ی اجرا:
    cp fix_sticky_header.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_sticky_header.py
"""

import sys
from pathlib import Path

TARGET = Path("frontend/src/components/layout/Header.jsx")

OLD = "<header className='aq-sticky-header' style={{ zIndex: 1050, position: 'relative' }}>"
NEW = "<header className='aq-sticky-header' style={{ zIndex: 1050 }}>"


def main():
    if not TARGET.exists():
        print(f"❌ فایل پیدا نشد: {TARGET.resolve()}")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    count = content.count(OLD)

    if count == 0:
        print("⚠️ انکر پیدا نشد. شاید قبلاً فیکس شده یا خط عوض شده. دستی چک کن.")
        sys.exit(1)

    if count > 1:
        print(f"⚠️ {count} مورد پیدا شد (انتظار داشتیم ۱ مورد). همه‌شون رو عوض می‌کنم.")

    backup_path = TARGET.with_suffix(TARGET.suffix + ".pre-sticky-header-fix-backup")
    backup_path.write_text(content, encoding="utf-8")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")

    print(f"✅ {count} مورد تو {TARGET} فیکس شد: 'position: relative' حذف شد.")
    print(f"بک‌آپ: {backup_path}")
    print("حالا git diff بزن تا تغییر رو ببینی.")


if __name__ == "__main__":
    main()
