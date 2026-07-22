#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_aurora_grid_background.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_aurora_grid_background.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_aurora_grid_background.py

کارها:
  1. frontend/src/components/ui/AuroraGridBackground.jsx -> کامپوننت جدید (یه نمونه، نه پشت هر کارت)
  2. frontend/src/pages/HomePage.jsx -> فقط دور Row گرید محصولات پیچیده می‌شه (فروشگاه/دسته‌بندی/جستجو
     همه از همین صفحه رد می‌شن، چون بر اساس query فیلتر می‌کنه)
  3. frontend/src/index.css -> استایل صحنه append می‌شه + .product-card نیمه‌شفاف با backdrop-blur می‌شه
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
# 1. New component: AuroraGridBackground.jsx
# ---------------------------------------------------------------------------
component_path = FRONTEND / "components" / "ui" / "AuroraGridBackground.jsx"

COMPONENT_CODE = '''import { useState, useEffect } from 'react'

const BEAM_COUNT = 60

const AuroraGridBackground = ({ beamCount = BEAM_COUNT }) => {
  const [beams, setBeams] = useState([])

  useEffect(() => {
    const generated = Array.from({ length: beamCount }).map((_, i) => {
      const riseDur = Math.random() * 2 + 4
      const dropDur = Math.random() * 3 + 3
      return {
        id: i,
        style: {
          left: `${Math.random() * 100}%`,
          width: `${Math.floor(Math.random() * 3) + 1}px`,
          animationDelay: `${Math.random() * 5}s`,
          animationDuration: `${riseDur}s, ${riseDur}s, ${dropDur}s`,
        },
      }
    })
    setBeams(generated)
  }, [beamCount])

  return (
    <div className='aq-aurora-scene' aria-hidden='true'>
      <div className='aq-aurora-floor' />
      <div className='aq-aurora-main-column' />
      <div className='aq-aurora-beam-container'>
        {beams.map((beam) => (
          <div key={beam.id} className='aq-aurora-beam' style={beam.style} />
        ))}
      </div>
    </div>
  )
}

export default AuroraGridBackground
'''

if component_path.exists():
    report("AuroraGridBackground.jsx", False, "این فایل از قبل وجود داره — چیزی رو overwrite نکردیم، دستی چک کن")
else:
    component_path.write_text(COMPONENT_CODE, encoding="utf-8")
    report("AuroraGridBackground.jsx", True, "فایل جدید ساخته شد")

# ---------------------------------------------------------------------------
# 2. HomePage.jsx patch
# ---------------------------------------------------------------------------
homepage_path = FRONTEND / "pages" / "HomePage.jsx"

if homepage_path.exists():
    content = homepage_path.read_text(encoding="utf-8")
    backup = homepage_path.with_suffix(homepage_path.suffix + ".pre-aurorabg-backup")

    old_import = "import ProductCard from '../components/ui/ProductCard'"
    new_import = (
        "import ProductCard from '../components/ui/ProductCard'\n"
        "import AuroraGridBackground from '../components/ui/AuroraGridBackground'"
    )

    old_grid = (
        "                    <Row className='g-3'>\n"
        "                      {data?.products?.map((product) => (\n"
        "                        <Col key={product._id} sm={12} md={6} lg={4} xl={3}>\n"
        "                          <ProductCard product={product} />\n"
        "                        </Col>\n"
        "                      ))}\n"
        "                    </Row>"
    )
    new_grid = (
        "                    <div className='aq-aurora-grid-wrapper'>\n"
        "                      <AuroraGridBackground />\n"
        "                      <div className='aq-aurora-grid-content'>\n"
        "                        <Row className='g-3'>\n"
        "                          {data?.products?.map((product) => (\n"
        "                            <Col key={product._id} sm={12} md={6} lg={4} xl={3}>\n"
        "                              <ProductCard product={product} />\n"
        "                            </Col>\n"
        "                          ))}\n"
        "                        </Row>\n"
        "                      </div>\n"
        "                    </div>"
    )

    if content.count(old_import) == 1 and content.count(old_grid) == 1:
        shutil.copy2(homepage_path, backup)
        content = content.replace(old_import, new_import)
        content = content.replace(old_grid, new_grid)
        homepage_path.write_text(content, encoding="utf-8")
        report("HomePage.jsx", True, f"پچ شد — بک‌آپ: {backup.name}")
    else:
        report("HomePage.jsx", False, "لنگر پیدا نشد یا تکراریه — هیچ تغییری اعمال نشد")
else:
    report("HomePage.jsx", False, f"فایل پیدا نشد: {homepage_path}")

# ---------------------------------------------------------------------------
# 3. index.css — append styles
# ---------------------------------------------------------------------------
index_css_path = FRONTEND / "index.css"

NEW_CSS = '''

/* --- aurora product grid background v1 --- */
.aq-aurora-grid-wrapper {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  padding: 16px;
  background: #000500;
  margin-bottom: 8px;
}

.aq-aurora-grid-content {
  position: relative;
  z-index: 1;
}

.aq-aurora-scene {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.aq-aurora-floor {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40%;
  background-image:
    linear-gradient(rgba(0, 255, 127, 0.15) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 127, 0.15) 1px, transparent 1px);
  background-size: 40px 40px;
  transform: perspective(300px) rotateX(60deg);
  transform-origin: bottom;
  animation: aq-aurora-move-grid 3s linear infinite;
  opacity: 0.6;
}

.aq-aurora-main-column {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 60%;
  background: rgba(0, 255, 127, 0.8);
  filter: blur(20px);
  animation: aq-aurora-main-glow 3s ease-in-out infinite alternate;
}

.aq-aurora-beam-container {
  position: absolute;
  inset: 0;
}

.aq-aurora-beam {
  position: absolute;
  bottom: 0;
  height: 40%;
  background: linear-gradient(to top, rgba(0, 255, 127, 0.8), rgba(60, 255, 157, 0));
  animation-name: aq-aurora-rise, aq-aurora-fade;
  animation-timing-function: ease-out, ease-in-out;
  animation-iteration-count: infinite, infinite;
}

@keyframes aq-aurora-rise {
  0% { transform: translateY(100%); opacity: 0; }
  10% { opacity: 1; }
  100% { transform: translateY(-10%); opacity: 0; }
}

@keyframes aq-aurora-fade {
  0%, 100% { opacity: 0; }
  5%, 80% { opacity: 0.7; }
}

@keyframes aq-aurora-main-glow {
  from { opacity: 0.6; filter: blur(25px); }
  to { opacity: 0.8; filter: blur(15px); }
}

@keyframes aq-aurora-move-grid {
  from { background-position: 0 0; }
  to { background-position: -40px -20px; }
}

/* semi-transparent glass cards so the aurora glow shows through */
.product-card {
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

@media (max-width: 576px) {
  .aq-aurora-grid-wrapper {
    padding: 10px;
    border-radius: 12px;
  }
}
'''

if index_css_path.exists():
    content = index_css_path.read_text(encoding="utf-8")
    if "/* --- aurora product grid background v1 --- */" in content:
        report("index.css", False, "این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    else:
        backup = index_css_path.with_suffix(index_css_path.suffix + ".pre-aurorabg-css-backup")
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
    print("قدم بعدی: سرور Vite رو کامل ری‌استارت کن (Ctrl+C و npm run dev) و تو Incognito تست کن.")
else:
    print(f"⚠️  {len(results) - ok_count} مورد ناموفق بود.")
    sys.exit(1)
