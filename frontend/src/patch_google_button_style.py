#!/usr/bin/env python3
"""
Patch: change Google Identity Services button style to filled_black + pill
shape (matches site's dark-matte-glass aesthetic). This only changes the
official renderButton() config params — the button itself is a Google
iframe, so custom CSS can't reach it; theme/shape/size/text/locale are the
only supported knobs.
Backs up pages/LoginPage.jsx before touching it.
"""
import shutil
import sys
from pathlib import Path

LOGIN_FILE = Path("pages/LoginPage.jsx")

OLD = (
    "          window.google.accounts.id.renderButton(el, {\n"
    "            theme: 'outline',\n"
    "            size: 'large',\n"
    "            width: 320,\n"
    "            locale: 'fa',\n"
    "          })"
)
NEW = (
    "          window.google.accounts.id.renderButton(el, {\n"
    "            theme: 'filled_black',\n"
    "            size: 'large',\n"
    "            width: 320,\n"
    "            shape: 'pill',\n"
    "            locale: 'fa',\n"
    "          })"
)


def main():
    if not LOGIN_FILE.exists():
        print(f"✗ {LOGIN_FILE} پیدا نشد — این اسکریپت رو باید تو frontend/src اجرا کنی")
        sys.exit(1)

    content = LOGIN_FILE.read_text(encoding="utf-8")

    count = content.count(OLD)
    if count == 0:
        print("✗ لنگر پیدا نشد — فایل واقعی با نسخه‌ی دیده‌شده فرق داره")
        sys.exit(1)
    if count > 1:
        print(f"✗ لنگر {count} بار پیدا شد (باید ۱ بار باشه) — برای ایمنی متوقف شد")
        sys.exit(1)

    backup_path = LOGIN_FILE.with_suffix(LOGIN_FILE.suffix + ".pre-googlebtnstyle-backup")
    shutil.copy2(LOGIN_FILE, backup_path)
    print(f"✓ بک‌آپ گرفته شد: {backup_path}")

    LOGIN_FILE.write_text(content.replace(OLD, NEW), encoding="utf-8")
    print("✓ استایل دکمه‌ی گوگل به filled_black + pill تغییر کرد")
    print("✓ تمام — سرور Vite رو کامل ری‌استارت کن و تو Incognito صفحه‌ی /login رو ببین")


if __name__ == "__main__":
    main()
