#!/usr/bin/env python3
"""
Fix: sliderController.js's createSlider and updateSlider never read/save
`location` (or `subtitle`) from the request body — new sliders always fall
back to the model's default ('home'), so the admin's "blog" tab filter
never finds anything, no matter how many sliders are created while that
tab is selected.

This patch:
- createSlider: destructures + saves `subtitle` and `location` too
- updateSlider: applies `req.body.subtitle` and `req.body.location` with
  the same `?? existing` fallback pattern already used for the other fields

Backs up the file before touching it.
"""
import shutil
import sys
from pathlib import Path

CONTROLLER_FILE = Path("controllers/sliderController.js")

OLD_CREATE = (
    "const createSlider = asyncHandler(async (req, res) => {\n"
    "  const { title, image, link, order } = req.body\n"
    "  const slider = await Slider.create({ title, image, link, order })"
)
NEW_CREATE = (
    "const createSlider = asyncHandler(async (req, res) => {\n"
    "  const { title, subtitle, image, link, order, location } = req.body\n"
    "  const slider = await Slider.create({ title, subtitle, image, link, order, location })"
)

OLD_UPDATE = (
    "    slider.title = req.body.title ?? slider.title\n"
    "    slider.image = req.body.image ?? slider.image\n"
    "    slider.link = req.body.link ?? slider.link\n"
    "    slider.isActive = req.body.isActive ?? slider.isActive\n"
    "    slider.order = req.body.order ?? slider.order"
)
NEW_UPDATE = (
    "    slider.title = req.body.title ?? slider.title\n"
    "    slider.subtitle = req.body.subtitle ?? slider.subtitle\n"
    "    slider.image = req.body.image ?? slider.image\n"
    "    slider.link = req.body.link ?? slider.link\n"
    "    slider.isActive = req.body.isActive ?? slider.isActive\n"
    "    slider.order = req.body.order ?? slider.order\n"
    "    slider.location = req.body.location ?? slider.location"
)

results = []


def backup(path: Path):
    bak = path.with_suffix(path.suffix + ".pre-sliderlocationfix-backup")
    shutil.copy2(path, bak)
    return bak


def main():
    if not CONTROLLER_FILE.exists():
        print(f"✗ {CONTROLLER_FILE} پیدا نشد — این اسکریپت رو باید تو ریشه‌ی backend اجرا کنی")
        sys.exit(1)

    content = CONTROLLER_FILE.read_text(encoding="utf-8")

    checks = [
        ("createSlider", OLD_CREATE),
        ("updateSlider", OLD_UPDATE),
    ]
    for label, anchor in checks:
        if content.count(anchor) != 1:
            print(f"✗ لنگر «{label}» یافت‌شده: {content.count(anchor)} بار (باید ۱ بار باشه) — فایل با نسخه‌ی دیده‌شده فرق داره")
            sys.exit(1)

    backup_path = backup(CONTROLLER_FILE)
    print(f"✓ بک‌آپ گرفته شد: {backup_path}")

    content = content.replace(OLD_CREATE, NEW_CREATE)
    content = content.replace(OLD_UPDATE, NEW_UPDATE)
    CONTROLLER_FILE.write_text(content, encoding="utf-8")

    print("✓ createSlider الان subtitle و location رو هم ذخیره می‌کنه")
    print("✓ updateSlider الان subtitle و location رو هم آپدیت می‌کنه")
    print("\n⚠️  مهم: اسلایدرهایی که قبلاً از تب «وبلاگ» ساخته بودی، تو دیتابیس با location='home' ذخیره شدن")
    print("   (چون همون باگ همیشه فعال بوده). بعد از این پچ، باید یا:")
    print("   ۱) اون اسلایدرهای قدیمی رو تو تب «صفحه اصلی» پیدا کنی و ویرایش کنی و location رو به «وبلاگ» عوض کنی، یا")
    print("   ۲) دوباره از تب «وبلاگ» اسلاید جدید بسازی")
    print("\n✓ تمام — سرور بک‌اند رو ری‌استارت کن (pm2 restart یا هر روشی که استفاده می‌کنی) و از تب وبلاگ یه اسلاید تست بساز")


if __name__ == "__main__":
    main()
