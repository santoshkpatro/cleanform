<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authLogin } from '../../api'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const credentials = reactive({
  email: '',
  password: '',
})

async function handleLogin() {
  try {
    const { data } = await authLogin({
      email: credentials.email,
      password: credentials.password,
    })

    authStore.setAuthUser(data.access_token)
    const { redirect } = route.query
    if (!redirect) {
      router.push({ name: 'home' })
    }

    router.push(redirect)
  } catch (e) {
    console.log(e.response.data.detail)
  }
}
</script>

<template>
  <div class="container">
    <form class="my-3" @submit.prevent="handleLogin">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="text"
          id="email"
          class="form-control"
          v-model="credentials.email"
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          id="password"
          class="form-control"
          v-model="credentials.password"
        />
      </div>

      <button class="btn btn-primary" type="submit">Login</button>
    </form>
  </div>
</template>
