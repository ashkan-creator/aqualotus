import os

file_path = os.path.expanduser("~/aqualotus/frontend/src/components/layout/Header.jsx")

if not os.path.exists(file_path):
    print("خطا: فایل پیدا نشد!")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن خط مربوط به تصویر لوگو و بزرگ‌تر کردن سایز آن همراه با تنظیم تراز
old_logo_line = "className='aq-brand-logo-img py-1' style={{ height: '50px', objectFit: 'contain' }}"
new_logo_line = "className='aq-brand-logo-img' style={{ height: '62px', objectFit: 'contain', marginTop: '-4px', marginBottom: '-4px' }}"

if old_logo_line in content:
    content = content.replace(old_logo_line, new_logo_line)
    print("تغییر سایز لوگو اعمال شد.")
else:
    # بررسی حالت بدون py-1 برای اطمینان
    old_logo_line_alt = "className='aq-brand-logo-img' style={{ height: '50px', objectFit: 'contain' }}"
    if old_logo_line_alt in content:
        content = content.replace(old_logo_line_alt, new_logo_line)
        print("تغییر سایز لوگو اعمال شد.")
    else:
        print("خطا: خط لوگو پیدا نشد. احتمالاً ساختار تغییر کرده است.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

