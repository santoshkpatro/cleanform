<script setup>
import { reactive, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getFormDetails } from '../../api'

const form = ref({})
const route = useRoute()
const router = useRouter()

onMounted(async () => {
  const { form_id } = route.params
  try {
    const { data } = await getFormDetails(form_id)
    form.value = data
  } catch (e) {
    console.log(e)
  }
})
</script>

<template>
  <div class="container">
    <div class="card">
      <div class="card-body">
        <h5>Name: {{ form.title }}</h5>
        <button
          @click="
            router.push({ name: 'formBuilder', params: { form_id: form.id } })
          "
          class="btn btn-sm btn-primary"
        >
          Build the form
        </button>
      </div>
    </div>
  </div>
</template>
