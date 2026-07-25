#!/usr/bin/env python3
"""
fix_vite_google_client_id_build.py

Root cause: frontend/.env exists locally but is gitignored (matched by the
".env" rule in .gitignore), so it never reaches Runflare's build. Vite's
`npm run build` in the Dockerfile therefore never sees VITE_GOOGLE_CLIENT_ID,
and the Google login button silently fails to initialize.

Fix: create frontend/.env.production (a different filename, NOT covered by
the ".env" gitignore rule) containing VITE_GOOGLE_CLIENT_ID. This is safe to
commit because a Google OAuth Client ID is a public identifier, not a secret
-- it's meant to ship in frontend code.

Run this from the project root (~/aqualotus/):
    python3 fix_vite_google_client_id_build.py

Backs up frontend/.env.production first if it already exists.
"""

import os
import re
import shutil
import sys

SOURCE_ENV = os.path.join("frontend", ".env")
TARGET_ENV = os.path.join("frontend", ".env.production")


def main():
    if not os.path.exists(SOURCE_ENV):
        print(f"[FAIL] {SOURCE_ENV} not found. Run this script from ~/aqualotus/")
        sys.exit(1)

    with open(SOURCE_ENV, "r", encoding="utf-8") as f:
        source_lines = f.readlines()

    client_id_line = None
    for line in source_lines:
        if line.strip().startswith("VITE_GOOGLE_CLIENT_ID="):
            client_id_line = line.strip()
            break

    if not client_id_line:
        print(f"[FAIL] Could not find VITE_GOOGLE_CLIENT_ID= in {SOURCE_ENV}. Aborting, no changes made.")
        sys.exit(1)

    if os.path.exists(TARGET_ENV):
        backup_path = TARGET_ENV + ".pre-viteclientid-backup"
        if not os.path.exists(backup_path):
            shutil.copy2(TARGET_ENV, backup_path)
        with open(TARGET_ENV, "r", encoding="utf-8") as f:
            existing = f.read()
        if client_id_line in existing:
            print(f"[INFO] {TARGET_ENV} already contains the correct VITE_GOOGLE_CLIENT_ID line, no changes needed.")
            sys.exit(0)
        print(f"[OK] backed up existing {TARGET_ENV} to {backup_path}")
        # Replace existing VITE_GOOGLE_CLIENT_ID line if present, else append
        if re.search(r"^VITE_GOOGLE_CLIENT_ID=.*$", existing, flags=re.M):
            new_content = re.sub(r"^VITE_GOOGLE_CLIENT_ID=.*$", client_id_line, existing, flags=re.M)
        else:
            new_content = existing.rstrip("\n") + "\n" + client_id_line + "\n"
    else:
        new_content = client_id_line + "\n"

    with open(TARGET_ENV, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] wrote {TARGET_ENV} with:")
    print(f"     {client_id_line}")
    print()
    print("[DONE] Patch applied successfully. ✓")
    print("Next steps:")
    print(f"  1. Confirm it will actually be committed (not accidentally gitignored):")
    print(f"     git check-ignore -v {TARGET_ENV}")
    print(f"     (should print NOTHING -- if it prints something, stop and tell Claude)")
    print(f"  2. git add {TARGET_ENV}")
    print(f"     git commit -m 'fix: add frontend/.env.production so Vite build has VITE_GOOGLE_CLIENT_ID'")
    print(f"     git push")
    print(f"  3. Redeploy on Runflare, then hard-refresh /login and check the Google button appears")


if __name__ == "__main__":
    main()
