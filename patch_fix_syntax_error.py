#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix: Remove extra /> on line 183
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

# Find and remove extra />
removed = False
for i, line in enumerate(lines):
    stripped = line.strip()
    # Look for standalone /> (not part of <img/> or <div/>)
    if stripped == '/>' and i > 0:
        prev_line = lines[i-1].strip()
        # If previous line ends with /> , this one is extra
        if prev_line.endswith('/>'):
            print(f"  [REMOVE] Extra /> at line {i+1}")
            del lines[i]
            removed = True
            break

if not removed:
    # Alternative: check line 183 specifically
    if len(lines) >= 183 and lines[182].strip() == '/>':
        print("  [REMOVE] Extra /> at line 183")
        del lines[182]
        removed = True

if not removed:
    print("  [WARN] Could not find extra />")
    sys.exit(1)

if not backup_file(PAGE_FILE, "syntax-fix"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(PAGE_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"  [WRITE] {os.path.basename(PAGE_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {PAGE_FILE}: {e}")
    sys.exit(1)

print("\n✓ Syntax error fixed!")
print("  Removed extra />")
print("\n  Next steps:")
print("    1. Restart Vite server (Ctrl+C then npm run dev)")
print("    2. Test in browser")
