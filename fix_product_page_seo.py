#!/usr/bin/env python3
"""
فیکس نبود SEO تو صفحه‌ی محصول (مهم‌ترین صفحه برای فروشگاه)

مشکل: ProductPage.jsx هیچ <Helmet> نداشت — یعنی صفحه‌ی هر محصول با همون
عنوان/توضیحات پیش‌فرض کلی سایت تو گوگل ایندکس میشه، نه با اسم/قیمت/عکس
خود محصول. بدون Open Graph هم لینک تو واتساپ/شبکه‌های اجتماعی زشت
preview میشه. بدون JSON-LD هم گوگل نمی‌تونه rich snippet (قیمت/موجودی)
تو نتایج جستجو نشون بده.

فیکس: اضافه‌کردن:
1. import { Helmet } from 'react-helmet-async'
2. یه بلوک <Helmet> بعد از return( اصلی، شامل:
   - <title> داینامیک با اسم محصول
   - meta description
   - Open Graph (og:title, og:description, og:image, og:type)
   - JSON-LD structured data (schema.org Product)

نحوه‌ی اجرا:
    cp fix_product_page_seo.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_product_page_seo.py
"""

import sys
from pathlib import Path

TARGET = Path("frontend/src/pages/ProductPage.jsx")

IMPORT_OLD = "import { toast } from 'react-toastify';"
IMPORT_NEW = (
    "import { toast } from 'react-toastify';\n"
    "import { Helmet } from 'react-helmet-async';"
)

RETURN_OLD = (
    "  return (\n"
    "    <Container className=\"py-4 py-lg-5 text-end text-white\" style={{ direction: 'rtl' }}>\n"
    "      \n"
    "      <nav aria-label=\"breadcrumb\" className=\"mb-4 overflow-x-auto pb-2\">"
)

RETURN_NEW = """  return (
    <Container className="py-4 py-lg-5 text-end text-white" style={{ direction: 'rtl' }}>
      {product && (
        <Helmet>
          <title>{`${product.name} | AquaLotus`}</title>
          <meta name="description" content={product.description?.slice(0, 160) || `خرید ${product.name} از فروشگاه آکوالوتوس`} />
          <meta property="og:type" content="product" />
          <meta property="og:title" content={product.name} />
          <meta property="og:description" content={product.description?.slice(0, 160) || ''} />
          {product.image && <meta property="og:image" content={product.image} />}
          <script type="application/ld+json">
            {JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'Product',
              name: product.name,
              description: product.description || '',
              image: product.image || (product.images && product.images[0]) || '',
              offers: {
                '@type': 'Offer',
                priceCurrency: 'IRR',
                price: product.price,
                availability: 'https://schema.org/InStock',
              },
            })}
          </script>
        </Helmet>
      )}

      <nav aria-label="breadcrumb" className="mb-4 overflow-x-auto pb-2">"""


def main():
    if not TARGET.exists():
        print(f"❌ فایل پیدا نشد: {TARGET.resolve()}")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    if "react-helmet-async" in content and "<Helmet>" in content:
        print("⚠️ به‌نظر می‌رسه قبلاً فیکس شده.")
        sys.exit(0)

    if IMPORT_OLD not in content:
        print("❌ انکر ایمپورت پیدا نشد. دستی چک کن.")
        sys.exit(1)
    if RETURN_OLD not in content:
        print("❌ انکر return پیدا نشد. دستی چک کن.")
        sys.exit(1)

    backup_path = TARGET.with_suffix(TARGET.suffix + ".pre-seo-fix-backup")
    backup_path.write_text(content, encoding="utf-8")

    new_content = content.replace(IMPORT_OLD, IMPORT_NEW, 1)
    new_content = new_content.replace(RETURN_OLD, RETURN_NEW, 1)
    TARGET.write_text(new_content, encoding="utf-8")

    print(f"✅ {TARGET}: SEO تگ‌ها اضافه شدن (title, meta description, Open Graph, JSON-LD).")
    print(f"بک‌آپ: {backup_path}")
    print("حالا git diff بزن تا تغییر رو ببینی.")


if __name__ == "__main__":
    main()
