#!/usr/bin/env python3
"""
اسکریپت پنل مدیریت ادمین
۱. می‌سازه: frontend/src/pages/admin/AdminPanelPage.jsx + .css
   (گرید کارت‌هایی که به همون صفحات ادمین موجود لینک می‌دن، هیچ منطقی رو دوباره‌نویسی نمی‌کنه)
۲. تو main.jsx: import لیزی جدید + مسیر '/admin/panel' رو اضافه می‌کنه
۳. تو Header.jsx: کل لیست ۱۳تایی دراپ‌داون ادمین رو با یه لینک «پنل مدیریت» جایگزین می‌کنه
   (دقیقاً مثل الگوی ساده‌ی مشتری: پنل کاربری + خروج)

همه‌چیز قبل از تغییر بک‌آپ می‌گیره. اگه انکرها پیدا نشن، اون فایل دست‌نخورده می‌مونه.
"""
import os
import shutil

ADMIN_PAGE_DIR = os.path.join("frontend", "src", "pages", "admin")
ADMIN_PAGE_PATH = os.path.join(ADMIN_PAGE_DIR, "AdminPanelPage.jsx")
ADMIN_CSS_PATH = os.path.join(ADMIN_PAGE_DIR, "AdminPanelPage.css")

MAIN_PATH = os.path.join("frontend", "src", "main.jsx")
MAIN_BACKUP = os.path.join("frontend", "src", "main.jsx.pre-adminpanel-backup")

HEADER_PATH = os.path.join("frontend", "src", "components", "layout", "Header.jsx")
HEADER_BACKUP = os.path.join("frontend", "src", "components", "layout", "Header.jsx.pre-adminpanel-backup")

ADMIN_PAGE_JSX = '''import { Container, Row, Col, Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import './AdminPanelPage.css'

const SECTIONS = [
  {
    title: 'مدیریت اصلی',
    items: [
      { to: '/admin/dashboard', label: 'داشبورد', icon: 'fa-gauge-high' },
      { to: '/admin/reports', label: 'گزارش\\u200cگیری', icon: 'fa-chart-line' },
      { to: '/admin/productlist', label: 'محصولات', icon: 'fa-boxes-stacked' },
      { to: '/admin/orderlist', label: 'سفارش\\u200cها', icon: 'fa-cart-shopping' },
      { to: '/admin/reviews', label: 'نظرات و پاسخ\\u200cها', icon: 'fa-comments' },
      { to: '/admin/userlist', label: 'کاربران', icon: 'fa-users' },
      { to: '/admin/familylist', label: 'خانواده\\u200cهای گیاهی', icon: 'fa-seedling' },
    ],
  },
  {
    title: 'محتوا و تنظیمات',
    items: [
      { to: '/admin/sliders', label: 'اسلایدر', icon: 'fa-images' },
      { to: '/admin/blog', label: 'وبلاگ', icon: 'fa-newspaper' },
      { to: '/admin/settings', label: 'تنظیمات', icon: 'fa-gear' },
      { to: '/admin/activity-log', label: 'لاگ فعالیت', icon: 'fa-list-check' },
      { to: '/admin/linkpages', label: 'لینک\\u200cساز', icon: 'fa-link' },
      { to: '/admin/custompages', label: 'صفحه\\u200cساز', icon: 'fa-layer-group' },
    ],
  },
]

const AdminPanelPage = () => {
  return (
    <>
      <Helmet><title>پنل مدیریت | AquaLotus</title></Helmet>
      <Container className='py-4'>
        <h4 className='mb-4'>پنل مدیریت</h4>

        {SECTIONS.map((section) => (
          <div key={section.title} className='mb-4'>
            <h6 className='text-muted mb-3'>{section.title}</h6>
            <Row className='g-3'>
              {section.items.map((item) => (
                <Col key={item.to} xs={6} md={4} lg={3}>
                  <Link to={item.to} className='admin-panel-card-link'>
                    <Card className='admin-panel-card'>
                      <Card.Body className='text-center p-3'>
                        <i className={`fa-solid ${item.icon} admin-panel-card-icon`}></i>
                        <div className='admin-panel-card-label'>{item.label}</div>
                      </Card.Body>
                    </Card>
                  </Link>
                </Col>
              ))}
            </Row>
          </div>
        ))}
      </Container>
    </>
  )
}

export default AdminPanelPage
'''

