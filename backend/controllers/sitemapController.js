import asyncHandler from 'express-async-handler'
import Product from '../models/productModel.js'
import Blog from '../models/blogModel.js'

const SITE_URL = process.env.SITE_URL || 'https://aqualotus.ir'

const generateSitemap = asyncHandler(async (req, res) => {
  const products = await Product.find({}).select('_id updatedAt name category')
  const blogs = await Blog.find({ isPublished: true }).select('_id updatedAt title')

  const now = new Date().toISOString().split('T')[0]

  const staticPages = [
    { url: '/', priority: '1.0', changefreq: 'daily' },
    { url: '/blog', priority: '0.8', changefreq: 'weekly' },
    { url: '/about', priority: '0.5', changefreq: 'monthly' },
    { url: '/contact', priority: '0.5', changefreq: 'monthly' },
    { url: '/filter?category=گیاه+زنده', priority: '0.9', changefreq: 'weekly' },
    { url: '/filter?category=کود+و+مکمل', priority: '0.7', changefreq: 'weekly' },
    { url: '/filter?category=بستر', priority: '0.7', changefreq: 'weekly' },
    { url: '/filter?category=لوازم+جانبی', priority: '0.7', changefreq: 'weekly' },
  ]

  let urls = staticPages.map((p) => `  <url>
    <loc>${SITE_URL}${p.url}</loc>
    <lastmod>${now}</lastmod>
    <changefreq>${p.changefreq}</changefreq>
    <priority>${p.priority}</priority>
  </url>`).join('\n')

  urls += products.map((p) => `
  <url>
    <loc>${SITE_URL}/product/${p._id}</loc>
    <lastmod>${new Date(p.updatedAt).toISOString().split('T')[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>`).join('')

  urls += blogs.map((b) => `
  <url>
    <loc>${SITE_URL}/blog/${b._id}</loc>
    <lastmod>${new Date(b.updatedAt).toISOString().split('T')[0]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>`).join('')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
${urls}
</urlset>`

  res.header('Content-Type', 'application/xml')
  res.header('Cache-Control', 'public, max-age=3600')
  res.send(xml)
})

export { generateSitemap }
