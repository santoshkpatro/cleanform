<script setup>
import { updateFormElement } from '../../api'
import { useBuilderStore } from '../../stores/builder'
import { notify } from "@kyvg/vue3-notification";

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
        title: 'Element updated successfully!'
    })
  } catch (e) {
    console.log(e)
  }
}
</script>

<template>
  <form @submit.prevent="changeElementSetting">
    <!-- required setting -->
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

    <!-- choice setting -->
    <div class="mb-2">
      <label for="" class="form-label">Choices</label>
      <input
        type="text"
        :value="builderStore.selectedElement.properties.choices.join(',')"
        @input="
          (event) =>
            (builderStore.selectedElement.properties.choices =
              event.target.value.split(','))
        "
        class="form-control"
      />
    </div>

    <!-- default checked choices -->
    <label for="" class="form-label">Default checked choices</label>
    <div
      class="form-check"
      v-for="choice in builderStore.selectedElement.properties.choices"
      :key="choice"
    >
      <input
        class="form-check-input"
        type="checkbox"
        id="flexCheckChecked"
        :value="choice"
        v-model="builderStore.selectedElement.properties.default_checked_choices"
      />
      <label class="form-check-label" for="flexCheckChecked">
        {{ choice }}
      </label>
    </div>

    <div class="d-grid gap-2">
      <button class="btn btn-sm btn-dark mt-2" type="submit">
        Update
      </button>
    </div>
  </form>
</template>
