import os

file_path = os.path.expanduser("~/aqualotus/frontend/src/components/ui/CustomerNotificationBell.jsx")

with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

old_style = """          style={{
            position: 'absolute',
            top: '45px',
            left: '0',
            width: '290px',"""

new_style = """          style={{
            position: 'absolute',
            top: '45px',
            left: window.innerWidth < 480 ? '-60px' : '0',
            width: window.innerWidth < 480 ? 'calc(100vw - 32px)' : '310px',
            maxWidth: '340px',"""

code = code.replace(old_style, new_style)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("استایل باکس نوتیفیکیشن کاربر کاملاً هوشمند و ریسپانسیو شد!")
