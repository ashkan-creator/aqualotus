#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix: Correct closing tags for motion.div
Line 209: </motion.div> -> </div>
Line 227: </div> -> </motion.div>
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

# Fix line 209: </motion.div> -> </div>
if len(lines) >= 209:
    line209 = lines[208]
    if '</motion.div>' in line209:
        lines[208] = line209.replace('</motion.div>', '</div>')
        print("  [FIX] Line 209: </motion.div> -> </div>")
    else:
        print(f"  [WARN] Line 209: expected </motion.div>, found: {line209.strip()}")
else:
    print("  [ERROR] File has less than 209 lines")

# Fix line 227: </div> -> </motion.div>
if len(lines) >= 227:
    line227 = lines[226]
    if '</div>' in line227:
        lines[226] = line227.replace('</div>', '</motion.div>')
        print("  [FIX] Line 227: </div> -> </motion.div>")
    else:
        print(f"  [WARN] Line 227: expected </div>, found: {line227.strip()}")
else:
    print("  [ERROR] File has less than 227 lines")

if not backup_file(PAGE_FILE, "tag-fix"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(PAGE_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"  [WRITE] {os.path.basename(PAGE_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {PAGE_FILE}: {e}")
    sys.exit(1)

print("\n✓ Both closing tags fixed!")
print("  Line 209: </motion.div> -> </div>")
print("  Line 227: </div> -> </motion.div>")
print("\n  Next steps:")
print("    1. Restart Vite server (Ctrl+C then npm run dev)")
print("    2. Test in browser")
