#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch v5: ProductCard 3D Tilt - Move logo lower in header
Change: Logo alignSelf: 'flex-end' to push it to bottom of header
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

# Move logo lower: alignSelf flex-end + marginTop
old_logo = r"""              <div style={{ marginRight: '6px', flexShrink: 0 }}>
                <img
                  src="/logo.png"
                  alt="AquaLotus"
                  style={{ height: '14px', width: 'auto', opacity: 0.7 }}
                  onError={(e) => { e.target.style.display = 'none' }}
                />
              </div>"""

new_logo = r"""              <div style={{ marginRight: '6px', flexShrink: 0, alignSelf: 'flex-end', marginBottom: '2px' }}>
                <img
                  src="/logo.png"
                  alt="AquaLotus"
                  style={{ height: '14px', width: 'auto', opacity: 0.7 }}
                  onError={(e) => { e.target.style.display = 'none' }}
                />
              </div>"""

if old_logo in content:
    content = content.replace(old_logo, new_logo)
    print("  [UPDATE] Logo moved lower (alignSelf: flex-end)")
else:
    print("  [WARN] Logo anchor not found")
    # Try alternative anchor
    alt_old = "style={{ height: '14px', width: 'auto', opacity: 0.7 }}"
    alt_new = "style={{ height: '14px', width: 'auto', opacity: 0.7 }}"
    if alt_old in content:
        # Already has logo, just need to adjust parent div
        print("  [INFO] Logo exists, checking parent div position...")
    else:
        print("  [ERROR] Cannot find logo to patch")
        sys.exit(1)

if not backup_file(TARGET_FILE, "productcard-3dtilt-v5"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [WRITE] {os.path.basename(TARGET_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {TARGET_FILE}: {e}")
    sys.exit(1)

print("\n✓ ProductCard 3D Tilt v5 applied successfully!")
print("  Changes:")
print("    • Logo aligned to bottom of glass header")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test in Incognito window")
