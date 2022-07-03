<script setup>
import { reactive, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getForms } from '../../api'

const router = useRouter()
const forms = ref([])

onMounted(async () => {
  try {
    const { data } = await getForms()
    forms.value = data.results
  } catch (e) {
    console.log(e)
  }
})
</script>

<template>
  <div class="container">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Name</th>
          <th scope="col"></th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(form, index) in forms" :key="form.id">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ form.title }}</td>
          <td>
            <button
              class="btn btn-sm btn-primary"
              @click="
                router.push({
                  name: 'formDetail',
                  params: { form_id: form.id },
                })
              "
            >
              View Detail
            </button>
          </td>
          <td>
            <button
              class="btn btn-sm btn-primary"
              @click="
                router.push({
                  name: 'formSubmissions',
                  params: { form_id: form.id },
                })
              "
            >
              View Submissions
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
