import axios from 'axios'

export const http = axios.create({
  baseURL: 'http://127.0.0.1:8000/v1/',
})

export const formHttp = axios.create({
  baseURL: 'http://127.0.0.1:8000/'
})

export const formView = (slug) => formHttp.get(`f/${slug}/`)
export const formSubmission = (slug, data) => formHttp.post(`f/${slug}/`, data=data)

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

export const getFormDetails = (form_id) => http.get(`forms/${form_id}/`)

export const getFormElements = (form_id) => http.get(`forms/${form_id}/elements/`)

export const getSubmissions = (form_id) => http.get(`forms/${form_id}/submissions/`)