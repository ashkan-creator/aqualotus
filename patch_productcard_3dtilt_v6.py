#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch v6: ProductCard 3D Tilt - Slightly smaller title font
Change: Title fontSize 0.78rem -> 0.72rem
"""

import os
import shutil
import sys

BASE_DIR = os.path.expanduser("~/aqualotus/frontend")
TARGET_FILE = os.path.join(BASE_DIR, "src", "components", "ui", "ProductCard.jsx")

def backup_file(path, suffix):
    if os.path.exists(path):
        backup_path = path.replace(".jsx", f".pre-{suffix}-backup.jsx")
        if not os.path.exists(backup_path):
            shutil.copy2(path, backup_path)
            print(f"  [BACKUP] {os.path.basename(path)} -> {os.path.basename(backup_path)}")
        else:
            print(f"  [SKIP BACKUP] {os.path.basename(backup_path)} already exists")
        return True
    print(f"  [ERROR] File not found: {path}")
    return False

with open(TARGET_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

old_title = "fontSize: '0.78rem', fontWeight: 700,"
new_title = "fontSize: '0.72rem', fontWeight: 700,"

if old_title in content:
    content = content.replace(old_title, new_title)
    print("  [UPDATE] Title fontSize: 0.78rem -> 0.72rem")
else:
    print("  [WARN] Title font anchor not found")

if not backup_file(TARGET_FILE, "productcard-3dtilt-v6"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [WRITE] {os.path.basename(TARGET_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {TARGET_FILE}: {e}")
    sys.exit(1)

print("\n✓ ProductCard 3D Tilt v6 applied successfully!")
print("  Changes:")
print("    • Title fontSize: 0.78rem -> 0.72rem")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test in Incognito window")
