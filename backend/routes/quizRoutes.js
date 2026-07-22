import express from 'express'
import { getQuizResults } from '../controllers/quizController.js'

const router = express.Router()

router.post('/results', getQuizResults)

export default router
