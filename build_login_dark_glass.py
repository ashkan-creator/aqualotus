#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_login_dark_glass.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_login_dark_glass.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_login_dark_glass.py

فقط index.css رو append می‌کنه. همه‌چیز داخل .aq-auth-card اسکوپ شده
تا رو ForgotPasswordPage/RegisterPage (که از همون .auth-card/.auth-title
استفاده می‌کنن ولی پس‌زمینه‌شون سفیده) تاثیر نذاره.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
css_path = ROOT / "frontend" / "src" / "index.css"

if not css_path.exists():
    print(f"✗ فایل پیدا نشد: {css_path}")
    sys.exit(1)

content = css_path.read_text(encoding="utf-8")
marker = "/* --- login page dark glass v1 --- */"

if marker in content:
    print("✗ این مارکر قبلاً وجود داره — چیزی اضافه نشد")
    sys.exit(1)

backup = css_path.with_suffix(css_path.suffix + ".pre-logindarkglass-backup")
shutil.copy2(css_path, backup)

extra_css = f'''

{marker}
.aq-auth-card {{
  --bs-card-color: #fff;
  background: rgba(10, 10, 10, 0.5) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  color: #fff !important;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
}}

.aq-auth-card .auth-title,
.aq-auth-card label,
.aq-auth-card .form-label,
.aq-auth-card span,
.aq-auth-card p,
.aq-auth-card .text-muted {{
  color: #fff !important;
}}

.aq-auth-card .form-control {{
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.25);
  color: #fff;
}}

.aq-auth-card .form-control::placeholder {{
  color: rgba(255, 255, 255, 0.55);
}}

.aq-auth-card .form-control:focus {{
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  border-color: rgba(0, 255, 127, 0.5);
  box-shadow: 0 0 0 0.2rem rgba(0, 255, 127, 0.15);
}}

.aq-auth-card .aq-auth-method-switch {{
  background: rgba(255, 255, 255, 0.08);
}}

.aq-auth-card .aq-auth-method-btn {{
  color: rgba(255, 255, 255, 0.75);
}}

.aq-auth-card .aq-auth-method-btn.active {{
  color: #fff;
}}

.aq-auth-card hr {{
  border-color: rgba(255, 255, 255, 0.2);
}}
'''

with open(css_path, "a", encoding="utf-8") as f:
    f.write(extra_css)

print(f"✓ index.css append شد — بک‌آپ: {backup.name}")
print("\nقدم بعدی: سرور Vite رو کامل ری‌استارت کن و تو Incognito صفحه‌ی لاگین رو چک کن.")
print("همینطور یه صفحه‌ی دیگه مثل /forgot-password رو هم چک کن که هنوز روشن/سفید مونده.")
