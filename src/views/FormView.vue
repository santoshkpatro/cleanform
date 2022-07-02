<script setup>
import { onMounted, ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { formView, formSubmission } from '../api'

const route = useRoute()
const router = useRouter()

const form = ref({})
const form_slug = ref('')
const elements = ref([])
const selectedElement = ref(0)
const submission = reactive({})

// Mounted
onMounted(async () => {
  const { slug } = route.params
  form_slug.value = slug

  try {
    const { data } = await formView(slug)
    form.value = data

    // Rearranging the elements
    data.elements_order.forEach((e) => {
      const element_obj = data.elements.find((i) => i.id === e)

      if (element_obj) {
        elements.value.push(element_obj)
      }
    })

    // Declaring the reactive data model
    elements.value.forEach((e) => {
      switch (e.type) {
        case 'input_field':
          submission[e.label] = ''
          break

        case 'checkbox_field':
          submission[e.label] = e.properties.default_checked_choices
          break

        case 'radio_field':
          submission[e.label] = e.properties.default_option
          break

        default:
          break
      }
    })
  } catch (e) {
    console.log(e)
  }
})

// Handle pagination
function handleNext() {
  selectedElement.value = selectedElement.value + 1
}

function handlePrevious() {
  selectedElement.value = selectedElement.value - 1
}

// Handle Submission
async function handleSubmission() {
  try {
    await formSubmission(form_slug.value, submission)
  } catch (e) {
    console.log(e)
  }
}
</script>

<template>
  <h1>Form: {{ form.title }}</h1>
  <div class="container">
    <form
      @submit.prevent="handleSubmission"
      class="border border-secondary p-5"
    >
      <div
        v-for="(element, idx) in elements"
        :key="element.id"
        class="my-2"
        v-show="idx === selectedElement"
      >
        <!-- Input Field Element -->
        <div v-if="element.type === 'input_field'">
          <label :for="element.id" class="form-label">{{
            element.label
          }}</label>
          <input
            :id="element.id"
            :type="element.properties.type ? element.properties.type : 'text'"
            class="form-control"
            :required="element.is_required"
            :name="element.label"
            v-model="submission[element.label]"
          />
        </div>

        <!-- Radio Field Element -->
        <div v-if="element.type === 'radio_field'">
          <label :for="element.id">{{ element.label }}</label>
          <div
            class="form-check"
            v-for="(option, index) in element.properties.options"
            :key="option"
          >
            <input
              class="form-check-input"
              type="radio"
              v-model="submission[element.label]"
              :name="element.label"
              :id="`${element.label} ${option}`"
              :value="option"
              :required="element.is_required"
            />
            <label
              class="form-check-laqbel"
              :for="`${element.label} ${option}`"
            >
              {{ option }}
            </label>
          </div>
        </div>

        <!-- Checkbox field element -->
        <div v-if="element.type === 'checkbox_field'">
          <label class="form-label" :for="element.id">
            {{ element.label }}
          </label>

          <div
            class="form-check"
            v-for="(choice, index) in element.properties.choices"
            :key="choice"
          >
            <input
              v-model="submission[element.label]"
              class="form-check-input"
              type="checkbox"
              :value="choice"
              :id="`${element.label} ${choice}`"
            />
            <label class="form-check-label" :for="`${element.label} ${choice}`">
              {{ choice }}
            </label>
          </div>
        </div>

        <!-- Pagination and Submit button -->
        <div class="clearfix mt-5">
          <button
            type="button"
            class="btn btn-outline-success btn-sm float-start"
            @click="handlePrevious"
            :disabled="selectedElement === 0"
          >
            Prev
          </button>
          <button
            type="button"
            class="btn btn-success btn-sm float-end"
            @click="handleNext"
            :disabled="selectedElement === elements.length - 1"
          >
            Next
          </button>
        </div>

        <!-- Submit button -->
        <div
          class="d-grid gap-2 mt-4"
          v-show="selectedElement === elements.length - 1"
        >
          <button class="btn btn-sm btn-primary" type="submit">Submit</button>
        </div>
      </div>
    </form>
  </div>
</template>
