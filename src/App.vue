<script setup>
import { onMounted, ref } from 'vue'
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { useAuthStore } from './stores/auth'
import { getUserStatus } from './api'

const isLoading = ref(false)

const authStore = useAuthStore()

onMounted(async () => {
  const access_token = localStorage.getItem('access_token')
  if (access_token) {
    isLoading.value = true

    try {
      await getUserStatus(access_token)
      authStore.setAuthUser(access_token)
    } catch (e) {
      localStorage.removeItem('access_token')
    } finally {
      isLoading.value = false
    }
  }
})
</script>

<template>
  <notifications />
  <Navbar />
  <RouterView v-if="!isLoading" />
</template>

<style>
/* @import '@/assets/base.css'; */
</style>
