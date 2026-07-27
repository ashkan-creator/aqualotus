#!/usr/bin/env python3
"""
فیکس باگ پولینگ ۴۰۱ تکراری تو NotificationBell و CustomerNotificationBell

مشکل: useGetUnreadCountQuery / useGetMyUnreadCountQuery با pollingInterval:30000
صدا زده میشن بدون هیچ گارد skip ای. چون این دو کامپوننت تو Header.jsx (لایه‌ی
مشترک همه‌ی صفحات) mount میشن، حتی رو صفحه‌ی /login (قبل از لاگین) هر ۳۰ ثانیه
درخواست میره و ۴۰۱ می‌گیره.

فیکس: اضافه‌کردن userInfo از redux auth state (دقیقاً همون الگویی که تو
ProductCard.jsx برای wishlist استفاده شده) و skip:!userInfo رو کوئری.

قبل از هر تغییری، بک‌آپ می‌گیره: <file>.pre-notification-401-fix-backup

نحوه‌ی اجرا:
    cp fix_notification_401_polling.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_notification_401_polling.py
"""

import re
import sys
from pathlib import Path

FILES = [
    {
        "path": Path("frontend/src/components/ui/CustomerNotificationBell.jsx"),
        "import_anchor": "import { FaBell } from 'react-icons/fa'",
        "hook_old": (
            "  const { data: unreadData } = useGetMyUnreadCountQuery(undefined, {\n"
            "    pollingInterval: 30000,\n"
            "  })"
        ),
        "hook_new": (
            "  const { userInfo } = useSelector((state) => state.auth)\n"
            "  const { data: unreadData } = useGetMyUnreadCountQuery(undefined, {\n"
            "    skip: !userInfo,\n"
            "    pollingInterval: 30000,\n"
            "  })"
        ),
    },
    {
        "path": Path("frontend/src/components/ui/NotificationBell.jsx"),
        "import_anchor": "import { FaBell } from 'react-icons/fa'",
        "hook_old": (
            "  const { data: unreadData } = useGetUnreadCountQuery(undefined, {\n"
            "    pollingInterval: 30000,\n"
            "  })"
        ),
        "hook_new": (
            "  const { userInfo } = useSelector((state) => state.auth)\n"
            "  const { data: unreadData } = useGetUnreadCountQuery(undefined, {\n"
            "    skip: !userInfo,\n"
            "    pollingInterval: 30000,\n"
            "  })"
        ),
    },
]

IMPORT_LINE = "import { useSelector } from 'react-redux'\n"


def patch_file(entry):
    path = entry["path"]
    if not path.exists():
        print(f"❌ فایل پیدا نشد: {path.resolve()}")
        return False

    content = path.read_text(encoding="utf-8")

    if "useSelector" in content and "react-redux" in content:
        print(f"ℹ️  {path}: ایمپورت useSelector از قبل هست، این قسمت رو رد می‌کنم.")
        already_imported = True
    else:
        already_imported = False

    if entry["hook_new"] in content:
        print(f"⚠️  {path}: به‌نظر می‌رسه قبلاً فیکس شده. رد می‌کنم.")
        return True

    if entry["hook_old"] not in content:
        print(f"❌ {path}: انکر مورد انتظار پیدا نشد. فایل رو دستی چک کن.")
        return False

    # بک‌آپ
    backup_path = path.with_suffix(path.suffix + ".pre-notification-401-fix-backup")
    backup_path.write_text(content, encoding="utf-8")

    new_content = content.replace(entry["hook_old"], entry["hook_new"])

    if not already_imported:
        if entry["import_anchor"] not in new_content:
            print(f"❌ {path}: انکر ایمپورت پیدا نشد، ایمپورت اضافه نشد.")
            return False
        new_content = new_content.replace(
            entry["import_anchor"],
            entry["import_anchor"] + "\n" + IMPORT_LINE.rstrip("\n"),
        )

    path.write_text(new_content, encoding="utf-8")
    print(f"✅ {path}: فیکس شد. بک‌آپ: {backup_path}")
    return True


def main():
    ok = True
    for entry in FILES:
        if not patch_file(entry):
            ok = False
    if ok:
        print("\n✅ همه‌چیز تمام شد. حالا git diff بزن و چک کن.")
    else:
        print("\n⚠️ بعضی فایل‌ها فیکس نشدن. بالا رو بخون و دستی بررسی کن.")
        sys.exit(1)


if __name__ == "__main__":
    main()
