<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()

function handleLogout() {
  authStore.removeAuthUser()
}
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-light">
    <div class="container">
      <router-link class="navbar-brand" :to="{ name: 'home' }"
        >Cleanform</router-link
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link :to="{ name: 'formList' }" class="nav-link"
              >My Forms</router-link
            >
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item" v-if="!authStore.isLoggedIn">
            <router-link
              class="btn btn-sm btn-primary mx-1"
              :to="{ name: 'login' }"
              >Login</router-link
            >
          </li>
          <li class="nav-item" v-if="!authStore.isLoggedIn">
            <router-link
              class="btn btn-sm btn-dark mx-1"
              :to="{ name: 'register' }"
              >Register</router-link
            >
          </li>
          <li class="nav-item" v-if="authStore.isLoggedIn">
            <button
              class="btn btn-sm btn-secondary"
              href="#"
              @click="handleLogout"
            >
              logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
