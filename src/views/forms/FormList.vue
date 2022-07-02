<script setup>
import { reactive, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getForms } from '../../api'

const router = useRouter()
const forms = ref([])

onMounted(async () => {
  try {
    const { data } = await getForms()
    forms.value = data.results
  } catch (e) {
    console.log(e)
  }
})
</script>

<template>
  <div class="container">
    <h5
      @click="router.push({ name: 'formDetail', params: { form_id: form.id } })"
      v-for="form in forms"
      :key="form.id"
    >
      {{ form.title }}
    </h5>
  </div>
</template>
