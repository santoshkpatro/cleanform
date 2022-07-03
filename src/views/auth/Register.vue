<script setup>
import { reactive } from 'vue'
import { useRoute } from 'vue-router'
import {
  verifyRegistrationToken,
  sendRegistrationEmail,
  register,
} from '../../api'

const route = useRoute()
const credentials = reactive({
  email: '',
  full_name: '',
  password: '',
  confirm_password: '',
})

const user = reactive({
  new_email: '',
  registration_token: '',
})

async function checkVerificationToken(token) {
  try {
    const { data } = await verifyRegistrationToken(token)
    credentials.email = data.email
  } catch (e) {
    console.log(e)
  }
}

async function sendRegistrationLink() {
  try {
    sendRegistrationEmail(user.new_email)
  } catch (e) {
    console.log(e)
  }
}

async function handleRegistration() {
  try {
    const { data } = await register(credentials, user.registration_token)
    console.log(data)
  } catch (e) {
    console.log(e)
  }
}

if (route.query.token) {
  checkVerificationToken(route.query.token)
  user.registration_token = route.query.token
}
</script>

<template>
  <div class="container">
    <!-- Registration Email -->
    <div v-if="!route.query.token">
      <div class="col-5">
        <form @submit.prevent="sendRegistrationLink">
          <label for="email" class="form-label">Enter your email address</label>
          <input
            v-model="user.new_email"
            type="text"
            class="form-control"
            id="name"
          />
          <button class="btn btn-success mt-3">Send registration link</button>
        </form>
      </div>
    </div>

    <!-- Registration Form -->
    <div v-else>
      <h5>Enter your details</h5>
      <form class="my-3" @submit.prevent="handleRegistration">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="text"
            id="email"
            disabled
            class="form-control"
            v-model="credentials.email"
          />
        </div>

        <div class="mb-3">
          <label for="full_name" class="form-label">Full Name</label>
          <input
            type="text"
            id="full_name"
            class="form-control"
            v-model="credentials.full_name"
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

        <div class="mb-3">
          <label for="confirm_password" class="form-label"
            >Confirm Password</label
          >
          <input
            type="password"
            id="confirm_password"
            class="form-control"
            v-model="credentials.confirm_password"
          />
        </div>

        <button class="btn btn-primary" type="submit">Login</button>
      </form>
    </div>
  </div>
</template>
