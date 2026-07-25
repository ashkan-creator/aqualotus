#!/usr/bin/env python3
"""
fix_csp_scriptsrcelem_hash.py

Follow-up to fix_csp_google_login.py: that script added the inline-script
hash to `scriptSrc` but forgot to also add it to `scriptSrcElem`. Since
scriptSrcElem is explicitly set, browsers use it (not scriptSrc) to decide
whether to allow <script> elements, including inline ones — so the inline
script was still being blocked. This adds the same hash to scriptSrcElem.

Run this from the project root (~/aqualotus/):
    python3 fix_csp_scriptsrcelem_hash.py

Backs up the file before changing it:
    backend/server.js -> backend/server.js.pre-csp-scriptsrcelem-backup
"""

import os
import shutil
import sys

SERVER_JS = os.path.join("backend", "server.js")

OLD_SCRIPT_SRC_ELEM = (
    "        scriptSrcElem: [\n"
    "          \"'self'\",\n"
    "          'https://accounts.google.com',\n"
    "          'https://cdnjs.cloudflare.com',\n"
    "        ],\n"
)

NEW_SCRIPT_SRC_ELEM = (
    "        scriptSrcElem: [\n"
    "          \"'self'\",\n"
    "          \"'sha256-leb84nt8JruMyqO8gxVVo/gdvTDvhjgKyIyiZMbMgmU='\",\n"
    "          'https://accounts.google.com',\n"
    "          'https://cdnjs.cloudflare.com',\n"
    "        ],\n"
)


def backup(path):
    backup_path = path + ".pre-csp-scriptsrcelem-backup"
    if not os.path.exists(backup_path):
        shutil.copy2(path, backup_path)
    return backup_path


def main():
    if not os.path.exists(SERVER_JS):
        print(f"[FAIL] {SERVER_JS} not found. Run this script from ~/aqualotus/")
        sys.exit(1)

    with open(SERVER_JS, "r", encoding="utf-8") as f:
        content = f.read()

    if NEW_SCRIPT_SRC_ELEM in content:
        print("[INFO] server.js already has the hash in scriptSrcElem, no changes needed.")
        sys.exit(0)

    count = content.count(OLD_SCRIPT_SRC_ELEM)
    if count == 0:
        print("[FAIL] Could not find the expected scriptSrcElem block in server.js.")
        print("       The file may have changed since this script was written.")
        print("       No changes were made. Send the output of:")
        print("       sed -n '/contentSecurityPolicy/,/^    }/p' backend/server.js")
        sys.exit(1)
    if count > 1:
        print(f"[FAIL] Found the scriptSrcElem block {count} times (expected exactly 1).")
        print("       Refusing to guess which one to patch. No changes were made.")
        sys.exit(1)

    backup_path = backup(SERVER_JS)

    new_content = content.replace(OLD_SCRIPT_SRC_ELEM, NEW_SCRIPT_SRC_ELEM, 1)
    with open(SERVER_JS, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] backed up to {backup_path}")
    print("[OK] added the inline-script hash to scriptSrcElem")
    print()
    print("[DONE] Patch applied successfully. ✓")
    print("Next steps:")
    print("  1. Review the diff: git diff backend/server.js")
    print("  2. git add -A && git commit -m 'fix: add inline script hash to scriptSrcElem CSP directive'")
    print("  3. git push")
    print("  4. Redeploy on Runflare, then hard-refresh /login and check Console again")


if __name__ == "__main__":
    main()
