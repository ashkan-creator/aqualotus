#!/usr/bin/env python3
"""
مرحله ۳ از ۵ — فیچر استایل‌دهی متن اسلایدر/وبلاگ

۱) ساخت یه فایل کمکی جدید frontend/src/utils/buildTextStyle.js که آبجکت
   titleStyle رو به یه آبجکت واقعی CSS تبدیل می‌کنه:
   - shadow + glow با هم ترکیب میشن تو یه textShadow واحد (چون CSS فقط
     یه property داره، ولی چندتا لایه‌ی shadow می‌تونه داشته باشه)
   - fontFamily از یه لیست محدود و امن (بدون نیاز به فونت جدید) map میشه
   - fadeIn یه کلاس CSS برمی‌گردونه (fade-in انیمیشن از قبل تو
     animations.css موجوده، از همون استفاده می‌کنیم)

۲) اعمال این تابع تو HeroSlider.jsx: هم رو تیتر اسلایدر خونه، هم رو
   تیتر پست‌های وبلاگ (که از همین کامپوننت رندر میشن).

نحوه‌ی اجرا:
    cp fix_titlestyle_render.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_titlestyle_render.py
"""

import sys
from pathlib import Path

HELPER_PATH = Path("frontend/src/utils/buildTextStyle.js")

HELPER_CONTENT = """// تبدیل آبجکت titleStyle (ذخیره‌شده تو دیتابیس) به استایل واقعی CSS
// برای تیتر اسلایدر/وبلاگ. shadow و glow هر دو با textShadow پیاده‌سازی
// میشن (چون CSS همچین چیز جدایی برای glow نداره، glow یعنی یه shadow
// با blur بیشتر و بدون offset).

const FONT_MAP = {
  default: "'Vazirmatn', sans-serif",
  serif: "Georgia, 'Vazirmatn', serif",
  mono: "'Courier New', monospace",
}

export function buildTextStyle(titleStyle) {
  if (!titleStyle) return {}

  const style = {}

  if (titleStyle.color) style.color = titleStyle.color
  if (titleStyle.textAlign) style.textAlign = titleStyle.textAlign
  style.fontFamily = FONT_MAP[titleStyle.fontFamily] || FONT_MAP.default

  const shadowLayers = []

  if (titleStyle.shadow?.enabled) {
    const { color = '#000000', blur = 8, offsetX = 0, offsetY = 2 } = titleStyle.shadow
    shadowLayers.push(`${offsetX}px ${offsetY}px ${blur}px ${color}`)
  }

  if (titleStyle.glow?.enabled) {
    const { color = '#52b788', intensity = 10 } = titleStyle.glow
    // گلو یعنی چند لایه shadow بدون offset با blur فزاینده، دور متن رو می‌گیره
    shadowLayers.push(`0 0 ${intensity}px ${color}`)
    shadowLayers.push(`0 0 ${intensity * 2}px ${color}`)
  }

  if (shadowLayers.length > 0) {
    style.textShadow = shadowLayers.join(', ')
  }

  return style
}

export function getTextStyleClassName(titleStyle) {
  return titleStyle?.fadeIn?.enabled ? 'aq-title-fade-in' : ''
}
"""

HERO_IMPORT_OLD = "import { useGetFeaturedPostsQuery } from '../../slices/blogApiSlice'"
HERO_IMPORT_NEW = (
    "import { useGetFeaturedPostsQuery } from '../../slices/blogApiSlice'\n"
    "import { buildTextStyle, getTextStyleClassName } from '../../utils/buildTextStyle'"
)

BLOG_SLIDES_OLD = (
    "    title: post.title,\n"
    "    image: post.image,\n"
)
BLOG_SLIDES_NEW = (
    "    title: post.title,\n"
    "    titleStyle: post.titleStyle,\n"
    "    image: post.image,\n"
)

TITLE_RENDER_OLD = (
    "            {slide.title && (\n"
    "              <h1 className='hero-title aq-display-title aq-reveal aq-reveal-1'>\n"
    "                {slide.title}\n"
    "              </h1>\n"
    "            )}"
)
TITLE_RENDER_NEW = (
    "            {slide.title && (\n"
    "              <h1\n"
    "                className={`hero-title aq-display-title aq-reveal aq-reveal-1 ${getTextStyleClassName(slide.titleStyle)}`}\n"
    "                style={buildTextStyle(slide.titleStyle)}\n"
    "              >\n"
    "                {slide.title}\n"
    "              </h1>\n"
    "            )}"
)


def main():
    # ۱) ساخت فایل کمکی
    if HELPER_PATH.exists():
        print(f"ℹ️  {HELPER_PATH}: از قبل وجود داره، رد می‌کنم.")
    else:
        HELPER_PATH.parent.mkdir(parents=True, exist_ok=True)
        HELPER_PATH.write_text(HELPER_CONTENT, encoding="utf-8")
        print(f"✅ {HELPER_PATH}: ساخته شد.")

    # ۲) پچ HeroSlider.jsx
    hero_path = Path("frontend/src/components/ui/HeroSlider.jsx")
    if not hero_path.exists():
        print(f"❌ فایل پیدا نشد: {hero_path.resolve()}")
        sys.exit(1)

    content = hero_path.read_text(encoding="utf-8")

    if "buildTextStyle" in content:
        print(f"⚠️  {hero_path}: به‌نظر می‌رسه قبلاً فیکس شده.")
        sys.exit(0)

    for old, new, name in [
        (HERO_IMPORT_OLD, HERO_IMPORT_NEW, "import"),
        (BLOG_SLIDES_OLD, BLOG_SLIDES_NEW, "blogSlides mapping"),
        (TITLE_RENDER_OLD, TITLE_RENDER_NEW, "title render"),
    ]:
        if old not in content:
            print(f"❌ انکر '{name}' پیدا نشد. دستی چک کن.")
            sys.exit(1)

    backup_path = hero_path.with_suffix(hero_path.suffix + ".pre-titlestyle-render-fix-backup")
    backup_path.write_text(content, encoding="utf-8")

    new_content = content.replace(HERO_IMPORT_OLD, HERO_IMPORT_NEW, 1)
    new_content = new_content.replace(BLOG_SLIDES_OLD, BLOG_SLIDES_NEW, 1)
    new_content = new_content.replace(TITLE_RENDER_OLD, TITLE_RENDER_NEW, 1)
    hero_path.write_text(new_content, encoding="utf-8")

    print(f"✅ {hero_path}: فیکس شد.")
    print(f"بک‌آپ: {backup_path}")
    print("\n✅ مرحله ۳ تمام شد. حالا git diff بزن و چک کن.")


if __name__ == "__main__":
    main()
