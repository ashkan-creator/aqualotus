#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix: Change </div> to </motion.div> on line 227
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

# Find <motion.div> and its corresponding </div>
motion_line = None
closing_line = None

for i, line in enumerate(lines):
    if '<motion.div' in line:
        motion_line = i
        print(f"  [FOUND] <motion.div> at line {i+1}")
    if motion_line is not None and '</div>' in line and closing_line is None:
        # Check if this </div> is after <motion.div> and not nested
        closing_line = i
        print(f"  [FOUND] </div> at line {i+1} (should be </motion.div>)")
        break

if motion_line is None:
    print("  [ERROR] <motion.div> not found")
    sys.exit(1)

if closing_line is None:
    print("  [ERROR] Closing </div> not found")
    sys.exit(1)

# Replace </div> with </motion.div>
lines[closing_line] = lines[closing_line].replace('</div>', '</motion.div>')
print(f"  [FIX] Line {closing_line+1}: </div> -> </motion.div>")

if not backup_file(PAGE_FILE, "closing-tag-fix"):
    print("[ABORT] Backup failed.")
    sys.exit(1)

try:
    with open(PAGE_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"  [WRITE] {os.path.basename(PAGE_FILE)}")
except Exception as e:
    print(f"  [ERROR] Writing {PAGE_FILE}: {e}")
    sys.exit(1)

print("\n✓ Closing tag fixed!")
print("  </div> -> </motion.div>")
print("\n  Next steps:")
print("    1. Restart Vite server (Ctrl+C then npm run dev)")
print("    2. Test in browser")
