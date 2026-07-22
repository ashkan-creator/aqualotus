#!/usr/bin/env python3
"""
اسکریپت هدر v15
۱. گروه‌بندی نهایی: لوگو تنها یه‌طرف، (منو+کاربر+سرچ+آیکون‌ها) با هم یه گروه اونور —
   فاصله فقط بین این دو گروه پخش می‌شه، دیگه به شانس RTL/مارجین اتوماتیک وابسته نیست.
۲. کمی کاهش پدینگ عمودی هدر (بدون تغییر سایز لوگو).
- هر دو فایل رو قبل از تغییر بک‌آپ می‌گیره.
- اگه انکرها پیدا نشن یا تکراری باشن، هیچ تغییری اعمال نمی‌شه (امن).
"""
import os
import shutil

HEADER_PATH = os.path.join("frontend", "src", "components", "layout", "Header.jsx")
HEADER_BACKUP = os.path.join("frontend", "src", "components", "layout", "Header.jsx.pre-v15-backup")

CSS_PATH = os.path.join("frontend", "src", "index.css")
CSS_BACKUP = os.path.join("frontend", "src", "index.css.pre-v15-backup")

CSS_PATCH = """
/* --- header v15 redesign --- */
.aqualotus-navbar {
  padding: 4px 0 !important;
}
"""

# --- JSX edits ---
ANCHOR_A_OLD = "<Nav className='d-none d-lg-flex ms-auto aq-navbar-center-nav'>"
ANCHOR_A_NEW = (
    "<div className='d-flex align-items-center aq-navbar-right-group' style={{ gap: '8px', minWidth: 0 }}>\n"
    "            <Nav className='d-none d-lg-flex aq-navbar-center-nav'>"
)

ANCHOR_B_OLD = (
    "              <FiSearch style={{ fontSize: '1.2rem', color: 'white' }} />\n"
    "            </button>\n"
    "            </div>\n"
    "          </div>"
)
ANCHOR_B_NEW = (
    "              <FiSearch style={{ fontSize: '1.2rem', color: 'white' }} />\n"
    "            </button>\n"
    "            </div>\n"
    "            </div>\n"
    "          </div>"
)

ANCHOR_C_OLD = "<div className='d-flex align-items-center w-100 aq-navbar-row' style={{ gap: '8px' }}>"
ANCHOR_C_NEW = "<div className='d-flex align-items-center w-100 aq-navbar-row' style={{ gap: '8px', justifyContent: 'space-between' }}>"


def patch_css():
    if not os.path.exists(CSS_PATH):
        print(f"✗ فایل {CSS_PATH} پیدا نشد.")
        return False
    shutil.copy2(CSS_PATH, CSS_BACKUP)
    print(f"✓ بک‌آپ index.css گرفته شد: {CSS_BACKUP}")

    with open(CSS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if "header v15 redesign" in content:
        print("✗ مارکر v15 قبلاً تو index.css موجوده — چیزی اضافه نشد.")
        return True

    with open(CSS_PATH, "a", encoding="utf-8") as f:
        f.write(CSS_PATCH)
    print("✓ پچ v15 (کاهش پدینگ هدر) به index.css اضافه شد")
    return True


def patch_jsx():
    if not os.path.exists(HEADER_PATH):
        print(f"✗ فایل {HEADER_PATH} پیدا نشد.")
        return False

    with open(HEADER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    count_a = content.count(ANCHOR_A_OLD)
    count_b = content.count(ANCHOR_B_OLD)
    count_c = content.count(ANCHOR_C_OLD)

    if "aq-navbar-right-group" in content:
        print("✗ به‌نظر می‌رسه این پچ قبلاً زده شده (aq-navbar-right-group پیدا شد). چیزی تغییر نکرد.")
        return True

    if count_a != 1:
        print(f"✗ انکر A دقیقاً یک‌بار پیدا نشد (پیدا شد: {count_a} بار). هیچ تغییری اعمال نشد — کد فعلی احتمالاً با نسخه‌ای که این اسکریپت روش نوشته شده فرق داره.")
        return False
    if count_b != 1:
        print(f"✗ انکر B دقیقاً یک‌بار پیدا نشد (پیدا شد: {count_b} بار). هیچ تغییری اعمال نشد.")
        return False
    if count_c != 1:
        print(f"✗ انکر C دقیقاً یک‌بار پیدا نشد (پیدا شد: {count_c} بار). هیچ تغییری اعمال نشد.")
        return False

    shutil.copy2(HEADER_PATH, HEADER_BACKUP)
    print(f"✓ بک‌آپ Header.jsx گرفته شد: {HEADER_BACKUP}")

    content = content.replace(ANCHOR_A_OLD, ANCHOR_A_NEW, 1)
    content = content.replace(ANCHOR_B_OLD, ANCHOR_B_NEW, 1)
    content = content.replace(ANCHOR_C_OLD, ANCHOR_C_NEW, 1)

    with open(HEADER_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ Nav دیگه ms-auto نداره و تو یه wrapper جدید با کاربر/سرچ/آیکون‌ها گروه شد")
    print("✓ ردیف اصلی هدر حالا justify-content: space-between داره (لوگو یه‌طرف، بقیه یه گروه اونور)")
    return True


def main():
    ok_css = patch_css()
    ok_jsx = patch_jsx()
    print("\n" + ("✓ همه‌چیز با موفقیت انجام شد." if ok_css and ok_jsx else "✗ بعضی مراحل ناموفق بودن — بالا رو ببین."))
    print("یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")


if __name__ == "__main__":
    main()
