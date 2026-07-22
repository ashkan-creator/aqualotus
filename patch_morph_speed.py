#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch: Speed up morph animation by 5x
Changes transition duration from default (~0.5s) to 0.1s
"""

import os
import shutil
import sys

BASE_DIR = os.path.expanduser("~/aqualotus/frontend")
CARD_FILE = os.path.join(BASE_DIR, "src", "components", "ui", "ProductCard.jsx")
PAGE_FILE = os.path.join(BASE_DIR, "src", "pages", "ProductPage.jsx")
CSS_FILE = os.path.join(BASE_DIR, "src", "index.css")

def backup_file(path, suffix):
    if os.path.exists(path):
        ext = os.path.splitext(path)[1]
        backup_path = path.replace(ext, f".pre-{suffix}-backup{ext}")
        if not os.path.exists(backup_path):
            shutil.copy2(path, backup_path)
            print(f"  [BACKUP] {os.path.basename(path)} -> {os.path.basename(backup_path)}")
        else:
            print(f"  [SKIP BACKUP] {os.path.basename(backup_path)} already exists")
        return True
    print(f"  [ERROR] File not found: {path}")
    return False

# ============ 1. ProductCard.jsx ============
with open(CARD_FILE, 'r', encoding='utf-8') as f:
    card = f.read()

# Add fast transition to motion.img
old_card = """              <motion.img
                key={imgIndex}
                src={allImages[imgIndex]}
                alt={product.name}
                loading='lazy'
                className='card-img-top product-img aq-slideshow-slide'
                layoutId={`product-img-${product._id}`}
                style={{
                  position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
                  transform: isHovered ? 'scale(1.1)' : 'scale(1)',
                  transition: 'transform 0.6s ease-out',
                  ...imgFilterStyle,
                }}
              />"""

new_card = """              <motion.img
                key={imgIndex}
                src={allImages[imgIndex]}
                alt={product.name}
                loading='lazy'
                className='card-img-top product-img aq-slideshow-slide'
                layoutId={`product-img-${product._id}`}
                transition={{ duration: 0.1, ease: "easeOut" }}
                style={{
                  position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
                  transform: isHovered ? 'scale(1.1)' : 'scale(1)',
                  ...imgFilterStyle,
                }}
              />"""

if old_card in card:
    card = card.replace(old_card, new_card)
    print("  [UPDATE] ProductCard: motion.img transition 0.1s")
else:
    print("  [WARN] ProductCard anchor not found")

# ============ 2. ProductPage.jsx ============
with open(PAGE_FILE, 'r', encoding='utf-8') as f:
    page = f.read()

old_page = """          <motion.img 
            src={images[selectedImageIndex]} 
            alt={product?.name} 
            layoutId={`product-img-${product?._id}`}
            className="img-fluid rounded-4 shadow-lg w-100 object-fit-contain" 
            style={{ maxHeight: '85vh', backgroundColor: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', padding: '20px' }}
          />"""

new_page = """          <motion.img 
            src={images[selectedImageIndex]} 
            alt={product?.name} 
            layoutId={`product-img-${product?._id}`}
            transition={{ duration: 0.1, ease: "easeOut" }}
            className="img-fluid rounded-4 shadow-lg w-100 object-fit-contain" 
            style={{ maxHeight: '85vh', backgroundColor: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', padding: '20px' }}
          />"""

if old_page in page:
    page = page.replace(old_page, new_page)
    print("  [UPDATE] ProductPage: motion.img transition 0.1s")
else:
    print("  [WARN] ProductPage anchor not found")

# ============ 3. CSS ============
with open(CSS_FILE, 'r', encoding='utf-8') as f:
    css = f.read()

# Update morph CSS block
old_css = """/* --- productcard-morph v1 --- */
/* Framer Motion layout animation styles */
.aq-product-card-3d .product-img {
  will-change: transform;
}

/* Ensure smooth morph transition */
[data-framer-motion-layout-id] {
  will-change: transform, width, height, opacity;
}

/* Disable morph on mobile for performance */
@media (max-width: 768px) {
  [data-framer-motion-layout-id] {
    transition: none !important;
  }
}"""

new_css = """/* --- productcard-morph v2 --- */
/* Framer Motion layout animation styles - 5x faster */
.aq-product-card-3d .product-img {
  will-change: transform;
}

/* Ensure smooth morph transition */
[data-framer-motion-layout-id] {
  will-change: transform, width, height, opacity;
}

/* Speed up all layout animations */
[data-framer-motion-layout-id] * {
  transition-duration: 0.1s !important;
}

/* Disable morph on mobile for performance */
@media (max-width: 768px) {
  [data-framer-motion-layout-id] {
    transition: none !important;
  }
}"""

if old_css in css:
    css = css.replace(old_css, new_css)
    print("  [UPDATE] CSS: morph speed 0.1s")
else:
    print("  [WARN] CSS anchor not found, appending new block")
    if '/* --- productcard-morph' not in css:
        css = css.rstrip() + '\n' + new_css
        print("  [APPEND] CSS morph v2 block")

# ============ Write All ============
for path, suffix in [(CARD_FILE, "morph-speed"), (PAGE_FILE, "morph-speed"), (CSS_FILE, "morph-speed")]:
    if not backup_file(path, suffix):
        print(f"[ABORT] Backup failed for {path}")
        sys.exit(1)

try:
    with open(CARD_FILE, 'w', encoding='utf-8') as f:
        f.write(card)
    print(f"  [WRITE] {os.path.basename(CARD_FILE)}")
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

try:
    with open(PAGE_FILE, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"  [WRITE] {os.path.basename(PAGE_FILE)}")
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

try:
    with open(CSS_FILE, 'w', encoding='utf-8') as f:
        f.write(css)
    print(f"  [WRITE] {os.path.basename(CSS_FILE)}")
except Exception as e:
    print(f"  [ERROR] {e}")
    sys.exit(1)

print("\n✓ Morph speed patch applied!")
print("  Changes:")
print("    • ProductCard: transition duration 0.1s")
print("    • ProductPage: transition duration 0.1s")
print("    • CSS: layout animation speed 0.1s")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test: Click a product -> morph should be 5x faster!")
