import nazarCompact from '../../assets/surreal/nazar-compact.png';
import horizonBanner from '../../assets/surreal/horizon-banner.png';
import iconSet from '../../assets/surreal/icon-set.png';

/**
 * SurrealAssets.jsx
 * ------------------
 * المان‌های گرافیکی سورئال برند AquaLotus (نظر، کوهستان، خورشید، موج، سیمرغ، ماهی، مرجان)
 * برای استفاده‌ی مشترک در Navbar، Footer، و HomePage.
 *
 * رنگ‌ها و فونت‌های پروژه دست‌نخورده می‌مونن؛ این‌ها فقط گرافیک تزئینی هستن.
 */

// نسخه‌ی فشرده برای Navbar (نظر + کوه + خورشید داخل مردمک)
export function NazarIcon({ size = 40, className = '' }) {
  return (
    <img
      src={nazarCompact}
      alt=""
      aria-hidden="true"
      width={size}
      height={size}
      className={`select-none pointer-events-none ${className}`}
      style={{ filter: 'opacity(0.9)' }}
    />
  );
}

// نسخه‌ی پهن افق (کوه + خورشید + موج) برای Footer
export function HorizonBanner({ className = '' }) {
  return (
    <img
      src={horizonBanner}
      alt=""
      aria-hidden="true"
      className={`w-full h-auto select-none pointer-events-none ${className}`}
    />
  );
}

/**
 * ست کامل آیکون‌ها (نظر، سیمرغ، کوه، بیابون، خورشید، موج، ماهی، مرجان)
 * این فعلاً یه شیت ترکیبی (sprite) هست، نه فایل‌های جدا.
 * برای استفاده‌ی مستقل هرکدوم (مثلاً فقط سیمرغ تو Hero)،
 * باید این عکس crop بشه به ۸ فایل جدا — اگه لازم شد بگو تا
 * یه اسکریپت Python با Pillow برات بنویسم که خودکار crop کنه.
 */
export function SurrealIconSheet({ className = '' }) {
  return (
    <img
      src={iconSet}
      alt=""
      aria-hidden="true"
      className={`select-none pointer-events-none ${className}`}
    />
  );
}
