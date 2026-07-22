#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch v4: Fix flicker - line by line replacement
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
    lines = f.readlines()

# Find the block to replace (lines 168-182, 0-indexed: 167-181)
start_line = 167  # line 168 (0-indexed)
end_line = 181    # line 182 (0-indexed)

# Verify content
expected_start = '          <div \n'
expected_img = '            <img\n'

if lines[start_line] == expected_start and expected_img in lines[start_line+4]:
    print(f"  [FOUND] Block at lines {start_line+1}-{end_line+1}")
else:
    print(f"  [WARN] Expected block not at lines {start_line+1}-{end_line+1}")
    # Search for it
    for i, line in enumerate(lines):
        if 'className="position-relative rounded-4 overflow-hidden mb-3' in line:
            start_line = i - 1
            print(f"  [FOUND] Block at lines {start_line+1}")
            break

# Build new block
new_block = [
    '          <motion.div \n',
    '            layoutId={`product-img-${product?._id}`}\n',
    '            transition={{ duration: 0.1, ease: "easeOut" }}\n',
    '            className="position-relative rounded-4 overflow-hidden mb-3 d-flex align-items-center justify-content-center" \n',
    '            style={{ aspectRatio: \'1 / 1\', maxHeight: \'500px\', cursor: \'zoom-in\' }}\n',
    '            onClick={() => setShowModal(true)}\n',
    '          >\n',
    '            <img\n',
    '              src={images[selectedImageIndex]}\n',
    '              alt={product?.name}\n',
    '              className="w-100 h-100 object-fit-contain p-2 p-md-4"\n',
    '              style={{ \n',
    '                filter: \'drop-shadow(0 10px 20px rgba(0,0,0,0.5))\'\n',
    '              }}\n',
    '            />\n',
]

# Replace lines
new_lines = lines[:start_line] + new_block + lines[end_line+1:]

if not backup_file(PAGE_FILE, "morph-flicker-v4"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(PAGE_FILE, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"  [WRITE] {os.path.basename(PAGE_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {PAGE_FILE}: {e}")
    sys.exit(1)

print("\n✓ Morph flicker fix v4 applied!")
print("  Changes:")
print("    • <div> -> <motion.div> with layoutId")
print("    • Removed fade opacity/transform/transition")
print("    • Kept drop-shadow filter")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test: Click product -> fast morph -> NO flicker!")
