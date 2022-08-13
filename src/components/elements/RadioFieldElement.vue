<script setup>
import { useBuilderStore } from '../../stores/builder'

const builderStore = useBuilderStore()
const { element } = defineProps(['element'])
defineEmits(['onDelete'])

</script>

<template>
  <div class="d-flex justify-content-between">
    <label :for="element.id">{{ element.label }}</label>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      fill="currentColor"
      class="bi bi-trash-fill"
      viewBox="0 0 16 16"
      v-if="builderStore.selectedElement === element"
      @click="$emit('onDelete', element)"
    >
      <path
        d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"
      />
    </svg>
  </div>
  <div
    class="form-check"
    v-for="(option, index) in element.properties.options"
    :key="option"
  >
    <input
      class="form-check-input"
      type="radio"
      :name="element.label"
      :id="`${element.label} ${option}`"
      :value="option"
      :required="element.is_required"
      :checked="element.properties.default_option === option"
    />
    <label class="form-check-laqbel" :for="`${element.label} ${option}`">
      {{ option }}
    </label>
  </div>
</template>
