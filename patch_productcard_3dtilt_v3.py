#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch v3: ProductCard 3D Tilt - Remove stock dot, wider header, more transparent
Changes:
  1. Remove stock indicator dot (green/grey circle)
  2. Wider glass header: right: 10px instead of 24px
  3. More transparent header: rgba(0,0,0,0.25)
"""

import os
import shutil
import sys

BASE_DIR = os.path.expanduser("~/aqualotus/frontend")
TARGET_FILE = os.path.join(BASE_DIR, "src", "components", "ui", "ProductCard.jsx")
CSS_FILE = os.path.join(BASE_DIR, "src", "index.css")

def backup_file(path, suffix):
    if os.path.exists(path):
        backup_path = path.replace(".jsx", f".pre-{suffix}-backup.jsx").replace(".css", f".pre-{suffix}-backup.css")
        if not os.path.exists(backup_path):
            shutil.copy2(path, backup_path)
            print(f"  [BACKUP] {os.path.basename(path)} -> {os.path.basename(backup_path)}")
        else:
            print(f"  [SKIP BACKUP] {os.path.basename(backup_path)} already exists")
        return True
    print(f"  [ERROR] File not found: {path}")
    return False

# Read current ProductCard.jsx
with open(TARGET_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove stock indicator block
old_stock = r"""          {/* Stock Indicator */}
          <div style={{
            position: 'absolute', top: '10px', right: '10px', zIndex: 5,
            width: '8px', height: '8px', borderRadius: '50%',
            backgroundColor: inStock ? '#52b788' : '#6c757d',
            animation: inStock ? 'aq-pulse 2s infinite' : 'none',
          }} />"""

if old_stock in content:
    content = content.replace(old_stock, "")
    print("  [REMOVE] Stock indicator dot")
else:
    print("  [WARN] Stock indicator anchor not found")

# 2. Wider header + more transparent
old_header = r"""          {/* Glassmorphism Header - Small, next to wishlist button */}
          <div style={{
            position: 'absolute', top: '10px', left: '50px', right: '24px', zIndex: 3,
            padding: '5px 10px',
            borderRadius: '10px',
            border: '1px solid rgba(255,255,255,0.1)',
            background: 'rgba(0,0,0,0.4)',
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
            color: '#fff',
            transform: 'translateZ(30px)',
          }}>"""

new_header = r"""          {/* Glassmorphism Header - Small, next to wishlist button */}
          <div style={{
            position: 'absolute', top: '10px', left: '50px', right: '10px', zIndex: 3,
            padding: '5px 10px',
            borderRadius: '10px',
            border: '1px solid rgba(255,255,255,0.08)',
            background: 'rgba(0,0,0,0.25)',
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
            color: '#fff',
            transform: 'translateZ(30px)',
          }}>"""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("  [UPDATE] Glass header: wider (right:10px) + more transparent (0.25)")
else:
    print("  [WARN] Glass header anchor not found")

# Backup and write
if not backup_file(TARGET_FILE, "productcard-3dtilt-v3"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [WRITE] {os.path.basename(TARGET_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {TARGET_FILE}: {e}")
    sys.exit(1)

print("\n✓ ProductCard 3D Tilt v3 applied successfully!")
print("  Changes:")
print("    • Removed stock indicator dot")
print("    • Glass header: wider (right:10px)")
print("    • Glass header: more transparent (rgba(0,0,0,0.25))")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test in Incognito window")
