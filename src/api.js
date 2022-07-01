import axios from 'axios'

export const http = axios.create({
  baseURL: 'http://127.0.0.1:8000/v1/',
})

export const getUserStatus = (access_token) => http.get('auth/status/', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
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

export const getProfile = () => http.get('auth/profile/')

export const getForms = () => http.get('forms/')