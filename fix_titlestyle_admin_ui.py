#!/usr/bin/env python3
"""
مرحله ۴ از ۵ — فیچر استایل‌دهی متن اسلایدر/وبلاگ

۱) ساخت کامپوننت مشترک TextStyleEditor.jsx (کالر پیکر رنگ فونت، سلکت
   فونت، دکمه‌های تراز، بخش شدو با enable/رنگ/بلور/آفست/inset، بخش گلو
   با enable/رنگ/شدت، چک‌باکس فید)
۲) وصل‌کردنش به SliderListPage.jsx (state فرم + مودال + پری‌فیل ادیت)
۳) وصل‌کردنش به BlogEditPage.jsx (state + پری‌فیل از پست + فرم + submit)

نحوه‌ی اجرا:
    cp fix_titlestyle_admin_ui.py ~/aqualotus/
    cd ~/aqualotus
    python3 fix_titlestyle_admin_ui.py
"""

import sys
from pathlib import Path

DEFAULT_TITLE_STYLE_JS = """{
  color: '#ffffff',
  fontFamily: 'default',
  textAlign: 'center',
  shadow: { enabled: false, color: '#000000', blur: 8, offsetX: 0, offsetY: 2, inset: false },
  glow: { enabled: false, color: '#52b788', intensity: 10 },
  fadeIn: { enabled: false },
}"""

EDITOR_PATH = Path("frontend/src/components/admin/TextStyleEditor.jsx")

EDITOR_CONTENT = """import { Form, Row, Col, ButtonGroup, Button } from 'react-bootstrap'

// کامپوننت مشترک تنظیم استایل متن (رنگ/فونت/تراز/شدو/گلو/فید)
// value: آبجکت titleStyle | onChange: (newTitleStyle) => void
const FONT_OPTIONS = [
  { value: 'default', label: 'وزیرمتن (پیش‌فرض)' },
  { value: 'serif', label: 'سریف' },
  { value: 'mono', label: 'مونو' },
]

const TextStyleEditor = ({ value, onChange }) => {
  const style = value || {
    color: '#ffffff',
    fontFamily: 'default',
    textAlign: 'center',
    shadow: { enabled: false, color: '#000000', blur: 8, offsetX: 0, offsetY: 2, inset: false },
    glow: { enabled: false, color: '#52b788', intensity: 10 },
    fadeIn: { enabled: false },
  }

  const update = (patch) => onChange({ ...style, ...patch })
  const updateShadow = (patch) => onChange({ ...style, shadow: { ...style.shadow, ...patch } })
  const updateGlow = (patch) => onChange({ ...style, glow: { ...style.glow, ...patch } })

  return (
    <div className='border rounded-3 p-3 mb-3' style={{ background: '#f8f9fa' }}>
      <div className='fw-bold mb-3 small text-muted'>🎨 استایل متن</div>

      <Row className='mb-3'>
        <Col xs={6}>
          <Form.Label className='small'>رنگ فونت</Form.Label>
          <Form.Control
            type='color'
            value={style.color}
            onChange={(e) => update({ color: e.target.value })}
            title='رنگ فونت'
          />
        </Col>
        <Col xs={6}>
          <Form.Label className='small'>فونت</Form.Label>
          <Form.Select value={style.fontFamily} onChange={(e) => update({ fontFamily: e.target.value })}>
            {FONT_OPTIONS.map((f) => (
              <option key={f.value} value={f.value}>{f.label}</option>
            ))}
          </Form.Select>
        </Col>
      </Row>

      <div className='mb-3'>
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
      </div>

      <Form.Check
        type='checkbox'
        id='titlestyle-shadow-enabled'
        label='سایه (شدو)'
        checked={style.shadow?.enabled || false}
        onChange={(e) => updateShadow({ enabled: e.target.checked })}
        className='mb-2'
      />
      {style.shadow?.enabled && (
        <Row className='mb-3 ps-3'>
          <Col xs={6} className='mb-2'>
            <Form.Label className='small'>رنگ سایه</Form.Label>
            <Form.Control type='color' value={style.shadow.color} onChange={(e) => updateShadow({ color: e.target.value })} />
          </Col>
          <Col xs={6} className='mb-2'>
            <Form.Check
              type='checkbox'
              id='titlestyle-shadow-inset'
              label='داخلی (inset)'
              checked={style.shadow.inset || false}
              onChange={(e) => updateShadow({ inset: e.target.checked })}
            />
          </Col>
          <Col xs={12} className='mb-2'>
            <Form.Label className='small'>میزان محو شدگی: {style.shadow.blur}px</Form.Label>
            <Form.Range min={0} max={40} value={style.shadow.blur} onChange={(e) => updateShadow({ blur: Number(e.target.value) })} />
          </Col>
          <Col xs={6}>
            <Form.Label className='small'>افست افقی: {style.shadow.offsetX}px</Form.Label>
            <Form.Range min={-20} max={20} value={style.shadow.offsetX} onChange={(e) => updateShadow({ offsetX: Number(e.target.value) })} />
          </Col>
          <Col xs={6}>
            <Form.Label className='small'>افست عمودی: {style.shadow.offsetY}px</Form.Label>
            <Form.Range min={-20} max={20} value={style.shadow.offsetY} onChange={(e) => updateShadow({ offsetY: Number(e.target.value) })} />
          </Col>
        </Row>
      )}

      <Form.Check
        type='checkbox'
        id='titlestyle-glow-enabled'
        label='درخشش (گلو)'
        checked={style.glow?.enabled || false}
        onChange={(e) => updateGlow({ enabled: e.target.checked })}
        className='mb-2'
      />
      {style.glow?.enabled && (
        <Row className='mb-3 ps-3'>
          <Col xs={6} className='mb-2'>
            <Form.Label className='small'>رنگ درخشش</Form.Label>
            <Form.Control type='color' value={style.glow.color} onChange={(e) => updateGlow({ color: e.target.value })} />
          </Col>
          <Col xs={6} className='mb-2'>
            <Form.Label className='small'>شدت: {style.glow.intensity}px</Form.Label>
            <Form.Range min={0} max={40} value={style.glow.intensity} onChange={(e) => updateGlow({ intensity: Number(e.target.value) })} />
          </Col>
        </Row>
      )}

      <Form.Check
        type='checkbox'
        id='titlestyle-fadein-enabled'
        label='انیمیشن ظاهرشدن (فید)'
        checked={style.fadeIn?.enabled || false}
        onChange={(e) => update({ fadeIn: { enabled: e.target.checked } })}
      />
    </div>
  )
}

export default TextStyleEditor
"""

