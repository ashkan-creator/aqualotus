import asyncHandler from 'express-async-handler'
import Product from '../models/productModel.js'
import Blog from '../models/blogModel.js'

const SITE_URL = process.env.SITE_URL || 'https://aqualotus.ir'

const generateSitemap = asyncHandler(async (req, res) => {
  const products = await Product.find({}).select('_id updatedAt')
  const blogs = await Blog.find({}).select('_id updatedAt')

  const staticPages = [
    { url: '/', priority: '1.0' },
    { url: '/about', priority: '0.5' },
    { url: '/contact', priority: '0.5' },
    { url: '/blog', priority: '0.7' },
  ]

  let urls = staticPages
    .map(
      (p) => `  <url>
    <loc>${SITE_URL}${p.url}</loc>
    <priority>${p.priority}</priority>
  </url>`
    )
    .join('\n')

  urls += products
    .map(
      (p) => `
  <url>
    <loc>${SITE_URL}/product/${p._id}</loc>
    <lastmod>${new Date(p.updatedAt).toISOString().split('T')[0]}</lastmod>
    <priority>0.8</priority>
  </url>`
    )
    .join('')

  urls += blogs
    .map(
      (b) => `
  <url>
    <loc>${SITE_URL}/blog/${b._id}</loc>
    <lastmod>${new Date(b.updatedAt).toISOString().split('T')[0]}</lastmod>
    <priority>0.6</priority>
  </url>`
    )
    .join('')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`

  res.header('Content-Type', 'application/xml')
  res.send(xml)
})

export { generateSitemap }
