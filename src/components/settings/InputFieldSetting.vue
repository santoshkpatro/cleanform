<script setup>
import { updateFormElement } from '../../api'
import { useBuilderStore } from '../../stores/builder'
import { notify } from '@kyvg/vue3-notification'

const builderStore = useBuilderStore()

async function changeElementSetting() {
  try {
    await updateFormElement(
      builderStore.form.id,
      builderStore.selectedElement.id,
      builderStore.selectedElement
    )

    notify({
      type: 'success',
      title: 'Element updated successfully!',
    })
  } catch (e) {
    notify({
      type: 'error',
      title: 'Unable to update',
    })
  }
}
</script>

<template>
  <form @submit.prevent="changeElementSetting">
    <!-- Required setting -->
    <div class="form-check form-switch mb-2">
      <input
        v-model="builderStore.selectedElement.is_required"
        class="form-check-input"
        type="checkbox"
        role="switch"
        id="required"
        :checked="builderStore.selectedElement.is_required"
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
        v-model="builderStore.selectedElement.label"
      />
    </div>

    <!-- placeholder setting -->
    <div class="mb-2">
      <label for="placeholder" class="form-label">Placeholder</label>
      <input
        type="text"
        id="placeholder"
        class="form-control"
        v-model="builderStore.selectedElement.properties.placeholder"
      />
    </div>

    <!-- type settting -->
    <div class="mb-2">
      <label for="type" class="form-label">Type</label>
      <select
        class="form-select"
        v-model="builderStore.selectedElement.properties.type"
      >
        <option value="text" selected>Text</option>
        <option value="number">Number</option>
        <option value="email">Email</option>
      </select>
    </div>

    <div class="d-grid gap-2">
      <button class="btn btn-sm btn-dark mt-2" type="submit">Update</button>
    </div>
  </form>
</template>
