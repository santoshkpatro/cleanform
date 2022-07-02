<script setup>
import { reactive, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getFormDetails, getFormElements } from '../../api'

const form = ref({})
const elements = ref([])
const route = useRoute()

onMounted(async () => {
  const { form_id } = route.params

  // Fetching the form
  try {
    const { data } = await getFormDetails(form_id)
    form.value = data
  } catch (e) {
    console.log(e)
  }

  // Fetching the form elements
  try {
    const { data } = await getFormElements(form_id)
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
      </div>
    </div>
  </div>
</template>
