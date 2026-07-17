import nodemailer from 'nodemailer'

const sendEmail = async ({ to, subject, html }) => {
  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: Number(process.env.SMTP_PORT) || 587,
    secure: false,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  })

  await transporter.sendMail({
    from: `"AquaLotus" <${process.env.SMTP_USER}>`,
    to,
    subject,
    html,
  })
}

export default sendEmail
