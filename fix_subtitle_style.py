#!/usr/bin/env python3
"""
اضافه‌کردن استایل متن به زیرعنوان اسلایدر (نه فقط عنوان)

مشکل: buildTextStyle فقط رو <h1> عنوان اعمال می‌شد، زیرعنوان
(<p className='hero-subtitle'>) بدون هیچ رنگ/شدو/گلو می‌موند —
یعنی رو پس‌زمینه‌های شلوغ ممکنه ناخوانا بشه.

فیکس: همون titleStyle (رنگ/شدو/گلو/فید) که برای عنوان تنظیم میشه،
رو زیرعنوان هم اعمال میشه.

نحوه‌ی اجرا:
    cp fix_subtitle_style.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_subtitle_style.py
"""

import sys
from pathlib import Path

TARGET = Path("frontend/src/components/ui/HeroSlider.jsx")

OLD = (
    "            {slide.subtitle && (\n"
    "              <p className='hero-subtitle aq-reveal aq-reveal-2'>{slide.subtitle}</p>\n"
    "            )}"
)
NEW = (
    "            {slide.subtitle && (\n"
    "              <p\n"
    "                className={`hero-subtitle aq-reveal aq-reveal-2 ${getTextStyleClassName(slide.titleStyle)}`}\n"
    "                style={buildTextStyle(slide.titleStyle)}\n"
    "              >\n"
    "                {slide.subtitle}\n"
    "              </p>\n"
    "            )}"
)


def main():
    if not TARGET.exists():
        print(f"❌ فایل پیدا نشد: {TARGET.resolve()}")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    if "buildTextStyle(slide.titleStyle)" in content and content.count("buildTextStyle(slide.titleStyle)") >= 2:
        print("⚠️ به‌نظر می‌رسه قبلاً فیکس شده (هم عنوان هم زیرعنوان استایل دارن).")
        sys.exit(0)

    if OLD not in content:
        print("❌ انکر پیدا نشد. دستی چک کن.")
        sys.exit(1)

    backup_path = TARGET.with_suffix(TARGET.suffix + ".pre-subtitle-style-fix-backup")
    backup_path.write_text(content, encoding="utf-8")

    new_content = content.replace(OLD, NEW, 1)
    TARGET.write_text(new_content, encoding="utf-8")

    print(f"✅ {TARGET}: استایل زیرعنوان هم اضافه شد.")
    print(f"بک‌آپ: {backup_path}")
    print("حالا git diff بزن تا تغییر رو ببینی.")


if __name__ == "__main__":
    main()
