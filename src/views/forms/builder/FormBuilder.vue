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

<template>
  <div class="builder">
    <div class="col-2">1</div>
    <div class="col-2">2</div>
    <div class="col-2">3</div>
    <div class="col-2">4</div>
    <div class="col-2">5</div>
    <div class="col-2">5</div>
    <div class="col-2">6</div>
    <div class="col-2">7</div>
    <div class="col-2">8</div>
    <div class="col-2">9</div>
    <div class="col-2">10</div>
    <div class="col-2">11</div>
    <div class="col-2">12</div>
  </div>
</template>

<style>
.scrolling-wrapper {
  overflow-x: auto;
}
.builder {
  overflow-x: scroll;
  display: flex;
}
</style>
