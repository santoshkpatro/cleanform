<script setup>
import { reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getFormDetails, getFormElements } from '../../../api'

const route = useRoute()
const router = useRouter()

const builder = reactive({
  form: {},
  elements: [],
})

onMounted(async () => {
  const { form_id } = route.params

  try {
    const formResponse = await getFormDetails(form_id)
    builder.form = formResponse.data

    const elementResponse = await getFormElements(form_id)

    formResponse.data.elements.forEach((e) => {
      const obj = elementResponse.data.find((o) => o.id === e)
      builder.elements.push(obj)
    })
  } catch (e) {
    console.log(e)
  }
})
</script>

<template></template>

<style>
.scrolling-wrapper {
  overflow-x: auto;
}
</style>
