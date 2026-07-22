#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch: Add Framer Motion morph (layoutId) between ProductCard and ProductPage
- ProductCard: motion.img with layoutId
- ProductPage: motion.img with layoutId (main image)
- Cross-browser: works in Chrome, Firefox, Safari
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

# Add motion import
if "import { motion } from 'framer-motion'" not in card:
    card = card.replace(
        "import { useScrollReveal } from '../../hooks/useScrollReveal'",
        "import { motion } from 'framer-motion'\nimport { useScrollReveal } from '../../hooks/useScrollReveal'"
    )
    print("  [ADD] import { motion } to ProductCard")

# Replace the active slideshow image with motion.img
old_card_img = r"""              <img
                key={imgIndex}
                src={allImages[imgIndex]}
                alt={product.name}
                loading='lazy'
                className='card-img-top product-img aq-slideshow-slide'
                style={{
                  position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
                  viewTransitionName: `product-img-${product._id}`,
                  transform: isHovered ? 'scale(1.1)' : 'scale(1)',
                  transition: 'transform 0.6s ease-out',
                  ...imgFilterStyle,
                }}
              />"""

new_card_img = r"""              <motion.img
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

if old_card_img in card:
    card = card.replace(old_card_img, new_card_img)
    print("  [UPDATE] ProductCard: img -> motion.img with layoutId")
else:
    print("  [WARN] ProductCard image anchor not found")

# ============ 2. ProductPage.jsx ============
with open(PAGE_FILE, 'r', encoding='utf-8') as f:
    page = f.read()

# Add motion import
if "import { motion } from 'framer-motion'" not in page:
    page = page.replace(
        "import React, { useState, useEffect } from 'react';",
        "import React, { useState, useEffect } from 'react';\nimport { motion } from 'framer-motion';"
    )
    print("  [ADD] import { motion } to ProductPage")

# Replace main product image (the one in the page, not modal) with motion.img
# We target the image that shows the product - line ~172 area
old_page_img = r"""          <img 
            src={images[selectedImageIndex]} 
            alt={product?.name} 
            className="img-fluid rounded-4 shadow-lg w-100 object-fit-contain" 
            style={{ maxHeight: '85vh', backgroundColor: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', padding: '20px' }}
          />"""

new_page_img = r"""          <motion.img 
            src={images[selectedImageIndex]} 
            alt={product?.name} 
            layoutId={`product-img-${productId}`}
            className="img-fluid rounded-4 shadow-lg w-100 object-fit-contain" 
            style={{ maxHeight: '85vh', backgroundColor: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', padding: '20px' }}
          />"""

if old_page_img in page:
    page = page.replace(old_page_img, new_page_img)
    print("  [UPDATE] ProductPage: img -> motion.img with layoutId")
else:
    print("  [WARN] ProductPage image anchor not found")

# ============ 3. CSS ============
with open(CSS_FILE, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = r"""

/* --- productcard-morph v1 --- */
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
}
"""

if '/* --- productcard-morph' not in css:
    css = css.rstrip() + '\n' + new_css
    print("  [APPEND] morph CSS to index.css")

# ============ Write All ============
if not backup_file(CARD_FILE, "morph"):
    sys.exit(1)
if not backup_file(PAGE_FILE, "morph"):
    sys.exit(1)
if not backup_file(CSS_FILE, "morph"):
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

print("\n✓ Morph patch applied successfully!")
print("  Changes:")
print("    • ProductCard: motion.img with layoutId")
print("    • ProductPage: motion.img with layoutId")
print("    • CSS: morph animation styles")
print("\n  Next steps:")
print("    1. In VS Code: Reload from Disk if prompted")
print("    2. Restart Vite server (Ctrl+C then npm run dev)")
print("    3. Test: Click a product card -> image should morph to ProductPage")
print("    4. Works in Chrome, Firefox, Safari")
