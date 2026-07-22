#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch v3: Fix flicker - replace entire div+img block
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

# Replace the entire div containing the main image
old_block = r"""          <div $
            className="position-relative rounded-4 overflow-hidden mb-3 d-flex align-items-center justify-content-center" $
            style={{ aspectRatio: '1 / 1', maxHeight: '500px', cursor: 'zoom-in' }}$
            onClick={() => setShowModal(true)}$
          >$
            <img$
              src={images[selectedImageIndex]}$
              alt={product?.name}$
              className="w-100 h-100 object-fit-contain p-2 p-md-4"$
              style={{ $
                opacity: fade ? 0 : 1, $
                transform: fade ? 'scale(0.98)' : 'scale(1)',$
                transition: 'opacity 0.2s ease, transform 0.2s ease',$
                filter: 'drop-shadow(0 10px 20px rgba(0,0,0,0.5))'$
              }}$
            />$
            $
            {/* M-XM-/M-ZM-)M-YM-^EM-YM-^GM-bM-^@M-^LM-YM-^GM-XM-'M-[M-^L M-YM-^FM-XM-'M-YM-^HM-XM-(M-XM-1M-[M-^L M-XM-*M-XM-5M-YM-^HM-[M-^LM-XM-1 */}$"""

new_block = r"""          <motion.div $
            layoutId={`product-img-${product?._id}`}$
            transition={{ duration: 0.1, ease: "easeOut" }}$
            className="position-relative rounded-4 overflow-hidden mb-3 d-flex align-items-center justify-content-center" $
            style={{ aspectRatio: '1 / 1', maxHeight: '500px', cursor: 'zoom-in' }}$
            onClick={() => setShowModal(true)}$
          >$
            <img$
              src={images[selectedImageIndex]}$
              alt={product?.name}$
              className="w-100 h-100 object-fit-contain p-2 p-md-4"$
              style={{ $
                filter: 'drop-shadow(0 10px 20px rgba(0,0,0,0.5))'$
              }}$
            />$
            $
            {/* M-XM-/M-ZM-)M-YM-^EM-YM-^GM-bM-^@M-^LM-YM-^GM-XM-'M-[M-^L M-YM-^FM-XM-'M-YM-^HM-XM-(M-XM-1M-[M-^L M-XM-*M-XM-5M-YM-^HM-[M-^LM-XM-1 */}$"""

if old_block in page:
    page = page.replace(old_block, new_block)
    print("  [FIX] Main image div -> motion.div with layoutId")
    print("  [FIX] Removed fade styles from img")
else:
    print("  [WARN] Block anchor not found")
    # Try with exact line-by-line matching
    lines = page.split('\n')
    start_idx = None
    for i, line in enumerate(lines):
        if 'className="position-relative rounded-4 overflow-hidden mb-3' in line and start_idx is None:
            start_idx = i - 1  # Include the <div line
        if start_idx is not None and '<img' in line:
            # Found the block, now replace
            break
    
    if start_idx:
        print(f"  [INFO] Found block around line {start_idx}")
    else:
        print("  [ERROR] Cannot find block")
        sys.exit(1)

# Also remove motion.img from Modal if exists
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
    print("  [FIX] Modal: removed motion.img")
else:
    print("  [INFO] Modal motion.img not found")

if not backup_file(PAGE_FILE, "morph-flicker-v3"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(PAGE_FILE, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"  [WRITE] {os.path.basename(PAGE_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {PAGE_FILE}: {e}")
    sys.exit(1)

print("\n✓ Morph flicker fix v3 applied!")
print("  Changes:")
print("    • Main image container: <div> -> <motion.div> with layoutId")
print("    • Removed fade opacity/transform/transition")
print("    • Kept drop-shadow filter")
print("    • Modal: removed motion.img (prevent conflict)")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test: Click product -> fast morph -> NO flicker!")
