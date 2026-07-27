// تبدیل آبجکت titleStyle (ذخیره‌شده تو دیتابیس) به استایل واقعی CSS
// برای تیتر اسلایدر/وبلاگ. shadow و glow هر دو با textShadow پیاده‌سازی
// میشن (چون CSS همچین چیز جدایی برای glow نداره، glow یعنی یه shadow
// با blur بیشتر و بدون offset).

const FONT_MAP = {
  default: "'Vazirmatn', sans-serif",
  serif: "Georgia, 'Vazirmatn', serif",
  mono: "'Courier New', monospace",
}

export function buildTextStyle(titleStyle) {
  if (!titleStyle) return {}

  const style = {}

  if (titleStyle.color) style.color = titleStyle.color
  if (titleStyle.textAlign) style.textAlign = titleStyle.textAlign
  style.fontFamily = FONT_MAP[titleStyle.fontFamily] || FONT_MAP.default

  const shadowLayers = []

  if (titleStyle.shadow?.enabled) {
    const { color = '#000000', blur = 8, offsetX = 0, offsetY = 2 } = titleStyle.shadow
    shadowLayers.push(`${offsetX}px ${offsetY}px ${blur}px ${color}`)
  }

  if (titleStyle.glow?.enabled) {
    const { color = '#52b788', intensity = 10 } = titleStyle.glow
    // گلو یعنی چند لایه shadow بدون offset با blur فزاینده، دور متن رو می‌گیره
    shadowLayers.push(`0 0 ${intensity}px ${color}`)
    shadowLayers.push(`0 0 ${intensity * 2}px ${color}`)
  }

  if (shadowLayers.length > 0) {
    style.textShadow = shadowLayers.join(', ')
  }

  return style
}

export function getTextStyleClassName(titleStyle) {
  return titleStyle?.fadeIn?.enabled ? 'aq-title-fade-in' : ''
}
