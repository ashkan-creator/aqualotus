#!/usr/bin/env python3
"""
اسکریپت هدر v19 — برگردوندن v18
حالا که منوی کاربر کوتاهه (۳ آیتم)، دیگه نیازی به popperConfig (که برای جلوگیری از فلیپ منوی بلند
ادمین گذاشته بودیم) نیست، و به‌نظر می‌رسه همین باعث بریده‌شدن متن منو رو موبایل شده.
این اسکریپت فقط همون خط رو حذف می‌کنه، برمی‌گرده به موقعیت‌یابی پیش‌فرض Bootstrap.
"""
import os
import shutil

HEADER_PATH = os.path.join("frontend", "src", "components", "layout", "Header.jsx")
HEADER_BACKUP = os.path.join("frontend", "src", "components", "layout", "Header.jsx.pre-v19-backup")

OLD_BLOCK = (
    "                    id='user-menu'\n"
    "                    align='end'\n"
    "                    popperConfig={{ strategy: 'fixed', modifiers: [{ name: 'flip', enabled: false }] }}\n"
    "                  >"
)
NEW_BLOCK = (
    "                    id='user-menu'\n"
    "                    align='end'\n"
    "                  >"
)


def main():
    if not os.path.exists(HEADER_PATH):
        print(f"✗ فایل {HEADER_PATH} پیدا نشد. این اسکریپت رو تو ریشه‌ی پروژه (~/aqualotus) اجرا کن.")
        return

    with open(HEADER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    count = content.count(OLD_BLOCK)
    if count == 0:
        if "popperConfig" not in content:
            print("✗ popperConfig تو Header.jsx پیدا نشد — احتمالاً قبلاً برگردونده شده. چیزی تغییر نکرد.")
        else:
            print("✗ انکر دقیق پیدا نشد (ولی popperConfig هست) — دستی چک لازمه. چیزی تغییر نکرد.")
        return
    if count != 1:
        print(f"✗ انکر بیش از یک‌بار پیدا شد ({count} بار) — برای امنیت چیزی تغییر نکرد.")
        return

    shutil.copy2(HEADER_PATH, HEADER_BACKUP)
    print(f"✓ بک‌آپ گرفته شد: {HEADER_BACKUP}")

    content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)

    with open(HEADER_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ popperConfig حذف شد — دراپ‌داون کاربر به موقعیت‌یابی پیش‌فرض Bootstrap برگشت")
    print(f"✓ فایل ذخیره شد: {HEADER_PATH}")
    print("✓ تمام. یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")


if __name__ == "__main__":
    main()
