#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

card_path = './frontend/src/components/ui/ProductCard.jsx'
with open(card_path, 'r', encoding='utf-8') as f:
    card_content = f.read()

if 'index = 0' not in card_content and 'initial={{ opacity: 0' not in card_content:
    card_content = card_content.replace(
        'const ProductCard = ({ product }) => {',
        'const ProductCard = ({ product, index = 0 }) => {'
    )
    old_outer = "<div ref={revealRef} className='aq-scroll-init h-100'>"
    new_outer = """<div ref={revealRef} className='aq-scroll-init h-100'>
      <motion.div
        initial={{ opacity: 0, y: 45, scale: 0.96 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: -25, scale: 0.92 }}
        transition={{
          duration: 0.55,
          delay: Math.min(index * 0.07, 0.7),
          ease: [0.25, 0.1, 0.25, 1],
        }}
        layout
        style={{ height: '100%' }}
      >"""
    card_content = card_content.replace(old_outer, new_outer)
    old_end = """        </div>
      </div>
    </div>
  )
}

export default ProductCard"""
    new_end = """        </div>
      </div>
      </motion.div>
    </div>
  )
}

export default ProductCard"""
    card_content = card_content.replace(old_end, new_end)
    with open(card_path, 'w', encoding='utf-8') as f:
        f.write(card_content)
    print('✅ ProductCard.jsx پچ شد')
else:
    print('⏭️ ProductCard.jsx قبلاً پچ شده')

home_path = './frontend/src/pages/HomePage.jsx'
with open(home_path, 'r', encoding='utf-8') as f:
    home_content = f.read()

if "AnimatePresence" not in home_content:
    home_content = home_content.replace(
        "import { useGetProductsQuery } from '../slices/productsApiSlice'",
        "import { useGetProductsQuery } from '../slices/productsApiSlice'\nimport { AnimatePresence } from 'framer-motion'"
    )
    old_map = """                  <Row className='g-3'>
                    {data?.products?.map((product) => (
                      <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                        <ProductCard product={product} />
                      </Col>
                    ))}
                  </Row>"""
    new_map = """                  <Row className='g-3'>
                    <AnimatePresence mode='popLayout'>
                      {data?.products?.map((product, index) => (
                        <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                          <ProductCard product={product} index={index} />
                        </Col>
                      ))}
                    </AnimatePresence>
                  </Row>"""
    home_content = home_content.replace(old_map, new_map)
    with open(home_path, 'w', encoding='utf-8') as f:
        f.write(home_content)
    print('✅ HomePage.jsx پچ شد')
else:
    print('⏭️ HomePage.jsx قبلاً پچ شده')

print("""
🎉 تمام شد!
   • ورود: fade + slide-up + scale (stagger 70ms)
   • خروج: fade + slide-up + shrink
   • reorder: smooth با layout prop
npm run client  →  ری‌استارت کن
""")
