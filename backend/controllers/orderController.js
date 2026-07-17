import asyncHandler from 'express-async-handler'
import Order from '../models/orderModel.js'
import Notification from '../models/notificationModel.js'
import Product from '../models/productModel.js'

// @desc    ساخت سفارش جدید
// @route   POST /api/orders
// @access  Private
const addOrderItems = asyncHandler(async (req, res) => {
  const {
    orderItems,
    shippingAddress,
    paymentMethod,
    itemsPrice,
    shippingPrice,
    totalPrice,
  } = req.body

  if (orderItems && orderItems.length === 0) {
    res.status(400)
    throw new Error('سبد خرید خالی است')
  }

  const order = new Order({
    orderItems: orderItems.map((x) => ({
      ...x,
      product: x._id,
      _id: undefined,
    })),
    user: req.user._id,
    shippingAddress,
    paymentMethod,
    itemsPrice,
    shippingPrice,
    totalPrice,
  })

  const createdOrder = await order.save()

  await Notification.create({
    type: 'new_order',
    title: 'سفارش جدید ثبت شد',
    message: `${req.user.name} یک سفارش جدید به مبلغ ${totalPrice.toLocaleString('fa-IR')} تومان ثبت کرد`,
    link: `/admin/orderlist`,
    relatedId: createdOrder._id,
  })

  res.status(201).json(createdOrder)
})

// @desc    دریافت سفارش با ID
// @route   GET /api/orders/:id
// @access  Private
const getOrderById = asyncHandler(async (req, res) => {
  const order = await Order.findById(req.params.id).populate(
    'user',
    'name email'
  )

  if (order) {
    res.json(order)
  } else {
    res.status(404)
    throw new Error('سفارش پیدا نشد')
  }
})

// @desc    آپلود رسید و درخواست تأیید پرداخت
// @route   PUT /api/orders/:id/pay
// @access  Private
const updateOrderToPaid = asyncHandler(async (req, res) => {
  const order = await Order.findById(req.params.id)

  if (order) {
    order.paymentResult = {
      receiptImage: req.body.receiptImage,
      receiptNote: req.body.receiptNote || '',
    }
    // isPaid بعد از تأیید ادمین true میشه
    const updatedOrder = await order.save()
    res.json(updatedOrder)
  } else {
    res.status(404)
    throw new Error('سفارش پیدا نشد')
  }
})

// @desc    تأیید پرداخت توسط ادمین
// @route   PUT /api/orders/:id/confirm
// @access  Private/Admin
const confirmOrderPayment = asyncHandler(async (req, res) => {
  const order = await Order.findById(req.params.id)

  if (order) {
    order.isPaid = true
    order.paidAt = Date.now()
    order.paymentResult.confirmedAt = Date.now()
    order.paymentResult.confirmedBy = req.user.name
    const updatedOrder = await order.save()
    for (const item of order.orderItems) {
      await Product.updateOne({ _id: item.product }, { $inc: { soldCount: item.qty } })
    }
    await Notification.create({
      type: 'order_confirmed',
      title: 'پرداخت شما تأیید شد',
      message: `پرداخت سفارش #${order._id.toString().slice(-6)} تأیید شد و سفارش شما در حال آماده‌سازی است`,
      link: `/order/${order._id}`,
      relatedId: order._id,
      user: order.user,
    })
    res.json(updatedOrder)
  } else {
    res.status(404)
    throw new Error('سفارش پیدا نشد')
  }
})

// @desc    آپدیت وضعیت ارسال
// @route   PUT /api/orders/:id/deliver
// @access  Private/Admin
const updateOrderToDelivered = asyncHandler(async (req, res) => {
  const order = await Order.findById(req.params.id)

  if (order) {
    order.isDelivered = true
    order.deliveredAt = Date.now()
    const updatedOrder = await order.save()
    await Notification.create({
      type: 'order_delivered',
      title: 'سفارش شما ارسال شد',
      message: `سفارش #${order._id.toString().slice(-6)} ارسال شد`,
      link: `/order/${order._id}`,
      relatedId: order._id,
      user: order.user,
    })
    res.json(updatedOrder)
  } else {
    res.status(404)
    throw new Error('سفارش پیدا نشد')
  }
})

// @desc    دریافت سفارش‌های کاربر
// @route   GET /api/orders/myorders
// @access  Private
const getMyOrders = asyncHandler(async (req, res) => {
  const orders = await Order.find({ user: req.user._id })
  res.json(orders)
})

// @desc    دریافت همه سفارش‌ها (ادمین)
// @route   GET /api/orders
// @access  Private/Admin
const getOrders = asyncHandler(async (req, res) => {
  const orders = await Order.find({}).populate('user', 'id name')
  res.json(orders)
})

export {
  addOrderItems,
  getOrderById,
  updateOrderToPaid,
  confirmOrderPayment,
  updateOrderToDelivered,
  getMyOrders,
  getOrders,
}