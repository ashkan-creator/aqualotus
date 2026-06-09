import bcrypt from 'bcryptjs'

const users = [
  {
    name: 'ادمین AquaLotus',
    email: 'admin@aqualotus.ir',
    password: bcrypt.hashSync('123456', 10),
    isAdmin: true,
  },
  {
    name: 'محمدحسین اکبری زرین',
    email: 'ashkan@aqualotus.ir',
    password: bcrypt.hashSync('123456', 10),
    isAdmin: false,
  },
  {
    name: 'سارا محمدی',
    email: 'sara@aqualotus.ir',
    password: bcrypt.hashSync('123456', 10),
    isAdmin: false,
  },
]

export default users