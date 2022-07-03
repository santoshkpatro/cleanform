<script setup>
import { reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getFormDetails, getFormElements } from '../../../api'

const route = useRoute()
const router = useRouter()

const builder = reactive({
  form: {},
  elements: [],
  selectedElement: '',
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

function viewSelectedElement(element_id) {
  builder.selectedElement = builder.elements.find(
    (element) => element.id === element_id
  )
}
</script>

<template>
  <!-- Elements List -->
  <div class="builder mt-2">
    <div
      class="col-2 mx-2"
      v-for="(element, index) in builder.elements"
      :key="element"
      @click="viewSelectedElement(element.id)"
    >
      <div class="card">
        <div class="card-body">
          <h5 class="text-center">Page - {{ index + 1 }}</h5>
        </div>
      </div>
    </div>
    <div class="col-2 mx-2">
      <div class="card">
        <div class="card-body">
          <div class="text-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="25"
              height="25"
              fill="currentColor"
              class="bi bi-plus-circle"
              viewBox="0 0 16 16"
            >
              <path
                d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
              />
              <path
                d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Element Editor -->
  <div class="container mt-5">
    <div v-if="builder.selectedElement"></div>
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
