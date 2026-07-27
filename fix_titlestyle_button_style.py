#!/usr/bin/env python3
"""
استایل‌دهی دکمه‌های تراز تو TextStyleEditor.jsx

مشکل: دکمه‌های تراز (راست/وسط/چپ) با استایل خام بوت‌استرپ (ButtonGroup)
رندر میشن که هم‌رنگ پالت سبز سایت نیست و هیچ موشن/هاور نداره.

فیکس: یه کلاس CSS اختصاصی (.aq-align-btn) با ترنزیشن نرم، هاور
(لیفت + سایه)، و حالت فعال با گرادیان سبز سایت.

نحوه‌ی اجرا:
    cp fix_titlestyle_button_style.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_titlestyle_button_style.py
"""

import sys
from pathlib import Path

EDITOR_PATH = Path("frontend/src/components/admin/TextStyleEditor.jsx")

OLD_BUTTONS_BLOCK = """      <div className='mb-3'>
        <Form.Label className='small d-block'>تراز متن</Form.Label>
        <ButtonGroup size='sm'>
          {[
            { value: 'right', label: 'راست' },
            { value: 'center', label: 'وسط' },
            { value: 'left', label: 'چپ' },
          ].map((a) => (
            <Button
              key={a.value}
              variant={style.textAlign === a.value ? 'success' : 'outline-secondary'}
              onClick={() => update({ textAlign: a.value })}
            >
              {a.label}
            </Button>
          ))}
        </ButtonGroup>
      </div>"""

NEW_BUTTONS_BLOCK = """      <div className='mb-3'>
        <Form.Label className='small d-block'>تراز متن</Form.Label>
        <div className='d-flex gap-2'>
          {[
            { value: 'right', label: 'راست' },
            { value: 'center', label: 'وسط' },
            { value: 'left', label: 'چپ' },
          ].map((a) => (
            <button
              key={a.value}
              type='button'
              className={`aq-align-btn ${style.textAlign === a.value ? 'active' : ''}`}
              onClick={() => update({ textAlign: a.value })}
            >
              {a.label}
            </button>
          ))}
        </div>
      </div>"""

IMPORT_OLD = "import { Form, Row, Col, ButtonGroup, Button } from 'react-bootstrap'"
IMPORT_NEW = "import { Form, Row, Col } from 'react-bootstrap'"

CSS_PATH = Path("frontend/src/animations.css")
CSS_BLOCK = """
/* --- TextStyleEditor: دکمه‌های تراز متن --- */
.aq-align-btn {
  padding: 6px 18px;
  border-radius: 8px;
  border: 1.5px solid #d0d7de;
  background: #ffffff;
  color: #444;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.aq-align-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(45, 106, 79, 0.18);
  border-color: #52b788;
  color: #2d6a4f;
}
.aq-align-btn.active {
  background: linear-gradient(135deg, #2d6a4f 0%, #52b788 100%);
  border-color: transparent;
  color: #fff;
  box-shadow: 0 3px 10px rgba(45, 106, 79, 0.35);
}
.aq-align-btn.active:hover {
  transform: translateY(-2px) scale(1.03);
}
"""


def main():
    if not EDITOR_PATH.exists():
        print(f"❌ فایل پیدا نشد: {EDITOR_PATH.resolve()}")
        sys.exit(1)

    content = EDITOR_PATH.read_text(encoding="utf-8")

    if "aq-align-btn" in content:
        print(f"⚠️ {EDITOR_PATH}: به‌نظر می‌رسه قبلاً فیکس شده.")
    else:
        if OLD_BUTTONS_BLOCK not in content:
            print("❌ انکر دکمه‌ها پیدا نشد. دستی چک کن.")
            sys.exit(1)
        if IMPORT_OLD not in content:
            print("❌ انکر ایمپورت پیدا نشد. دستی چک کن.")
            sys.exit(1)

        backup_path = EDITOR_PATH.with_suffix(EDITOR_PATH.suffix + ".pre-button-style-fix-backup")
        backup_path.write_text(content, encoding="utf-8")

        new_content = content.replace(IMPORT_OLD, IMPORT_NEW, 1)
        new_content = new_content.replace(OLD_BUTTONS_BLOCK, NEW_BUTTONS_BLOCK, 1)
        EDITOR_PATH.write_text(new_content, encoding="utf-8")
        print(f"✅ {EDITOR_PATH}: فیکس شد.")

    if not CSS_PATH.exists():
        print(f"❌ فایل پیدا نشد: {CSS_PATH.resolve()}")
        sys.exit(1)

    css_content = CSS_PATH.read_text(encoding="utf-8")
    if "aq-align-btn" in css_content:
        print(f"⚠️ {CSS_PATH}: استایل دکمه‌ها از قبل هست.")
    else:
        css_backup = CSS_PATH.with_suffix(CSS_PATH.suffix + ".pre-align-btn-css-backup")
        css_backup.write_text(css_content, encoding="utf-8")
        CSS_PATH.write_text(css_content + CSS_BLOCK, encoding="utf-8")
        print(f"✅ {CSS_PATH}: استایل دکمه‌های تراز اضافه شد.")

    print("\n✅ تمام شد. حالا git diff بزن و چک کن.")


if __name__ == "__main__":
    main()