SLIDER_PATH = Path("frontend/src/pages/admin/SliderListPage.jsx")

SLIDER_IMPORT_OLD = "import { Container, Table, Button, Form, Modal, Card, Row, Col, Badge, Nav } from 'react-bootstrap'"
SLIDER_IMPORT_NEW = (
    SLIDER_IMPORT_OLD
    + "\nimport TextStyleEditor from '../../components/admin/TextStyleEditor'"
)

SLIDER_STATE_OLD = "  const [form, setForm] = useState({ title: '', subtitle: '', image: '', link: '/', order: 0, location: 'home' })"
SLIDER_STATE_NEW = (
    "  const defaultTitleStyle = "
    + DEFAULT_TITLE_STYLE_JS
    + "\n"
    "  const [form, setForm] = useState({ title: '', subtitle: '', image: '', link: '/', order: 0, location: 'home', titleStyle: defaultTitleStyle })"
)

SLIDER_OPENCREATE_OLD = "    setForm({ title: '', subtitle: '', image: '', link: '/', order: sliders?.length || 0, location: activeLocation })"
SLIDER_OPENCREATE_NEW = "    setForm({ title: '', subtitle: '', image: '', link: '/', order: sliders?.length || 0, location: activeLocation, titleStyle: defaultTitleStyle })"

SLIDER_OPENEDIT_OLD = "      title: slider.title || '',\n      subtitle: slider.subtitle || '',"
SLIDER_OPENEDIT_NEW = (
    "      title: slider.title || '',\n"
    "      subtitle: slider.subtitle || '',\n"
    "      titleStyle: slider.titleStyle || defaultTitleStyle,"
)

SLIDER_FORM_INSERT_OLD = (
    "            <Form.Group className='mb-3'>\n"
    "              <Form.Label>تصویر <span className='text-danger'>*</span></Form.Label>"
)
SLIDER_FORM_INSERT_NEW = (
    "            <TextStyleEditor value={form.titleStyle} onChange={(titleStyle) => setForm({ ...form, titleStyle })} />\n\n"
    "            <Form.Group className='mb-3'>\n"
    "              <Form.Label>تصویر <span className='text-danger'>*</span></Form.Label>"
)

BLOG_PATH = Path("frontend/src/pages/admin/BlogEditPage.jsx")

BLOG_IMPORT_ANCHOR_CANDIDATES = [
    "import { useState, useEffect } from 'react'",
]
BLOG_IMPORT_NEW_SUFFIX = "\nimport TextStyleEditor from '../../components/admin/TextStyleEditor'"

BLOG_STATE_OLD = "  const [relatedProducts, setRelatedProducts] = useState([])"
BLOG_STATE_NEW = (
    "  const [relatedProducts, setRelatedProducts] = useState([])\n"
    "  const [titleStyle, setTitleStyle] = useState("
    + DEFAULT_TITLE_STYLE_JS
    + ")"
)

