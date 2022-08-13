<script setup>
const { element } = defineProps(['element'])
</script>

<template>
  <label :for="element.id" class="form-label">{{ element.label }}</label>
  <input
    :id="element.id"
    :type="element.properties.type ? element.properties.type : 'text'"
    class="form-control"
    :required="element.is_required"
    :name="element.label"
    :placeholder="element.properties.placeholder"
  />
</template>
