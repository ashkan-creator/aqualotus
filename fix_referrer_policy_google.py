#!/usr/bin/env python3
"""
fix_referrer_policy_google.py

Root cause: helmet() has no explicit referrerPolicy, so it defaults to
"Referrer-Policy: no-referrer" -- confirmed via curl -Ik on the live site.
This suppresses the Referer header on ALL cross-origin requests, including
the request to Google's GSI button iframe (accounts.google.com/gsi/button),
which Google partly relies on to verify the embedding origin. Without a
Referer, Google can't confirm the origin even though it IS correctly
registered in Cloud Console -- producing a persistent origin_mismatch/400
that has nothing to do with Google Cloud Console settings.

Fix: add referrerPolicy: { policy: 'strict-origin-when-cross-origin' } to
the same helmet() config. This is a widely-used safe default (sends only
the origin, not the full URL, to cross-origin destinations) and is what
most browsers use as their own default when a site sets no policy at all.

Run this from the project root (~/aqualotus/):
    python3 fix_referrer_policy_google.py

Backs up backend/server.js first:
    backend/server.js -> backend/server.js.pre-referrerpolicy-backup
"""

import os
import shutil
import sys

SERVER_JS = os.path.join("backend", "server.js")

OLD_ANCHOR = (
    "    crossOriginResourcePolicy: { policy: 'cross-origin' },\n"
    "    contentSecurityPolicy: {\n"
)

NEW_ANCHOR = (
    "    crossOriginResourcePolicy: { policy: 'cross-origin' },\n"
    "    referrerPolicy: { policy: 'strict-origin-when-cross-origin' },\n"
    "    contentSecurityPolicy: {\n"
)


def backup(path):
    backup_path = path + ".pre-referrerpolicy-backup"
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
        print("[INFO] server.js already has referrerPolicy set, no changes needed.")
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
    print("[OK] added referrerPolicy: { policy: 'strict-origin-when-cross-origin' } to helmet() config")
    print()
    print("[DONE] Patch applied successfully. ✓")
    print("Next steps:")
    print("  1. Review the diff: git diff backend/server.js")
    print("  2. git add -A && git commit -m 'fix: set referrer-policy to strict-origin-when-cross-origin for Google login'")
    print("  3. git push")
    print("  4. Redeploy on Runflare, then hard-refresh /login (incognito, no device emulation)")
    print("     and click the Google button again")


if __name__ == "__main__":
    main()
