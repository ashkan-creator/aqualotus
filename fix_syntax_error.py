import os

file_path = os.path.expanduser("~/aqualotus/frontend/src/components/layout/Header.jsx")

if not os.path.exists(file_path):
    print("خطا: فایل پیدا نشد!")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# تبدیل خط تیره به camelCase در آبجکت استایل ری‌اکت
old_style_line = "display: 'flex', alignItems: 'center', justify-content: 'space-between', flexShrink: 0,"
new_style_line = "display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexShrink: 0,"

if old_style_line in content:
    content = content.replace(old_style_line, new_style_line)
    print("خطای سینتکسی سایدبار موبایل اصلاح شد.")
else:
    # حالت جایگزین برای اطمینان از فاصله‌ها
    content = content.replace("justify-content:", "justifyContent:")
    print("جایگزینی عمومی کلید justifyContent انجام شد.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

