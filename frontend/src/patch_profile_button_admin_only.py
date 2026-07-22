#!/usr/bin/env python3
"""
Patch (v2 — corrected requirement): show "پنل کاربری" only for non-admin
users; hide it for admins. Wraps the existing LinkContainer in an
`{!userInfo.isAdmin && (...)}` condition, matching the style of the
isAdmin block right below it. Does NOT delete the line (v1 of this
script deleted it unconditionally — that was wrong, this replaces it).
Backs up the file before touching it.
"""
import shutil
import sys
from pathlib import Path

HEADER_FILE = Path("components/layout/Header.jsx")

OLD = (
    "                      <LinkContainer to='/profile'><NavDropdown.Item>پنل کاربری</NavDropdown.Item></LinkContainer>\n"
    "                      \n"
)
NEW = (
    "                      {!userInfo.isAdmin && (\n"
    "                        <LinkContainer to='/profile'><NavDropdown.Item>پنل کاربری</NavDropdown.Item></LinkContainer>\n"
    "                      )}\n"
    "                      \n"
)


def main():
    if not HEADER_FILE.exists():
        print(f"✗ {HEADER_FILE} پیدا نشد — این اسکریپت رو باید تو frontend/src اجرا کنی")
        sys.exit(1)

    content = HEADER_FILE.read_text(encoding="utf-8")

    count = content.count(OLD)
    if count == 0:
        print("✗ لنگر پیدا نشد. اگه قبلاً patch_remove_profile_button.py (نسخه‌ی اول) رو اجرا کردی و موفق شده، خط از فایل حذف شده — cat -n بزن و بخش دراپ‌داون رو دستی برام بفرست")
        sys.exit(1)
    if count > 1:
        print(f"✗ لنگر {count} بار پیدا شد (باید ۱ بار باشه) — برای ایمنی متوقف شد")
        sys.exit(1)

    backup_path = HEADER_FILE.with_suffix(HEADER_FILE.suffix + ".pre-profilebtn-adminonly-backup")
    shutil.copy2(HEADER_FILE, backup_path)
    print(f"✓ بک‌آپ گرفته شد: {backup_path}")

    HEADER_FILE.write_text(content.replace(OLD, NEW), encoding="utf-8")
    print("✓ «پنل کاربری» حالا فقط برای کاربر عادی نشون داده میشه، برای ادمین مخفیه")
    print("✓ تمام — سرور Vite رو کامل ری‌استارت کن و با یه یوزر عادی و یه یوزر ادمین جدا تست کن")


if __name__ == "__main__":
    main()
