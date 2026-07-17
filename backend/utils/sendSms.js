import Kavenegar from 'kavenegar'

const sendSms = ({ to, message }) => {
  return new Promise((resolve, reject) => {
    const api = Kavenegar.KavenegarApi({ apikey: process.env.KAVENEGAR_API_KEY })
    api.Send(
      {
        message,
        sender: process.env.KAVENEGAR_SENDER,
        receptor: to,
      },
      (response, status) => {
        if (status === 200) {
          resolve(response)
        } else {
          reject(new Error(`Kavenegar error, status: ${status}`))
        }
      }
    )
  })
}

export default sendSms
