/**
 * slugify.js
 * ------------
 * تبدیل نام فارسی محصول به یک اسلاگ خوانا برای URL.
 * حروف فارسی/عربی حفظ می‌شن، فاصله‌ها به خط‌تیره تبدیل می‌شن،
 * نیم‌فاصله (ZWNJ) حذف می‌شه، و کاراکترهای غیرمجاز پاک می‌شن.
 */

export const slugify = (text) => {
  if (!text) return ''
  return text
    .toString()
    .trim()
    .replace(/\u200c/g, '') // حذف نیم‌فاصله
    .replace(/[^\u0600-\u06FF\u0750-\u077Fa-zA-Z0-9\s-]/g, '') // حذف علائم غیرمجاز
    .replace(/\s+/g, '-') // فاصله‌ها به خط‌تیره
    .replace(/-+/g, '-') // چند خط‌تیره پشت‌سرهم به یکی
    .replace(/^-+|-+$/g, '') // حذف خط‌تیره‌ی ابتدا/انتها
}

/**
 * تولید اسلاگ یکتا با چک کردن دیتابیس.
 * اگه اسلاگ تکراری بود، عدد افزایشی (-2, -3, ...) بهش اضافه می‌شه.
 *
 * @param {Model} Model - مدل Mongoose (مثلاً Product)
 * @param {String} name - نام فارسی که ازش اسلاگ ساخته می‌شه
 * @param {String} [excludeId] - شناسه‌ی سندی که باید از چک یکتایی مستثنی بشه (برای ویرایش)
 */
export const generateUniqueSlug = async (Model, name, excludeId = null) => {
  const base = slugify(name) || 'product'
  let candidate = base
  let counter = 2

  // eslint-disable-next-line no-constant-condition
  while (true) {
    const query = { slug: candidate }
    if (excludeId) query._id = { $ne: excludeId }
    const exists = await Model.findOne(query).select('_id')
    if (!exists) return candidate
    candidate = `${base}-${counter}`
    counter += 1
  }
}
