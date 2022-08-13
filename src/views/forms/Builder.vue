<script setup>
import { ref, onMounted } from 'vue'
import {
  getFormDetails,
  getFormElements,
  updateFormElementOrder,
} from '../../api'
import { useBuilderStore } from '../../stores/builder'
import draggable from 'vuedraggable'
import { notify } from "@kyvg/vue3-notification";


import InputFieldElement from '../../components/elements/InputFieldElement.vue'
import RadioFieldElement from '../../components/elements/RadioFieldElement.vue'
import CheckboxFieldElement from '../../components/elements/CheckboxFieldElement.vue'

import InputFieldSetting from '../../components/settings/InputFieldSetting.vue'
import RadioFieldSetting from '../../components/settings/RadioFieldSetting.vue'
import CheckboxFieldSetting from '../../components/settings/CheckboxFieldSetting.vue'

const { formId } = defineProps(['formId'])
const builderStore = useBuilderStore()

onMounted(async () => {
  // API Call to fetch form details
  try {
    const formResponse = await getFormDetails(formId)
    builderStore.setForm(formResponse.data)
  } catch (e) {
    notify({
      type: 'error',
      title: 'Unable to fetch form details.',
    })
  }

  // API Call to fetch form elements
  try {
    const elementResponse = await getFormElements(formId)
    builderStore.setFormElements(elementResponse.data)
  } catch (e) {
    notify({
      type: 'error',
      title: 'Unable to fetch form elements.',
    })
  }
})

async function handleUpdate() {
  try {
    await updateFormElementOrder(formId, builderStore.ordering)
  } catch (e) {
    notify({
      type: 'error',
      title: 'Unable to update form element order',
    })
  }
}
</script>

<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-6" v-if="builderStore.selectedElement">
        <div class="d-flex justify-content-between">
          <h5>Element Setting</h5>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="30"
            height="30"
            fill="currentColor"
            class="bi bi-x"
            viewBox="0 0 16 16"
            @click="builderStore.removeSelectedElement"
          >
            <path
              d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"
            />
          </svg>
        </div>
        <InputFieldSetting
          v-if="builderStore.selectedElement.type === 'input_field'"
        />
        <RadioFieldSetting
          v-if="builderStore.selectedElement.type === 'radio_field'"
        />
        <CheckboxFieldSetting
          v-if="builderStore.selectedElement.type === 'checkbox_field'"
        />
      </div>
      <div :class="{ 'col-12': !builderStore.selectedElement, 'col-6': builderStore.selectedElement }">
        <h3>{{ builderStore.form.title }}</h3>
        <draggable
          v-model="builderStore.formElements"
          group="element"
          @start="drag = true"
          @end="drag = false"
          @update="handleUpdate"
          item-key="id"
        >
          <template #item="{ element }">
            <div
              class="my-2 p-3 shadow bg-body rounded border-secondary border-1"
              id="element"
              :class="{
                'selected-element': builderStore.selectedElement === element,
              }"
              @click="builderStore.setSelectedElement(element)"
            >
              <InputFieldElement
                v-if="element.type === 'input_field'"
                :element="element"
              />
              <RadioFieldElement
                v-if="element.type === 'radio_field'"
                :element="element"
              />
              <CheckboxFieldElement
                v-if="element.type === 'checkbox_field'"
                :element="element"
              />
            </div>
          </template>
        </draggable>
        <div class="d-grid gap-2 mt-3">
          <button class="btn btn-dark">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#element:hover {
  cursor: pointer;
}

.selected-element {
  border-style: dashed;
}
</style>
