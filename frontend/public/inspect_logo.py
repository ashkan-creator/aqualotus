#!/usr/bin/env python3
"""
اسکریپت تشخیصی (فقط خواندنی، هیچ فایلی رو تغییر نمی‌ده)
هدف: فهمیدن اینکه چرا logo.png شطرنجی دیده می‌شه
"""
from PIL import Image
from collections import Counter

PATH = "logo.png"

def main():
    try:
        img = Image.open(PATH)
    except FileNotFoundError:
        print(f"✗ فایل {PATH} پیدا نشد. این اسکریپت رو تو پوشه‌ی frontend/public اجرا کن.")
        return
    except Exception as e:
        print(f"✗ خطا در باز کردن فایل: {e}")
        return

    print(f"✓ فایل باز شد: {PATH}")
    print(f"  فرمت: {img.format}")
    print(f"  مود رنگ: {img.mode}")
    print(f"  سایز: {img.size}")

    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    print(f"  کانال آلفا (شفافیت) داره؟ {has_alpha}")

    if img.mode != "RGBA":
        img_rgba = img.convert("RGBA")
    else:
        img_rgba = img

    w, h = img_rgba.size
    pixels = img_rgba.load()

    # هیستوگرام مقادیر آلفا (نمونه‌گیری هر ۵ پیکسل برای سرعت)
    alpha_counter = Counter()
    for y in range(0, h, 5):
        for x in range(0, w, 5):
            alpha_counter[pixels[x, y][3]] += 1

    print("\n  توزیع مقادیر آلفا (نمونه‌برداری‌شده):")
    for alpha_val, count in sorted(alpha_counter.items())[:10]:
        print(f"    آلفا={alpha_val}: {count} پیکسل")
    if len(alpha_counter) > 10:
        print(f"    ... و {len(alpha_counter) - 10} مقدار دیگه")

    fully_transparent = alpha_counter.get(0, 0)
    fully_opaque = alpha_counter.get(255, 0)
    total_sampled = sum(alpha_counter.values())
    print(f"\n  کاملاً شفاف (آلفا=۰): {fully_transparent} از {total_sampled} نمونه")
    print(f"  کاملاً مات (آلفا=۲۵۵): {fully_opaque} از {total_sampled} نمونه")

    # رنگ‌های غالب تو یه گوشه (که احتمالاً پس‌زمینه‌ست، نه خود لوگو)
    print("\n  رنگ‌های غالب تو گوشه بالا-چپ عکس (۵۰x۵۰ پیکسل اول):")
    corner_colors = Counter()
    for y in range(min(50, h)):
        for x in range(min(50, w)):
            corner_colors[pixels[x, y]] += 1
    for color, count in corner_colors.most_common(6):
        print(f"    RGBA{color}: {count} پیکسل")

    # چک کردن الگوی شطرنجی: مقایسه‌ی پیکسل (0,0) با (8,0) با (16,0) و غیره
    print("\n  بررسی تناوب افقی (برای پیدا کردن سایز کاشی شطرنجی) رو ردیف y=10:")
    y_test = min(10, h - 1)
    row_sample = [pixels[x, y_test] for x in range(min(64, w))]
    print(f"    ۶۴ پیکسل اول ردیف y={y_test}: {row_sample[:16]} ...")

if __name__ == "__main__":
    main()
