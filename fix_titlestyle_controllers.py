#!/usr/bin/env python3
"""
مرحله ۲ از ۵ — فیچر استایل‌دهی متن اسلایدر/وبلاگ

اضافه‌کردن پذیرش فیلد titleStyle تو کنترلرهای create/update اسلایدر و وبلاگ.

نحوه‌ی اجرا:
    cp fix_titlestyle_controllers.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_titlestyle_controllers.py
"""

import sys
from pathlib import Path

PATCHES = [
    {
        "path": Path("backend/controllers/sliderController.js"),
        "old": (
            "  const { title, subtitle, image, link, order, location } = req.body\n"
            "  const slider = await Slider.create({ title, subtitle, image, link, order, location })\n"
        ),
        "new": (
            "  const { title, subtitle, image, link, order, location, titleStyle } = req.body\n"
            "  const slider = await Slider.create({ title, subtitle, image, link, order, location, titleStyle })\n"
        ),
    },
    {
        "path": Path("backend/controllers/sliderController.js"),
        "old": (
            "    slider.location = req.body.location ?? slider.location\n"
        ),
        "new": (
            "    slider.location = req.body.location ?? slider.location\n"
            "    slider.titleStyle = req.body.titleStyle ?? slider.titleStyle\n"
        ),
    },
    {
        "path": Path("backend/controllers/blogController.js"),
        "old": (
            "  const { title, content, image, video, isPublished, relatedProducts } = req.body\n"
        ),
        "new": (
            "  const { title, content, image, video, isPublished, relatedProducts, titleStyle } = req.body\n"
        ),
    },
    {
        "path": Path("backend/controllers/blogController.js"),
        "old": (
            "    post.relatedProducts = req.body.relatedProducts ?? post.relatedProducts\n"
        ),
        "new": (
            "    post.relatedProducts = req.body.relatedProducts ?? post.relatedProducts\n"
            "    post.titleStyle = req.body.titleStyle ?? post.titleStyle\n"
        ),
    },
]


def main():
    ok = True
    for patch in PATCHES:
        path = patch["path"]
        if not path.exists():
            print(f"❌ فایل پیدا نشد: {path.resolve()}")
            ok = False
            continue

        content = path.read_text(encoding="utf-8")

        if patch["new"] in content:
            print(f"ℹ️  {path}: به‌نظر می‌رسه این تیکه قبلاً فیکس شده. رد می‌کنم.")
            continue

        count = content.count(patch["old"])
        if count == 0:
            print(f"❌ {path}: انکر پیدا نشد:\n{patch['old']!r}")
            ok = False
            continue
        if count > 1:
            print(f"⚠️  {path}: {count} مورد پیدا شد (انتظار ۱ مورد). فقط اولی رو عوض می‌کنم.")

        backup_path = path.with_suffix(path.suffix + ".pre-titlestyle-controller-fix-backup")
        if not backup_path.exists():
            backup_path.write_text(content, encoding="utf-8")

        new_content = content.replace(patch["old"], patch["new"], 1)
        path.write_text(new_content, encoding="utf-8")
        print(f"✅ {path}: فیکس شد.")

    if ok:
        print("\n✅ مرحله ۲ تمام شد. حالا git diff بزن و چک کن.")
    else:
        print("\n⚠️ بعضی موارد فیکس نشدن.")
        sys.exit(1)


if __name__ == "__main__":
    main()
