#!/usr/bin/env python3
"""
fix_compression_and_cache.py

Adds gzip compression middleware and Cache-Control headers for static
assets (product image uploads + built frontend files) to backend/server.js,
and adds the `compression` package to package.json.

Run this from the project root (~/aqualotus/):
    python3 fix_compression_and_cache.py

It backs up every file it touches before changing it:
    backend/server.js       -> backend/server.js.pre-compression-cache-backup
    package.json             -> package.json.pre-compression-cache-backup
"""

import json
import os
import shutil
import sys

SERVER_JS = os.path.join("backend", "server.js")
PACKAGE_JSON = "package.json"


def backup(path):
    backup_path = path + ".pre-compression-cache-backup"
    if not os.path.exists(backup_path):
        shutil.copy2(path, backup_path)
    return backup_path


def patch_server_js():
    if not os.path.exists(SERVER_JS):
        print(f"[FAIL] {SERVER_JS} not found. Run this script from ~/aqualotus/")
        return False

    with open(SERVER_JS, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes_made = []

    # 1. Add the compression import, right after the express-mongo-sanitize import
    import_anchor = "import mongoSanitize from 'express-mongo-sanitize'\n"
    if import_anchor not in content:
        print("[FAIL] Could not find import anchor for compression import. Aborting, no changes made.")
        return False
    if "import compression from 'compression'" not in content:
        content = content.replace(
            import_anchor,
            import_anchor + "import compression from 'compression'\n",
            1,
        )
        changes_made.append("added compression import")

    # 2. Add app.use(compression()) right after the helmet() block
    helmet_anchor = (
        "app.use(\n"
        "  helmet({\n"
        "    crossOriginResourcePolicy: { policy: 'cross-origin' },\n"
        "  })\n"
        ")\n"
    )
    if helmet_anchor not in content:
        print("[FAIL] Could not find helmet() anchor block. Aborting, no changes made.")
        return False
    if "app.use(compression())" not in content:
        content = content.replace(
            helmet_anchor,
            helmet_anchor + "\napp.use(compression())\n",
            1,
        )
        changes_made.append("added app.use(compression())")

    # 3. Add Cache-Control to the /uploads static route (product images)
    old_uploads_static = (
        "app.use('/uploads', express.static(path.join(__dirname, '../uploads')))\n"
    )
    new_uploads_static = (
        "app.use(\n"
        "  '/uploads',\n"
        "  express.static(path.join(__dirname, '../uploads'), {\n"
        "    maxAge: '7d',\n"
        "  })\n"
        ")\n"
    )
    if old_uploads_static in content:
        content = content.replace(old_uploads_static, new_uploads_static, 1)
        changes_made.append("added 7-day Cache-Control to /uploads static route")
    elif new_uploads_static in content:
        pass  # already patched
    else:
        print("[FAIL] Could not find the /uploads express.static line as expected. Aborting, no changes made.")
        return False

    # 4. Add Cache-Control to the frontend/dist static route (JS/CSS/assets),
    #    but exclude index.html from caching so future deploys show up immediately.
    old_dist_static = (
        "app.use(express.static(path.join(__dirname, '../frontend/dist')))\n"
    )
    new_dist_static = (
        "app.use(\n"
        "  express.static(path.join(__dirname, '../frontend/dist'), {\n"
        "    maxAge: '1d',\n"
        "    index: false,\n"
        "  })\n"
        ")\n"
    )
    if old_dist_static in content:
        content = content.replace(old_dist_static, new_dist_static, 1)
        changes_made.append("added 1-day Cache-Control to frontend/dist static route (index.html excluded)")
    elif new_dist_static in content:
        pass  # already patched
    else:
        print("[FAIL] Could not find the frontend/dist express.static line as expected. Aborting, no changes made.")
        return False

    if content == original:
        print("[INFO] server.js already patched, no changes needed.")
        return True

    backup_path = backup(SERVER_JS)
    with open(SERVER_JS, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] backed up to {backup_path}")
    for c in changes_made:
        print(f"[OK] {c}")
    return True


def patch_package_json():
    if not os.path.exists(PACKAGE_JSON):
        print(f"[FAIL] {PACKAGE_JSON} not found. Run this script from ~/aqualotus/")
        return False

    with open(PACKAGE_JSON, "r", encoding="utf-8") as f:
        raw = f.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[FAIL] Could not parse package.json as JSON: {e}. Aborting, no changes made.")
        return False

    if "dependencies" not in data or not isinstance(data["dependencies"], dict):
        print("[FAIL] No 'dependencies' object found in package.json. Aborting, no changes made.")
        return False

    if "compression" in data["dependencies"]:
        print("[INFO] package.json already has compression as a dependency, no changes needed.")
        return True

    backup_path = backup(PACKAGE_JSON)

    data["dependencies"]["compression"] = "^1.7.4"
    # sort dependencies alphabetically to match common package.json convention
    data["dependencies"] = dict(sorted(data["dependencies"].items()))

    with open(PACKAGE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"[OK] backed up to {backup_path}")
    print("[OK] added \"compression\": \"^1.7.4\" to dependencies")
    return True


def main():
    print("=== Patching backend/server.js ===")
    ok1 = patch_server_js()
    print()
    print("=== Patching package.json ===")
    ok2 = patch_package_json()
    print()
    if ok1 and ok2:
        print("[DONE] All patches applied successfully. ✓")
        print("Next steps:")
        print("  1. Review the diff: git diff backend/server.js package.json")
        print("  2. npm install   (to install compression locally / update package-lock.json)")
        print("  3. git add -A && git commit -m 'perf: add gzip compression + cache-control for static assets'")
        print("  4. git push   (uses SSH remote)")
        print("  5. Redeploy on Runflare (استقرار جدید -> GIT tab -> pick the new commit)")
        sys.exit(0)
    else:
        print("[DONE] One or more patches failed. ✗ No partial changes were left in place for the failed file(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
