#!/usr/bin/env python3
"""
مرحله ۴ب — اصلاح انکر برای BlogEditPage.jsx

فقط قسمت BlogEditPage.jsx که تو اسکریپت قبلی گیر کرد رو دوباره امتحان
می‌کنه، با انکر درست (شامل خط Form.Label).

نحوه‌ی اجرا:
    cp fix_titlestyle_blogform_retry.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_titlestyle_blogform_retry.py
"""

import sys
from pathlib import Path

BLOG_PATH = Path("frontend/src/pages/admin/BlogEditPage.jsx")

DEFAULT_TITLE_STYLE_JS = """{
  color: '#ffffff',
  fontFamily: 'default',
  textAlign: 'center',
  shadow: { enabled: false, color: '#000000', blur: 8, offsetX: 0, offsetY: 2, inset: false },
  glow: { enabled: false, color: '#52b788', intensity: 10 },
  fadeIn: { enabled: false },
}"""

IMPORT_OLD = "import { useState, useEffect } from 'react'"
IMPORT_NEW = IMPORT_OLD + "\nimport TextStyleEditor from '../../components/admin/TextStyleEditor'"

STATE_OLD = "  const [relatedProducts, setRelatedProducts] = useState([])"
STATE_NEW = (
    "  const [relatedProducts, setRelatedProducts] = useState([])\n"
    "  const [titleStyle, setTitleStyle] = useState(" + DEFAULT_TITLE_STYLE_JS + ")"
)

PREFILL_OLD = "      setIsPublished(post.isPublished)"
PREFILL_NEW = (
    "      setIsPublished(post.isPublished)\n"
    "      if (post.titleStyle) setTitleStyle(post.titleStyle)"
)

SUBMIT_OLD = "      await updatePost({ id, title, content, image, video, isPublished, relatedProducts }).unwrap()"
SUBMIT_NEW = "      await updatePost({ id, title, content, image, video, isPublished, relatedProducts, titleStyle }).unwrap()"

FORM_OLD = (
    "          <Form.Group className='mb-3'>\n"
    "            <Form.Label>عنوان</Form.Label>\n"
    "            <Form.Control value={title} onChange={(e) => setTitle(e.target.value)} required />\n"
    "          </Form.Group>"
)
FORM_NEW = (
    "          <Form.Group className='mb-3'>\n"
    "            <Form.Label>عنوان</Form.Label>\n"
    "            <Form.Control value={title} onChange={(e) => setTitle(e.target.value)} required />\n"
    "          </Form.Group>\n\n"
    "          <TextStyleEditor value={titleStyle} onChange={setTitleStyle} />"
)

REPLACEMENTS = [
    (IMPORT_OLD, IMPORT_NEW, "import"),
    (STATE_OLD, STATE_NEW, "state"),
    (PREFILL_OLD, PREFILL_NEW, "prefill"),
    (SUBMIT_OLD, SUBMIT_NEW, "submit"),
    (FORM_OLD, FORM_NEW, "form insert"),
]


def main():
    if not BLOG_PATH.exists():
        print(f"❌ فایل پیدا نشد: {BLOG_PATH.resolve()}")
        sys.exit(1)

    content = BLOG_PATH.read_text(encoding="utf-8")

    if "TextStyleEditor" in content:
        print("⚠️ به‌نظر می‌رسه قبلاً فیکس شده (جزئی یا کامل). بذار چک کنیم:")
        for _, new, name in REPLACEMENTS:
            status = "✅" if new in content else "❌ هنوز نیست"
            print(f"  {name}: {status}")
        sys.exit(0)

    ok = True
    for old, new, name in REPLACEMENTS:
        if old not in content:
            print(f"❌ انکر '{name}' پیدا نشد.")
            ok = False

    if not ok:
        print("دستی چک کن، هیچی نوشته نشد.")
        sys.exit(1)

    backup_path = BLOG_PATH.with_suffix(BLOG_PATH.suffix + ".pre-titlestyle-blog-fix-backup")
    backup_path.write_text(content, encoding="utf-8")

    new_content = content
    for old, new, name in REPLACEMENTS:
        new_content = new_content.replace(old, new, 1)

    BLOG_PATH.write_text(new_content, encoding="utf-8")
    print(f"✅ {BLOG_PATH}: همه‌ی ۵ تغییر اعمال شد.")
    print(f"بک‌آپ: {backup_path}")
    print("حالا git diff بزن تا تغییر رو ببینی.")


if __name__ == "__main__":
    main()
