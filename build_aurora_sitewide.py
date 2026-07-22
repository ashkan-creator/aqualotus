#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_aurora_sitewide.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_aurora_sitewide.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_aurora_sitewide.py

کارها:
  1. frontend/src/pages/HomePage.jsx -> Wrapper قبلی دور گرید برداشته می‌شه (برمی‌گرده به حالت ساده)
  2. frontend/src/App.jsx -> پس‌زمینه‌ی اورورا دور <main> اضافه می‌شه، به‌جز مسیرهای /admin و /login
  3. frontend/src/index.css -> کلاس‌های جدید سراسری append می‌شن (مارکر قبلی گرید دست‌نخورده می‌مونه،
     چون .product-card همچنان باید شیشه‌ای بمونه)
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
FRONTEND = ROOT / "frontend" / "src"

results = []


def report(label, ok, note):
    results.append((label, ok, note))


# ---------------------------------------------------------------------------
# 1. Revert HomePage.jsx wrapper
# ---------------------------------------------------------------------------
homepage_path = FRONTEND / "pages" / "HomePage.jsx"

if homepage_path.exists():
    content = homepage_path.read_text(encoding="utf-8")
    backup = homepage_path.with_suffix(homepage_path.suffix + ".pre-aurora-sitewide-backup")

    old_import = (
        "import ProductCard from '../components/ui/ProductCard'\n"
        "import AuroraGridBackground from '../components/ui/AuroraGridBackground'"
    )
    new_import = "import ProductCard from '../components/ui/ProductCard'"

    old_grid = (
        "                  <div className='aq-aurora-grid-wrapper'>\n"
        "                    <AuroraGridBackground />\n"
        "                    <div className='aq-aurora-grid-content'>\n"
        "                      <Row className='g-3'>\n"
        "                        {data?.products?.map((product) => (\n"
        "                          <Col key={product._id} sm={12} md={6} lg={4} xl={3}>\n"
        "                            <ProductCard product={product} />\n"
        "                          </Col>\n"
        "                        ))}\n"
        "                      </Row>\n"
        "                    </div>\n"
        "                  </div>"
    )
    new_grid = (
        "                  <Row className='g-3'>\n"
        "                    {data?.products?.map((product) => (\n"
        "                      <Col key={product._id} sm={12} md={6} lg={4} xl={3}>\n"
        "                        <ProductCard product={product} />\n"
        "                      </Col>\n"
        "                    ))}\n"
        "                  </Row>"
    )

    if content.count(old_import) == 1 and content.count(old_grid) == 1:
        shutil.copy2(homepage_path, backup)
        content = content.replace(old_import, new_import)
        content = content.replace(old_grid, new_grid)
        homepage_path.write_text(content, encoding="utf-8")
        report("HomePage.jsx (revert)", True, f"برگردونده شد — بک‌آپ: {backup.name}")
    else:
        report("HomePage.jsx (revert)", False, "لنگر پیدا نشد — احتمالاً از قبل برگردونده شده یا فرق داره")
else:
    report("HomePage.jsx (revert)", False, f"فایل پیدا نشد: {homepage_path}")

# ---------------------------------------------------------------------------
# 2. App.jsx patch
# ---------------------------------------------------------------------------
app_path = FRONTEND / "App.jsx"

