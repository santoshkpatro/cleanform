<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authLogin } from '../../api'
// import router from '../../router';
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const credentials = reactive({
  email: '',
  password: '',
})

onMounted(() => {
  console.log(route.query)
})

async function handleLogin() {
  try {
    const { data } = await authLogin({
      email: credentials.email,
      password: credentials.password,
    })
    
    authStore.setAuthUser(data.access_token)

    // check for next query params
    if(route.query.hasOwnProperty('redirect')) {
      router.push(route.query.redirect)
    } else {
      // Redirecting to home page
      router.push({name: 'home'})
    }

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
