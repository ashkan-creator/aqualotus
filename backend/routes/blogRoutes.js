import express from 'express'
import {
  getPosts,
  getAllPosts,
  getPostById,
  createPost,
  updatePost,
  deletePost,
} from '../controllers/blogController.js'
import { protect, admin } from '../middleware/authMiddleware.js'

const router = express.Router()
router.route('/').get(getPosts).post(protect, admin, createPost)
router.get('/all', protect, admin, getAllPosts)
router.route('/:id').get(getPostById).put(protect, admin, updatePost).delete(protect, admin, deletePost)

export default router
