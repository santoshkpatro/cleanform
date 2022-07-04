<script setup>
import { reactive, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getForms, createForm, updateForm } from '../../api'

const router = useRouter()
const forms = ref([])
const newForm = reactive({
  title: '',
  description: '',
  is_live: false,
})

onMounted(async () => {
  try {
    const { data } = await getForms()
    forms.value = data.results
  } catch (e) {
    console.log(e)
  }
})

async function handleUpdateForm(form) {
  try {
    const { data } = await updateForm(form.id, form)
    console.log(data)
  } catch (e) {
    console.log(e)
  } finally {
    newForm.title = ''
    newForm.description = ''
  }
}
</script>

<template>
  <div class="container">
    <!-- Create a new form -->
    <form @submit.prevent="createNewForm" class="mb-5">
      <div class="mb-2">
        <label for="title" class="form-label">Form name</label>
        <input
          type="text"
          class="form-control"
          v-model="newForm.title"
          required
        />
      </div>
      <div class="mb-2">
        <label for="title" class="form-label">Description</label>
        <textarea
          class="form-control"
          id="exampleFormControlTextarea1"
          rows="3"
          v-model="newForm.description"
        ></textarea>
      </div>
      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-sm btn-success">
          Create form
        </button>
      </div>
    </form>

    <!-- Existing forms -->
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Name</th>
          <th scope="col"></th>
          <th scope="col"></th>
          <th scope="col">Is Live</th>
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
          <td>
            <div class="form-check form-switch">
              <input
                v-model="form.is_live"
                class="form-check-input"
                type="checkbox"
                role="switch"
                id="flexSwitchCheckChecked"
                :checked="form.is_live"
                @input="handleUpdateForm({ ...form, is_live: !form.is_live })"
              />
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
