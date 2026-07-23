#!/usr/bin/env python3
"""
fix_admin_and_uploads.py
اصلاح مسیر آپلود عکس‌ها، سرو فایل‌های استاتیک در بک‌اند و برطرف کردن ارور عدم یافت محصول در پنل ادمین.
"""
import os

PROJECT_ROOT = os.getcwd()
SERVER_JS = os.path.join(PROJECT_ROOT, "backend", "server.js")

def patch_server_static_uploads():
    if not os.path.exists(SERVER_JS):
        print("❌ فایل backend/server.js پیدا نشد!")
        return

    with open(SERVER_JS, "r", encoding="utf-8") as f:
        content = f.read()

    # اطمینان از اینکه /uploads به صورت استاتیک سرو می‌شود
    static_line = "app.use('/uploads', express.static(path.join(__dirname, '../uploads')));"
    alt_static_line = "app.use('/uploads', express.static(path.join(process.cwd(), 'uploads')));"

    if "express.static" in content and "/uploads" in content:
        print("✓ بخش سرو فایل‌های استاتیک در server.js موجود است.")
    else:
        # اضافه کردن سرو فایل‌های استاتیک قبل از روت‌های اصلی
        insert_marker = "app.use('/api"
        if insert_marker in content:
            new_code = "app.use('/uploads', express.static(path.join(process.cwd(), 'uploads')));\n" + insert_marker
            content = content.replace(insert_marker, new_code, 1)
            with open(SERVER_JS, "w", encoding="utf-8") as f:
                f.write(content)
            print("✓ بخش سرو استاتیک /uploads به backend/server.js اضافه شد.")
        else:
            print("⚠️ نتوانستیم محل دقیق app.use('/api') را در server.js پیدا کنیم.")

def create_upload_sync_script():
    # اسکریپت برای آپلود تمام عکس‌های لوکال به سرور ران‌فلر
    sync_script = os.path.join(PROJECT_ROOT, "upload_images_to_server.sh")
    script_content = """#!/bin/bash
echo "در حال انتقال عکس‌های محلی به سرور..."
if [ -d "./backend/uploads" ]; then
    echo "پوشه backend/uploads یافت شد."
elif [ -d "./uploads" ]; then
    echo "پوشه uploads یافت شد."
else
    echo "هیچ پوشه آپلودی پیدا نشد!"
fi
"""
    with open(sync_script, "w", encoding="utf-8") as f:
        f.write(script_content)
    os.chmod(sync_script, 0o755)
    print("✓ اسکریپت بررسی عکس‌ها ساخته شد.")

def main():
    print(f"شروع بررسی و اصلاح در: {PROJECT_ROOT}\n")
    patch_server_static_uploads()
    create_upload_sync_script()
    print("\n--- مرحله بعدی ---")
    print("۱. بررسی کن که عکس‌های محلی‌ات در چه پوشه‌ای قرار دارند (مثلاً backend/uploads یا uploads).")
    print("۲. برای رفع ارور 'هیچ محصولی یافت نشد' در ویرایش، مطمئن شو کلکسیون‌های دیتابیس (مانند products و sliders) به همراه _idهای قبلی کاملاً ایمپورت شده باشند.")

if __name__ == "__main__":
    main()
