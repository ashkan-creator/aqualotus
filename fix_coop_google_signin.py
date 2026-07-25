#!/usr/bin/env python3
"""
fix_coop_google_signin.py

Root cause (per Google's own official Sign In With Google documentation):
helmet() has no explicit crossOriginOpenerPolicy, so it defaults to
"Cross-Origin-Opener-Policy: same-origin" (confirmed via curl -Ik on the
live site). This fully isolates the browsing context of our page from any
popup/iframe opened by a different origin -- including Google's own GSI
library, which relies on postMessage back and forth between our page and
its own iframe/popup during the sign-in handshake. With COOP: same-origin,
the browser severs that cross-origin window reference, so when Google's
code tries `otherWindow.postMessage(...)`, otherWindow is null -- which is
EXACTLY the "Cannot read properties of null (reading 'postMessage')" error
seen on accounts.google.com/gsi/transform.

Google's documentation for this exact scenario recommends:
  Cross-Origin-Opener-Policy: same-origin-allow-popups
This keeps the isolation benefits for same-origin windows while still
allowing postMessage communication with popups/iframes your page opens
(such as Google's own sign-in popup), which is required for GSI to work.

Run this from the project root (~/aqualotus/):
    python3 fix_coop_google_signin.py

Backs up backend/server.js first:
    backend/server.js -> backend/server.js.pre-coop-fix-backup
"""

import os
import shutil
import sys

SERVER_JS = os.path.join("backend", "server.js")

OLD_ANCHOR = (
    "    crossOriginResourcePolicy: { policy: 'cross-origin' },\n"
    "    referrerPolicy: { policy: 'strict-origin-when-cross-origin' },\n"
)

NEW_ANCHOR = (
    "    crossOriginResourcePolicy: { policy: 'cross-origin' },\n"
    "    crossOriginOpenerPolicy: { policy: 'same-origin-allow-popups' },\n"
    "    referrerPolicy: { policy: 'strict-origin-when-cross-origin' },\n"
)


def backup(path):
    backup_path = path + ".pre-coop-fix-backup"
    if not os.path.exists(backup_path):
        shutil.copy2(path, backup_path)
    return backup_path


def main():
    if not os.path.exists(SERVER_JS):
        print(f"[FAIL] {SERVER_JS} not found. Run this script from ~/aqualotus/")
        sys.exit(1)

    with open(SERVER_JS, "r", encoding="utf-8") as f:
        content = f.read()

    if NEW_ANCHOR in content:
        print("[INFO] server.js already has crossOriginOpenerPolicy set correctly, no changes needed.")
        sys.exit(0)

    count = content.count(OLD_ANCHOR)
    if count == 0:
        print("[FAIL] Could not find the expected helmet() config anchor in server.js.")
        print("       The file may have changed since this script was written.")
        print("       No changes were made. Send the output of:")
        print("       sed -n '/helmet(/,/contentSecurityPolicy/p' backend/server.js")
        sys.exit(1)
    if count > 1:
        print(f"[FAIL] Found the anchor {count} times (expected exactly 1).")
        print("       Refusing to guess which one to patch. No changes were made.")
        sys.exit(1)

    backup_path = backup(SERVER_JS)

    new_content = content.replace(OLD_ANCHOR, NEW_ANCHOR, 1)
    with open(SERVER_JS, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] backed up to {backup_path}")
    print("[OK] added crossOriginOpenerPolicy: { policy: 'same-origin-allow-popups' } to helmet() config")
    print()
    print("[DONE] Patch applied successfully. ✓")
    print("Next steps:")
    print("  1. Review the diff: git diff backend/server.js")
    print("  2. git add -A && git commit -m 'fix: allow popups in COOP so Google Sign-In postMessage works'")
    print("  3. git push")
    print("  4. Redeploy on Runflare, then hard-refresh /login in a clean incognito tab")
    print("     (no DevTools device emulation, no VPN browser extension) and click Google button")


if __name__ == "__main__":
    main()
