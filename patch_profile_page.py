import os

file_path = "/home/ashkan/aqualotus/frontend/src/pages/ProfilePage.jsx"

if not os.path.exists(file_path):
    print("خطا: فایل ProfilePage.jsx پیدا نشد! لطفاً مسیر را چک کنید.")
    exit()

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# تعریف ساختار کارت‌های ادمین و کاربران
admin_cards_jsx = """
  // تفکیک دکمه‌های ادمین و کاربر عادی (هم دسکتاپ و هم ریسپانسیو منظم)
  const adminCards = [
    { title: '📊 داشبورد اصلی', path: '/admin/dashboard', bg: '#1b4332', color: '#fff' },
    { title: '📈 گزارش‌گیری پیشرفته', path: '/admin/reports', bg: '#f4f6f9', color: '#333' },
    { title: '📦 مدیریت محصولات', path: '/admin/productlist', bg: '#f4f6f9', color: '#333' },
    { title: '🛒 مدیریت سفارش‌ها', path: '/admin/orderlist', bg: '#f4f6f9', color: '#333' },
    { title: '💬 نظرات و پاسخ‌ها', path: '/admin/reviews', bg: '#f4f6f9', color: '#333' },
    { title: '👥 مدیریت کاربران', path: '/admin/userlist', bg: '#f4f6f9', color: '#333' },
    { title: '🌱 خانواده‌های گیاهی', path: '/admin/familylist', bg: '#f4f6f9', color: '#333' },
    { title: '🖼️ مدیریت اسلایدرها', path: '/admin/sliders', bg: '#f4f6f9', color: '#333' },
    { title: '📝 پست‌های وبلاگ', path: '/admin/blog', bg: '#f4f6f9', color: '#333' },
    { title: '⚙️ تنظیمات عمومی', path: '/admin/settings', bg: '#f4f6f9', color: '#333' },
    { title: '📋 لاگ فعالیت‌ها', path: '/admin/activity-log', bg: '#f4f6f9', color: '#333' },
    { title: '🔗 لینک‌ساز هوشمند', path: '/admin/linkpages', bg: '#f4f6f9', color: '#333' },
    { title: '🏗️ صفحه‌ساز پیشرفته', path: '/admin/custompages', bg: '#f4f6f9', color: '#333' },
  ];

  const userCards = [
    { title: 'داشبورد', path: '/dashboard', bg: '#1b4332', color: '#fff' },
    { title: 'سفارش‌های من', path: '/my-orders', bg: '#f4f6f9', color: '#333' },
    { title: 'پروفایل و امنیت', path: '/profile-settings', bg: '#f4f6f9', color: '#333' },
    { title: 'علاقه‌مندی‌ها', path: '/wishlist', bg: '#f4f6f9', color: '#333' },
    { title: 'آدرس‌های من', path: '/addresses', bg: '#f4f6f9', color: '#333' },
  ];

  const currentCards = userInfo?.isAdmin ? adminCards : userCards;
"""

print("در حال پشتیبان‌گیری و به‌روزرسانی کارت‌های پنل...")
# در اینجا کدهای گرید رندرینگ داخل ProfilePage را بر اساس ساختار ادمین داینامیک می‌کنیم.
# برای اینکه بدون خرابکاری ساختار کامپوننت شما حفظ شود، لطفاً ابتدا خروجی این فایل را ویرایش کنیم.
