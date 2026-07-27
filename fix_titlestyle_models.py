#!/usr/bin/env python3
"""
مرحله ۱ از ۵ — فیچر استایل‌دهی متن اسلایدر/وبلاگ

اضافه‌کردن فیلد titleStyle (رنگ، فونت، تراز، شدو، گلو، فید) به مدل‌های
Slider و Blog. این یه ساب-اسکیمای مشترکه که بعداً هم تو ادمین پنل هم
تو رندر فرانت استفاده میشه.

نحوه‌ی اجرا:
    cp fix_titlestyle_models.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_titlestyle_models.py
"""

import sys
from pathlib import Path

TITLE_STYLE_SCHEMA = """    titleStyle: {
      color: { type: String, default: '#ffffff' },
      fontFamily: { type: String, default: 'default' },
      textAlign: { type: String, enum: ['right', 'center', 'left'], default: 'center' },
      shadow: {
        enabled: { type: Boolean, default: false },
        color: { type: String, default: '#000000' },
        blur: { type: Number, default: 8 },
        offsetX: { type: Number, default: 0 },
        offsetY: { type: Number, default: 2 },
        inset: { type: Boolean, default: false },
      },
      glow: {
        enabled: { type: Boolean, default: false },
        color: { type: String, default: '#52b788' },
        intensity: { type: Number, default: 10 },
      },
      fadeIn: {
        enabled: { type: Boolean, default: false },
      },
    },
"""

PATCHES = [
    {
        "path": Path("backend/models/sliderModel.js"),
        "old": "    order: { type: Number, default: 0 },\n",
        "new": "    order: { type: Number, default: 0 },\n" + TITLE_STYLE_SCHEMA,
    },
    {
        "path": Path("backend/models/blogModel.js"),
        "old": "    relatedProducts: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Product' }],\n",
        "new": "    relatedProducts: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Product' }],\n" + TITLE_STYLE_SCHEMA,
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

        if "titleStyle" in content:
            print(f"ℹ️  {path}: به‌نظر می‌رسه قبلاً فیکس شده. رد می‌کنم.")
            continue

        count = content.count(patch["old"])
        if count == 0:
            print(f"❌ {path}: انکر پیدا نشد. دستی چک کن.")
            ok = False
            continue
        if count > 1:
            print(f"⚠️  {path}: {count} مورد پیدا شد (انتظار ۱ مورد). فقط اولی رو عوض می‌کنم.")

        backup_path = path.with_suffix(path.suffix + ".pre-titlestyle-fix-backup")
        if not backup_path.exists():
            backup_path.write_text(content, encoding="utf-8")

        new_content = content.replace(patch["old"], patch["new"], 1)
        path.write_text(new_content, encoding="utf-8")
        print(f"✅ {path}: titleStyle اضافه شد.")

    if ok:
        print("\n✅ مرحله ۱ تمام شد. حالا git diff بزن و چک کن.")
    else:
        print("\n⚠️ بعضی فایل‌ها فیکس نشدن.")
        sys.exit(1)


if __name__ == "__main__":
    main()
