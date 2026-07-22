#!/usr/bin/env python3
"""
اسکریپت هدر v20 — جابه‌جایی موقعیت آیکون سرچ موبایل و آیکون کاربر
"""
import os
import shutil

HEADER_PATH = os.path.join("frontend", "src", "components", "layout", "Header.jsx")
HEADER_BACKUP = os.path.join("frontend", "src", "components", "layout", "Header.jsx.pre-v20-backup")

BUTTON_BLOCK = (
    "              <button\n"
    "                className='d-md-none'\n"
    "                onClick={() => setMobileSearchOpen(true)}\n"
    "                style={{ background: 'rgba(255,255,255,0.12)', border: 'none', cursor: 'pointer', borderRadius: '6px', padding: '7px 9px', display: 'flex', alignItems: 'center' }}\n"
    "              >\n"
    "                <FiSearch style={{ fontSize: '1.2rem', color: 'white' }} />\n"
    "              </button>\n\n"
)

INSERT_ANCHOR = "              {userInfo && !userInfo.isAdmin && <CustomerNotificationBell />}"


def main():
    if not os.path.exists(HEADER_PATH):
        print(f"✗ فایل {HEADER_PATH} پیدا نشد. این اسکریپت رو تو ریشه‌ی پروژه (~/aqualotus) اجرا کن.")
        return

    with open(HEADER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    count_button = content.count(BUTTON_BLOCK)
    count_anchor = content.count(INSERT_ANCHOR)

    if count_button != 1:
        print(f"✗ بلوک دکمه‌ی سرچ دقیقاً یک‌بار پیدا نشد (پیدا شد: {count_button} بار). چیزی تغییر نکرد.")
        return
    if count_anchor != 1:
        print(f"✗ انکر محل درج دقیقاً یک‌بار پیدا نشد (پیدا شد: {count_anchor} بار). چیزی تغییر نکرد.")
        return

    shutil.copy2(HEADER_PATH, HEADER_BACKUP)
    print(f"✓ بک‌آپ گرفته شد: {HEADER_BACKUP}")

    # حذف دکمه از جای فعلیش
    content = content.replace(BUTTON_BLOCK, "", 1)
    # درج دوباره‌ش درست قبل از آیکون‌های اعلان (یعنی بعد از آیکون کاربر)
    content = content.replace(INSERT_ANCHOR, BUTTON_BLOCK + INSERT_ANCHOR, 1)

    with open(HEADER_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ جای آیکون سرچ موبایل و آیکون کاربر عوض شد")
    print(f"✓ فایل ذخیره شد: {HEADER_PATH}")
    print("✓ تمام. یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")


if __name__ == "__main__":
    main()
