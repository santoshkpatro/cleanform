<script setup>
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { useAuthStore } from './stores/auth'
import { getUserStatus } from './api'


onMounted(async () => {
  const authStore = useAuthStore()

  const access_token = localStorage.getItem('access_token')
  if (access_token) {
    
    try {
      await getUserStatus(access_token)
      authStore.setAuthUser(access_token)
    } catch (e) {
      console.log(e)
      localStorage.removeItem('access_token')
    }

  }
})
</script>

<template>
  <Navbar />
  <RouterView />
</template>

<style>
/* @import '@/assets/base.css'; */
</style>
