#!/usr/bin/env python3
"""
Corrective patch (v2) for HeroSlider.jsx only — the first attempt
(inside patch_blog_slider_feature.py) failed because its anchor didn't
account for a Persian comment line that sits between the two lines it
was trying to match. This version includes that comment line exactly.

Run from the project root (same place as before, ~/aqualotus).

When location === 'blog', pulls slides from featured blog posts instead
of the generic Slider collection. Home behavior (location === 'home')
is untouched.
"""
import shutil
import sys
from pathlib import Path

HERO_FILE = Path("frontend/src/components/ui/HeroSlider.jsx")

OLD_IMPORT = "import { useGetSlidersQuery } from '../../slices/sliderApiSlice'"
NEW_IMPORT = (
    "import { useGetSlidersQuery } from '../../slices/sliderApiSlice'\n"
    "import { useGetFeaturedPostsQuery } from '../../slices/blogApiSlice'"
)

OLD_DATA = (
    "  const { data: dbSliders } = useGetSlidersQuery(location)\n\n"
    "  // اگه ادمین اسلاید تو دیتابیس داشت از اونا استفاده کن وگرنه static\n"
    "  const slides = dbSliders && dbSliders.length > 0 ? dbSliders : staticSlides"
)
NEW_DATA = (
    "  const { data: dbSliders } = useGetSlidersQuery(location, { skip: location === 'blog' })\n"
    "  const { data: featuredPosts } = useGetFeaturedPostsQuery(undefined, { skip: location !== 'blog' })\n\n"
    "  const blogSlides = (featuredPosts || []).map((post) => ({\n"
    "    _id: post._id,\n"
    "    title: post.title,\n"
    "    image: post.image,\n"
    "    link: `/blog/${post._id}`,\n"
    "    buttonText: 'مطالعه مطلب',\n"
    "  }))\n\n"
    "  // اگه ادمین اسلاید تو دیتابیس داشت از اونا استفاده کن وگرنه static (یا پست‌های فعال‌شده برای وبلاگ)\n"
    "  const slides =\n"
    "    location === 'blog'\n"
    "      ? (blogSlides.length > 0 ? blogSlides : staticSlides)\n"
    "      : (dbSliders && dbSliders.length > 0 ? dbSliders : staticSlides)"
)


def main():
    if not HERO_FILE.exists():
        print(f"✗ {HERO_FILE} پیدا نشد — این اسکریپت رو باید از ریشه‌ی پروژه (~/aqualotus) اجرا کنی")
        sys.exit(1)

    content = HERO_FILE.read_text(encoding="utf-8")

    if "useGetFeaturedPostsQuery" in content:
        print("✗ به نظر میاد این فایل قبلاً پچ شده (useGetFeaturedPostsQuery پیدا شد) — دوباره اجرا نشد")
        sys.exit(1)

    if content.count(OLD_IMPORT) != 1:
        print(f"✗ لنگر ایمپورت یافت‌شده: {content.count(OLD_IMPORT)} بار (باید ۱ بار باشه)")
        sys.exit(1)
    if content.count(OLD_DATA) != 1:
        print(f"✗ لنگر دیتا یافت‌شده: {content.count(OLD_DATA)} بار (باید ۱ بار باشه) — فایل با نسخه‌ی دیده‌شده فرق داره")
        sys.exit(1)

    backup_path = HERO_FILE.with_suffix(HERO_FILE.suffix + ".pre-heroblogfix-backup")
    shutil.copy2(HERO_FILE, backup_path)
    print(f"✓ بک‌آپ گرفته شد: {backup_path}")

    content = content.replace(OLD_IMPORT, NEW_IMPORT)
    content = content.replace(OLD_DATA, NEW_DATA)
    HERO_FILE.write_text(content, encoding="utf-8")

    print("✓ HeroSlider.jsx پچ شد — location='blog' الان از پست‌های فعال‌شده استفاده می‌کنه")
    print("✓ تمام — فرانت رو کامل ری‌استارت کن، بعد یه پست بلاگ رو از تب «وبلاگ» فعال کن و /blog رو رفرش کن")


if __name__ == "__main__":
    main()
