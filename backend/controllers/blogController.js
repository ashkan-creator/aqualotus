import asyncHandler from 'express-async-handler'
import Blog from '../models/blogModel.js'

// @desc    دریافت پست‌های منتشر شده
// @route   GET /api/blog
// @access  Public
const getPosts = asyncHandler(async (req, res) => {
  const posts = await Blog.find({ isPublished: true })
    .sort({ createdAt: -1 })
    .populate('user', 'name')
  res.json(posts)
})

// @desc    دریافت پست‌های فعال‌شده برای اسلایدر وبلاگ
// @route   GET /api/blog/featured
// @access  Public
const getFeaturedPosts = asyncHandler(async (req, res) => {
  const posts = await Blog.find({ isPublished: true, featuredInSlider: true })
    .sort({ createdAt: -1 })
    .populate('user', 'name')
  res.json(posts)
})

// @desc    دریافت همه پست‌ها برای ادمین
// @route   GET /api/blog/all
// @access  Private/Admin
const getAllPosts = asyncHandler(async (req, res) => {
  const posts = await Blog.find({}).sort({ createdAt: -1 }).populate('user', 'name')
  res.json(posts)
})

// @desc    دریافت یک پست
// @route   GET /api/blog/:id
// @access  Public
const getPostById = asyncHandler(async (req, res) => {
  const post = await Blog.findById(req.params.id)
    .populate('user', 'name')
    .populate('relatedProducts')
  if (post) {
    res.json(post)
  } else {
    res.status(404)
    throw new Error('پست پیدا نشد')
  }
})

// @desc    ساخت پست جدید
// @route   POST /api/blog
// @access  Private/Admin
const createPost = asyncHandler(async (req, res) => {
  const { title, content, image, video, isPublished, relatedProducts } = req.body
  const post = await Blog.create({
    user: req.user._id,
    title,
    content,
    image: image || '',
    video: video || '',
    isPublished: isPublished || false,
    relatedProducts: relatedProducts || [],
  })
  res.status(201).json(post)
})

// @desc    آپدیت پست
// @route   PUT /api/blog/:id
// @access  Private/Admin
const updatePost = asyncHandler(async (req, res) => {
  const post = await Blog.findById(req.params.id)
  if (post) {
    post.title = req.body.title ?? post.title
    post.content = req.body.content ?? post.content
    post.image = req.body.image ?? post.image
    post.video = req.body.video ?? post.video
    post.isPublished = req.body.isPublished ?? post.isPublished
    post.featuredInSlider = req.body.featuredInSlider ?? post.featuredInSlider
    post.relatedProducts = req.body.relatedProducts ?? post.relatedProducts
    const updated = await post.save()
    res.json(updated)
  } else {
    res.status(404)
    throw new Error('پست پیدا نشد')
  }
})

// @desc    حذف پست
// @route   DELETE /api/blog/:id
// @access  Private/Admin
const deletePost = asyncHandler(async (req, res) => {
  const post = await Blog.findById(req.params.id)
  if (post) {
    await Blog.deleteOne({ _id: post._id })
    res.json({ message: 'پست حذف شد' })
  } else {
    res.status(404)
    throw new Error('پست پیدا نشد')
  }
})

export { getPosts, getFeaturedPosts, getAllPosts, getPostById, createPost, updatePost, deletePost }