BLOG_PREFILL_OLD = "      setIsPublished(post.isPublished)"
BLOG_PREFILL_NEW = (
    "      setIsPublished(post.isPublished)\n"
    "      if (post.titleStyle) setTitleStyle(post.titleStyle)"
)

BLOG_SUBMIT_OLD = "      await updatePost({ id, title, content, image, video, isPublished, relatedProducts }).unwrap()"
BLOG_SUBMIT_NEW = "      await updatePost({ id, title, content, image, video, isPublished, relatedProducts, titleStyle }).unwrap()"

BLOG_FORM_INSERT_OLD = (
    "          <Form.Group className='mb-3'>\n"
    "            <Form.Control value={title} onChange={(e) => setTitle(e.target.value)} required />\n"
    "          </Form.Group>"
)
BLOG_FORM_INSERT_NEW = (
    "          <Form.Group className='mb-3'>\n"
    "            <Form.Control value={title} onChange={(e) => setTitle(e.target.value)} required />\n"
    "          </Form.Group>\n\n"
    "          <TextStyleEditor value={titleStyle} onChange={setTitleStyle} />"
)


def patch(path, replacements, label):
    if not path.exists():
        print(f"❌ فایل پیدا نشد: {path.resolve()}")
        return False
    content = path.read_text(encoding="utf-8")
    if "TextStyleEditor" in content:
        print(f"ℹ️  {path}: به‌نظر می‌رسه قبلاً فیکس شده. رد می‌کنم.")
        return True

    backup_path = path.with_suffix(path.suffix + f".pre-titlestyle-{label}-fix-backup")
    ok = True
    new_content = content
    for old, new, name in replacements:
        if new in new_content:
            continue
        if old not in new_content:
            print(f"❌ {path}: انکر '{name}' پیدا نشد.")
            ok = False
            continue
        new_content = new_content.replace(old, new, 1)

    if not ok:
        return False

    if new_content != content:
        backup_path.write_text(content, encoding="utf-8")
        path.write_text(new_content, encoding="utf-8")
        print(f"✅ {path}: فیکس شد.")
    else:
        print(f"ℹ️  {path}: تغییری لازم نبود.")
    return True


def main():
    ok = True

    # ۱) ساخت فایل TextStyleEditor.jsx
    if EDITOR_PATH.exists():
        print(f"ℹ️  {EDITOR_PATH}: از قبل وجود داره، رد می‌کنم.")
    else:
        EDITOR_PATH.parent.mkdir(parents=True, exist_ok=True)
        EDITOR_PATH.write_text(EDITOR_CONTENT, encoding="utf-8")
        print(f"✅ {EDITOR_PATH}: ساخته شد.")

    # ۲) SliderListPage.jsx
    ok &= patch(
        SLIDER_PATH,
        [
            (SLIDER_IMPORT_OLD, SLIDER_IMPORT_NEW, "import"),
            (SLIDER_STATE_OLD, SLIDER_STATE_NEW, "state"),
            (SLIDER_OPENCREATE_OLD, SLIDER_OPENCREATE_NEW, "openCreate"),
            (SLIDER_OPENEDIT_OLD, SLIDER_OPENEDIT_NEW, "openEdit"),
            (SLIDER_FORM_INSERT_OLD, SLIDER_FORM_INSERT_NEW, "form insert"),
        ],
        "slider",
    )

    # ۳) BlogEditPage.jsx
    blog_content = BLOG_PATH.read_text(encoding="utf-8") if BLOG_PATH.exists() else ""
    blog_import_old = None
    for cand in BLOG_IMPORT_ANCHOR_CANDIDATES:
        if cand in blog_content:
            blog_import_old = cand
            break
    if blog_import_old is None:
        print(f"❌ {BLOG_PATH}: انکر ایمپورت پیدا نشد.")
        ok = False
    else:
        ok &= patch(
            BLOG_PATH,
            [
                (blog_import_old, blog_import_old + BLOG_IMPORT_NEW_SUFFIX, "import"),
                (BLOG_STATE_OLD, BLOG_STATE_NEW, "state"),
                (BLOG_PREFILL_OLD, BLOG_PREFILL_NEW, "prefill"),
                (BLOG_SUBMIT_OLD, BLOG_SUBMIT_NEW, "submit"),
                (BLOG_FORM_INSERT_OLD, BLOG_FORM_INSERT_NEW, "form insert"),
            ],
            "blog",
        )

    if ok:
        print("\\n✅ مرحله ۴ تمام شد. حالا git diff بزن و چک کن.")
    else:
        print("\\n⚠️ بعضی موارد فیکس نشدن. بالا رو بخون.")
        sys.exit(1)


if __name__ == "__main__":
    main()
