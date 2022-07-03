import { defineStore } from 'pinia'
import { http } from '../api'

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    isAuthenticated: false,
    profile: {}
  }),
  getters: {
    isLoggedIn: (state) => state.isAuthenticated
  },
  actions: {
    setAuthUser(access_token) {
      this.isAuthenticated = true
      localStorage.setItem('access_token', access_token)
      http.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    },
    removeAuthUser() {
      this.isAuthenticated = false
      localStorage.removeItem('access_token')
      location.reload()
    }
  }
})
