#!/usr/bin/env python3
"""
فیکس باگ بریدگی محتوا تو منوی همبرگری (DrawerSection)

مشکل: تو Header.jsx، کامپوننت DrawerSection یه maxHeight ثابت 200px داره
(با overflow:hidden) وقتی باز میشه. اگه محتوای داخلش (مثلاً لیست ۹ تایی
خانواده‌های گیاهی) بیشتر از 200px جا بگیره، بقیه‌ش کاملاً بریده و مخفی
میشه — نه اسکرول میشه نه دیده میشه. این روی همه‌ی بخش‌های drawer اثر
می‌ذاره، نه فقط خانواده‌ها.

فیکس: maxHeight سقف رو از 200px به یه عدد خیلی بزرگ‌تر (2000px) می‌بریم
تا هیچ محتوایی واقعاً بریده نشه، در حالی که transition رو maxHeight هنوز
درست کار می‌کنه (چون از 0 به یه عدد مثبت میره، نه به 'none').

نحوه‌ی اجرا:
    cp fix_drawer_section_maxheight.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_drawer_section_maxheight.py
"""

import sys
from pathlib import Path

TARGET = Path("frontend/src/components/layout/Header.jsx")

OLD = "maxHeight: isOpen ? '200px' : '0'"
NEW = "maxHeight: isOpen ? '2000px' : '0'"


def main():
    if not TARGET.exists():
        print(f"❌ فایل پیدا نشد: {TARGET.resolve()}")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    count = content.count(OLD)

    if count == 0:
        print("⚠️ انکر پیدا نشد. شاید قبلاً فیکس شده یا کد عوض شده. دستی چک کن.")
        sys.exit(1)

    if count > 1:
        print(f"⚠️ {count} مورد پیدا شد (انتظار داشتیم ۱ مورد). همه‌شون رو عوض می‌کنم.")

    backup_path = TARGET.with_suffix(TARGET.suffix + ".pre-drawer-maxheight-fix-backup")
    backup_path.write_text(content, encoding="utf-8")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")

    print(f"✅ {count} مورد تو {TARGET} از 200px به 2000px تغییر کرد.")
    print(f"بک‌آپ: {backup_path}")
    print("حالا git diff بزن تا تغییر رو ببینی.")


if __name__ == "__main__":
    main()
