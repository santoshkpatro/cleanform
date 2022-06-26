import axios from 'axios'

export const http = axios.create({
  baseURL: 'http://127.0.0.1:8000/v1/',
})

export const authLogin = (data) => http.post('auth/login/', data)
export const verifyRegistrationToken = (token) =>
  http.get('auth/register/', {
    params: {
      token,
    },
  })

export const sendRegistrationEmail = (email) =>
  http.get('auth/register/email/', {
    params: {
      email,
    },
  })
export const register = (credentials, token) =>
  http.post('auth/register/', credentials, {
    params: {
      token: token,
    },
  })