if app_path.exists():
    content = app_path.read_text(encoding="utf-8")
    backup = app_path.with_suffix(app_path.suffix + ".pre-aurora-sitewide-backup")

    old_import = "import ErrorBoundary from './components/ui/ErrorBoundary'"
    new_import = (
        "import ErrorBoundary from './components/ui/ErrorBoundary'\n"
        "import AuroraGridBackground from './components/ui/AuroraGridBackground'"
    )

    old_main = (
        "      <Header />\n"
        "      <main className='py-3'>\n"
        "        {suppressPageTransition ? (\n"
        "          // در طول یه ناوبری View-Transition، بدون هیچ افکت Framer —\n"
        "          // تا صفحه‌ی قدیم/جدید هم‌پوشانی نداشته باشن و مورف کار کنه\n"
        "          <div key={location.pathname}>\n"
        "            <ErrorBoundary>\n"
        "              <Outlet />\n"
        "            </ErrorBoundary>\n"
        "          </div>\n"
        "        ) : (\n"
        "          <AnimatePresence mode='wait'>\n"
        "            <PageTransition key={location.pathname}>\n"
        "              <ErrorBoundary>\n"
        "                <Outlet />\n"
        "              </ErrorBoundary>\n"
        "            </PageTransition>\n"
        "          </AnimatePresence>\n"
        "        )}\n"
        "      </main>\n"
        "      <Footer />"
    )
    new_main = (
        "      <Header />\n"
        "      <main className={`py-3 ${isAuroraExcluded ? '' : 'aq-aurora-site-main'}`}>\n"
        "        {!isAuroraExcluded && <AuroraGridBackground />}\n"
        "        <div className={isAuroraExcluded ? '' : 'aq-aurora-site-content'}>\n"
        "          {suppressPageTransition ? (\n"
        "            // در طول یه ناوبری View-Transition، بدون هیچ افکت Framer —\n"
        "            // تا صفحه‌ی قدیم/جدید هم‌پوشانی نداشته باشن و مورف کار کنه\n"
        "            <div key={location.pathname}>\n"
        "              <ErrorBoundary>\n"
        "                <Outlet />\n"
        "              </ErrorBoundary>\n"
        "            </div>\n"
        "          ) : (\n"
        "            <AnimatePresence mode='wait'>\n"
        "              <PageTransition key={location.pathname}>\n"
        "                <ErrorBoundary>\n"
        "                  <Outlet />\n"
        "                </ErrorBoundary>\n"
        "              </PageTransition>\n"
        "            </AnimatePresence>\n"
        "          )}\n"
        "        </div>\n"
        "      </main>\n"
        "      <Footer />"
    )

    old_location_line = "  const location = useLocation()"
    new_location_line = (
        "  const location = useLocation()\n"
        "  const isAuroraExcluded = location.pathname.startsWith('/admin') || location.pathname === '/login'"
    )

    checks_ok = (
        content.count(old_import) == 1
        and content.count(old_main) == 1
        and content.count(old_location_line) == 1
    )

    if checks_ok:
        shutil.copy2(app_path, backup)
        content = content.replace(old_import, new_import)
        content = content.replace(old_location_line, new_location_line)
        content = content.replace(old_main, new_main)
        app_path.write_text(content, encoding="utf-8")
        report("App.jsx", True, f"پچ شد — بک‌آپ: {backup.name}")
    else:
        report(
            "App.jsx", False,
            f"لنگر پیدا نشد یا تکراریه (import:{content.count(old_import)}, "
            f"main:{content.count(old_main)}, location:{content.count(old_location_line)}) — هیچ تغییری اعمال نشد"
        )
else:
    report("App.jsx", False, f"فایل پیدا نشد: {app_path}")

# ---------------------------------------------------------------------------
# 3. index.css — append sitewide wrapper styles
# ---------------------------------------------------------------------------
index_css_path = FRONTEND / "index.css"

NEW_CSS = '''

/* --- aurora sitewide main background v1 --- */
.aq-aurora-site-main {
  position: relative;
  overflow: hidden;
  background: #000500;
}

.aq-aurora-site-content {
  position: relative;
  z-index: 1;
}
'''

if index_css_path.exists():
    content = index_css_path.read_text(encoding="utf-8")
    if "/* --- aurora sitewide main background v1 --- */" in content:
        report("index.css", False, "این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    else:
        backup = index_css_path.with_suffix(index_css_path.suffix + ".pre-aurora-sitewide-css-backup")
        shutil.copy2(index_css_path, backup)
        with open(index_css_path, "a", encoding="utf-8") as f:
            f.write(NEW_CSS)
        report("index.css", True, f"استایل append شد — بک‌آپ: {backup.name}")
else:
    report("index.css", False, f"فایل پیدا نشد: {index_css_path}")

# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("گزارش نهایی:")
print("=" * 60)
ok_count = 0
for label, ok, note in results:
    mark = "✓" if ok else "✗"
    print(f"{mark} {label} — {note}")
    if ok:
        ok_count += 1
print("=" * 60)
if ok_count == len(results):
    print("همه‌چیز با موفقیت اعمال شد.")
    print("قدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito تست کن.")
    print("چک کن: /admin و /login باید همون روشن/سفید بمونن، بقیه‌ی صفحات مشتری باید تیره باشن.")
else:
    print(f"⚠️  {len(results) - ok_count} مورد ناموفق بود.")
    sys.exit(1)
