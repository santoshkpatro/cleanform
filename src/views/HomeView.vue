<script setup>
import { useRouter } from 'vue-router';

const router = useRouter()
</script>

<template>
  <body>
    <div class="container d-flex align-items-center justify-content-center">
      <div>
        <h1>Simple Clean Forms SASS Application</h1>
        <button class="btn btn-sm btn-primary" @click="router.push({ name: 'formList' })">Click Here to get started!!</button>
      </div>
    </div>
  </body>
</template>

<style scoped>
body {
  height: 80vh;
}
.container {
  height: 100%;
}
</style>
