import Product from '../models/productModel.js'

// @desc    گرفتن نتیجه کوییز انتخاب گیاه مناسب
// @route   POST /api/quiz/results
// @access  عمومی
const getQuizResults = async (req, res) => {
  try {
    const { careLevel, lightNeeds, co2Needs, position, growthRate, needsSoil } = req.body

    const products = await Product.find({ category: 'گیاه زنده' }).lean()

    const scored = products.map((p) => {
      let score = 0
      if (careLevel && p.careLevel === careLevel) score++
      if (lightNeeds && p.lightNeeds === lightNeeds) score++
      if (co2Needs && p.co2Needs === co2Needs) score++
      if (position && p.position === position) score++
      if (growthRate && p.growthRate === growthRate) score++
      if (typeof needsSoil === 'boolean' && p.needsSoil === needsSoil) score++
      return { ...p, quizScore: score }
    })

    scored.sort((a, b) => b.quizScore - a.quizScore)

    const RESULT_COUNT = 5
    const results = scored.slice(0, RESULT_COUNT)

    res.json({ results })
  } catch (error) {
    res.status(500).json({ message: error.message })
  }
}

export { getQuizResults }
