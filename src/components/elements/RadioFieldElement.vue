<script setup>
const { element } = defineProps(['element'])
</script>

<template>
  <label :for="element.id">{{ element.label }}</label>
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
