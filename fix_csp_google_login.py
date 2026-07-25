#!/usr/bin/env python3
"""
fix_csp_google_login.py

Adds explicit Content-Security-Policy directives to the helmet() config in
backend/server.js so that:
  - Google Identity Services script (accounts.google.com/gsi/client) can load
    and its login button can render in an iframe (frameSrc + connectSrc too)
  - the cdnjs.cloudflare.com three.js script can load
  - the specific inline script that was being blocked (identified by its
    sha256 hash from the browser console) is allowed to execute

Without this, helmet's default CSP (script-src 'self') silently blocks all
three, which is why the Google login button doesn't work.

Run this from the project root (~/aqualotus/):
    python3 fix_csp_google_login.py

It backs up the file before changing it:
    backend/server.js -> backend/server.js.pre-csp-fix-backup
"""

import os
import shutil
import sys

SERVER_JS = os.path.join("backend", "server.js")

OLD_HELMET_BLOCK = (
    "app.use(\n"
    "  helmet({\n"
    "    crossOriginResourcePolicy: { policy: 'cross-origin' },\n"
    "  })\n"
    ")\n"
)

NEW_HELMET_BLOCK = (
    "app.use(\n"
    "  helmet({\n"
    "    crossOriginResourcePolicy: { policy: 'cross-origin' },\n"
    "    contentSecurityPolicy: {\n"
    "      directives: {\n"
    "        defaultSrc: [\"'self'\"],\n"
    "        scriptSrc: [\n"
    "          \"'self'\",\n"
    "          \"'sha256-leb84nt8JruMyqO8gxVVo/gdvTDvhjgKyIyiZMbMgmU='\",\n"
    "          'https://accounts.google.com',\n"
    "          'https://cdnjs.cloudflare.com',\n"
    "        ],\n"
    "        scriptSrcElem: [\n"
    "          \"'self'\",\n"
    "          'https://accounts.google.com',\n"
    "          'https://cdnjs.cloudflare.com',\n"
    "        ],\n"
    "        frameSrc: [\"'self'\", 'https://accounts.google.com'],\n"
    "        connectSrc: [\"'self'\", 'https://accounts.google.com'],\n"
    "      },\n"
    "    },\n"
    "  })\n"
    ")\n"
)


def backup(path):
    backup_path = path + ".pre-csp-fix-backup"
    if not os.path.exists(backup_path):
        shutil.copy2(path, backup_path)
    return backup_path


def main():
    if not os.path.exists(SERVER_JS):
        print(f"[FAIL] {SERVER_JS} not found. Run this script from ~/aqualotus/")
        sys.exit(1)

    with open(SERVER_JS, "r", encoding="utf-8") as f:
        content = f.read()

    if NEW_HELMET_BLOCK in content:
        print("[INFO] server.js already has the CSP fix applied, no changes needed.")
        sys.exit(0)

    count = content.count(OLD_HELMET_BLOCK)
    if count == 0:
        print("[FAIL] Could not find the expected helmet() block in server.js.")
        print("       The file may have changed since this script was written.")
        print("       No changes were made. Send the output of:")
        print("       sed -n '/helmet(/,/^)/p' backend/server.js")
        sys.exit(1)
    if count > 1:
        print(f"[FAIL] Found the helmet() block {count} times (expected exactly 1).")
        print("       Refusing to guess which one to patch. No changes were made.")
        sys.exit(1)

    backup_path = backup(SERVER_JS)

    new_content = content.replace(OLD_HELMET_BLOCK, NEW_HELMET_BLOCK, 1)
    with open(SERVER_JS, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] backed up to {backup_path}")
    print("[OK] added contentSecurityPolicy directives to helmet() config")
    print("     allowed: accounts.google.com, cdnjs.cloudflare.com, and the")
    print("     one known inline script hash")
    print()
    print("[DONE] Patch applied successfully. ✓")
    print("Next steps:")
    print("  1. Review the diff: git diff backend/server.js")
    print("  2. git add -A && git commit -m 'fix: allow Google login + cdnjs scripts through CSP'")
    print("  3. git push")
    print("  4. Redeploy on Runflare (استقرار جدید -> GIT tab -> pick the new commit)")
    print("  5. Hard-refresh https://aqualotus.ir/login and check the Console tab again")
    print("     for any REMAINING CSP errors (there may be others we haven't seen yet —")
    print("     if so, send the new console output and we'll add exactly those to the list)")


if __name__ == "__main__":
    main()
