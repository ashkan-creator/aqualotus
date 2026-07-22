#!/usr/bin/env python3
"""
اسکریپت هدر v18
علت احتمالی جدید پرش آیکون/منوی کاربر: کتابخونه‌ی Popper.js (که زیرِ NavDropdown کار می‌کنه)
وقتی منو جا نمی‌شه (فقط تو حالت ادمین با ۱۲ آیتم) سعی می‌کنه موقعیتش رو خودکار جابه‌جا/فلیپ کنه،
که باعث نوسان/پرش می‌شه. این اسکریپت این رفتار خودکار رو فقط رو دراپ‌داون کاربر خاموش می‌کنه
و موقعیت‌یابی رو با strategy:'fixed' پایدارتر می‌کنه.
"""
import os
import shutil

HEADER_PATH = os.path.join("frontend", "src", "components", "layout", "Header.jsx")
HEADER_BACKUP = os.path.join("frontend", "src", "components", "layout", "Header.jsx.pre-v18-backup")

ANCHOR_OLD = (
    "                    id='user-menu'\n"
    "                    align='end'\n"
    "                  >"
)
ANCHOR_NEW = (
    "                    id='user-menu'\n"
    "                    align='end'\n"
    "                    popperConfig={{ strategy: 'fixed', modifiers: [{ name: 'flip', enabled: false }] }}\n"
    "                  >"
)


def main():
    if not os.path.exists(HEADER_PATH):
        print(f"✗ فایل {HEADER_PATH} پیدا نشد. این اسکریپت رو تو ریشه‌ی پروژه (~/aqualotus) اجرا کن.")
        return

    with open(HEADER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if "popperConfig" in content:
        print("✗ به‌نظر می‌رسه این پچ قبلاً زده شده (popperConfig پیدا شد). چیزی تغییر نکرد.")
        return

    count = content.count(ANCHOR_OLD)
    if count != 1:
        print(f"✗ انکر دقیقاً یک‌بار پیدا نشد (پیدا شد: {count} بار). هیچ تغییری اعمال نشد — کد فعلی احتمالاً با نسخه‌ای که این اسکریپت روش نوشته شده فرق داره. لطفاً دوباره خروجی cat Header.jsx رو بفرست.")
        return

    shutil.copy2(HEADER_PATH, HEADER_BACKUP)
    print(f"✓ بک‌آپ گرفته شد: {HEADER_BACKUP}")

    content = content.replace(ANCHOR_OLD, ANCHOR_NEW, 1)

    with open(HEADER_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ فلیپ خودکار Popper رو دراپ‌داون کاربر خاموش شد و موقعیت‌یابی ثابت شد")
    print(f"✓ فایل ذخیره شد: {HEADER_PATH}")
    print("✓ تمام. یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")


if __name__ == "__main__":
    main()
