#!/usr/bin/env python3
"""
Patch: remove the "پنل کاربری" (user profile panel) item from Header's
user dropdown, keeping only "پنل مدیریت" (admin panel, admin-only).
Backs up the file before touching it.
"""
import shutil
import sys
from pathlib import Path

HEADER_FILE = Path("components/layout/Header.jsx")

OLD = "                        <LinkContainer to='/profile'><NavDropdown.Item>پنل کاربری</NavDropdown.Item></LinkContainer>\n                        \n"
NEW = ""


def main():
    if not HEADER_FILE.exists():
        print(f"✗ {HEADER_FILE} پیدا نشد — این اسکریپت رو باید تو frontend/src اجرا کنی")
        sys.exit(1)

    content = HEADER_FILE.read_text(encoding="utf-8")

    count = content.count(OLD)
    if count == 0:
        print("✗ لنگر پیدا نشد — احتمالاً این خط قبلاً حذف شده یا فایل با نسخه‌ی دیده‌شده فرق داره")
        sys.exit(1)
    if count > 1:
        print(f"✗ لنگر {count} بار پیدا شد (باید ۱ بار باشه) — برای ایمنی متوقف شد")
        sys.exit(1)

    backup_path = HEADER_FILE.with_suffix(HEADER_FILE.suffix + ".pre-removeprofilebtn-backup")
    shutil.copy2(HEADER_FILE, backup_path)
    print(f"✓ بک‌آپ گرفته شد: {backup_path}")

    HEADER_FILE.write_text(content.replace(OLD, NEW), encoding="utf-8")
    print(f"✓ دکمه‌ی «پنل کاربری» از دراپ‌داون هدر حذف شد")
    print("✓ تمام — حالا سرور Vite رو کامل ری‌استارت کن و تو Incognito تست کن (با یوزر ادمین و یوزر عادی هر دو)")


if __name__ == "__main__":
    main()
