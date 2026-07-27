#!/usr/bin/env python3
"""
فیکس باگ فیلتر خانواده‌ی گیاهی («نتیجه‌ای یافت نشد»)

مشکل: کلیک رو یه خانواده تو منوی همبرگری، اسم خانواده رو به‌عنوان
`keyword` می‌فرستاد، و بک‌اند `keyword` رو فقط رو فیلد `name` محصول
سرچ می‌کرد (نه رو فیلد واقعی `family` که خودش تو مدل محصول وجود داره).
برای خانواده‌هایی که اسمشون دقیقاً تو اسم محصول تکرار نمیشه (یا فاصله/
پرانتز فرق داره، مثل «کریپتو کورین(کریپتون)» در برابر اسم محصول
«کریپتوکورین ...») این باعث «نتیجه‌ای یافت نشد» میشد.

فیکس (۳ فایل):
1. backend/controllers/productController.js: فیلتر مستقل family اضافه شد
2. frontend/src/pages/HomePage.jsx: خوندن family از URL و پاس دادن به کوئری
3. frontend/src/components/layout/Header.jsx: کلیک خانواده حالا family
   می‌فرسته، نه keyword

نحوه‌ی اجرا:
    cp fix_family_filter.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_family_filter.py
"""

import sys
from pathlib import Path

PATCHES = [
    {
        "path": Path("backend/controllers/productController.js"),
        "old": (
            "  if (req.query.keyword) {\n"
            "    filter.name = { $regex: req.query.keyword, $options: 'i' }\n"
            "  }\n"
        ),
        "new": (
            "  if (req.query.keyword) {\n"
            "    filter.name = { $regex: req.query.keyword, $options: 'i' }\n"
            "  }\n"
            "  if (req.query.family) {\n"
            "    filter.family = req.query.family\n"
            "  }\n"
        ),
    },
    {
        "path": Path("frontend/src/pages/HomePage.jsx"),
        "old": (
            "    category: '',\n"
            "  })\n"
        ),
        "new": (
            "    category: '',\n"
            "    family: '',\n"
            "  })\n"
        ),
    },
    {
        "path": Path("frontend/src/pages/HomePage.jsx"),
        "old": (
            "      category: searchParams.get('category') || '',\n"
            "    })\n"
            "    setSortBy(searchParams.get('sortBy') || 'newest')\n"
        ),
        "new": (
            "      category: searchParams.get('category') || '',\n"
            "      family: searchParams.get('family') || '',\n"
            "    })\n"
            "    setSortBy(searchParams.get('sortBy') || 'newest')\n"
        ),
    },
    {
        "path": Path("frontend/src/pages/HomePage.jsx"),
        "old": (
            "    maxPrice: filters.maxPrice,\n"
            "    sortBy,\n"
            "  }\n"
        ),
        "new": (
            "    maxPrice: filters.maxPrice,\n"
            "    family: filters.family,\n"
            "    sortBy,\n"
            "  }\n"
        ),
    },
    {
        "path": Path("frontend/src/components/layout/Header.jsx"),
        "old": (
            "                <SubItem key={f._id} label={f.name} onClick={() => goToFilter({ keyword: f.name })} />"
        ),
        "new": (
            "                <SubItem key={f._id} label={f.name} onClick={() => goToFilter({ family: f.name })} />"
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
            print(f"❌ {path}: انکر پیدا نشد:\n{patch['old']!r}\nدستی چک کن.")
            ok = False
            continue
        if count > 1:
            print(f"⚠️  {path}: {count} مورد پیدا شد (انتظار ۱ مورد بود). فقط اولی رو عوض می‌کنم.")

        backup_path = path.with_suffix(path.suffix + ".pre-family-filter-fix-backup")
        if not backup_path.exists():
            backup_path.write_text(content, encoding="utf-8")

        new_content = content.replace(patch["old"], patch["new"], 1)
        path.write_text(new_content, encoding="utf-8")
        print(f"✅ {path}: فیکس شد.")

    if ok:
        print("\n✅ همه‌ی فایل‌ها فیکس شدن. حالا git diff بزن و چک کن.")
    else:
        print("\n⚠️ بعضی فایل‌ها فیکس نشدن. بالا رو بخون و دستی بررسی کن.")
        sys.exit(1)


if __name__ == "__main__":
    main()
