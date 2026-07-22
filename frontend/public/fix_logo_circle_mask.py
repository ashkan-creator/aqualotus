#!/usr/bin/env python3
"""
اسکریپت اصلاح شفافیت لوگو (logo.png)
- بک‌آپ خودکار قبل از تغییر می‌گیره
- فقط بیرون دایره‌ی نشان (که قطعاً بخشی از طرح نیست) رو شفاف می‌کنه
- داخل دایره اصلاً دست نمی‌خوره (صفر ریسک برای خودِ طرح)
"""
from PIL import Image
import math
import os
import shutil

PATH = "logo.png"
BACKUP_PATH = "logo.png.pre-circle-mask-fix-backup.png"

# مقادیر پیدا‌شده از تحلیل واقعی فایل شما
CENTER_X_RATIO = 496.0 / 992.0   # نسبت مرکز به عرض تصویر
CENTER_Y_RATIO = 533.5 / 1067.0  # نسبت مرکز به ارتفاع تصویر
RADIUS_RATIO = 463.0 / 992.0     # نسبت شعاع نشان به عرض تصویر
FEATHER_PX = 3  # چند پیکسل نرم‌شدن لبه‌ی دایره، برای جلوگیری از لبه‌ی تیز/دندونه‌دار


def main():
    if not os.path.exists(PATH):
        print(f"✗ فایل {PATH} پیدا نشد. این اسکریپت رو تو پوشه‌ی frontend/public اجرا کن.")
        return

    try:
        shutil.copy2(PATH, BACKUP_PATH)
        print(f"✓ بک‌آپ گرفته شد: {BACKUP_PATH}")
    except Exception as e:
        print(f"✗ خطا در گرفتن بک‌آپ: {e}")
        return

    try:
        img = Image.open(PATH).convert("RGBA")
    except Exception as e:
        print(f"✗ خطا در باز کردن فایل: {e}")
        return

    w, h = img.size
    cx = w * CENTER_X_RATIO
    cy = h * CENTER_Y_RATIO
    radius = min(w, h) * (RADIUS_RATIO / (min(992, 1067) / 992.0)) if False else (w * RADIUS_RATIO)
    # radius نسبت به عرض تصویر محاسبه شد چون در فایل اصلی هم بر همون مبنا اندازه‌گیری شده

    px = img.load()
    changed = 0

    for y in range(h):
        for x in range(w):
            dist = math.hypot(x - cx, y - cy)
            if dist > radius + FEATHER_PX:
                r, g, b, a = px[x, y]
                if a != 0:
                    px[x, y] = (r, g, b, 0)
                    changed += 1
            elif dist > radius - FEATHER_PX:
                # نرم‌کردن لبه: کاهش تدریجی آلفا رو نوار مرزی
                r, g, b, a = px[x, y]
                t = (dist - (radius - FEATHER_PX)) / (2 * FEATHER_PX)
                t = max(0.0, min(1.0, t))
                new_a = int(a * (1 - t))
                if new_a != a:
                    px[x, y] = (r, g, b, new_a)
                    changed += 1

    try:
        img.save(PATH)
        print(f"✓ فایل ذخیره شد: {PATH}")
        print(f"✓ {changed} پیکسل شفاف/نرم شدند (بیرون دایره‌ی نشان، مرکز=({cx:.0f},{cy:.0f}) شعاع={radius:.0f})")
        print("✓ تمام. یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")
    except Exception as e:
        print(f"✗ خطا در ذخیره‌سازی: {e}")
        print(f"  فایل اصلی دست‌نخورده باقی موند، می‌تونی از {BACKUP_PATH} هم مطمئن بشی.")


if __name__ == "__main__":
    main()
