#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch: Fix morph layoutId mismatch
ProductPage must use product._id instead of productId (slug)
"""

import os
import shutil
import sys

BASE_DIR = os.path.expanduser("~/aqualotus/frontend")
PAGE_FILE = os.path.join(BASE_DIR, "src", "pages", "ProductPage.jsx")

def backup_file(path, suffix):
    if os.path.exists(path):
        ext = os.path.splitext(path)[1]
        backup_path = path.replace(ext, f".pre-{suffix}-backup{ext}")
        if not os.path.exists(backup_path):
            shutil.copy2(path, backup_path)
            print(f"  [BACKUP] {os.path.basename(path)} -> {os.path.basename(backup_path)}")
        else:
            print(f"  [SKIP BACKUP] {os.path.basename(backup_path)} already exists")
        return True
    print(f"  [ERROR] File not found: {path}")
    return False

with open(PAGE_FILE, 'r', encoding='utf-8') as f:
    page = f.read()

# Fix: change layoutId from productId to product._id
old_layout = "layoutId={`product-img-${productId}`}"
new_layout = "layoutId={`product-img-${product?._id}`}"

if old_layout in page:
    page = page.replace(old_layout, new_layout)
    print("  [FIX] layoutId: productId -> product._id")
else:
    print("  [WARN] layoutId anchor not found")
    # Try alternative
    alt_old = 'layoutId={`product-img-${productId}`}'
    if alt_old in page:
        page = page.replace(alt_old, new_layout)
        print("  [FIX] layoutId (alt): productId -> product._id")
    else:
        print("  [ERROR] Cannot find layoutId to fix")
        sys.exit(1)

if not backup_file(PAGE_FILE, "morph-fix"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(PAGE_FILE, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"  [WRITE] {os.path.basename(PAGE_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {PAGE_FILE}: {e}")
    sys.exit(1)

print("\n✓ Morph layoutId fix applied!")
print("  Changes:")
print("    • ProductPage layoutId: productId -> product._id")
print("    • Now layoutId matches between ProductCard and ProductPage")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test: Click a product card -> image should morph!")
