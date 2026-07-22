#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch: Fix flicker after morph animation
Remove conflicting fade transition from main product image
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

# Find and remove fade transition from main image container
# The main image is around line 172-183 area
old_main_img = r"""            <div 
              className="position-relative rounded-4 overflow-hidden bg-dark"
              style={{
                opacity: fade ? 0 : 1,
                transform: fade ? 'scale(0.98)' : 'scale(1)',
                transition: 'opacity 0.2s ease, transform 0.2s ease',
              }}
            >
              <img
                src={images[selectedImageIndex]}
                alt={product?.name}
                className="img-fluid w-100 object-fit-contain"
                style={{ maxHeight: '500px', cursor: 'pointer' }}
                onClick={() => setShowModal(true)}
              />
            </div>"""

new_main_img = r"""            <div 
              className="position-relative rounded-4 overflow-hidden bg-dark"
            >
              <motion.img
                src={images[selectedImageIndex]}
                alt={product?.name}
                layoutId={`product-img-${product?._id}`}
                transition={{ duration: 0.1, ease: "easeOut" }}
                className="img-fluid w-100 object-fit-contain"
                style={{ maxHeight: '500px', cursor: 'pointer' }}
                onClick={() => setShowModal(true)}
              />
            </div>"""

if old_main_img in page:
    page = page.replace(old_main_img, new_main_img)
    print("  [FIX] Main image: removed fade, added motion.img with layoutId")
else:
    print("  [WARN] Main image anchor not found")
    # Try to find the img with fade style
    if "opacity: fade ? 0 : 1" in page:
        print("  [INFO] Found fade opacity, attempting targeted fix...")
        # Remove fade styles from main image container
        page = page.replace(
            """style={{
                opacity: fade ? 0 : 1,
                transform: fade ? 'scale(0.98)' : 'scale(1)',
                transition: 'opacity 0.2s ease, transform 0.2s ease',
              }}""",
            """style={{}}"""
        )
        print("  [FIX] Removed fade transition from main image container")

# Also fix the Modal image to not conflict
old_modal = r"""          <motion.img 
            src={images[selectedImageIndex]} 
            alt={product?.name} 
            layoutId={`product-img-${product?._id}`}
            transition={{ duration: 0.1, ease: "easeOut" }}
            className="img-fluid rounded-4 shadow-lg w-100 object-fit-contain" 
            style={{ maxHeight: '85vh', backgroundColor: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', padding: '20px' }}
          />"""

new_modal = r"""          <img 
            src={images[selectedImageIndex]} 
            alt={product?.name} 
            className="img-fluid rounded-4 shadow-lg w-100 object-fit-contain" 
            style={{ maxHeight: '85vh', backgroundColor: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', padding: '20px' }}
          />"""

if old_modal in page:
    page = page.replace(old_modal, new_modal)
    print("  [FIX] Modal image: removed motion.img (prevent double layoutId)")
else:
    print("  [WARN] Modal image anchor not found")

if not backup_file(PAGE_FILE, "morph-flicker"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(PAGE_FILE, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"  [WRITE] {os.path.basename(PAGE_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {PAGE_FILE}: {e}")
    sys.exit(1)

print("\n✓ Morph flicker fix applied!")
print("  Changes:")
print("    • Main image: removed fade transition, added motion.img")
print("    • Modal image: removed motion.img (prevent conflict)")
print("    • layoutId only on main image, no fade state conflict")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test: Click product -> morph -> no flicker!")