ADMIN_PAGE_CSS = """.admin-panel-card-link {
  text-decoration: none;
  display: block;
}

.admin-panel-card {
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
  height: 100%;
}

.admin-panel-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  border-color: rgba(27, 67, 50, 0.3);
}

.admin-panel-card-icon {
  font-size: 1.6rem;
  color: #1b4332;
  margin-bottom: 8px;
  display: block;
}

.admin-panel-card-label {
  font-size: 0.85rem;
  color: #333;
  font-weight: 500;
}
"""


def create_admin_page():
    os.makedirs(ADMIN_PAGE_DIR, exist_ok=True)
    if os.path.exists(ADMIN_PAGE_PATH):
        print(f"✗ {ADMIN_PAGE_PATH} از قبل وجود داره — دست نخورد (اگه می‌خوای جایگزین بشه بگو).")
    else:
        with open(ADMIN_PAGE_PATH, "w", encoding="utf-8") as f:
            f.write(ADMIN_PAGE_JSX)
        print(f"✓ ساخته شد: {ADMIN_PAGE_PATH}")

    if os.path.exists(ADMIN_CSS_PATH):
        print(f"✗ {ADMIN_CSS_PATH} از قبل وجود داره — دست نخورد.")
    else:
        with open(ADMIN_CSS_PATH, "w", encoding="utf-8") as f:
            f.write(ADMIN_PAGE_CSS)
        print(f"✓ ساخته شد: {ADMIN_CSS_PATH}")


def patch_main():
    if not os.path.exists(MAIN_PATH):
        print(f"✗ فایل {MAIN_PATH} پیدا نشد.")
        return

    with open(MAIN_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if "AdminPanelPage" in content:
        print("✗ main.jsx قبلاً AdminPanelPage رو داره — چیزی تغییر نکرد.")
        return

    import_anchor = "const AdminCustomPageEditPage = lazy(() => import('./pages/admin/CustomPageEditPage'))"
    route_anchor = "{ path: 'custompages/:id/edit', element: withSuspense(AdminCustomPageEditPage) },"

    if content.count(import_anchor) != 1 or content.count(route_anchor) != 1:
        print("✗ انکرهای main.jsx پیدا نشدن (یا تکراری بودن) — main.jsx دست نخورد.")
        return

    shutil.copy2(MAIN_PATH, MAIN_BACKUP)
    print(f"✓ بک‌آپ main.jsx گرفته شد: {MAIN_BACKUP}")

    content = content.replace(
        import_anchor,
        import_anchor + "\nconst AdminPanelPage = lazy(() => import('./pages/admin/AdminPanelPage'))",
        1,
    )
    content = content.replace(
        route_anchor,
        route_anchor + "\n          { path: 'panel', element: withSuspense(AdminPanelPage) },",
        1,
    )

    with open(MAIN_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ main.jsx: import لیزی + مسیر '/admin/panel' اضافه شد")


def patch_header():
    if not os.path.exists(HEADER_PATH):
        print(f"✗ فایل {HEADER_PATH} پیدا نشد.")
        return

    with open(HEADER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if "/admin/panel" in content:
        print("✗ Header.jsx قبلاً به /admin/panel لینک داره — چیزی تغییر نکرد.")
        return

    # انکرهای فقط-ASCII (نه متن فارسی) برای پیدا کردن مرز دقیق بلوک آیتم‌های ادمین
    start_marker = "<LinkContainer to='/admin/dashboard'>"
    end_marker = "\n                        </>\n                      )}"

    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("✗ انکر شروع (admin/dashboard) تو Header.jsx پیدا نشد — دست نخورد.")
        return

    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        print("✗ انکر پایان بلوک ادمین پیدا نشد — دست نخورد. ساختار Header.jsx احتمالاً فرق داره.")
        return

    shutil.copy2(HEADER_PATH, HEADER_BACKUP)
    print(f"✓ بک‌آپ Header.jsx گرفته شد: {HEADER_BACKUP}")

    replacement = "<LinkContainer to='/admin/panel'><NavDropdown.Item>\U0001F6E0\uFE0F پنل مدیریت</NavDropdown.Item></LinkContainer>"
    content = content[:start_idx] + replacement + content[end_idx:]

    with open(HEADER_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Header.jsx: لیست ۱۳تایی ادمین با یه لینک «پنل مدیریت» جایگزین شد")


def main():
    create_admin_page()
    patch_main()
    patch_header()
    print("\nتمام. یادت نره: سرور Vite رو کامل ری‌استارت کن و تو Incognito چک کن.")


if __name__ == "__main__":
    main()
