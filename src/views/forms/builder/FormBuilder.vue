<script setup>
import { reactive, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  getFormDetails,
  getFormElements,
  updateFormElement,
  createFormElement,
} from '../../../api'

const route = useRoute()
const router = useRouter()

const builder = reactive({
  form: {},
  elements: [],
  selectedElement: '',
})

const newElement = ref('input_field')

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

async function changeElementSetting() {
  const { form_id } = route.params

  try {
    const { data } = await updateFormElement(
      form_id,
      builder.selectedElement.id,
      builder.selectedElement
    )
    console.log(data)
  } catch (e) {
    console.log(e)
  }
}

async function addNewElement() {
  const { form_id } = route.params

  switch (newElement.value) {
    case 'input_field':
      try {
        const { data } = await createFormElement(form_id, {
          type: 'input_field',
          label: 'New Input Field',
          description: '',
          is_required: false,
          properties: {
            type: 'text',
            placeholder: '',
          },
          layouts: {},
          validations: {},
        })

        builder.elements.push(data)
        builder.form.elements.push(data.id)
      } catch (e) {
        console.log(e)
      }

      break

    case 'radio_field':
      try {
        const { data } = await createFormElement(form_id, {
          type: 'radio_field',
          label: 'New Radio Field',
          description: '',
          is_required: false,
          properties: {
            options: ['Option 1', 'Option 2', 'Option 3'],
            default_option: ['Option 2'],
          },
          layouts: {},
          validations: {},
        })

        builder.elements.push(data)
        builder.form.elements.push(data.id)
      } catch (e) {
        console.log(e)
      }
      break

    case 'checkbox_field':
      try {
        const { data } = await createFormElement(form_id, {
          type: 'checkbox_field',
          label: 'New checkbox Field',
          description: '',
          is_required: false,
          properties: {
            choices: ['Choice 1', 'Choice 2', 'Choice 3', 'Choice 4'],
            default_checked_choices: ['Choice 2', 'Choice 3'],
          },
          layouts: {},
          validations: {},
        })

        builder.elements.push(data)
        builder.form.elements.push(data.id)
      } catch (e) {
        console.log(e)
      }
      break

    default:
      break
  }
}
</script>

