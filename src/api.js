import axios from 'axios'

export const http = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL}/v1`
})

export const formHttp = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL}/`
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

export const createForm = (data) => http.post('forms/', data)

export const getForms = () => http.get('forms/')

export const updateForm = (form_id, data) => http.put(`forms/${form_id}/`, data)

export const updateFormElementOrder = (form_id, new_order) => http.patch(`forms/${form_id}/`, {
  "elements": new_order
})

export const getFormDetails = (form_id) => http.get(`forms/${form_id}/`)

export const getFormElements = (form_id) => http.get(`forms/${form_id}/elements/`)

export const createFormElement = (form_id, data) => http.post(`forms/${form_id}/elements/`, data)

export const updateFormElement = (form_id, element_id, new_data) => http.put(`forms/${form_id}/elements/${element_id}/`, new_data)

export const deleteFormElement = (formId, elementId) => http.delete(`forms/${formId}/elements/${elementId}/`)

export const getSubmissions = (form_id) => http.get(`forms/${form_id}/submissions/`)
