#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch v4: ProductCard 3D Tilt - Add logo back, higher transparency
Changes:
  1. Add logo image back to glass header
  2. Higher card transparency: 0.75 -> 0.88
  3. Higher body transparency: 0.75 -> 0.88
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

with open(TARGET_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add logo back to glass header
old_header_inner = r"""            <div className="d-flex justify-content-between align-items-center">
              <div style={{ flex: 1, minWidth: 0, overflow: 'hidden' }}>
                <h6 style={{
                  margin: 0, fontSize: '0.78rem', fontWeight: 700,
                  lineHeight: 1.2, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  {product.name}
                </h6>
                <p style={{
                  margin: '2px 0 0', fontSize: '0.62rem', color: 'rgba(255,255,255,0.75)',
                  overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  محل کاشت: {product.position || product.careLevel || '—'}
                </p>
              </div>
            </div>"""

new_header_inner = r"""            <div className="d-flex justify-content-between align-items-center">
              <div style={{ flex: 1, minWidth: 0, overflow: 'hidden' }}>
                <h6 style={{
                  margin: 0, fontSize: '0.78rem', fontWeight: 700,
                  lineHeight: 1.2, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  {product.name}
                </h6>
                <p style={{
                  margin: '2px 0 0', fontSize: '0.62rem', color: 'rgba(255,255,255,0.75)',
                  overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  محل کاشت: {product.position || product.careLevel || '—'}
                </p>
              </div>
              <div style={{ marginRight: '6px', flexShrink: 0 }}>
                <img
                  src="/logo.png"
                  alt="AquaLotus"
                  style={{ height: '14px', width: 'auto', opacity: 0.7 }}
                  onError={(e) => { e.target.style.display = 'none' }}
                />
              </div>
            </div>"""

if old_header_inner in content:
    content = content.replace(old_header_inner, new_header_inner)
    print("  [ADD] Logo back to glass header")
else:
    print("  [WARN] Header inner anchor not found")

# 2. Higher body transparency
old_body_bg = "background: 'rgba(10,10,10,0.75)',"
new_body_bg = "background: 'rgba(10,10,10,0.88)',"

if old_body_bg in content:
    content = content.replace(old_body_bg, new_body_bg)
    print("  [UPDATE] Body transparency: 0.75 -> 0.88")
else:
    print("  [WARN] Body bg anchor not found")

# Backup and write
if not backup_file(TARGET_FILE, "productcard-3dtilt-v4"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [WRITE] {os.path.basename(TARGET_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {TARGET_FILE}: {e}")
    sys.exit(1)

# 3. Update CSS transparency
with open(CSS_FILE, 'r', encoding='utf-8') as f:
    css_content = f.read()

old_css_bg = "background: rgba(15, 15, 15, 0.75);"
new_css_bg = "background: rgba(15, 15, 15, 0.88);"

if old_css_bg in css_content:
    css_content = css_content.replace(old_css_bg, new_css_bg)
    print("  [UPDATE] CSS card transparency: 0.75 -> 0.88")
else:
    print("  [WARN] CSS bg anchor not found")

try:
    with open(CSS_FILE, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"  [WRITE] {os.path.basename(CSS_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing CSS: {e}")
    sys.exit(1)

print("\n✓ ProductCard 3D Tilt v4 applied successfully!")
print("  Changes:")
print("    • Logo added back to glass header")
print("    • Card transparency: 0.75 -> 0.88")
print("    • Body transparency: 0.75 -> 0.88")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test in Incognito window")
