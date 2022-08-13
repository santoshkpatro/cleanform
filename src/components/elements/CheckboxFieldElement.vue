<script setup>
const { element } = defineProps(['element'])
</script>

<template>
  <label class="form-label" :for="element.id">
    {{ element.label }}
  </label>

  <div
    class="form-check"
    v-for="(choice, index) in element.properties.choices"
    :key="choice"
  >
    <input
      class="form-check-input"
      type="checkbox"
      :checked="element.properties.default_checked_choices.includes(choice)"
      :value="choice"
      :id="`${element.label} ${choice}`"
    />
    <label class="form-check-label" :for="`${element.label} ${choice}`">
      {{ choice }}
    </label>
  </div>
</template>