<template>
  <!-- Elements List -->
  <div class="container builder mt-2">
    <div
      class="col-2 mx-2"
      v-for="(element, index) in builder.elements"
      :key="element"
      @click="viewSelectedElement(element.id)"
    >
      <div class="card">
        <div
          class="card-body"
          :class="{
            'bg-dark text-white': builder.selectedElement.id === element.id,
          }"
        >
          <h5 class="text-center">Page - {{ index + 1 }}</h5>
          <p>{{ element.label }}</p>
        </div>
      </div>
    </div>
    <div class="col-2 mx-2">
      <div
        class="card"
        data-bs-toggle="modal"
        data-bs-target="#addElementModal"
      >
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
    <div v-if="builder.selectedElement">
      <!-- Input Field Element -->
      <div class="row" v-if="builder.selectedElement.type === 'input_field'">
        <div class="col me-2">
          <label :for="builder.selectedElement.id" class="form-label">{{
            builder.selectedElement.label
          }}</label>
          <input
            :required="builder.selectedElement.is_required"
            :id="builder.selectedElement.id"
            :type="builder.selectedElement.properties.type"
            class="form-control"
            :placeholder="builder.selectedElement.properties.placeholder"
          />
        </div>
        <div class="col ms-2">
          <h5>Settings :</h5>
          <!-- required setting -->
          <div class="form-check form-switch mb-2">
            <input
              v-model="builder.selectedElement.is_required"
              class="form-check-input"
              type="checkbox"
              role="switch"
              id="required"
              :checked="builder.selectedElement.is_required"
            />
            <label class="form-check-label" for="required">Required</label>
          </div>

          <!-- label setting -->
          <div class="mb-2">
            <label for="label" class="form-label">Label</label>
            <input
              type="text"
              id="label"
              class="form-control"
              v-model="builder.selectedElement.label"
            />
          </div>

          <!-- placeholder setting -->
          <div class="mb-2">
            <label for="placeholder" class="form-label">Placeholder</label>
            <input
              type="text"
              id="placeholder"
              class="form-control"
              v-model="builder.selectedElement.properties.placeholder"
            />
          </div>

          <!-- type settting -->
          <div class="mb-2">
            <label for="type" class="form-label">Type</label>
            <select
              class="form-select"
              v-model="builder.selectedElement.properties.type"
            >
              <option value="text" selected>Text</option>
              <option value="number">Number</option>
              <option value="email">Email</option>
            </select>
          </div>

          <div class="d-grid gap-2">
            <button class="btn btn-sm btn-dark" @click="changeElementSetting">
              Update
            </button>
          </div>
        </div>
      </div>

      <!-- Radio Field Element -->
      <div class="row" v-if="builder.selectedElement.type === 'radio_field'">
        <div class="col me-2">
          <label :for="builder.selectedElement.id" class="form-label">{{
            builder.selectedElement.label
          }}</label>

          <div
            class="form-check"
            v-for="option in builder.selectedElement.properties.options"
            :key="option"
          >
            <input
              class="form-check-input"
              type="radio"
              :checked="
                option === builder.selectedElement.properties.default_option
              "
              name="`${builder.selectedElement.label} ${option}`"
              :id="`${builder.selectedElement.id} ${option}`"
            />
            <label
              class="form-check-label"
              :for="`${builder.selectedElement.id} ${option}`"
            >
              {{ option }}
            </label>
          </div>
        </div>
        <div class="col ms-2">
          <h5>Settings:</h5>
          <!-- required setting -->
          <div class="form-check form-switch mb-2">
            <input
              v-model="builder.selectedElement.is_required"
              class="form-check-input"
              type="checkbox"
              role="switch"
              id="required"
              :checked="builder.selectedElement.is_required"
            />
            <label class="form-check-label" for="required">Required</label>
          </div>

          <!-- label setting -->
          <div class="mb-2">
            <label for="label" class="form-label">Label</label>
            <input
              type="text"
              id="label"
              class="form-control"
              v-model="builder.selectedElement.label"
            />
          </div>

          <!-- options setting -->
          <div class="mb-2">
            <label for="" class="form-label">Options</label>
            <input
              type="text"
              :value="builder.selectedElement.properties.options.join(',')"
              @input="
                (event) =>
                  (builder.selectedElement.properties.options =
                    event.target.value.split(','))
              "
              class="form-control"
            />
          </div>

          <!-- default option setting -->
          <div class="mb-2">
            <label for="" class="form-label">Default Option</label>
            <select
              class="form-select"
              v-model="builder.selectedElement.properties.default_option"
            >
              <option
                v-for="option in builder.selectedElement.properties.options"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <div class="d-grid gap-2">
            <button class="btn btn-sm btn-dark" @click="changeElementSetting">
              Update
            </button>
          </div>
        </div>
      </div>

      <!-- Choice Field Element -->
      <div class="row" v-if="builder.selectedElement.type === 'checkbox_field'">
        <div class="col me-2">
          <label :for="builder.selectedElement.id" class="form-label">{{
            builder.selectedElement.label
          }}</label>
          <div
            class="form-check"
            v-for="choice in builder.selectedElement.properties.choices"
            :key="choice"
          >
            <input
              class="form-check-input"
              type="checkbox"
              id="flexCheckChecked"
              :checked="
                builder.selectedElement.properties.default_checked_choices.includes(
                  choice
                )
              "
            />
            <label class="form-check-label" for="flexCheckChecked">
              {{ choice }}
            </label>
          </div>
        </div>
        <div class="col ms-2">
          <h5>Settings:</h5>
          <!-- required setting -->
          <div class="form-check form-switch mb-2">
            <input
              v-model="builder.selectedElement.is_required"
              class="form-check-input"
              type="checkbox"
              role="switch"
              id="required"
              :checked="builder.selectedElement.is_required"
            />
            <label class="form-check-label" for="required">Required</label>
          </div>

          <!-- label setting -->
          <div class="mb-2">
            <label for="label" class="form-label">Label</label>
            <input
              type="text"
              id="label"
              class="form-control"
              v-model="builder.selectedElement.label"
            />
          </div>

          <!-- choice setting -->
          <div class="mb-2">
            <label for="" class="form-label">Choices</label>
            <input
              type="text"
              :value="builder.selectedElement.properties.choices.join(',')"
              @input="
                (event) =>
                  (builder.selectedElement.properties.choices =
                    event.target.value.split(','))
              "
              class="form-control"
            />
          </div>

          <!-- default checked choices -->
          <label for="" class="form-label">Default checked choices</label>
          <div
            class="form-check"
            v-for="choice in builder.selectedElement.properties.choices"
            :key="choice"
          >
            <input
              class="form-check-input"
              type="checkbox"
              id="flexCheckChecked"
              :value="choice"
              v-model="
                builder.selectedElement.properties.default_checked_choices
              "
            />
            <label class="form-check-label" for="flexCheckChecked">
              {{ choice }}
            </label>
          </div>

          <div class="d-grid gap-2">
            <button class="btn btn-sm btn-dark" @click="changeElementSetting">
              Update
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Element Modal -->
  <div
    class="modal fade"
    id="addElementModal"
    tabindex="-1"
    aria-labelledby="addElementModal"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addElementModal">Add Element</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <form @submit.prevent="addNewElement">
          <div class="modal-body">
            <label for="" class="form-label">Select Element type</label>
            <select class="form-select" v-model="newElement">
              <option value="input_field" selected>Input Element</option>
              <option value="radio_field">Radio Element</option>
              <option value="checkbox_field">Choice Element</option>
            </select>
          </div>
          <div class="modal-footer">
            <button
              type="submit"
              class="btn btn-primary"
              data-bs-dismiss="modal"
            >
              Add Element
            </button>
          </div>
        </form>
      </div>
    </div>
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
