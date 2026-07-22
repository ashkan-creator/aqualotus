#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch v2: Fix flicker - exact anchor match
Replace main product image with motion.img, remove fade conflict
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

# Exact anchor from sed output
old_img = r"""            <img$
              src={images[selectedImageIndex]}$
              alt={product?.name}$
              className="w-100 h-100 object-fit-contain p-2 p-md-4"$
              style={{ $
                opacity: fade ? 0 : 1, $
                transform: fade ? 'scale(0.98)' : 'scale(1)',$
                transition: 'opacity 0.2s ease, transform 0.2s ease',$
                filter: 'drop-shadow(0 10px 20px rgba(0,0,0,0.5))'$
              }}$
            />"""

new_img = r"""            <motion.img$
              src={images[selectedImageIndex]}$
              alt={product?.name}$
              layoutId={`product-img-${product?._id}`}$
              transition={{ duration: 0.1, ease: "easeOut" }}$
              className="w-100 h-100 object-fit-contain p-2 p-md-4"$
              style={{ $
                filter: 'drop-shadow(0 10px 20px rgba(0,0,0,0.5))'$
              }}$
            />"""

if old_img in page:
    page = page.replace(old_img, new_img)
    print("  [FIX] Main image -> motion.img, removed fade styles")
else:
    print("  [WARN] Exact anchor not found, trying flexible match...")
    # Try without $ line endings (flexible whitespace)
    import re
    pattern = r'<img\s+src=\{images\[selectedImageIndex\]\}\s+alt=\{product\?\.\name\}\s+className="w-100 h-100 object-fit-contain p-2 p-md-4"\s+style=\{\{\s+opacity: fade \? 0 : 1,\s+transform: fade \? \'scale\(0\.98\)\' : \'scale\(1\)\',\s+transition: \'opacity 0\.2s ease, transform 0\.2s ease\',\s+filter: \'drop-shadow\(0 10px 20px rgba\(0,0,0,0\.5\)\)\'\s+\}\}\s+/>'
    
    if re.search(pattern, page):
        page = re.sub(pattern, r"""<motion.img
              src={images[selectedImageIndex]}
              alt={product?.name}
              layoutId={`product-img-${product?._id}`}
              transition={{ duration: 0.1, ease: "easeOut" }}
              className="w-100 h-100 object-fit-contain p-2 p-md-4"
              style={{
                filter: 'drop-shadow(0 10px 20px rgba(0,0,0,0.5))'
              }}
            />""", page)
        print("  [FIX] Main image -> motion.img (regex match)")
    else:
        print("  [ERROR] Cannot find image to patch")
        sys.exit(1)

# Also remove motion.img from Modal (prevent double layoutId)
old_modal = r"""          <motion.img $
            src={images[selectedImageIndex]} $
            alt={product?.name} $
            layoutId={`product-img-${product?._id}`}$
            transition={{ duration: 0.1, ease: "easeOut" }}$
            className="img-fluid rounded-4 shadow-lg w-100 object-fit-contain" $
            style={{ maxHeight: '85vh', backgroundColor: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', padding: '20px' }}$
          />"""

new_modal = r"""          <img $
            src={images[selectedImageIndex]} $
            alt={product?.name} $
            className="img-fluid rounded-4 shadow-lg w-100 object-fit-contain" $
            style={{ maxHeight: '85vh', backgroundColor: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', padding: '20px' }}$
          />"""

if old_modal in page:
    page = page.replace(old_modal, new_modal)
    print("  [FIX] Modal image -> plain img (remove duplicate layoutId)")
else:
    print("  [INFO] Modal motion.img not found (may already be fixed)")

if not backup_file(PAGE_FILE, "morph-flicker-v2"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(PAGE_FILE, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"  [WRITE] {os.path.basename(PAGE_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {PAGE_FILE}: {e}")
    sys.exit(1)

print("\n✓ Morph flicker fix v2 applied!")
print("  Changes:")
print("    • Main image: <img> -> <motion.img> with layoutId")
print("    • Removed fade opacity/transform/transition (conflicted with morph)")
print("    • Kept drop-shadow filter")
print("    • Modal: removed motion.img (prevent double layoutId)")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test: Click product -> fast morph -> NO flicker!")
