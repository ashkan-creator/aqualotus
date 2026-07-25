#!/usr/bin/env python3
"""
fix_product_gallery_missing_image.py

Root cause: frontend/src/pages/ProductPage.jsx line 163 builds the gallery
image list as:

    const images = product?.images?.length > 0 ? product.images : [product?.image || '/placeholder.webp'];

Whenever product.images has any items, product.image (the separate main/
cover photo field, confirmed independent in backend/controllers/
productController.js) is completely discarded -- so every product with a
non-empty images array is missing exactly one photo (its main image).

Fix: merge product.image into the array (placed first), but only if it
isn't already present, so we neither lose the main photo nor duplicate it.

Run this from the project root (~/aqualotus/):
    python3 fix_product_gallery_missing_image.py

Backs up the file first:
    frontend/src/pages/ProductPage.jsx -> frontend/src/pages/ProductPage.jsx.pre-gallery-mainimage-backup
"""

import os
import shutil
import sys

TARGET = os.path.join("frontend", "src", "pages", "ProductPage.jsx")

OLD_LINE = (
    "  const images = product?.images?.length > 0 ? product.images : [product?.image || '/placeholder.webp'];\n"
)

NEW_LINE = (
    "  const images = product?.images?.length > 0\n"
    "    ? (product?.image && !product.images.includes(product.image)\n"
    "        ? [product.image, ...product.images]\n"
    "        : product.images)\n"
    "    : [product?.image || '/placeholder.webp'];\n"
)


def backup(path):
    backup_path = path + ".pre-gallery-mainimage-backup"
    if not os.path.exists(backup_path):
        shutil.copy2(path, backup_path)
    return backup_path


def main():
    if not os.path.exists(TARGET):
        print(f"[FAIL] {TARGET} not found. Run this script from ~/aqualotus/")
        sys.exit(1)

    with open(TARGET, "r", encoding="utf-8") as f:
        content = f.read()

    if NEW_LINE in content:
        print("[INFO] ProductPage.jsx already has the fix applied, no changes needed.")
        sys.exit(0)

    count = content.count(OLD_LINE)
    if count == 0:
        print("[FAIL] Could not find the expected `const images = ...` line in ProductPage.jsx.")
        print("       The file may have changed since this script was written.")
        print("       No changes were made. Send the output of:")
        print("       sed -n '160,166p' frontend/src/pages/ProductPage.jsx")
        sys.exit(1)
    if count > 1:
        print(f"[FAIL] Found the line {count} times (expected exactly 1).")
        print("       Refusing to guess which one to patch. No changes were made.")
        sys.exit(1)

    backup_path = backup(TARGET)

    new_content = content.replace(OLD_LINE, NEW_LINE, 1)
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] backed up to {backup_path}")
    print("[OK] merged product.image into the gallery images array (deduped)")
    print()
    print("[DONE] Patch applied successfully. ✓")
    print("Next steps:")
    print("  1. Review the diff: git diff frontend/src/pages/ProductPage.jsx")
    print("  2. git add -A && git commit -m 'fix: include main product image in gallery, not just images[]'")
    print("  3. git push")
    print("  4. Redeploy on Runflare, then check a product page that previously showed one fewer photo")


if __name__ == "__main__":
    main()
